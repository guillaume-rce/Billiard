import tkinter as tk
import numpy as np

_RATIO = 8
_DIMENSION = 190, 95
_BILLE = 6.15

def init():
    root = tk.Tk()

    _CANVAS = tk.Canvas(root, height= _DIMENSION[1]*_RATIO+100, width=_DIMENSION[0]*_RATIO+100)
    _CANVAS.pack()

    _CANVAS.create_rectangle(50, 50, _DIMENSION[0]*_RATIO, _DIMENSION[1]*_RATIO, fill="green")

    return root, _CANVAS


def ajoutBille(canvas, position, color):
    bille = canvas.create_oval(position[1]+50, position[0]+50, position[1]+(_BILLE*_RATIO)+50,position[0]+(_BILLE*_RATIO)+50, fill=color)
    return bille

def ajoutTrou(canvas, position):
    trou = canvas.create_rectangle(position[0]*_RATIO, position[1]*_RATIO, position[0]*_RATIO+50, position[1]*_RATIO+50, fill="black")
    return trou

def creatTable(positionRouge, positionJaune, positionNoir, positionBlanche, posTrou):
    bille = {"rouge":[], "jaune":[], "blanche":[], "noir":[]}
    trou = []
    for pos in posTrou:
        trou.append((ajoutTrou(_canvas, pos), pos))
    if positionRouge:
        for position in positionRouge:
            bille["rouge"].append((ajoutBille(_canvas, position, "red"), position))
    if positionJaune:
        for position in positionJaune:
            bille["jaune"].append((ajoutBille(_canvas, position, "yellow"), position))
    if positionNoir:
        bille["noir"] = (ajoutBille(_canvas, positionNoir, "black"), positionNoir)
    if positionBlanche:
        bille["blanche"] = (ajoutBille(_canvas, positionBlanche, "white"), positionNoir)
    return {"bille":bille, "trou":trou}

def Trai(selectBille, table, canvas):
    for trai in selectBille:
        trou = table["trou"][trai-2][1]
        bille = selectBille[trai][1][1]
        canvas.create_line(trou[0]*_RATIO+50, trou[1]*_RATIO+50, bille[0]+50, bille[1]+50)

def selectBille(table, joeur):
    posTrou = table["trou"]
    posBille = table["bille"][joeur]
    dist = {}
    for trou in posTrou:
        distTrou = []
        for bille in posBille:
            pos = np.array([ trou[1][0] - bille[1][0], trou[1][1] - bille[1][1]])
            print(pos)
            distTrou.append(np.linalg.norm(pos))
        dist[trou[0]] = (round(min(distTrou),2), posBille[distTrou.index(min(distTrou))])
    return dist

root, _canvas = init()
positionRouge = [[30, 40], [100, 100], [500,800]]
positionTrou = ([0,0], [_DIMENSION[0], 0], [0, _DIMENSION[1]], [_DIMENSION[0], _DIMENSION[1]])
table = creatTable(positionRouge, [], [], [], positionTrou)
print(table)
dist = selectBille(table, "rouge")
print(dist)
Trai(dist, table, _canvas)



root.mainloop()
