from io import TextIOWrapper
from pathlib import Path
from typing import Any, Hashable, Callable, Dict
from functools import _make_key, partial
import pickle, inspect, threading, shutil

CACHE_DIR = '__pyfilecache__'

class _FileCached:
    def __init__(
            self,
            user_function,
            reader: Callable[[TextIOWrapper], Any],
            writer: Callable[[Any, TextIOWrapper], None],
            typed: bool = False
    ):
        self.lock = threading.Lock()

        self.reader, self.writer = reader, writer
        self.typed = typed
        self.user_function = user_function

        self._build()

    def _build(self):
        """
        init the index of CACHE_DIR
        """
        self.code_path = Path(inspect.getfile(self.user_function))
        self.cache_dir = self.code_path.parent.joinpath(CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
        self.funcache_dir = self.cache_dir.joinpath(f'{self.code_path.name}...{self.user_function.__qualname__}')
        self.funcache_dir.mkdir(exist_ok=True)
        self.index_dir = self.funcache_dir.joinpath('index')
        if not self.index_dir.exists():
            with open(self.index_dir, 'wb') as f:
                pickle.dump({}, f)

    def __call__(self, *args, **kwds):
        """
        wrapper of user_function
        """
        fidxp = self.fp(*args, **kwds)
        if fidxp.exists():
            with open(fidxp, 'rb') as f:
                return self.reader(f)
        else:
            result = self.user_function(*args, **kwds)
            with open(fidxp, 'wb') as f:
                self.writer(result, f)
            return result
        
    def fp(self, *args, **kwds):
        """
        the file path where the result of user_function(*args, **kwds) stored
        """
        key = tuple(_make_key((self.user_function.__code__.co_code, *args), kwds, self.typed))
        idx = self._key2findex(key)
        return self.funcache_dir.joinpath(f'_{idx}')

    def _key2findex(self, key: Hashable) -> int:
        self.lock.acquire()
        try:
            with open(self.index_dir, "rb") as f:
                index: Dict[Any, int] = pickle.load(f)
            result = index.get(key)
            if result is None:
                with open(self.index_dir, "wb") as f:
                    index[key] = len(index)
                    pickle.dump(index, f)
        finally:
            self.lock.release()
        return index[key]
    
    def clear(self):
        """
        clear all stored results of this function
        """
        shutil.rmtree(self.funcache_dir)
        self._build()

def file_cache(
    user_function = None, *,
    reader: Callable[[TextIOWrapper], Any] = pickle.load,
    writer: Callable[[Any, TextIOWrapper], None] = pickle.dump,
    typed: bool = False
):
    """
    decorator of a slow function that stores the result to disk  

    Usage Example:
    ```py
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
    """
    if user_function is None: return partial(_FileCached, reader=reader, writer=writer, typed=typed)
    return _FileCached(user_function, reader, writer, typed)