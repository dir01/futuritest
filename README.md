Installation
============

Dealing with parser requires the following steps:

1) Add custom log format to the `nginx.conf`'s `http` section

    log_format my_log_format '$msec|$cookie_id|$uri|$status|$request_time|$request_length';

2) Specify `my_log_format` as desired format for your `access.log`

    access_log  /var/log/nginx/futuritest-access.log my_log_format buffer=32k;

3) Create virtualenv

    virtualenv ~/env/

4) Install required python dependencies

    pip install -r requirements.txt

5) Run fake webserver (this webserver responds with random content for any dispatched url)

    python application.py

6) Run log monitor itself providing path to `access.log` file,
and, optionally, mongo database and collection names

    python logmonitor.py /var/log/nginx/futuritest-access.log --database=test --collection=logs

7) Generate fake traffic with `send_requests.py`

    python send_requests.py http://localhost/

8) In order to force log rotation

    sudo logrotate /etc/logrotate.d/nginx -vf


DB choice justification
=======================

Since task is pretty trivial, there is no much to justify, really.

MongoDB was chosen since it has rich query language which can potentially allow
any further logs analysis, write speed is high enough, and if not, write sharding
is supported out of box for easy horizontal scaling.
Long story short, it's good enough for our purposes.
