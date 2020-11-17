from config import *
import primitive
import line
from PyQt5 import QtCore, QtGui


class Curve(primitive.Primitive):
    def __init__(self, color: QtGui.QColor = QtGui.QColor("black"),
                 algorithm: str = "Bezier"):
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

    def changePos(self, pos: QtCore.QPoint, num: int = None):
        if num is None:
            num = len(self.PosiSet) - 1
        self.PosiSet[num] = pos

    # end the polygon input
    def endInput(self):
        self.isEnd = True
        self.rewrite()

    def rewrite(self):
        self.pointList.clear()

    def returnPointList(self):
        self.pointList.clear()
        if len(self.PosiSet) < 2:
            return

        if self.algorithm == "Bezier":
            self.curve_bezier()
        else:
            self.curve_bspline()

        rtn = self.pointList.copy()
        self.pointList.clear()
        return rtn

    def curve_bezier(self):
        # LOG("bezier")
        x = self.PosiSet[0].x()
        y = self.PosiSet[0].y()
        pos_len = len(self.PosiSet)
        x_array = [0.0] * pos_len
        y_array = [0.0] * pos_len

        self.pointList.append(self.PosiSet[0])
        t = 0.0
        while t <= 1:
            for k in range(pos_len):
                x_array[k] = self.PosiSet[k].x()
                y_array[k] = self.PosiSet[k].y()
            for i in range(1, pos_len):
                for j in range(pos_len - i):
                    x_array[j] = (1 - t) * x_array[j] + t * x_array[j + 1]
                    y_array[j] = (1 - t) * y_array[j] + t * y_array[j + 1]
            if abs(toInt(x_array[0]) - toInt(x)) == 0 and abs(toInt(y_array[0]) - toInt(y)) == 0:
                pass
            elif abs(toInt(x_array[0]) - toInt(x)) <= 1 and abs(toInt(y_array[0]) - toInt(y)) <= 1:
                self.pointList.append(QtCore.QPoint(toInt(x_array[0]), toInt(y_array[0])))
            else:
                tempLine = line.Line(QtCore.QPoint(toInt(x), toInt(y)),
                                     QtCore.QPoint(toInt(x_array[0]), toInt(y_array[0])),
                                     self.color, "Bresenham")
                tempList = tempLine.getDrawPoint()
                if tempList is not None:
                    self.pointList.extend(tempLine.getDrawPoint())
            x = x_array[0]
            y = y_array[0]
            t += 1 / 64 * pos_len

    def curve_bspline(self):
        k = 3
        pos_len = len(self.PosiSet)

        begin = True
        x_s = 0
        y_s = 0

        u = k
        while u <= pos_len:
            x = 0
            y = 0
            for i in range(pos_len):
                ratio = self.bspline_tool(u, i, k)
                # LOG(ratio)
                x += self.PosiSet[i].x() * ratio
                y += self.PosiSet[i].y() * ratio
            # LOG(x, y)
            if x == 0 and y == 0:
                u += 1.0 / 100
                continue
            if begin is True:
                self.pointList.append(QtCore.QPoint(toInt(x), toInt(y)))
                x_s = x
                y_s = y
                begin = False
            else:
                if abs(toInt(x_s) - toInt(x)) == 0 and abs(toInt(y_s) - toInt(y)) == 0:
                    pass
                elif abs(toInt(x_s) - toInt(x)) <= 1 and abs(toInt(y_s) - toInt(y)) <= 1:
                    self.pointList.append(QtCore.QPoint(toInt(x), toInt(y)))
                else:
                    tempLine = line.Line(QtCore.QPoint(toInt(x_s), toInt(y_s)),
                                         QtCore.QPoint(toInt(x), toInt(y)),
                                         self.color, "Bresenham")
                    tempList = tempLine.getDrawPoint()
                    if tempList is not None:
                        self.pointList.extend(tempLine.getDrawPoint())
                x_s = x
                y_s = y
            u += 1.0 / 100

    def bspline_tool(self, u, i: int, k: int):
        # LOG(u, ' ', i, ' ', k)
        if k == 0:
            if i < u < i + 1:
                return 1
            else:
                return 0
        res = 0.0
        if k != 0:
            res += (u - i) / k * self.bspline_tool(u, i, k - 1) \
                   + (i + k + 1 - u) / k * self.bspline_tool(u, i + 1, k - 1)
        return res

    def translate(self, dx: int, dy: int):
        # LOG("trans: ", dx, dy)
        for i in range(len(self.PosiSet)):
            point = self.PosiSet[i]
            temp_x = point.x()
            temp_y = point.y()
            # LOG(temp_x + dx, ' ', temp_y + dy)
            self.PosiSet[i] = QtCore.QPoint(temp_x + dx, temp_y + dy)
        self.startPos = self.PosiSet[0]
        self.rewrite()

    def rotate(self, x: int, y: int, r: int):
        # LOG("base: ", x, " ", y)
        for i in range(len(self.PosiSet)):
            point = self.PosiSet[i]
            temp_x = point.x()
            temp_y = point.y()
            # LOG("node ", i, ': ', temp_x, " ", temp_y)
            # LOG(r, cos_(r), sin_(r))
            # LOG(x + (temp_x - x) * cos_(r) - (temp_y - y) * sin_(r),
            #     ' ',
            #     y + (temp_x - x) * sin_(r) + (temp_y - y) * cos_(r))
            self.PosiSet[i] = QtCore.QPoint(toInt(x + (temp_x - x) * cos_(r) - (temp_y - y) * sin_(r)),
                                            toInt(y + (temp_x - x) * sin_(r) + (temp_y - y) * cos_(r)))
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
