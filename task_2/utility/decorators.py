import time

def request_time_used(debug):
    '''Prints amount of time passed and records return by the request function'''
    def decorator(func):
        def wrapper(*args, **kwargs):
            if debug:
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                print(f'operation took {round(end - start, 3)} seconds')
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
