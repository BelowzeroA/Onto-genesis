from enum import Enum


class AlgoNodeType(Enum):
    Signaller = 1
    ResponseAwaiter = 2
    Delay = 3