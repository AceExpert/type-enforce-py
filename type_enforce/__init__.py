from typing import NamedTuple, Literal, List

from .core import enforce_type
from .processors import argument_processor
from . import utils

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

__all__: List[str] = ['enforce_type', 'argument_processor', 'utils']
__version__: str = "0.5"
version_info: VersionInfo = VersionInfo(major=3, minor=8, micro=6, releaselevel='final', serial=0)
__author__: str = "Cybertron"
__copyright__: str = "Copyright (c) 2021 - present Cybertron"