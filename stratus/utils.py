def unchangeable_fields(user, app_label, fields=None):
    """
    Given a user, app_label, and list of fields this will return all
    the fields the user DOES NOT have permissions to change.

    """
    fields = fields or []
    return [field for field in fields
        if not user.has_perm('%s.change_%s' % (app_label, field))]
