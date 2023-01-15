import numpy as np


def toVector(p1: np.ndarray, p2: np.ndarray):
    '''La fonction prend en entrée deux tableaux numpy (p1 et p2) et renvoie un dictionnaire contenant la norme du vecteur allant de p1 à p2 et le vecteur lui-même. Le vecteur est obtenu en soustrayant p2 à p1 element-wise, et sa norme est calculée grâce à la fonction numpy.linalg.norm.'''
    vect = np.array(p1-p2)
    return {"norme":np.linalg.norm(vect), "vecteur": vect}

def projOrtho(vect: dict):
    pass

def convert_coordinates(xs, ys):
  """Convertit les coordonnées en np.array sous la forme (xs, ys) en np.array sous la forme ((x1, y1), (x2, y2), ...)
  
  Args:
    xs: np.array des coordonnées en abscisses
    ys: np.array des coordonnées en ordonnées
    
  Returns:
    np.array de points sous la forme ((x1, y1), (x2, y2), ...)
  """
  points = np.stack((xs, ys), axis=-1)
  return points

def is_obstacle_on_trajectory(
    p1: tuple,
    p2: tuple,
    obs: tuple,
    radius: float,
):
    '''
    La fonction is_obstacle_on_trajectory prend en entrée 4 arguments :

    - p1 : un tableau NumPy représentant la position initiale de la boule
    - p2 : un tableau NumPy représentant la position finale de la boule
    - obs : un tableau NumPy représentant la position de l'obstacle
    - radius : un nombre flottant représentant le diamètre de la boule et de l'obstacle

    La fonction renvoie True si l'obstacle se trouve sur la trajectoire de la boule, False sinon.

    Pour déterminer si l'obstacle se trouve sur la trajectoire de la boule, la fonction effectue les étapes suivantes :

    - Calcule la distance entre la position initiale p1 et la position finale p2 de la boule. Pour cela, elle utilise la fonction np.linalg.norm qui permet de calculer la norme d'un vecteur (ici, le vecteur p1 - p2).
    - Calcule la distance entre la position initiale p1 de la boule et la position de l'obstacle obs. Pour cela, elle utilise également la fonction np.linalg.norm.
    - Calcule la distance entre la position finale p2 de la boule et la position de l'obstacle obs. Pour cela, elle utilise encore une fois la fonction np.linalg.norm.
    - Vérifie si l'obstacle est assez proche de la position initiale ou de la position finale de la boule. Pour cela, elle compare les distances calculées précédemment (distance_obs_p1 et distance_obs_p2) avec radius. Si l'une des distances est inférieure ou égale à radius, cela signifie que l'obstacle est assez proche de la position initiale ou de la position finale de la boule et la fonction renvoie True.
    - Si l'obstacle n'est pas assez proche de la position initiale ou de la position finale de la boule, la fonction vérifie s'il se trouve sur la trajectoire de la boule. Pour cela, elle calcule la somme des distances entre l'obstacle et la position initiale et finale de la boule (distance_obs_p1 + distance_obs_p2). Si la somme des distances entre l'obstacle et la position initiale et finale de la boule (distance_obs_p1 + distance_obs_p2) est inférieure ou égale à la distance entre la position initiale et finale de la boule (distance), cela signifie que l'obstacle se trouve sur la trajectoire de la boule et la fonction renvoie True.
    '''
    
    distance = np.linalg.norm(p1 - p2)
    distance_obs_p1 = np.linalg.norm(p1 - obs)
    distance_obs_p2 = np.linalg.norm(p2 - obs)

    if distance_obs_p1 <= radius or distance_obs_p2 <= radius:
        return True
    elif (distance_obs_p1 + distance_obs_p2) <= distance:
        return True
    else:
        return False


class Vector2D:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
