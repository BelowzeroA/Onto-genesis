from enum import Enum


class AlgoNodeType(Enum):
    Ramification = 1
    Signaller = 2
    ResponseAwaiter = 3
    Delay = 4