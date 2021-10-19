import jsonpickle as jsonpickle
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b


def json_encode(obj: any):
    return jsonpickle.encode(obj, unpicklable=False, indent=4)
