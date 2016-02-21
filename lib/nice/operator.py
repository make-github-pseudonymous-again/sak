
def keysetter(key):
    if not isinstance(key, str):
        raise TypeError('key name must be a string')
    resolve = key.split('.')
    head, last = tuple(resolve[:-1]), resolve[-1]

    def g(obj,value):
        for key in head :
            obj = obj[key]
        obj[last] = value

    return g

def keygetter(key):
    if not isinstance(key, str):
        raise TypeError('key name must be a string')
    return lambda obj : resolve_key(obj, key)

def resolve_key(obj, key):
    for name in key.split('.'):
        obj = obj[name]
    return obj
