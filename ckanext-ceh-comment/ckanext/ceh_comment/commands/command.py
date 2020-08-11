from __future__ import print_function

import sys
from pprint import pprint

from ckan import model
from ckan.logic import get_action, ValidationError
from ckan.plugins import toolkit

from ckan.lib.cli import CkanCommand

class CehComment(CkanCommand):
    '''CehComment remotely mastered metadata

    Usage:

      cehcomment initdb
        - Creates the necessary tables in the database

      cehcomment cleandb
        - Remove the tables in the database

    The command should be run from the ckanext-ceh-comment directory and expect
    a development.ini file to be present. Most of the time you will
    specify the config explicitly though::

        paster cehcomment [command] --config=../ckan/development.ini

    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = 2
    min_args = 0

    def command(self):
        self._load_config()

        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        self.admin_user = get_action('get_site_user')(context, {})

        print('')

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)
        cmd = self.args[0]
        if cmd == 'initdb':
            self.initdb()
        elif cmd == 'cleandb':
            self.cleandb()
        else:
            print('Command {0} not recognized'.format(cmd))

    def _load_config(self):
        super(CehComment, self)._load_config()

    def initdb(self):
        from ckanext.ceh_comment.model import init_db as db_setup
        db_setup()

        print('DB tables created')

    def cleandb(self):
        from ckanext.ceh_comment.model import clean_db as db_remove
        db_remove()

        print('DB tables removed')