import typing, inspect, asyncio
from inspect import Parameter

from .processors import argument_processor
from .utils import get_defaults

def enforce_type(func: typing.Union[typing.Callable, typing.Coroutine]) -> typing.Callable:
    def wrapper(*args, **kwargs):
        defs, args, kwargs = get_defaults(func), list(args).copy(), kwargs.copy()
        for key, val in defs.items():
            print(len(args) , val[2])
            if val[1] in [Parameter.POSITIONAL_ONLY, Parameter.VAR_POSITIONAL, Parameter.POSITIONAL_OR_KEYWORD] and len(args)-1 > val[2] and key not in kwargs:
                args.insert(val[2], val[0])
            elif val[1] in [Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD] and key not in kwargs:
                kwargs[key] = val[0]
        annotation_vals = {list(func.__code__.co_varnames).index(key):vals for key, vals in func.__annotations__.items()}
        args = [argument_processor(annotation_vals[j], i) if j in list(annotation_vals.keys()) and i != None else i for i,j in zip(args, range(len(args)))]
        kwargs = {key:argument_processor(func.__annotations__[key], value) if key in func.__annotations__ and value != None else value for key, value in kwargs.items()}
        if inspect.iscoroutinefunction(func): 
            return asyncio.run(argument_processor(func.__annotations__['return'], func(*args, **kwargs)) if 'return' in func.__annotations__ else func(*args, **kwargs))
        else:
            return argument_processor(func.__annotations__['return'], func(*args, **kwargs)) if 'return' in func.__annotations__ else func(*args, **kwargs)
    return wrapper