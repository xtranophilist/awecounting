import multiprocessing

bind = "127.0.0.1:8000"
workers = 3
errorlog = '../log/gunicorn.log'
#accesslog = 'gunicorn-access.log'
#loglevel = 'debug'
proc_name = 'gunicorn_acubor'
