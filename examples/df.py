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