# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from time import sleep
from celery import Celery


app = Celery('tasks', broker='amqp://', backend='redis://')


@app.task
def wait(secs):
    print('waiting for {secs} seconds.'.format(secs=secs))
    sleep(secs)
    print('done waiting {secs} seconds.'.format(secs=secs))


@app.task
def error(secs):
    print('throwing in {secs} seconds.'.format(secs=secs))
    sleep(secs)
    raise Exception('Thrown after {secs} seconds.'.format(secs=secs))


# Stuff for CLI experiments


from .debug import display_status  # noqa
g, b = wait.si(4), error.si(2)
