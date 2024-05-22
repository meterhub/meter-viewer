import typing as t

global_func: t.Dict[str, t.Any] = {}


def use_func(name: str):
    f = global_func.get(name, None)
    if not f:
        raise ValueError(f"func {name} not found")


def must_str(object) -> str:
    return str(object)


def must_loop(arr: t.Iterable, func: t.Callable, custom_error):
    """raise custom error if not looped"""
    is_loop, set_loop = looped()

    for element in arr:
        func(element)
        set_loop()

    if not is_loop():
        raise custom_error("must loop")


def looped():
    loop = False

    def is_loop():
        return loop

    def set_loop():
        nonlocal loop
        loop = True

    return is_loop, set_loop
