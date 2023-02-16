import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
from modules.utils import Vector2D


class Hole:
    next_id = 0
    radius = 9.5

    def __init__(self, x: int, y: int, tags: list = []) -> None:
        """
        Initialize a new hole with the given x and y position and optional tags.
        The hole is assigned a unique ID.
        """
        self.id = Hole.next_id  # Assign the next available ID to this ball
        Hole.next_id += 1  # Increment the next available ID
        
        self.x = x
        self.y = y
        self.tags = tags
    
    def add_tag(self, tag: str) -> None:
        """
        Add the given tag to the hole's list of tags.
        """
        self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove the given tag from the hole's list of tags.
        """
        self.tags.remove(tag)
    
    def get_tag(self) -> list:
        return self.tags
    
    def get_position(self) -> np.ndarray:
        """
        Return the hole's position as a numpy array of the form [x, y].
        """
        return np.array([self.x, self.y])
    
    def distance_to(self, other) -> float:
        """
        Return the distance between this hole and the other ball.
        """
        return np.linalg.norm(self.get_position() - other.get_position())
    
    def distance_to_position(self, x: float, y: float):
        """
        Return the distance between this hole and the position.
        """
        return np.linalg.norm(self.get_position() - np.array([x, y]))
    
    def contains_point(self, x, y) -> bool:
        """
        Return True if the point (x, y) is inside this hole, False otherwise.
        """
        return self.distance_to(np.array([x, y])) <= Ball.radius
    
    @classmethod
    def get_by_id(cls, id: int, holes: list):
        """
        Return the hole with the given ID, or None if no such hole exists.
        """
        for hole in holes:
            if hole.id == id:
                return hole
        return None
    
    @classmethod
    def get_by_position(self, x: int, y: int, holes_store: "HoleStore") -> "Hole":
        """
        Return the hole at the given position, or None if no such hole exists.
        """
        for hole in holes_store.get_holes():
            if hole.x == x and hole.y == y:
                return hole
        return None

    @classmethod
    def get_by_tag(cls, tag: str, holes: list) -> list:
        """
        Return a list of balls with the given tag.
        """
        holes = []
        for hole in holes:
            if tag in hole.tags:
                holes.append(hole)
        return holes
    
    @classmethod
    def get_positions(cls, holes: list) -> np.ndarray:
        """
        Return the positions of all balls as a numpy array of the form [[x1, y1], [x2, y2], ...].
        """
        xs = []
        ys = []
        for hole in holes:
            xs.append(hole.x)
            ys.append(hole.y)
        return np.array((xs, ys))
    
    @classmethod
    def num_balls(cls, holes: list) -> int:
        """
        Return the number of balls.
        """
        return len(holes)
    
    @classmethod
    def add_tag_to_all(cls, tag: str, holes) -> None:
        """
        Add the given tag to all balls in the given list.
        """
        for hole in holes:
            hole.add_tag(tag)
    
    def __repr__(self) -> str:
        return "Hole({self.id}, {self.x}, {self.y}, {self.tags})".format(self=self)
    
    def __str__(self) -> str:
        return "Hole {self.id} at ({self.x}, {self.y})".format(self=self)


class HoleStore:
    def __init__(self) -> None:
        TABLE_DIMENSION = Table.TABLE_DIMENSION
        self.holes = [
            Hole(0, 0),
            Hole(TABLE_DIMENSION[0], 0),
            Hole(0, TABLE_DIMENSION[1]),
            Hole(TABLE_DIMENSION[0], TABLE_DIMENSION[1]),
            Hole(TABLE_DIMENSION[0]/2, 0),
            Hole(TABLE_DIMENSION[0]/2, TABLE_DIMENSION[1]),
        ]
    
    def get_positions(self):
        """
        Return the positions of all balls of the given color as a numpy array of the form [x1, y1, x2, y2, ...].
        If no color is specified, return the positions of all balls.
        """
        xs = []
        ys = []
        for hole in self.holes:
            xs.append(hole.x)
            ys.append(hole.y)
        return np.array((xs, ys))
    
    def find_hole(self, x: float, y: float) -> Hole:
        """
        Find the ball at the given position, if any.
        
        Parameters:
        - x: The x-coordinate of the position to search.
        - y: The y-coordinate of the position to search.
        
        Returns:
        - The ball at the given position, or None if no ball is found.
        """
        for hole in self.holes:
            distance = hole.distance_to(x, y)
            if distance < Hole.radius:  # Assume the ball is at the given position if it is closer than its radius
                return hole
        # If no ball is found, return None
        return None
    
    def get_all(self):
        return self.holes
    
    def get_hole(self, id: int):
        return Hole.get_by_id(id, self.holes)
    
    def get_holes_by_tag(self, tag: str):
        return Hole.get_by_tag(tag, self.holes)


class Ball:
    next_id = 0  # Class attribute to keep track of the next available ID
    radius = 5.7

    def __init__(self, x: int, y: int, tags: list = []) -> None:
        """
        Initialize a new ball with the given x and y position and optional tags.
        The ball is assigned a unique ID.
        """
        self.id = Ball.next_id  # Assign the next available ID to this ball
        Ball.next_id += 1  # Increment the next available ID
        
        self.x = x
        self.y = y
        self.player = False
        self.tags = tags
    
    @property
    def is_player(self) -> bool:
        return self.player
    
    @is_player.setter
    def set_player(self, value: bool) -> None:
        self.player = value

    def update_position(self, x: int, y: int) -> None:
        """
        Update the ball's position to the given x and y coordinates.
        """
        self.x = x
        self.y = y
    
    def add_tag(self, tag: str) -> None:
        """
        Add the given tag to the ball's list of tags.
        """
        self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove the given tag from the ball's list of tags.
        """
        self.tags.remove(tag)
    
    def get_tag(self) -> list:
        return self.tags
    
    def get_position(self) -> np.ndarray:
        """
        Return the ball's position as a numpy array of the form [x, y].
        """
        return np.array([self.x, self.y])
    
    def distance_to(self, other) -> float:
        """
        Return the distance between this ball and the other ball.
        """
        return np.linalg.norm(self.get_position() - other.get_position())
    
    def distance_to_position(self, x: float, y: float):
        """
        Return the distance between this ball and the position.
        """
        return np.linalg.norm(self.get_position() - np.array([x, y]))

    def collides_with(self, other_ball: 'Ball') -> bool:
        """
        Return True if this ball collides with the other ball, False otherwise.
        """
        return self.distance_to(other_ball) <= 2 * Ball.radius

    def contains_point(self, x: int, y: int) -> bool:
        """
        Return True if the point (x, y) is inside this ball, False otherwise.
        """
        return self.distance_to(np.array([x, y])) <= Ball.radius
    
    def is_in_trajectory(self, departure: tuple[int, int], arrival: tuple[int, int]) -> bool:
        """
        Return True if the ball is on the given trajectory. 
        """     
        # Check if the ball is on the line defined by the departure and arrival points
        # See https://math.stackexchange.com/questions/274712/calculate-on-which-side-of-a-straight-line-is-a-given-point-located
        d = (arrival[0] - departure[0]) * (self.y - departure[1]) - (arrival[1] - departure[1]) * (self.x - departure[0])
        return -Ball.radius*2 <= d <= Ball.radius*2
    
    def __repr__(self) -> str:
        return "Ball({self.id}, {self.x}, {self.y}, {self.tags})".format(self=self)
    
    def __str__(self) -> str:
        return "Ball {self.id} at ({self.x}, {self.y})".format(self=self)
    
    @classmethod
    def get_by_position(cls, x: int, y: int, ball_store: "BallStore") -> 'Ball':
        """
        Return the ball at the given position, or None if no such ball exists.
        """
        for ball in ball_store.get_all():
            if ball.x == x and ball.y == y:
                return ball
        return None
    
    @classmethod
    def get_by_id(cls, id: int, balls: list['Ball']):
        """
        Return the ball with the given ID, or None if no such ball exists.
        """
        for ball in balls:
            if ball.id == id:
                return ball
        return None
    
    @classmethod
    def get_by_tag(cls, tag: str, balls: list['Ball']) -> list:
        """
        Return a list of balls with the given tag.
        """
        balls = []
        for ball in balls:
            if tag in ball.tags:
                balls.append(ball)
        return balls
    
    @classmethod
    def get_positions(cls, balls: list['Ball']) -> np.ndarray:
        """
        Return the positions of all balls as a numpy array of the form [[x1, y1], [x2, y2], ...].
        """
        xs = []
        ys = []
        for ball in balls:
            xs.append(ball.x)
            ys.append(ball.y)
        return np.array((xs, ys))
    
    @classmethod
    def num_balls(cls, balls: list['Ball']) -> int:
        """
        Return the number of balls.
        """
        return len(balls)
    
    @classmethod
    def add_tag_to_all(cls, tag: str, balls: list['Ball']) -> None:
        """
        Add the given tag to all balls in the given list.
        """
        for ball in balls:
            ball.add_tag(tag)

    def __eq__(self, other: "Ball") -> bool:
        """
        Return True if the balls have the same ID, False otherwise.
        """
        return self.id == other.id

    def __repr__(self) -> str:
        """
        Return a string representation of the instance.
        """
        return "Ball({self.id}, {self.x}, {self.y}, {self.tags})".format(self=self)
    
    def __str__(self) -> str:
        """
        Return a string representation of the ball.
        """
        return "Ball {self.id} at ({self.x}, {self.y})".format(self=self)

class BallStore:
    def __init__(self):
        self.balls = {
            "red": [],
            "yellow": [],
            "white": [],
            "black": [],
        }
    
    def add_balls(self, xs: list, ys: list, color: str):
        """
        Add balls with the given coordinates and color to the store.
        """
        for i in range(len(xs)):
            ball = Ball(xs[i], ys[i])
            self.balls[color].append(ball)
    
    def add_ball(self, x: int, y: int, color: str):
        """
        Add a ball with the given coordinates and color to the store.
        """
        ball = Ball(x, y)
        self.balls[color].append(ball)
    
    def remove_ball(self, ball: Ball, color: str):
        """
        Remove the given ball from the store.
        """
        self.balls[color].remove(ball)
    
    def remove_ball_by_id(self, id: int, color: str):
        """
        Remove the ball with the given ID from the store.
        """
        self.balls[color].remove(Ball.get_by_id(id, self.balls[color]))
    
    def get_all(self, color: str = None) -> list[Ball]:
        """
        Return the list of balls with the given color in the store.
        If no color is specified, return the list of all balls.
        """
        if color:
            return self.balls[color]
        else:
            balls = []
            for color in self.balls:
                balls += self.balls[color]
            return balls
    
    def get_white_ball(self) -> Ball:
        """
        Return the list of white balls in the store.
        """
        return self.balls["white"][0]

    def get_black_ball(self) -> Ball:
        """
        Return the list of black balls in the store.
        """
        return self.balls["black"][0]
    
    def get_colors(self):
        """
        Return a list of the colors of all balls in the store.
        """
        colors = []
        for color in self.balls:
            for ball in self.balls[color]:
                colors.append(color)
        return colors
    
    def update_positions(self, xs: list, ys: list, color: str):
        """
        Update the positions of all balls of the given color to the given coordinates.
        Note that the number of coordinates can be different to the number of balls.
        """
        if len(xs) != len(ys):
            raise ValueError("The number of x-coordinates must be equal to the number of y-coordinates.")
        
        for ball in self.balls[color]:
            self.remove_ball(ball, color)
        
        self.add_balls(xs, ys, color)
    
    def get_positions(self, color: str = None):
        """
        Return the positions of all balls of the given color as a numpy array of the form [x1, y1, x2, y2, ...].
        If no color is specified, return the positions of all balls.
        """
        xs = []
        ys = []
        balls = self.get_all(color)
        for ball in balls:
            xs.append(ball.x)
            ys.append(ball.y)
        return np.array((xs, ys))
    
    def find_ball(self, x: float, y: float, color: str = None) -> Ball:
        """
        Find the ball at the given position, if any.
        
        Parameters:
        - x: The x-coordinate of the position to search.
        - y: The y-coordinate of the position to search.
        - color: The color of the ball to search for. If not specified, search for any ball.
        
        Returns:
        - The ball at the given position, or None if no ball is found.
        """
        for ball_color in self.balls:
            if color is None or color == ball_color:  # Check if the ball color matches the search criteria
                for ball in self.balls[ball_color]:
                    distance = ball.distance_to_position(x, y)
                    if distance < Ball.radius:  # Assume the ball is at the given position if it is closer than its radius
                        return ball
        # If no ball is found, return None
        return None
    
    def set_players(self, player_color: str, opponent_color: str) -> None:
        """Set the player property of all balls with the given player and opponent colors.

        Args:
            player_color: The color of the balls controlled by the player.
            opponent_color: The color of the balls controlled by the opponent.
        """
        if player_color == opponent_color:
            raise ValueError("The player color and opponent color must be different.")
        if player_color not in self.balls or opponent_color not in self.balls:
            raise ValueError("The player color and opponent color must be valid colors.")
        if player_color == "white" or opponent_color == "white" or player_color == "black" or opponent_color == "black":
            raise ValueError("The player color and opponent color must not be white or black.")

        for ball in self.get_all(player_color):
            ball.set_player = True
        
        for ball in self.get_all(opponent_color):
            ball.set_player = False

    def get_player_color(self) -> str:
        '''
        Return the player color.
        '''
        for color, ball in zip(self.get_colors(), self.get_all()):
            if ball.is_player:
                return color

class Table:
    """
    A class representing a table.
    """

    TABLE_DIMENSION = (190, 95)  # Class constant

    def __init__(self):
        """
        Initialize the table.
        """
        self.fig, self.ax = plt.subplots()
    
    def draw_table(self):
        """
        Draw the table.
        """
        self.rect = Rectangle((0, 0), self.TABLE_DIMENSION[0], self.TABLE_DIMENSION[1], fc='g')
        self.ax.add_patch(self.rect)
        self.ax.margins(0.05, 0.1)

    def draw_text(self, text: str, x: float, y: float, color: str = "black"):
        """
        Draw the given text at the given position.
        """
        plt.text(x, y, text)

    def draw_holes(self, hole_store: HoleStore):
        """
        Display the holes from the table's HoleStore.
        """
        for hole in hole_store.get_all():
            self.draw_text(hole.id, hole.x, hole.y, color="white")
            self.ax.add_patch(Circle((hole.x, hole.y), radius=Hole.radius/2, color='blue'))

    def draw_balls(self, ball_store: BallStore):
        """
        Display the balls from the table's BallStore.
        """
        # Get the positions of all balls in the BallStore
        ball_positions = ball_store.get_positions()
        xs = ball_positions[0]
        ys = ball_positions[1]
        
        # Get the colors of all balls in the BallStore
        ball_colors = ball_store.get_colors()
        
        # Add a Circle patch for each ball to the plot
        for x, y, color in zip(xs, ys, ball_colors):
            self.draw_ball_id(ball_store.find_ball(x, y, color))
            self.ax.add_patch(Circle((x, y), radius=Ball.radius/2, color=color))
    
    def draw_ball_id(self, ball: Ball):
        """
        Draw the id of the given ball.
        """
        self.draw_text(ball.id, ball.x, ball.y)

    def draw_line(self, first_ball: Ball, second_ball: Ball, color: str):
        """
        Draw a liaison between the two given balls.
        """
        self.draw_line_by_coords(
            first_ball.x, first_ball.y,
            second_ball.x, second_ball.y,
            color
        )

    def draw_line_by_coords(self, x1: float, y1: float, x2: float, y2: float, color: str):
        """
        Draw a liaison between the two given points.
        """
        x = np.array((x1, x2))
        y = np.array((y1, y2))
        plt.plot(x, y, color=color)
    
    def draw_cross(self, x: float, y: float, color: str):
        """
        Draw a cross at the given position.
        """
        plt.plot(x, y, 'x', color=color)
    
    def draw_cross_by_angle(self, ball: Ball, angle: float, color: str):
        """
        Draw a cross at the given angle from the given ball.
        """
        x = ball.x + Ball.radius * np.cos(angle)
        y = ball.y + Ball.radius * np.sin(angle)
        self.draw_cross(x, y, color=color)
    
    def draw_vector(self, x: int, y: int, vector: Vector2D, color: str = "red"):
        """
        Draw a vector starting at the given position.
        """
        self.draw_line_by_coords(x, y, x + vector.x, y + vector.y, color=color)
        plt.arrow(
            x, y, vector.x, vector.y,
            head_width=2.5,
            head_length=2.5,
            fc=color, ec=color)
    
    def clear(self):
        """
        Update the table with the given BallStore.
        """
        self.ax.clear()
        self.fig, self.ax = plt.subplots()

    def update_all(self,
                   hole_store: HoleStore,
                   ball_store: BallStore,
                   ):
        """
        Update the table with the given HoleStore and BallStore.
        """
        self.clear()
        self.draw_table()
        self.draw_holes(hole_store)
        self.draw_balls(ball_store)

    def display(self):
        """
        Display the table using Matplotlib.
        """
        plt.show()
    
    def save(self, filename: str):
        self.fig.savefig(filename)

    @classmethod
    def set_table_dimension(cls, size_x: int, size_y: int) -> None:
        cls.TABLE_DIMENSION = (size_x, size_y)