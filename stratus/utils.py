def nameify(obj, kind):
    return obj.__class__.__name__.split(kind)[0].lower()
