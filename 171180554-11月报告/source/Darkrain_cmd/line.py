from config import *
import primitive
from PyQt5 import QtCore, QtGui


class Line(primitive.Primitive):
    """line class"""

    def __init__(self, sPos: QtCore.QPoint = QtCore.QPoint(0, 0),
                 ePos: QtCore.QPoint = QtCore.QPoint(0, 0),
                 color: QtGui.QColor = QtGui.QColor("black"),
                 algorithm: str = "Bresenham"):
        super().__init__()
        self.startPos = sPos
        self.endPos = ePos
        self.color = color
        self.algorithm = algorithm
        if algorithm != "Bresenham" and algorithm != "DDA":
            ErrorExit("Wrong Line Algorithm", -1)
        self.pointList = []
        if sPos != ePos:
            self.rewrite()

    def setStart(self, pst=QtCore.QPoint):
        self.startPos = pst

    def setEnd(self, pst=QtCore.QPoint):
        """set the end point of the line
        """
        self.endPos = pst
        self.rewrite()

    def rewrite(self):
        # clear PointList
        self.pointList.clear()

        # start rewrite
        if self.startPos.x() != self.endPos.x():
            if self.algorithm == "Bresenham":
                self.AlgorBresenham()
            else:
                self.AlgorDDA()
        else:  # k not exit
            if self.startPos.y() < self.endPos.y():
                for i in range(self.startPos.y(), self.endPos.y()):
                    self.pointList.append(QtCore.QPoint(self.startPos.x(), i))
            else:
                for i in range(self.endPos.y(), self.startPos.y()):
                    self.pointList.append(QtCore.QPoint(self.startPos.x(), i))

    def getDrawPoint(self):
        return self.pointList

    def AlgorDDA(self):
        # set x and y pos
        startX = self.startPos.x()
        startY = self.startPos.y()
        endX = self.endPos.x()
        endY = self.endPos.y()

        # get k of the line
        k = (endY - startY) / (endX - startX)

        dX = abs(self.startPos.x() - self.endPos.x())
        dY = abs(self.startPos.y() - self.endPos.y())
        # 2 way:
        if -1 <= k <= 1:
            # get start end
            if startX > endX:
                startX = self.endPos.x()
                startY = self.endPos.y()
                endX = self.startPos.x()
                endY = self.startPos.y()
            else:
                pass
            y = float(startY)
            for x in range(startX, endX + 1):
                if y > 0:
                    temp = int(y + 0.5)
                else:
                    temp = int(y - 0.5)
                self.pointList.append(QtCore.QPoint(x, temp))
                y += k
        else:  # |k|>1
            # get start end
            if startY > endY:
                startX = self.endPos.x()
                startY = self.endPos.y()
                endX = self.startPos.x()
                endY = self.startPos.y()
            else:
                startY -= 0
            x = float(startX)
            for y in range(startY, endY + 1):
                if x > 0:
                    temp = int(x + 0.5)
                else:
                    temp = int(x - 0.5)
                self.pointList.append(QtCore.QPoint(temp, y))
                x += 1 / k
        pass  # end of AlgorBresenham

    def AlgorBresenham(self):
        # set x and y pos
        startX = self.startPos.x()
        startY = self.startPos.y()
        endX = self.endPos.x()
        endY = self.endPos.y()

        # get k of the line
        k = (endY - startY) / (endX - startX)

        dX = abs(self.startPos.x() - self.endPos.x())
        dY = abs(self.startPos.y() - self.endPos.y())
        # 2 way:
        if -1 <= k <= 1:
            d1 = 2 * dY
            d2 = 2 * (dY - dX)
            p = 2 * dY - dX
            # choose step
            if k > 0:
                step = 1
            else:
                step = -1
            # get start end
            if startX > endX:
                startX = self.endPos.x()
                startY = self.endPos.y()
                endX = self.startPos.x()
                endY = self.startPos.y()
            y = startY
            self.pointList.append(QtCore.QPoint(startX, startY))
            self.pointList.append(QtCore.QPoint(endX, endY))
            for x in range(startX, endX + 1):
                self.pointList.append(QtCore.QPoint(x, y))
                if p < 0:
                    p += d1
                else:
                    y += step
                    p += d2

        else:  # |k|>1
            d1 = 2 * dX
            d2 = 2 * (dX - dY)
            p = 2 * dX - dY
            # choose step
            if k > 0:
                step = 1
            else:
                step = -1
            # get start end
            if startY > endY:
                startX = self.endPos.x()
                startY = self.endPos.y()
                endX = self.startPos.x()
                endY = self.startPos.y()
            x = startX
            for y in range(startY, endY + 1):
                self.pointList.append(QtCore.QPoint(x, y))
                if p < 0:
                    p += d1
                else:
                    x += step
                    p += d2
        pass  # end of AlgorBresenham

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

    def clip(self, x1: int, y1: int, x2: int, y2: int, algorithm: str):
        if algorithm:
            self.clip_Cohen_Sutherland(x1, y1, x2, y2)
        self.rewrite()

    def clip_Cohen_Sutherland(self, x1: int, y1: int, x2: int, y2: int):
        xMin = x1
        yMin = y1
        xMax = x2
        yMax = y2
        X1 = float(self.startPos.x())
        Y1 = float(self.startPos.y())
        X2 = float(self.endPos.x())
        Y2 = float(self.endPos.y())
        code1 = getOutCode(X1, Y1, xMin, xMax, yMin, yMax)
        code2 = getOutCode(X2, Y2, xMin, xMax, yMin, yMax)
        acc = False
        while True:
            if (code1 | code2) == 0:
                acc = True
                break
            elif code1 & code2:
                break
            else:
                code = code1
                if code1 == 0:
                    code = code2
                if code & TOP:
                    x = X1 + (X2 - X1) * (yMax - Y1) / (Y2 - Y1)
                    y = yMax
                elif code & BOTTOM:
                    x = X1 + (X2 - X1) * (yMin - Y1) / (Y2 - Y1)
                    y = yMin
                elif code & RIGHT:
                    y = Y1 + (Y2 - Y1) * (xMax - X1) / (X2 - X1)
                    x = xMax
                else:
                    y = Y1 + (Y2 - Y1) * (xMin - X1) / (X2 - X1)
                    x = xMin

                if code == code1:
                    X1 = x
                    Y1 = y
                    code1 = getOutCode(X1, Y1, xMin, xMax, yMin, yMax)
                else:
                    X2 = x
                    Y2 = y
                    code2 = getOutCode(X2, Y2, xMin, xMax, yMin, yMax)
        if acc:
            self.startPos = QtCore.QPoint(toInt(X1), toInt(Y1))
            self.endPos = QtCore.QPoint(toInt(X2), toInt(Y2))
        else:
            self.startPos = QtCore.QPoint(-1, -1)
            self.endPos = QtCore.QPoint(-1, -1)
        pass
