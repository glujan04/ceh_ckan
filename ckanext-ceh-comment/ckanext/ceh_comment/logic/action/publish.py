import datetime
import ckanext.ceh_comment.model as comment_model
from ckan import logic
from ckan.lib.base import abort
import logging

log = logging.getLogger(__name__)


def comment_publish(context, data_dict):
    model = context['model']

    #logic.check_access("comment_publish", context, data_dict)

    cid = logic.get_or_bust(data_dict, 'id')
    comment = comment_model.Comment.get(cid)
    if not comment:
        abort(404)

    if data_dict.get('state') == u'true':
        comment.approval_status = comment_model.COMMENT_APPROVED
    if data_dict.get('state') == u'false':
        comment.approval_status = comment_model.COMMENT_PENDING
    comment.modified_date = datetime.datetime.now()

    model.Session.add(comment)
    model.Session.commit()

    return {'success': True}