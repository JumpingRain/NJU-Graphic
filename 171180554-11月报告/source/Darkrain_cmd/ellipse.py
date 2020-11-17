from config import *
import primitive
from PyQt5 import QtCore, QtGui


class Ellipse(primitive.Primitive):
    def __init__(self, color: QtGui.QColor = QtGui.QColor("black")):
        super().__init__()
        self.startPos = QtCore.QPoint(0, 0)
        self.endPos = QtCore.QPoint(0, 0)
        self.PosiSet = []
        self.color = color
        self.pointList = []

    def setStart(self, pst=QtCore.QPoint):
        self.startPos = pst

    def setEnd(self, pst=QtCore.QPoint):
        """set the end point of the line"""
        self.endPos = pst
        self.rewrite()

    def rewrite(self):
        # clear PointList
        self.pointList.clear()

        # start rewrite
        # same y
        # TODO:why the ellipse disappear!
        if abs(self.startPos.x() - self.endPos.x()) <= 1:
            if self.startPos.y() < self.endPos.y():
                for i in range(self.startPos.y(), self.endPos.y()):
                    self.pointList.append(QtCore.QPoint(self.startPos.x(), i))
            else:
                for i in range(self.endPos.y(), self.startPos.y()):
                    self.pointList.append(QtCore.QPoint(self.startPos.x(), i))
        # same x
        elif abs(self.startPos.y() - self.endPos.y()) <= 1:
            if self.startPos.x() < self.endPos.x():
                for i in range(self.startPos.x(), self.endPos.x()):
                    self.pointList.append(QtCore.QPoint(i, self.startPos.y()))
            else:
                for i in range(self.endPos.x(), self.startPos.x()):
                    self.pointList.append(QtCore.QPoint(i, self.startPos.y()))
        # normal
        else:
            centerX = int((self.startPos.x() + self.endPos.x()) / 2)
            centerY = int((self.startPos.y() + self.endPos.y()) / 2)
            rX = int(abs(self.startPos.x() - self.endPos.x()) / 2)
            rY = int(abs(self.startPos.y() - self.endPos.y()) / 2)
            self.AlgorBresenhamCircle(centerX, centerY, rX, rY)

    def getDrawPoint(self):
        return self.pointList

    def AlgorBresenhamCircle(self, centerX, centerY, rx, ry):
        # get the long r and short r
        # horizontalFocus to judge if circle is horizontal
        if rx > ry:
            shortR = ry
            longR = rx
            horizontalFocus = True
        else:
            shortR = rx
            longR = ry
            horizontalFocus = False
        # get square
        SquareShortR = shortR * shortR
        SquareLongR = longR * longR
        # init temp point
        tempX = 0
        tempY = shortR

        # paint first half
        p1 = SquareShortR - SquareLongR * shortR + SquareLongR / 4.0
        while tempX * SquareShortR < tempY * SquareLongR:
            if p1 < 1:
                p1 += 2 * SquareShortR * tempX + 3 * SquareShortR
                tempX += 1
            else:
                p1 += 2 * SquareShortR * tempX + 3 * SquareShortR - 2 * SquareLongR * tempY + 2 * SquareLongR
                tempX += 1
                tempY -= 1
            self.addPoint(centerX, centerY, tempX, tempY, horizontalFocus)

        # paint last half
        p2 = SquareShortR * (tempX + 0.5) * (tempX + 0.5) \
            + SquareLongR * (tempY - 1) * (tempY - 1) \
            - SquareShortR * SquareLongR
        while tempY > 0:
            if p2 > 0:
                p2 -= 2 * SquareLongR * tempY + 3 * SquareLongR
                tempY -= 1
            else:
                p2 += 2 * SquareShortR * tempX + 3 * SquareShortR - 2 * SquareLongR * tempY + 2 * SquareLongR
                tempX += 1
                tempY -= 1
            self.addPoint(centerX, centerY, tempX, tempY, horizontalFocus)
        pass

    # draw four point
    def addPoint(self, centerX, centerY, x, y, horizontalFocus: bool):
        if horizontalFocus:
            self.pointList.append(QtCore.QPoint(-x + centerX, +y + centerY))
            self.pointList.append(QtCore.QPoint(+x + centerX, -y + centerY))
            self.pointList.append(QtCore.QPoint(-x + centerX, -y + centerY))
            self.pointList.append(QtCore.QPoint(+x + centerX, +y + centerY))
        else:
            self.pointList.append(QtCore.QPoint(-y + centerX, +x + centerY))
            self.pointList.append(QtCore.QPoint(+y + centerX, -x + centerY))
            self.pointList.append(QtCore.QPoint(-y + centerX, -x + centerY))
            self.pointList.append(QtCore.QPoint(+y + centerX, +x + centerY))

    def translate(self, dx: int, dy: int):
        self.startPos = QtCore.QPoint(self.startPos.x() + dx, self.startPos.y() + dy)
        self.endPos = QtCore.QPoint(self.endPos.x() + dx, self.endPos.y() + dy)
        self.rewrite()

    def rotate(self, x: int, y: int, r: int):
        temp_x = self.startPos.x()
        temp_y = self.startPos.y()
        self.startPos = QtCore.QPoint(x + (temp_x - x) * cos_(r) - (temp_y - y) * sin_(r),
                                      y + (temp_x - x) * sin_(r) - (temp_y - y) * cos_(r))
        temp_x = self.endPos.x()
        temp_y = self.endPos.y()
        self.endPos = QtCore.QPoint(x + (temp_x - x) * cos_(r) - (temp_y - y) * sin_(r),
                                    y + (temp_x - x) * sin_(r) - (temp_y - y) * cos_(r))
        self.rewrite()

    def scale(self, x: int, y: int, r: float):
        temp_x = self.startPos.x()
        temp_y = self.startPos.y()
        self.startPos = QtCore.QPoint(toInt(temp_x * r + x * (1 - r)),
                                      toInt(temp_y * r + y * (1 - r)))
        temp_x = self.endPos.x()
        temp_y = self.endPos.y()
        self.startPos = QtCore.QPoint(toInt(temp_x * r + x * (1 - r)),
                                      toInt(temp_y * r + y * (1 - r)))
        self.rewrite()