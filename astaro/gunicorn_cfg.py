import multiprocessing

cores = multiprocessing.cpu_count()
workers = multiprocessing.cpu_count() * 2 + 1
print "%s CPU cores found. Starting %d workers" % (cores, workers)

bind = "127.0.0.1:8000"

#accesslog = "/var/log/gunicorn/access.log"
#errorlog  = "/var/log/gunicorn/error.log"
