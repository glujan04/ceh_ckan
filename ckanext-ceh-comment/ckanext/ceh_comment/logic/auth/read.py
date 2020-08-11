import logging
from pylons.i18n import _

import ckan.authz as authz
from ckan import logic
import ckanext.ceh_comment.model as comment_model


log = logging.getLogger(__name__)


def thread_read(context, data_dict):
    model = context['model']
    user = context['user']

    userobj = model.User.get(user)
    # If sysadmin.
    if authz.is_sysadmin(user):
        return {'success': True}

    cid = logic.get_or_bust(data_dict, 'id')

    commentThread = comment_model.CommentThread.get(cid)
    if not commentThread:
        return {'success': False, 'msg': _('Thread does not exist')}

    #if commentThread.user_id is not userobj.id:
    #    return {'success': False, 'msg': _('User is not the author of the commentThread')}

    return {'success': True}