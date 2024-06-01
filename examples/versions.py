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