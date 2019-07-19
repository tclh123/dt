import time
import random
import string
import importlib


def import_class(s):
    if ':' in s:
        mod, attr = s.split(':')
    else:
        parts = s.split('.')
        mod, attr = parts[:-1], parts[-1]
    return getattr(importlib.import_module(mod), attr)


def random_string(n):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(n))


def gen_timestamp():
    return int(time.time())
