from config import *
import primitive
from PyQt5 import QtCore, QtGui


class Curve(primitive.Primitive):
    def __init__(self, color: QtGui.QColor = QtGui.QColor("black")):
        super().__init__()
        self.startPos = QtCore.QPoint(0, 0)
        self.PosiSet = []
        self.color = color
        self.pointList = []

    def setStart(self, pst: QtCore.QPoint):
        self.startPos = pst
        self.PosiSet.append(pst)

    def appendPos(self, pst: QtCore.QPoint):
        lastPos = self.PosiSet[len(self.PosiSet) - 1]
        dX = abs(lastPos.x() - pst.x())
        dY = abs(lastPos.y() - pst.y())
        # need more action
        # ---
        if (dX <= 2 and dY <= 5) or (dY <= 2 and dX <= 5) \
                or (1/1.5 < dX / float(dY+0.1) <= 1.5 and (dX <= 6 or dY <= 6)):
            print("pass")
            pass
        else:
            print(self.PosiSet)
            self.PosiSet.append(pst)
            self.rewrite()

    def rewrite(self):
        # self.pointList.clear()

        print(len(self.PosiSet))
        if len(self.PosiSet) < 2:
            return

        # normal line
        i = len(self.PosiSet) - 2
        tempLine = line.Line(self.PosiSet[i], self.PosiSet[i + 1], self.color)
        self.pointList.extend(tempLine.getDrawPoint())
        del tempLine

        LOG("end rewrite")
