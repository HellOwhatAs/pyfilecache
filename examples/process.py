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

        print(func.lock_dir)
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
