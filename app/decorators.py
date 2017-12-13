from threading import Thread
from multiprocessing import Process


def async_thread(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def async_process(f):
    def wrapper(*args, **kwargs):
        p = Process(target=f, args=args, kwargs=kwargs)
        p.start()
    return wrapper
