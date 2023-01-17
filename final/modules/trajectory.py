from modules.elements import Table, Ball, BallStore, Hole, HoleStore

_DIFICULTIES_LEVEL = {
    'ONE CENTIMETER' = 0.2,
    'BOUNCE' = 10,
    'TOUCH A BALL' = 30,
    'TOUCH BLACK BALL' = 50,
}  # TODO: Define the level

def check_intersection(ball: Ball, x: int, y: int, ball_store: BallStore) -> bool:
        """
        Check if a move to the given ball is valid.
        A move is valid if it stays within the dimensions of the table, does not collide with any balls in the BallStore, and does not intersect with any balls in the BallStore that have the "opponent_ball" tag.
        
        Parameters:
        - ball: The ball to move.
        - x: The x-coordinate of the target position.
        - y: The y-coordinate of the target position.
        
        Returns:
        - True if the move is valid, False otherwise.
        """
        # Check if the target position is within the dimensions of the tab
        if x < 0 or x > Table.TABLE_DIMENSION[0] or y < 0 or y > Table.TABLE_DIMENSION[1]:
            return False
        
        # Check for intersection with opponent balls in the BallStore
        for other_ball in ball_store.get_balls():
            if other_ball != ball:
                distance = other_ball.distance_to_position(x, y)
                if distance < Ball.radius:  # Assume intersection if the ball is closer than its radius to the opponent ball
                    return False

        # If no collision or intersection is detected, the move is considered to be valid
        return True

class Trajectory:
    next_id = 0
    max_bounce = 0

    def __init__(self, starting_ball: Ball, final_ball: Ball, tags: list = []) -> None:
        self.id = Trajectory.next_id  # Assign the next available ID to this ball
        Trajectory.next_id += 1  # Increment the next available ID
        self.bounce = Trajectory.max_bounce

        self.starting_ball = starting_ball
        self.final_ball = final_ball
        self.distance = starting_ball.distance_to(final_ball)
        self.tags = tags
        self.difficulty = 0

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
    
    def get_balls(self) -> tuple:
        return self.starting_ball, self.final_ball
    
    def check_intersection(self, ball_store: BallStore) -> bool:
        return check_intersection(self.starting_ball, self.final_ball.x, self.final_ball.y, ball_store)
    
    @classmethod
    def get_by_id(cls, id: int, trajectories: list):
        """
        Return the ball with the given ID, or None if no such ball exists.
        """
        for trajectory in trajectories:
            if trajectory.id == id:
                return trajectory
        return None
    
    @classmethod
    def get_by_tag(cls, tag: str, trajectories: list) -> list:
        """
        Return a list of balls with the given tag.
        """
        Trajectories = []
        for trajectory in trajectories:
            if tag in trajectory.tags:
                Trajectories.append(trajectory)
        return Trajectories
    
    @classmethod
    def num_trajectory(cls, trajectories: list) -> int:
        """
        Return the number of balls.
        """
        return len(trajectories)
    
    @classmethod
    def add_tag_to_all(cls, tag: str, trajectories) -> None:
        """
        Add the given tag to all balls in the given list.
        """
        for trajectory in trajectories:
            trajectory.add_tag(tag)
    
    @classmethod
    def set_max_bounce(cls, value: int) -> None:
        Trajectory.max_bounce = value


class TrajectoryStore:
    def __init__(self) -> None:
        self.trajectories = {}
    
    def add_trajectories(self, ball_store: BallStore) -> None:
        balls = ball_store.get_balls('red')
        white_ball = ball_store.get_balls('white')
        for ball in balls:
    
    def add_trajectory(self, starting_ball: Ball, final_ball: Ball, tags: list = []) -> None:
        if starting_ball.id in list(self.trajectories.keys()):
            self.trajectories[starting_ball.id].append(Trajectory(starting_ball, final_ball, tags))
        else:
            self.trajectories[starting_ball.id] = [Trajectory(starting_ball, final_ball, tags)]
    
    def remove_trajectory(self, id: int) -> None:
        """
        Remove the trajectory with the given ID.
        """
        for key, value in self.trajectories.items():
            for i, trajectory in enumerate(value):
                if trajectory.id == id:
                    del value[i]
                    if len(value) == 0:
                        del self.trajectories[key]
    
    def remove_ball(self, ball: Ball) -> None:
        del self.trajectories[ball.id]
    
    def get_trajectories(self, ball: Ball) -> list[Trajectory]:
        return self.trajectories[ball.id]
    
    def is_possible(self, ball: Ball, ball_store: BallStore) -> list:
        ids = []
        for id, trajectory in enumerate(self.trajectories[ball.id]):
            if trajectory.check_intersection(ball_store):
                ids.append(id)
        return ids

class SelectTrajectories:
    def __init__(self) -> None:
        pass
    
    def select_trajectories(self, ballStore: BallStore, holes_store: HoleStore) -> TrajectoryStore:
        trajectory_store = TrajectoryStore
        for player_ball in ballStore.get_balls(ballStore.get_player_color()):
            pass  # TODO: set trajectories