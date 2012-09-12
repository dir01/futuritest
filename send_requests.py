import random
import urllib2
from urlparse import urljoin

from utils import generate_random_string

BASE_URL = 'http://127.0.0.1:8081'


def send_request():
    opener = urllib2.build_opener()
    user_id = random.randint(0, 12)
    if user_id:
        opener.addheaders.append(('Cookie', 'id=%s' % user_id))
    path_length = random.randint(0, 20)
    path = generate_random_string(path_length)
    opener.open(urljoin(BASE_URL, path))


if __name__ == '__main__':
    while True:
        send_request()
