# Copyright (c) 2024 Julian Müller (ChaoticByte)

from os import environ as _environ
from pathlib import Path as _Path
from .msg import ComponentLogger as _ComponentLogger

_logger = _ComponentLogger("Environment", print_timestamp=False)

try:
    ACCESS_CONTROL_ALLOW_ORIGIN = str(_environ["ACCESS_CONTROL_ALLOW_ORIGIN"])
    API_STT_MODEL = _Path(_environ["API_STT_MODEL"])
except KeyError as e:
    _logger.critical(f"Missing {e}")
    exit(1)
except Exception as e:
    _logger.critical(f"An exception occured: {e}")
    exit(1)
