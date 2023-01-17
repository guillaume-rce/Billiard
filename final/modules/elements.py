import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


class Hole:
    next_id = 0
    radius = 9.5

    def __init__(self, x: int, y: int, tags: list = []) -> None:
        """
        Initialize a new hole with the given x and y position and optional tags.
        The hole is assigned a unique ID.
        """
        self.id = Ball.next_id  # Assign the next available ID to this ball
        Ball.next_id += 1  # Increment the next available ID
        
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
    
    def distance_to(self, other_ball) -> float:
        """
        Return the distance between this hole and the other ball.
        """
        return np.linalg.norm(self.get_position() - other_ball.get_position())
    
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
        self.tags = tags

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
    
    def distance_to(self, other_ball) -> float:
        """
        Return the distance between this ball and the other ball.
        """
        return np.linalg.norm(self.get_position() - other_ball.get_position())
    
    def distance_to_position(self, x: float, y: float):
        """
        Return the distance between this ball and the position.
        """
        return np.linalg.norm(self.get_position() - np.array([x, y]))

    def collides_with(self, other_ball) -> bool:
        """
        Return True if this ball collides with the other ball, False otherwise.
        """
        return self.distance_to(other_ball) <= 2 * Ball.radius

    def contains_point(self, x, y) -> bool:
        """
        Return True if the point (x, y) is inside this ball, False otherwise.
        """
        return self.distance_to(np.array([x, y])) <= Ball.radius
    
    def set_player(self, player) -> None:
        """
        Set this ball as belonging to the given player.
        Player should be either "player" or "opponent".
        """
        if player == "player":
            self.tags.append("player_ball")
        elif player == "opponent":
            self.tags.append("opponent_ball")
        else:
            raise ValueError("Invalid player. Player should be either 'player' or 'opponent'.")
    
    @classmethod
    def get_by_id(cls, id: int, balls: list):
        """
        Return the ball with the given ID, or None if no such ball exists.
        """
        for ball in balls:
            if ball.id == id:
                return ball
        return None
    
    @classmethod
    def get_by_tag(cls, tag: str, balls: list) -> list:
        """
        Return a list of balls with the given tag.
        """
        balls = []
        for ball in balls:
            if tag in ball.tags:
                balls.append(ball)
        return balls
    
    @classmethod
    def get_positions(cls, balls: list) -> np.ndarray:
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
    def num_balls(cls, balls: list) -> int:
        """
        Return the number of balls.
        """
        return len(balls)
    
    @classmethod
    def add_tag_to_all(cls, tag: str, balls) -> None:
        """
        Add the given tag to all balls in the given list.
        """
        for ball in balls:
            ball.add_tag(tag)


class BallStore:
    def __init__(self):
        self.balls = {
            "red": [],
            "yellow": [],
            "white": [],
            "black": [],
        }
    
    def add_balls(self, xs, ys, color):
        """
        Add balls with the given coordinates and color to the store.
        """
        for i in range(len(xs)):
            ball = Ball(xs[i], ys[i])
            self.balls[color].append(ball)
    
    def remove_ball(self, ball, color):
        """
        Remove the given ball from the store.
        """
        self.balls[color].remove(ball)
    
    def get_balls(self, color=None) -> list[Ball]:
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
    
    def get_colors(self):
        """
        Return a list of the colors of all balls in the store.
        """
        colors = []
        for color in self.balls:
            for ball in self.balls[color]:
                colors.append(color)
        return colors
    
    def update_positions(self, xs, ys, color):
        """
        Update the positions of all the balls of the given color in the store according to xs and ys.
        """
        for i in range(len(xs)):
            ball = self.balls[color][i]
            ball.update_position(xs[i], ys[i])
    
    def get_positions(self, color=None):
        """
        Return the positions of all balls of the given color as a numpy array of the form [x1, y1, x2, y2, ...].
        If no color is specified, return the positions of all balls.
        """
        xs = []
        ys = []
        balls = self.get_balls(color)
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
                    distance = ball.distance_to(x, y)
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
        # Set player property of player balls
        for player_ball in self.get_balls(player_color):
            player_ball.set_player("player")
        
        # Set player property of opponent balls
        for player_ball in self.get_balls(opponent_color):
            player_ball.set_player("player")


    def get_player_color(self) -> str:
        '''
        Return the player color.
        '''
        if 'player_ball' in self.get_balls('red')[0].get_tag():
            return 'red'
        else:
            return 'yellow'


class Table:
    """
    A class representing a table.
    """

    TABLE_DIMENSION = (190, 95)  # Class constant

    def __init__(self, ball_store: BallStore, hole_store: HoleStore):
        """
        Initialize a new Table instance with the given BallStore.

        Parameters:
        - ball_store: A BallStore object.
        """
        self.ball_store = ball_store
        self.fig, self.ax = plt.subplots()
        self.rect = Rectangle((0, 0), self.TABLE_DIMENSION[0], self.TABLE_DIMENSION[1], fc='g')
        self.ax.add_patch(self.rect)
        self.ax.margins(0.05, 0.1)

        holes_positions = hole_store.get_positions()
        xs = holes_positions[0]
        ys = holes_positions[1]

        for x, y in zip(xs, ys):
            self.ax.add_patch(Circle((x, y), radius=Hole.radius/2, color='blue'))
    
    def display_balls(self):
        """
        Display the balls from the table's BallStore.
        """
        
        # Get the positions of all balls in the BallStore
        ball_positions = self.ball_store.get_positions()
        xs = ball_positions[0]
        ys = ball_positions[1]
        
        # Get the colors of all balls in the BallStore
        ball_colors = self.ball_store.get_colors()
        
        # Add a Circle patch for each ball to the plot
        for x, y, color in zip(xs, ys, ball_colors):
            self.ax.add_patch(Circle((x, y), radius=Ball.radius/2, color=color))
    
    def liaison(self, first_ball: Ball, second_ball: Ball, color: str):
        x = np.array(first_ball.x, second_ball.y)
        y = np.array(first_ball.y, second_ball.y)
        plt.plot(x, y, color=color)

    def liaison_by_coords(self, x1: float, y1: float, x2: float, y2: float, color: str):
        x = np.array(x1, x2)
        y = np.array(y1, y2)
        plt.plot(x, y, color=color)

    def update_ball_store(self, ball_store: BallStore):
        """
        Update the table's BallStore with the given BallStore.
        
        Parameters:
        - ball_store: A BallStore object.
        """
        self.ball_store = ball_store
    
    def display(self):
        """
        Display the table using Matplotlib.
        """
        plt.show()
    
    def save(self, filename: str):
        self.fig.savefig(filename)

    @classmethod
    def set_table_dimension(size_x: int, size_y: int) -> None:
        Table.TABLE_DIMENSION = (size_x, size_y)