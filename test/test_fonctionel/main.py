import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from modules import table as tab

dimension = 190, 95
taille_bille = 5.7
trou = (
    [0, dimension[0], 0, dimension[0], dimension[0]/2, dimension[0]/2],
    [0, 0, dimension[1], dimension[1], 0, dimension[1]]
)
bille_rouge = [[30, 40, 150, 20], [40, 30, 70, 60]]
bille_jaune = [[10, 40, 150], [80, 40, 10]]
bille_blanche = [40, 80]
cmap = 'RdGy'

table = tab.Billard(
    trou,
    taille_bille,
    dimension,
    bille_rouge,
    bille_jaune,
    bille_blanche,
    cmap
)
table.repartBille("ROUGE")
table.selectTrou()
table.showLine()
table.selectBille()
table.affiche()