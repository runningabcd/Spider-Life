from functools import wraps
import time


def run_time(func):
    @wraps(func)
    def runti(*args, **kwargs):
        start_ti = time.perf_counter()
        r = func(*args, **kwargs)
        end_ti = time.perf_counter()
        _ti = end_ti - start_ti
        print(f'{func.__name__} >>>>> run times >>>>> {_ti}')
        return r

    return runti
