# pyfilecache
cache the results of slow-running functions to disk, with multi-process safety

## Install
```
pip install pyfilecache
```

## Examples

### Basic Usage
```py
# examples/add.py
from pyfilecache import file_cache

@file_cache
def add(a, b):
    print(f'adding {repr(a)} and {repr(b)}')
    return a + b

print(repr(add(1, 2)))
print(repr(add(1, 2)))
print(repr(add('1', '2')))
print(repr(add('1', '2')))
```

```
$ python3 examples/add.py
adding 1 and 2
3
3
adding '1' and '2'
'12'
'12'
$ python3 examples/add.py
3
3
'12'
'12'
```

### Customized Reader and Writer

```py
# examples/df.py
import pandas as pd
from functools import partial
from pyfilecache import file_cache

@file_cache(
    reader=partial(pd.read_csv, index_col=0),
    writer=pd.DataFrame.to_csv
)
def func(a, b):
    print("func called with args", a, b)
    return pd.DataFrame(
        data = {
            'col1': [1, 2],
            'col2': [a, b]
        }
    )

print(func(3, 4))
print(func(3, 4))
```

```
$ python3 examples/df.py 
func called with args 3 4
   col1  col2
0     1     3
1     2     4
   col1  col2
0     1     3
1     2     4
$ python3 examples/df.py 
   col1  col2
0     1     3
1     2     4
   col1  col2
0     1     3
1     2     4
```

### Multi-Process Safety
```py
# examples/process.py
from pyfilecache import file_cache
import multiprocessing

@file_cache
def func(a, b):
    print(a, b)
    return a + b

def loop():
    while True:
        print(func(1, 2))
        print(func('1', '2'))

        print(func.fp(1, 2))
        func.clear()

        print(func(1, 2))
        print(func('1', '2'))
        func.clear()

        print(func(1, 2))
        print(func(3, 4))
        print(func(5, 6))

if __name__ == '__main__':
    ps = [multiprocessing.Process(target=loop) for _ in range(10)]
    list(map(multiprocessing.Process.start, ps))
    list(map(multiprocessing.Process.join, ps))
```

### Cache Non-Pure Function with Different Versions

> [!NOTE]
> nonlocal variables used in function (e.g. `outer`) and version string (e.g. `"v0"`, `"v1"`) must correspond

```py
# examples/versions.py
from pyfilecache import file_cache

@file_cache
def func(x: int):
    print(f'multiply {outer} and {x}')
    return outer * x

outer = 100
print(func(2))
print(func(10))

outer = 5
print(func['v0'](2))
print(func['v0'](10))

outer = 1
print(func['v1'](2))
print(func['v1'](10))
```

```
$ python3 examples/versions.py 
multiply 100 and 2
200
multiply 100 and 10
1000
multiply 5 and 2
10
multiply 5 and 10
50
multiply 1 and 2
2
multiply 1 and 10
10
$ python3 examples/versions.py 
200
1000
10
50
2
10
```

### Functions with Different Signatures
```py
# examples/signatures.py
from pyfilecache import file_cache

@file_cache
def func(x = 1000):
    print('OK')
    return x

print(func())

@file_cache
def func(x = 100):
    print('OK')
    return x

print(func())

@file_cache
def func(x: int = 100) -> int:
    print('OK')
    return x

print(func())
```

```
$ python3 examples/signatures.py 
OK
1000
OK  
100 
OK 
100
$ python3 examples/signatures.py 
1000
100
100
```