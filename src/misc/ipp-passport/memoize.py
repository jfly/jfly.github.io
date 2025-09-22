def memoize(func):
    remembered = {}

    def memoized(*args):
        if args not in remembered:
            remembered[args] = func(*args)
        return remembered[args]

    return memoized
