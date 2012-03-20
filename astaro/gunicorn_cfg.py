import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
#accesslog = "/var/log/gunicorn/access.log"
#errorlog  = "/var/log/gunicorn/error.log"

