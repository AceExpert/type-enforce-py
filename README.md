# type-enforce-py
Supports enforcing type annotations on functions and coroutines. Complete support for types from typing module.

## Installation

##### Windows
```cmd
py -m pip install type-enforce
```
##### Unix/MacOS
```bash
python3 -m pip install type-enforce
```

## Examples

##### 1. Basic usage
```py
from type_enforce import enforce_type

@enforce_type
def my_typed_fn(text: str, age: int, time: datetime.datetime.fromisoformat):
    print(type(text), type(age), type(time))

my_typed_fn(234324, "47539", '2021-09-15T07:49:38.412586') #time in isoformat is passed to the fromisoformat classmethod of datetime class which converts it to an actual datetime class, the same goes with the first two arguments
```

##### 2. Usage with typing.Union, typing.Literal and other types.
```py
@enforce_type
def myfn(val: typing.Dict[str, typing.Union[float, int]]):
    print(type(val), val)
    print(" ".join([str(type(i))+" + "+str(type(j)) for i, j in val.items()]))

myfn({'hello':'3453', True: '345.345'}) # Output: <class 'dict'> {'hello':'3453', True: '345.345'} \n <class 'str'> + <class 'int'> <class 'str'> + <class 'float'>

@enforce_type
def literal_example(value: typing.Literal['no', 'yes']):
    print(value)

literal_example('yes') #Ok
literal_example('yas') #Error
literal_example('no') #Ok
```

### What this does under the hood ?
First checks if the type of the value is one of the annotated types, if yes then returns it else tries to convert it according to the annotation if at all it is convertible if it fails, a TypeError is thrown most probably or the callable to which the value was passed could even throw a custom error for example: datetime.datetime.fromisoformat. 

###### Enjoy making your functions statically / strongly typed.