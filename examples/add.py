from pyfilecache import file_cache

@file_cache
def add(a, b):
    print(f'adding {repr(a)} and {repr(b)}')
    return a + b

print(repr(add(1, 2)))
print(repr(add(1, 2)))
print(repr(add('1', '2')))
print(repr(add('1', '2')))