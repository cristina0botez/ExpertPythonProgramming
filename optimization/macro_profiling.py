from cProfile import Profile
from pstats import Stats
import time


def medium():
    time.sleep(0.01)


def light():
    time.sleep(0.001)


def heavy():
    for i in range(100):
        light()
        medium()
        medium()
    time.sleep(2)


def error_raiser():
    raise RuntimeError('BOOM!')


def main():
    for i in range(2):
        heavy()
        try:
            error_raiser()
        except RuntimeError as e:
            print e


def print_stats(name, s, *stats_filter):
    print '=' * 40, name, '=' * 40
    s.print_stats(*stats_filter)


def fib_iterative(n):
    if n == 1:
        return 0
    a, b = 0, 1
    for i in range(2, n):
        a, b = b, a+b
    return b


def fib_recursive(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fib_recursive(n-2) + fib_recursive(n-1)


def fib_generator(n):
    def the_generator():
        a, b = 0, 1
        while 1:
            yield a
            a, b = b, a+b
    for _, fib in zip(range(n), the_generator()):
        pass
    return fib


def stats_for_main():
    p = Profile()
    p.runcall(main)
    p.dump_stats('main.stats')
    s = Stats(p)
    s.strip_dirs().sort_stats('time', 'cumulative')
    print_stats('MAIN - ALL STATS', s)
    print_stats('MAIN - CALLERS', s, 'sleep')
    print_stats('MAIN - CALLEES', s, 'heavy')


def stats_for_fib(type_, fib):
    p = Profile()
    p.runcall(fib, 30)
    p.dump_stats(type_.lower().replace(' ', '_') + '.stats')
    s = Stats(p)
    s.strip_dirs().sort_stats('time', 'cumulative')
    print_stats(type_, s)


if __name__ == '__main__':
    stats_for_main()
    stats_for_fib('ITERATIVE FIBONACCI', fib_iterative)
    stats_for_fib('RECURSIVE FIBONACCI', fib_recursive)
    stats_for_fib('GENERATOR FIBONACCI', fib_generator)
