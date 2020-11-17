from PyQt5.QtGui import QPixmap, QColor, QPen, QPainter
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QApplication
import line, ellipse, curve, primitive, polygon
from config import *
import sys


class MyLabel:
    def __init__(self):
        # init PixMap
        self.mainPixMap = QPixmap(100, 100)
        self.mainPixMap.fill(QColor("white"))

        # init painter
        self.mainPen = QPen()
        self.mainPen.setColor(QColor("black"))
        self.mainPen.setWidth(1)
        self.painter = QPainter()
        self.painter.begin(self.mainPixMap)
        self.painter.setPen(self.mainPen)

        # init primList to save primitives
        self.primList = {}
        self.nowPrim = -1
        self.nowChoose = -1

    def reShowPic(self) -> None:
        self.mainPixMap.fill(QColor("white"))
        # TODO:REWRITE!!!!!!!!! reset_color
        tempColor = self.mainPen.color()
        for x in self.primList:
            prim = self.primList[x]
            self.mainPen.setColor(prim.color)
            self.painter.setPen(self.mainPen)
            tempList = prim.returnPointList()
            for point in tempList:
                self.painter.drawPoint(point)
        self.mainPen.setColor(tempColor)
        self.painter.setPen(self.mainPen)

    def resetCanvas(self, width, height):
        if width <= 0 or height <= 0:
            LOG("illegal width or height")
            return
        self.painter.end()
        self.mainPixMap = QPixmap(width, height)
        self.mainPixMap.fill(QColor("white"))
        self.painter.begin(self.mainPixMap)
        self.painter.setPen(self.mainPen)
        self.primList.clear()

    def saveCanvas(self, pass_file, dirName):
        self.reShowPic()
        filePath = './' + dirName + '/' + pass_file + '.bmp'
        if filePath:
            if self.mainPixMap.save(filePath) is None:
                LOG("save failed")
        if filePath is None:
            LOG("save failed")
        LOG("SavePath: " + filePath)

    def setColor(self, R: int, G: int, B: int):
        self.mainPen.setColor(QColor(R, G, B))
        self.painter.setPen(self.mainPen)

    def drawLine_(self, id_, x1, y1, x2, y2, algorithm):
        newLine = line.Line(QPoint(x1, y1), QPoint(x2, y2), self.mainPen.color(), algorithm)
        self.primList[id_] = newLine

    def drawPolygon_(self, id_, n, algorithm, node_list):
        if len(node_list) <= 2:
            LOG("too small points for polygon")
            return
        newPolygon = polygon.Polygon(self.mainPen.color(), algorithm)
        newPolygon.setStart(QPoint(node_list[0], node_list[1]))
        s = 2
        while s < len(node_list):
            newPolygon.appendPos(QPoint(node_list[s], node_list[s + 1]))
            s += 2
        newPolygon.endInput()
        self.primList[id_] = newPolygon

    def drawEllipse_(self, id_, x, y, rx, ry):
        newEllipse = ellipse.Ellipse(self.mainPen.color())
        newEllipse.setStart(QPoint(x - rx, y - ry))
        newEllipse.setEnd(QPoint(x + rx, y + ry))
        self.primList[id_] = newEllipse

    def drawCurve_(self, id_, n, algorithm, node_list):
        if len(node_list) <= 2:
            LOG("too small points for polygon")
            return
        newCurve = curve.Curve(self.mainPen.color(), algorithm)
        newCurve.setStart(QPoint(node_list[0], node_list[1]))
        s = 2
        while s < len(node_list):
            newCurve.appendPos(QPoint(node_list[s], node_list[s + 1]))
            s += 2
        newCurve.endInput()
        self.primList[id_] = newCurve

    def translate_(self, id_, dx, dy):
        self.primList[id_].translate(dx, dy)

    def rotate_(self, id_, x, y, r):
        self.primList[id_].rotate(x, y, r)

    def scale_(self, id_, x, y, r):
        self.primList[id_].scale(x, y, r)

    def clip_(self, id_, x1, y1, x2, y2, algorithm):
        self.primList[id_].clip(x1, y1, x2, y2, algorithm)

    def start(self, _filename, _saveDir):
        f = open(_filename)
        lineStr = f.readline()
        while lineStr:
            sList = lineStr.split()
            if len(sList) == 0:
                lineStr = f.readline()
                continue
            sHead = sList[0]
            # LOG(sList)
            # start
            if sHead == "resetCanvas":
                self.resetCanvas(int(sList[1]), int(sList[2]))
            elif sHead == "saveCanvas":
                self.saveCanvas(sList[1], _saveDir)
            elif sHead == "setColor":
                self.setColor(int(sList[1]), int(sList[2]), int(sList[3]))
            elif sHead == "drawLine":
                self.drawLine_(int(sList[1]), int(sList[2]), int(sList[3]),
                               int(sList[4]), int(sList[5]), sList[6])
            elif sHead == "drawPolygon":
                temp_id = int(sList[1])
                temp_n = int(sList[2])
                temp_al = sList[3]
                lineStr = f.readline()
                sList = lineStr.split()
                num_list_new = [int(x) for x in sList]
                self.drawPolygon_(temp_id, temp_n, temp_al, num_list_new)
            elif sHead == "drawEllipse":
                self.drawEllipse_(int(sList[1]), int(sList[2]), int(sList[3]),
                                  int(sList[4]), int(sList[5]))
            elif sHead == "drawCurve":
                temp_id = int(sList[1])
                temp_n = int(sList[2])
                temp_al = sList[3]
                lineStr = f.readline()
                sList = lineStr.split()
                num_list_new = [int(x) for x in sList]
                self.drawCurve_(temp_id, temp_n, temp_al, num_list_new)
            elif sHead == "translate":
                self.translate_(int(sList[1]), int(sList[2]), int(sList[3]))
            elif sHead == "rotate":
                self.rotate_(int(sList[1]), int(sList[2]), int(sList[3]), int(sList[4]))
            elif sHead == "scale":
                self.scale_(int(sList[1]), int(sList[2]), int(sList[3]), float(sList[4]))
            elif sHead == "clip":
                self.clip_(int(sList[1]), int(sList[2]), int(sList[3]),
                           int(sList[4]), int(sList[5]), sList[6])
            else:
                LOG("Error find! Please check input:")
                LOG("Failed input as: ", lineStr)
            # end
            lineStr = f.readline()

        LOG("DarkrainSp finish")
        sys.exit()
        pass


if __name__ == "__main__":
    App = QApplication([])
    if len(sys.argv) != 3:
        LOG("输入参数数量错误")
        exit()
    filename = sys.argv[1]
    saveDir = sys.argv[2]
    mkdir(saveDir)
    myLabel = MyLabel()
    LOG("DarkrainSp start")
    myLabel.start(filename, saveDir)
