# Copyright (c) 2024 Julian Müller (ChaoticByte)

from datetime import datetime as _datetime
from os import environ as _environ
from sys import stderr as _stderr
from sys import stdout as _stdout
from typing import Any as _Any

class ComponentLogger:

    LEVELS = [
        "DEBUG",
        "INFO",
        "WARN",
        "ERROR",
        "CRITICAL"
    ]

    def __init__(self, component: str, level: int = 1, print_timestamp: bool = True):
        '''level may be overwritten by environment variable LOGLEVEL'''
        assert type(component) == str
        assert type(level) == int
        assert type(print_timestamp) == bool
        self.component = component
        self.level = level
        if "LOGLEVEL" in _environ:
            loglevel_ = _environ["LOGLEVEL"]
            if loglevel_ in self.LEVELS:
                self.level = self.LEVELS.index(loglevel_)
        self.print_timestamp = print_timestamp

    def _log(self, msg: _Any, level: int, file = _stdout):
        assert type(level) == int
        if level >= self.level:
            if self.print_timestamp:
                t = _datetime.now().astimezone().strftime(r'%Y-%m-%d %H:%M:%S %z')
                print(f"[{t}] [{self.component}] [{self.LEVELS[level]}] {msg}", file=file)
            else:
                print(f"[{self.component}] [{self.LEVELS[level]}] {msg}", file=file)

    def debug(self, msg: _Any):
        self._log(msg, 0)

    def info(self, msg: _Any):
        self._log(msg, 1)

    def warning(self, msg: _Any):
        self._log(msg, 2, file=_stderr)

    def error(self, msg: _Any):
        self._log(msg, 3, file=_stderr)

    def critical(self, msg: _Any):
        self._log(msg, 4, file=_stderr)
