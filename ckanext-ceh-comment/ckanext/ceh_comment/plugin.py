import logging
import base64
import hashlib
import hmac
import simplejson
import time

from ckan.common import request
from ckan.lib.helpers import url_for_static_or_external
import ckan.plugins as p
from flask import Blueprint
import ckanext.ceh_comment.views as ceh_view

log = logging.getLogger(__name__)


class CommentPlugin(p.SingletonPlugin):
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
    p.implements(p.IBlueprint)


    # IPackageController

    def before_view(self, pkg_dict):
        # TODO: append comments from model to pkg_dict
        return pkg_dict


    # IConfigurer

    def update_config(self, config_):
        p.toolkit.add_template_directory(config_, "templates")
        #p.toolkit.add_public_directory(config_, 'public')
        p.toolkit.add_resource('fanstatic', 'ckanext_comment')

    @classmethod
    def ceh_comments(cls):
        '''Para agregar un comentario'''

        c = p.toolkit.c

        # Inicializa
        timestamp = 'blank'

        # Se obtiene al usuario si se encuentra logueado
        user_dict = {}
        try:
            user_dict = p.toolkit.get_action('user_show')({'keep_email': True},
                                                          {'id': c.user})

        # Blanquea campos si el usuario no ha sido logueado
        except:
            user_dict['id'] = ''
            user_dict['name'] = ''
            user_dict['email'] = ''

        # genera un timestamp
        timestamp = int(time.time())

        # Se crea un identificador
        try:
            identifier = c.controller
            if identifier == 'package':
                identifier = 'dataset'
            if c.current_package_id:
                identifier += '::' + c.current_package_id
            elif c.id:
                identifier += '::' + c.id
            else:
                # No se puede generar un identifier
                identifier = ''
            # Caso especial
            if c.action == 'resource_read':
                identifier = 'dataset-resource::' + c.resource_id
        except:
            identifier = ''
        data = {'identifier': identifier,
                'id': user_dict['id'],
                'timestamp': timestamp}

        return p.toolkit.render_snippet('ceh_comments.html', data)

    @classmethod
    def _ceh_notify_panel(cls):
        '''Agrega un icono de notificacion en la parte superior para el usuario logueado'''

        c = p.toolkit.c

        # Se obtiene al usuario si se encuentra logueado
        user_dict = {}
        try:
            user_dict = p.toolkit.get_action('user_show')({'keep_email': True},
                                                          {'id': c.user})

        # Blanquea campos si el usuario no ha sido logueado
        except:
            user_dict['id'] = ''
            user_dict['name'] = ''
            user_dict['email'] = ''

        data = { 'id': user_dict['id'] }
        return p.toolkit.render_snippet('ceh_notify.html', data)

    @classmethod
    def _new_comments(cls):
        '''Cantidad de comentarios nuevos'''
        import ckan.model as model
        from ckan.logic import get_action
        approval = 'pending'
        count = get_action('comment_count')({'model': model}, {'approval': approval})
        return count

    def get_helpers(self):
        return {'ceh_comments': self.ceh_comments,
                'new_comments': self._new_comments,
                'ceh_notify': self._ceh_notify_panel,
                'get_comment_thread': self._get_comment_thread,
                'get_comment_all_dataset': self._get_comment_all_dataset,
                'get_comment_count_for_dataset': self._get_comment_count_for_dataset}

    def get_actions(self):
        from ckanext.ceh_comment.logic.action import get, create, delete, update, publish, read, thread_delete

        return {
            "comment_create": create.comment_create,
            "thread_show": get.thread_show,
            "comment_update": update.comment_update,
            "comment_show": get.comment_show,
            "comment_delete": delete.comment_delete,
            "comment_count": get.comment_count,
            "thread_list": get.thread_list,
            "thread_read": read.thread_read,
            "thread_delete": thread_delete.thread_delete,
            "comment_publish": publish.comment_publish
        }

    def get_auth_functions(self):
        from ckanext.ceh_comment.logic.auth import get, create, delete, update, read, thread_delete

        return {
            'comment_create': create.comment_create,
            'comment_update': update.comment_update,
            'thread_read': read.thread_read,
            'thread_delete': thread_delete.thread_delete,
            'comment_show': get.comment_show,
            'comment_delete': delete.comment_delete,
            "comment_count": get.comment_count
        }

    def _get_comment_thread(self, dataset_name):
        '''Obtiene los thread new comments activos'''

        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        return get_action('thread_show')({'model': model, 'with_deleted': True}, {'url_list': url})

    def _get_comment_all_dataset(self, id):
        import ckan.model as model
        from ckan.logic import get_action
        return get_action('thread_list')({'model': model}, {'userid': id})

    def _get_comment_count_for_dataset(self, dataset_name):
        import ckan.model as model
        from ckan.logic import get_action
        url = '/dataset/%s' % dataset_name
        count = get_action('comment_count')({'model': model}, {'url': url})
        return count


    # IRoutes

    def before_map(self, map):
        """
            /dataset/NAME/comments/reply/PARENT_ID
            /dataset/NAME/comments/add
        """
        controller = 'ckanext.ceh_comment.controller:CommentController'
        map.connect('/dataset/{dataset_id}/comments/add', controller=controller, action='add')
        map.connect('/dataset/{dataset_id}/comments/{comment_id}/edit', controller=controller, action='edit')
        map.connect('/dataset/{dataset_id}/comments/{comment_id}/publish', controller=controller, action='publish')
        map.connect('/dataset/publish', controller=controller, action='publish_ren')
        map.connect('/dataset/{dataset_id}/comments/{parent_id}/reply', controller=controller, action='reply')
        map.connect('/dataset/{dataset_id}/comments/{comment_id}/delete', controller=controller, action='delete')
        map.connect('/comments/list', controller=controller, action='list')
        map.connect('/dataset/list/{dataset_id}/thread/{thread_id}/read', controller=controller, action='read')
        map.connect('/dataset/list/{thread_id}/{d_name}/delete', controller=controller, action='delNotify')
        return map

