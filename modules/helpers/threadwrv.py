from threading import Thread
from typing import Any


class ThreadWRV(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args) -> Any:
        Thread.join(self, *args)
        return self._return
