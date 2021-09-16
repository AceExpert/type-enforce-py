import typing, inspect, warnings
from collections import *
from collections import abc

from .utils import isiterable

def argument_processor(typ: typing.Any, val: typing.Any) -> typing.Any:
    if typing.get_origin(typ) in [typing.Generic] or typ == typing.Any:
        return val
    elif isinstance(typ, abc.Callable) and not typing.get_origin(typ):
        try:
            isinstance(val, typ)
        except TypeError:
            return typ(val)
        else:
            if isinstance(val, typ):
                return val
            else:
                return typ(val)
    elif typing.get_origin(typ) == abc.Callable:
        if not isinstance(val, abc.Callable):
            raise TypeError(f"{val} isn't a {typ._name}")
        if not typing.get_args(typ): return val 
        typanots = typing.get_args(typ)
        annots, ind = {'return': typanots[-1]}, 0
        for pname, param in inspect.signature(val).parameters.items():
            if param.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.VAR_POSITIONAL]:
                annots[pname] = typanots[0][ind]
                ind += 1
        val.__annotations__ = annots
        return val
    elif typing.get_origin(typ) == typing.Union:
        types = typing.get_args(typ) 
        if not types: return val
        while [i for i in types if typing.get_origin(i) == typing.Union]:
            types = [typing.get_args(i) if typing.get_origin(i) == typing.Union else i for i in types]
        types = [str if i == typing.AnyStr else i for i in types]
        if not [i for i in types if typing.get_origin(i)]:
            if isinstance(val, tuple(i for i in types if i != typing.Any)):
                return val
            elif typing.Any in types:
                return val
        for i in types:
            try:
                return argument_processor(i, val)
            except Exception:
                pass
        if typing.Any in types or typing.Generic in [typing.get_origin(i) for i in types]: return val 
        if type(None) in types: return None
        raise TypeError(f"{val} couldn't be converted or doesn't match any of the specified types.")
    elif typing.get_origin(typ) == typing.Literal:
        literals = typing.get_args(typ)
        if not literals: return val
        if val in literals:
            return val
        else:
            raise TypeError(f"{val} doesn't match any of the literals: {', '.join(literals)}")
    elif typing.get_origin(typ) in [list, set]:
        return typing.get_origin(typ)([argument_processor(typing.get_args(typ)[0], i) for i in val]) if typing.get_args(typ) else typing.get_origin(typ)(val)
    elif typing.get_origin(typ) in [dict, OrderedDict, ChainMap, abc.ItemsView]:
        return typing.get_origin(typ)({argument_processor(typing.get_args(typ)[0], key) if typing.get_args(typ) else key: argument_processor(typing.get_args(typ)[1], value) if typing.get_args(typ) else val for key, value in val.items()})
    elif typing.get_origin(typ) in [tuple]:
        return typing.get_origin(typ)(argument_processor(tuptype, tupval) for tuptype, tupval in zip(typing.get_args(typ), val)) if typing.get_args(typ) else typing.get_origin(typ)(val)
    elif typing.get_origin(typ) in [deque, Counter]:
        if not typing.get_args(typ): return typing.get_origin(typ)(val)
        iteron = val.values() if isinstance(val, dict) else val
        prval = {key: argument_processor(typing.get_args(typ)[0], value) for key, value in zip(val.keys(), iteron)} if isinstance(val, dict) else [argument_processor(typing.get_args(typ)[0], value) for value in iteron]
        return typing.get_origin(typ)(prval)
    elif typ in [typing.T]: return type(val)
    elif hasattr(abc, typ._name) and typing.get_origin(typ):
        if isinstance(val, typing.get_origin(typ)):
            return val
        elif typing.get_origin(typ) in [typing.Iterable, typing.Iterator]:
            if isiterable(val): return val
            else: raise TypeError(f"{val} isn't a {typ._name}")
        else:
            raise TypeError(f"{val} isn't a {typ._name}")
    else:
        warnings.warn(f"The type {typ} is either not a type, not available or not supported. So the value is passed as is.", RuntimeWarning)
        return val