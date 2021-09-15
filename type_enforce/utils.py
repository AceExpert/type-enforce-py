import typing, inspect

def isiterable(value: typing.Iterable) -> bool:
    try: iter(value)
    except TypeError: return False
    else: return True

def get_defaults(func: typing.Union[typing.Callable, typing.Coroutine]) -> typing.Dict[str, typing.Tuple[typing.Any, typing.Any, int]]:
    sig = inspect.signature(func)
    return {
        item[0]: [item[1].default, item[1].kind, ind] for item, ind in zip(sig.parameters.items(), range(len(sig.parameters.items()))) 
        if item[1].default is not inspect.Parameter.empty
    }