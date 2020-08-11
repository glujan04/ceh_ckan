def get_comment(data_dict):
    import ckan.logic as logic
    import ckanext.ceh_comment.model as model

    comment = data_dict.get('comment')
    if not comment:
        id = logic.get_or_bust(data_dict, 'id')
        comment = model.Comment.get(id)
    return comment
