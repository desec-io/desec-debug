import threading
from queue import Queue

import dns


_num_workers = 10
_queue = Queue(maxsize=0)
_workers = []


def _async_query(*, callback=None, **kwargs):
    _queue.put((callback, kwargs))


def _worker():
    while True:
        q = _queue.get()
        if q is None:
            break
        _do_work(*q)
        _queue.task_done()


def _do_work(callback, kwargs):
    response = dns.query.udp(**kwargs)
    if callback:
        callback(response, **kwargs)


def join():
    for _ in range(_num_workers):
        _queue.put(None)
    for w in _workers:
        w.join()


def query_all(where_list, q, **kwargs):
    _init()
    result = {}

    def rec(response, where, **kwargs):
        result[where_list[where]] = response

    for where in where_list:
        _async_query(
            q=q,  # TODO all queries use the same id .. but whatever for now
            where=where,
            callback=rec,
            **kwargs,
        )

    join()
    return result


def _init():
    _queue.queue.clear()  # TODO evil?
    while _workers:
        _workers.pop()
    for i in range(_num_workers):
        t = threading.Thread(target=_worker)
        t.start()
        _workers.append(t)
