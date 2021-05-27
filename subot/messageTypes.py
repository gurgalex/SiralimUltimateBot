from dataclasses import field, dataclass
from enum import Enum, auto
import numpy as np
from typing import Union



class MessageType(Enum):
    NEW_FRAME = auto()
    SCAN_FOR_ITEMS = auto()
    DRAW_DEBUG = auto()


@dataclass()
class ScanForItems:
    type: MessageType = field(init=False, default=MessageType.SCAN_FOR_ITEMS)

@dataclass()
class DrawDebug:
    type: MessageType = field(init=False, default=MessageType.DRAW_DEBUG)

@dataclass()
class NewFrame:
    """A new frame has arrived for processing"""
    type: MessageType = field(init=False, default=MessageType.NEW_FRAME)
    frame: np.ndarray


MessageImpl = Union[NewFrame, ScanForItems]