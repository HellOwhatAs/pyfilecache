# pyfilecache
cache results of slow function to disk

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