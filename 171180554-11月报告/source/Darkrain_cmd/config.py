import sys
from math import sin, cos, pi
from os import path
from os import makedirs


# output
def mkdir(path_):
    folder = path.exists(path_)
    if not folder:
        makedirs(path_)


# def LOG
def LOG(x):
    print('LOG: ' + x)


def ErrorExit(string="ERROR", outNum=-1):
    sys.stderr.write(string)
    raise SystemExit(outNum)


def sin_(r: int):
    return sin(pi * r / 180)


def cos_(r: int):
    return cos(pi * r / 180)


def toInt(x: float) -> int:
    if x > 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


# for clip
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def getOutCode(x:float,y:float,xMin:int,xMax:int,yMin:int,yMax:int):
    code = 0
    if x<xMin:
        code |= LEFT
    elif x>xMax:
        code |= RIGHT
    if y < yMin:
        code |= BOTTOM
    elif y > yMax:
        code |= TOP
    return code
