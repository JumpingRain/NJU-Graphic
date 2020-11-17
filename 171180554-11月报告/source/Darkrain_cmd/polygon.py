from config import *
import primitive
import line
from PyQt5 import QtCore, QtGui


class Polygon(primitive.Primitive):
    def __init__(self, color: QtGui.QColor = QtGui.QColor("black"),
                 algorithm: str = "Bresenham"):
        super().__init__()
        self.startPos = QtCore.QPoint(0, 0)
        self.PosiSet = []
        self.color = color
        self.algorithm = algorithm
        self.pointList = []
        # already be completely draw?
        self.isEnd = False

    def setStart(self, pst: QtCore.QPoint):
        self.startPos = pst
        self.PosiSet.append(pst)

    def appendPos(self, pst: QtCore.QPoint):
        self.PosiSet.append(pst)
        self.rewrite()

    def changePos(self, pos: QtCore.QPoint, num: int = None):
        if num is None:
            num = len(self.PosiSet) - 1
        self.PosiSet[num] = pos
        self.rewrite()

    # end the polygon input
    def endInput(self):
        self.isEnd = True
        self.rewrite()

    def rewrite(self):
        self.pointList.clear()
        if len(self.PosiSet) < 2:
            return

        # normal line
        for i in range(len(self.PosiSet) - 1):
            tempLine = line.Line(self.PosiSet[i], self.PosiSet[i + 1], self.color, self.algorithm)
            self.pointList.extend(tempLine.getDrawPoint())
            del tempLine

        # add last line
        if self.isEnd is True:
            tempLine = line.Line(self.PosiSet[len(self.PosiSet) - 1], self.startPos, self.color, self.algorithm)
            self.pointList.extend(tempLine.getDrawPoint())
            del tempLine

    def translate(self, dx: int, dy: int):
        for i in range(len(self.PosiSet)):
            point = self.PosiSet[i]
            temp_x = point.x()
            temp_y = point.y()
            self.PosiSet[i] = QtCore.QPoint(temp_x + dx, temp_y + dy)
        self.startPos = self.PosiSet[0]
        self.rewrite()

    def rotate(self, x: int, y: int, r: int):
        for i in range(len(self.PosiSet)):
            point = self.PosiSet[i]
            temp_x = point.x()
            temp_y = point.y()
            self.PosiSet[i] = QtCore.QPoint(x + (temp_x - x) * cos_(r) - (temp_y - y) * sin_(r),
                                            y + (temp_x - x) * sin_(r) - (temp_y - y) * cos_(r))
        self.startPos = self.PosiSet[0]
        self.rewrite()

    def scale(self, x: int, y: int, r: float):
        for i in range(len(self.PosiSet)):
            point = self.PosiSet[i]
            temp_x = point.x()
            temp_y = point.y()
            self.PosiSet[i] = QtCore.QPoint(toInt(temp_x * r + x * (1 - r)),
                                            toInt(temp_y * r + y * (1 - r)))
        self.startPos = self.PosiSet[0]
        self.rewrite()