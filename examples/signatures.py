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