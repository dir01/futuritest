import random
import string


def generate_random_string(length, symbols=string.letters):
    return ''.join(random.choice(symbols) for i in xrange(length))
