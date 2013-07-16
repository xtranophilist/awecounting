import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
errorlog = 'gunicorn.log'
#accesslog = 'gunicorn-access.log'
#loglevel = 'debug'
proc_name = 'gunicorn_acubor'
