'''A CKAN plugin that enables logging into CKAN using SSO IDOM.
'''
import json
import uuid
import logging
import requests
import re

# Unfortunately we need to import pylons directly here, because we need to
# put stuff into the Beaker session and CKAN's plugins toolkit doesn't let
# us do that yet.
#import pylons.session as session

#import pylons.config as config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers
from ckan.common import config, session

log = logging.getLogger(__name__)

class SsoPlugin(plugins.SingletonPlugin):
    '''A CKAN plugin that enables logging into CKAN using SSO IDOM.
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurable)


    domain = None

    def get_helpers(self):
        return {'ckanext_sso_domain': self.get_domain}

    def get_domain(self):
        return self.domain

    def configure(self, config):
        self.domain = None

    @staticmethod
    def update_config(config):
        '''Update CKAN's config with settings needed by this plugin.

        '''
        log.debug('update_config  - inicio')
        toolkit.add_template_directory(config, 'templates')
        #toolkit.add_public_directory(config, 'public')
        #toolkit.add_resource('fanstatic', 'sso')
        log.debug('update_config  - fin')

    @staticmethod
    def before_map(map):
        map.connect('sso','/user/login/sso',
                    controller='ckanext.sso.controller:SsoRedirectController', action='pagRever')
        return map

    def after_map(self, map):
        """
        Called after routes map is set up. ``after_map`` can be used to
        add fall-back handlers.
        :param map: Routes map object
        :returns: Modified version of the map object
        """
        return map

    def login(self):
        log.debug('login  - inicio')
        #params = toolkit.request.params
        if 'access_token' in toolkit.request.params:
            access_token = toolkit.request.params['access_token']
            bodyreq = {'idam.app':'a14'}
            headerreq = {'Content-Type': 'application/json','authorization': 'Bearer {0}'.format(access_token)}
            log.info('login - hearder = %s' % headerreq)
            resp = requests.post('https://intranetelhierro.idomdev.es/idamrest/api/v1/me/access',json=bodyreq, headers=headerreq)
            if resp.status_code != 200:
                log.error('login - error API SSO')
            else:
                log.info('login - OK API %s' % resp.text)
                data = resp.json()
                if data['authorized'] is True:
                    usernameCon = data['username'].split("@")[0]
                    username = re.sub('[^0-9a-zA-Z\-\_]+', '', usernameCon)
		    log.info('login - user: {0}'.format(username))
                    # Add username in session
                    session['ckannext-user'] = username

    def identify(self):
        log.debug('identify  - inicio')
        log.debug('identify  - Session: {0}'.format(session.get('ckannext-user')))
        if session.get('ckannext-user'):
            # Try to get the item that login() placed in the session.
            log.debug('identify  - session.user -> {0}'.format(session.get('ckannext-user')))
            user = session.get('ckannext-user')
            log.debug('identify  - user -> {0}'.format(user))

            # TODO
            # Solo hay que obtener el token de SSO, de ese token, obtener en nombre de usuario.
            # Cuando tengamos el usuario del localStorage insertarlo el la variable:
            # toolkit.c.user = "diegoindicadoresadmin"

            if user:
                # We've found a logged-in user. Set c.user to let CKAN know.
                toolkit.c.user = user
            else:
                toolkit.c.user = None
            log.debug('identify  - fin')


    def logout(self):
        '''Handle a logout.'''
        log.debug('logout  - inicio')
        # Delete the session item, so that identify() will no longer find it.
        session['ckannext-user'] = None
        toolkit.c.user = None
        log.debug('logout  - fin')
