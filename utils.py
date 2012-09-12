import random
import string


def generate_random_string(length, symbols=string.letters):
    return ''.join(random.choice(symbols) for i in xrange(length))


class Signal(object):
    def __init__(self):
        self.callbacks = set()

    def connect(self, callback):
        self.callbacks.add(callback)

    def disconnect(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def disconnect_all(self):
        self.callbacks.clear()

    def emit(self, *args, **kwargs):
        for callback in self.callbacks.copy():
            callback(*args, **kwargs)
