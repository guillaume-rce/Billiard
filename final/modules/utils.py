import numpy as np
from modules import elements as e

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


class Trajectory:
    def __init__(self, ball_store) -> None:
        self.ball_store = ball_store
    
    def update_ball_store(self, ball_store: e.BallStore):
        """
        Update the BallStore.
        
        Parameters:
        - ball_store: A BallStore object.
        """
        self.ball_store = ball_store
    
    def is_valid_move(self, ball: e.Ball, x: float, y: float) -> bool:
        """
        Check if a move to the given position is valid.
        A move is valid if it stays within the dimensions of the table, does not collide with any balls in the BallStore, and does not intersect with any balls in the BallStore that have the "opponent_ball" tag.
        
        Parameters:
        - ball: The ball to move.
        - x: The x-coordinate of the target position.
        - y: The y-coordinate of the target position.
        
        Returns:
        - True if the move is valid, False otherwise.
        """
        # Check if the target position is within the dimensions of the table
        if x < 0 or x > e.Table.TABLE_DIMENSION[0] or y < 0 or y > e.Table.TABLE_DIMENSION[1]:
            return False
        
        # Check for collision with balls in the BallStore
        for other_ball in self.ball_store.get_balls():
            if other_ball != ball:  # Don't check for collision with the ball being moved
                distance = other_ball.distance_to_position(x, y)
                if distance < 2 * e.Ball.radius:  # Assume balls are considered to be in collision if they are closer than 2 times their radius
                    return False
        
        # Check for intersection with opponent balls in the BallStore
        for opponent_ball in self.ball_store.get_balls():
            if "opponent_ball" in opponent_ball.tags:
                distance = opponent_ball.distance_to_position(x, y)
                if distance < e.Ball.radius:  # Assume intersection if the ball is closer than its radius to the opponent ball
                    return False

        # If no collision or intersection is detected, the move is considered to be valid
        return True