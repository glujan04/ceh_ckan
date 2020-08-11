import logging

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckan.lib.base import BaseController, config
import jinja2
from ckan.common import _, c, g, request


abort = base.abort
render = base.render


log = logging.getLogger(__name__)

class SsoRedirectController(BaseController):

    def pagRever(self, context=None):
        c = p.toolkit.c
        data = request.params or {}
        errors = {}
        error_summary = {}
        print data
        print config.get('email_to');

        #error_summary = errors
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
        return render('loginSSO.html', extra_vars=vars)