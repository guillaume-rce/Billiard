import matplotlib.pyplot as plt
import matplotlib.patches as pts
from matplotlib import cm
import numpy as np
from modules import utils

class Billard():
    def __init__(
        self,
        _TROU: tuple,
        _TAILLE_BILLE: float,
        _DIMENSION: tuple,
        _BILLE_ROUGE: list,
        _BILLE_JAUNE: list,
        _BILLE_BLANCHE: list,
        _CM: str,
    ) -> None:
        """
        La méthode init est le constructeur de la classe Billard. Elle est appelée lors de la création d'un objet de la classe Billard. Elle a pour but de définir les attributs de l'objet et de créer une figure matplotlib avec la table de billard et les billes.

        :param _TROU: un tuple de deux listes de coordonnées (x, y) représentant les positions des trous sur la table de billard
        :param _TAILLE_BILLE: la taille des billes en cm
        :param _DIMENSION: un tuple (largeur, hauteur) représentant les dimensions de la table de billard en cm
        :param _BILLE_ROUGE: une liste de deux listes de coordonnées (x, y) représentant les positions des billes rouges sur la table
        :param _BILLE_JAUNE: une liste de deux listes de coordonnées (x, y) représentant les positions des billes jaunes sur la table
        :param _BILLE_BLANCHE: une liste de deux coordonnées (x, y) représentant la position de la bille blanche sur la table
        :param _CM: un objet de la classe cm
        """
        self._TROU = _TROU
        self._TAILLE_BILLE = _TAILLE_BILLE
        self._DIMENSION = _DIMENSION
        self._BILLE_ROUGE = _BILLE_ROUGE
        self._BILLE_JAUNE = _BILLE_JAUNE
        self._BILLE_BLANCHE = _BILLE_BLANCHE
        self._CM = cm.get_cmap(_CM, 8)

        # Création de la figure matplotlib et de l'axe
        self.fig, self.ax = plt.subplots()
        
        # Création de l'objet représentant la table de billard et ajout à la figure
        self.table = pts.Rectangle((0, 0), _DIMENSION[0], _DIMENSION[1], color="green")
        self.ax.add_patch(self.table)
        
        # Création des objets représentant les billes rouges et jaunes et ajout à la figure
        for i in range(len(_BILLE_ROUGE[0])):
            c1 = plt.Circle((_BILLE_ROUGE[0][i], _BILLE_ROUGE[1][i]), radius=_TAILLE_BILLE/2, color="red")
            self.ax.add_artist(c1)

        for i in range(len(_BILLE_JAUNE[0])):
            c2 = plt.Circle((_BILLE_JAUNE[0][i], _BILLE_JAUNE[1][i]), radius=_TAILLE_BILLE/2, color="yellow")
            self.ax.add_artist(c2)
        
        # Création de l'objet représentant la bille blanche et ajout à la figure
        c3 = plt.Circle((_BILLE_BLANCHE[0], _BILLE_BLANCHE[1]), radius=_TAILLE_BILLE/2, color="white")
        self.ax.add_artist(c3)
        
        # Création des objets représentant les trous et ajout à la figure
        for i in range(len(_TROU[0])):
            self.ax.add_patch(pts.Rectangle((_TROU[0][i]-5, _TROU[1][i]-5), 10, 10))

    
    def updateParameters(
        self,
        _TROU: tuple = None,
        _TAILLE_BILLE: float = None,
        _DIMENSION: tuple = None,
        _BILLE_ROUGE: list = None,
        _BILLE_JAUNE: list = None,
        _BILLE_BLANCHE: list = None,
        _CM: cm = None,
    ) -> None:
        '''
        La méthode updateParameters permet de mettre à jour certains paramètres d'un objet de la classe Billard. Elle prend en paramètre plusieurs variables :

        :param _TROU: un tuple de deux listes de coordonnées (x, y) représentant les positions des trous sur la table de billard
        :param _TAILLE_BILLE: la taille des billes en cm
        :param _DIMENSION: un tuple (largeur, hauteur) représentant les dimensions de la table de billard en cm
        :param _BILLE_ROUGE: une liste de deux listes de coordonnées (x, y) représentant les positions des billes rouges sur la table
        :param _BILLE_JAUNE: une liste de deux listes de coordonnées (x, y) représentant les positions des billes jaunes sur la table
        :param _BILLE_BLANCHE: une liste de deux coordonnées (x, y) représentant la position de la bille blanche sur la table
        :param _CM: un objet de la classe cm

        La méthode vérifie si chaque variable a été passée en paramètre et si c'est le cas, elle met à jour l'attribut de l'objet avec la nouvelle valeur de la variable. Si la variable n'a pas été passée en paramètre, l'attribut n'est pas modifié.
        '''
        if _TROU is not None:
            self._TROU = _TROU

        if _TAILLE_BILLE is not None:
            self._TAILLE_BILLE = _TAILLE_BILLE
        
        if _DIMENSION is not None:
            self._DIMENSION = _DIMENSION

        if _BILLE_ROUGE is not None:
            self._BILLE_ROUGE = _BILLE_ROUGE
        
        if _BILLE_JAUNE is not None:
            self._BILLE_JAUNE = _BILLE_JAUNE
        
        if _BILLE_BLANCHE is not None:
            self._BILLE_BLANCHE = _BILLE_BLANCHE
        
        if _CM is not None:
            self._CM = cm.get_cmap(_CM, 8)

    def repartBille(self, couleurJoueur: str):
        '''
        La méthode repartBille de la classe Billard a pour but de déterminer les billes du joueur et les billes de l'adversaire en fonction de la couleur du joueur passée en paramètre (ROUGE ou JAUNE).

        Voici comment elle fonctionne en détail :

        - Si la couleur du joueur est ROUGE, alors l'attribut billeJoueur de l'objet prend la valeur de l'attribut _BILLE_ROUGE de l'objet et l'attribut billeAdverse prend la valeur de l'attribut _BILLE_JAUNE de l'objet.
        - Si la couleur du joueur est JAUNE, alors l'attribut billeJoueur de l'objet prend la valeur de l'attribut _BILLE_JAUNE de l'objet et l'attribut billeAdverse prend la valeur de l'attribut _BILLE_ROUGE de l'objet.
        '''
        if couleurJoueur == "ROUGE":
            self.billeJoueur = self._BILLE_ROUGE
            self.billeAdverse = self._BILLE_JAUNE
        else:
            self.billeJoueur = self._BILLE_JAUNE
            self.billeAdverse = self._BILLE_ROUGE

    def selectTrou(self):
        self.distance=[]
        for i in range(len(self._TROU[0])):
            dist = []
            Trou = self._TROU[0][i], self._TROU[1][i]
            
            for j in range(len(self.billeJoueur[0])):
                Trou = np.array(Trou)
                Bille = self.billeJoueur[0][j],self.billeJoueur[1][j]
                Bille = np.array(Bille)
                 
                if not self.obstacle(Trou, Bille):
                    dist.append(np.linalg.norm(Trou-Bille))
            try:
                distanceTrou = min(dist)
                index = dist.index(distanceTrou)
                self.distance.append((round(distanceTrou,2),{"trou":Trou, "bille":np.array([self.billeJoueur[0][index],self.billeJoueur[1][index]])}))
            except:
                pass

    def obstacle(self, P1: np.ndarray, P2: np.ndarray):
        obs = []
        start = np.array([P1[0], P1[1]])
        end = np.array([P2[0], P2[1]])

        for i in range(len(self.billeAdverse)):
            obstacle = np.array([self.billeAdverse[0][i], self.billeAdverse[1][i]])
            obs.append(
                utils.is_obstacle_on_trajectory(
                    start,
                    end,
                    obstacle,
                    self._TAILLE_BILLE,
                )
            )

        obs = np.array(obs)
        return np.any(obs == True)

    def showLine(self):
        for ligne in self.distance:
            x = np.array([ligne[1]["trou"][0],ligne[1]["bille"][0]])
            y = np.array([ligne[1]["trou"][1],ligne[1]["bille"][1]])
            plt.plot(x, y, color="black")
    
    def selectBille(self):
        for paire in self.distance:
            Trou = paire[1]["trou"]
            Bille = paire[1]["bille"]

            ba = Trou - Bille
            bc = self._BILLE_BLANCHE - Bille

            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)
            angle = np.degrees(angle)
            if angle > 100. and angle < 260. and not self.obstacle(self._BILLE_BLANCHE, Bille):
                x = np.array([Bille[0], self._BILLE_BLANCHE[0]])
                y = np.array([Bille[1], self._BILLE_BLANCHE[1]])
                plt.plot(x, y, color=self._CM((angle-90)/170))

                x = np.array([Bille[0],Trou[0]])
                y = np.array([Bille[1],Trou[1]])
                plt.plot(x, y, color=self._CM((angle-90)/170))
    
    def affiche(self):
        """
        La méthode affiche permet d'afficher la figure matplotlib représentant la table de billard et les billes.
        """
        plt.show()

    def save(self, filename: str):
        """
        La méthode save permet de sauvegarder la figure matplotlib représentant la table de billard et les billes dans un fichier.

        :param filename: le nom du fichier de sortie
        """
        self.fig.savefig(filename)