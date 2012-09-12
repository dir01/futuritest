import argparse
import random
import urllib2
from urlparse import urljoin

from utils import generate_random_string


def send_request(BASE_URL):
    opener = urllib2.build_opener()
    user_id = random.randint(0, 12)
    if user_id:
        opener.addheaders.append(('Cookie', 'id=%s' % user_id))
    path_length = random.randint(0, 20)
    path = generate_random_string(path_length)
    opener.open(urljoin(BASE_URL, path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs=1, default='http://ec2-107-21-87-174.compute-1.amazonaws.com/')
    args = parser.parse_args()

    while True:
        send_request(args.url[0])
