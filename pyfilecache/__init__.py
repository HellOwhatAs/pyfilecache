from io import TextIOWrapper
from pathlib import Path
from typing import Any, Hashable, Callable, Tuple, Dict
from functools import _make_key
import pickle, inspect, threading

CACHE_DIR = '__pyfilecache__'
KEY2INDEX_LOCK = threading.Lock()

def key2findex(key: Hashable, index_dir: Path) -> Tuple[int, bool]:
    KEY2INDEX_LOCK.acquire()
    with open(index_dir, "rb") as f:
        index: Dict[Any, int] = pickle.load(f)
    result = index.get(key)
    flag = result is None
    if flag:
        with open(index_dir, "wb") as f:
            index[key] = len(index)
            pickle.dump(index, f)
    KEY2INDEX_LOCK.release()
    return index[key], not flag
    
def file_cache(
        user_function = None, *,
        reader: Callable[[TextIOWrapper], Any] = None,
        writer: Callable[[Any, TextIOWrapper], None] = None,
        typed: bool = False
    ):
    
    if reader is None: reader = pickle.load
    if writer is None: writer = pickle.dump
        
    def wrapper_of_wrapper(user_function):

        code_path = Path(inspect.getfile(user_function))
        cache_dir = code_path.parent.joinpath(CACHE_DIR)
        cache_dir.mkdir(exist_ok=True)
        funcache_dir = cache_dir.joinpath(f'{code_path.name}...{user_function.__qualname__}')
        funcache_dir.mkdir(exist_ok=True)
        index_dir = funcache_dir.joinpath('index')
        if not index_dir.exists():
            with open(index_dir, 'wb') as f:
                pickle.dump({}, f)

        def wrapper(*args, **kwds):
            key = tuple(_make_key((user_function.__code__.co_code, *args), kwds, typed))
            idx, flag = key2findex(key, index_dir)
            fidxp = funcache_dir.joinpath(f'_{idx}')
            if flag and fidxp.exists():
                with open(fidxp, 'rb') as f:
                    return reader(f)
            else:
                result = user_function(*args, **kwds)
                with open(fidxp, 'wb') as f:
                    writer(result, f)
                return result
        return wrapper
    
    if user_function is None: return wrapper_of_wrapper
    return wrapper_of_wrapper(user_function)
        

        



if __name__ == '__main__':
    import pandas as pd
    from functools import partial
    df_cache = partial(file_cache, reader=pd.read_csv, writer=pd.DataFrame.to_csv)
    
    @df_cache
    def func(a, b):
        print(a, b)
        return pd.DataFrame(
            data = {
                'col1': [1, 2],
                'col2': [a, b]
            }
        )
    
    print(func(3, 4))