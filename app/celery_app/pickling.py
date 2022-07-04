def save(obj):
    return (obj.__class__, obj.__dict__)


def restore(cls, attributes):
    obj = cls.__new__(cls)
    obj.__dict__.update(attributes)
    return obj
