import datetime
import ckanext.ceh_comment.model as comment_model
import ckanext.ceh_comment.util as util
from ckan import logic
from pprint import pprint
import logging

log = logging.getLogger(__name__)


def comment_create(context, data_dict):
    model = context['model']
    user = context['user']

    userobj = model.User.get(user)

    #logic.check_access("comment_create", context, data_dict)

    # Valida que se tengan todos los campos requeridos.
    if not all([data_dict.get('comment')]):
        raise logic.ValidationError("Comment text is required")

    thread_id = data_dict.get('thread_id')

    if not thread_id:
        url = data_dict.get('url')
        if url:
            thread = comment_model.CommentThread.from_url(url)
            thread_id = thread.id if thread else None

    if not thread_id:
        raise logic.ValidationError("Thread identifier or URL is required")

    # Cleanup the comment
    cleaned_comment = util.clean_input(data_dict.get('comment'))

    # Create the object
    cmt = comment_model.Comment(thread_id=thread_id,
                                comment=cleaned_comment)
    cmt.user_id = userobj.id if userobj else None
    cmt.subject = data_dict.get('subject', 'No subject')
    cmt.email = data_dict.get('email', 'No Email')

    if 'creation_date' in context:
        cmt.creation_date = datetime.datetime.fromtimestamp(context['creation_date'])

    # Check if there is a parent ID and that it is valid
    # TODO, validity in this case includes checking parent is not
    # deleted.
    prt = data_dict.get('parent_id')
    if prt:
        parent = comment_model.Comment.get(prt)
        if parent:
            cmt.parent_id = parent.id

    # approval and spam checking removed
    commentThread = comment_model.CommentThread.get(thread_id)
    commentThread.active_thread = 'active'
    commentThread.state_thread = 'active'
    model.Session.add(commentThread)
    model.Session.add(cmt)
    model.Session.commit()

    return cmt.as_dict()
