from PyQt5 import QtCore
from config import *


class Primitive:
    def __init__(self):
        self.isEnd = True
        pass

    @staticmethod
    def setStart(self, pst: QtCore.QPoint):
        LOG("EMPTY!!!")
        pass

    @staticmethod
    def setEnd(self, pst: QtCore.QPoint):
        LOG("EMPTY")

    @staticmethod
    def rewrite(self):
        LOG("Empty")

    @staticmethod
    def returnPointList(self):
        LOG("empty")

    @staticmethod
    def translate(self, dx: int, dy: int):
        pass

    @staticmethod
    def rotate(self, x: int, y: int, r: int):
        pass

    @staticmethod
    def scale(self, x: int, y: int, r: float):
        pass

    @staticmethod
    def clip(self, x1: int, y1: int, x2: int, y2: int, algorithm: str):
        pass

    def endInput(self):
        pass
