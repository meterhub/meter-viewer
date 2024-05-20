import typing as t

global_func: t.Dict[str, t.Any] = {}


def use_func(name: str):
    f = global_func.get(name, None)
    if not f:
        raise ValueError(f"func {name} not found")


def must_str(object) -> str:
    return str(object)
