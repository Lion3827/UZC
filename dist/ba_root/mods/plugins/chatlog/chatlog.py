# ba_meta require api 9

from __future__ import annotations

import collections
import threading

_buffer: collections.deque = collections.deque(maxlen=50)
_lock = threading.Lock()


def push(aid: str, name: str, msg: str) -> None:
    with _lock:
        _buffer.append({
            'aid':  aid,
            'name': name,
            'msg':  msg,
        })


def snapshot() -> list:
    with _lock:
        return list(_buffer)


def enable() -> None:
    print('[chatlog] cargado')
