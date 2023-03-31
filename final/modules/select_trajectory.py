from types import NoneType
from modules.utils import Vector2D
from modules.elements import *
from modules.trajectory import *

DIFICULTIES = {
    'ONE CENTIMETER': 0.2,
    'ONE DEGREE': 0.1,
    'BOUNCE': 10,
    'TOUCH OPPONENT BALL': 20,
    'TOUCH BLACK BALL': 50,
}  # TODO: Define the level

class SelectTrajectory:
    """A class to select the best trajectory"""
    MAX_BOUNCE = 4  # The maximum number of bounce

    def __init__(self):
        self.trajectories = {}  # The trajectories soted by number of bounce (countain a list of TrajectoryStore)
        self._easiest = None
        self._hardest = None
    
    def add_trajectory(self, trajectory_store, number_of_bounce: int = 0):
        """Add the trajectory to the trajectories"""
        if number_of_bounce not in self.trajectories:
            self.trajectories[number_of_bounce] = []
        self.trajectories[number_of_bounce].append(trajectory_store)

    def get_easiest(self, ball_store: BallStore) -> tuple[list[TrajectoryStore], float]:
        """Return the easiest trajectory"""
        difficulty = min(self.get_trajectories_by_difficulty(ball_store).keys())
        self._easiest = self.get_trajectories_by_difficulty(ball_store, difficulty)
        return self._easiest, difficulty
    
    def get_hardest(self, ball_store: BallStore) -> tuple[list[Trajectory], float]:
        """Return the hardest trajectory"""
        difficulty = max(self.get_trajectories_by_difficulty(ball_store).keys())
        self._hardest = self.get_trajectories_by_difficulty(ball_store, difficulty)
        return self._hardest, difficulty
    
    def get_trajectories(self, number_of_bounce: int = None) -> list[TrajectoryStore]:
        """Return the trajectories"""
        if number_of_bounce is None:
            trajectories = []
            for number_of_bounce in self.trajectories:
                trajectories.extend(self.trajectories[number_of_bounce])
            return trajectories
        else:
            return self.trajectories[number_of_bounce]
    
    def get_trajectories_by_difficulty(self, ball_store: BallStore, which_difficulty: str = None) -> dict[list[TrajectoryStore]]|list[TrajectoryStore]:
        """Return the trajectories by difficulty"""
        trajectories = {}
        for bound, trajectory_stores in zip(self.trajectories.keys(), self.trajectories.values()):
            for trajectory_store in trajectory_stores:
                difficulty = int(round(SelectTrajectory.get_difficulty(trajectory_store, ball_store)))
                if difficulty not in trajectories:
                    trajectories[difficulty] = []
                trajectories[difficulty].append(trajectory_store)

        if which_difficulty is not None:
            return trajectories[which_difficulty]
        return trajectories

    
    @classmethod
    def select_trajectories(cls,
                         ball_store: BallStore, hole: Hole,
                         number_of_bounce: int = 1,
                         ball_already_use: list = None,
                         tags: list = []
                        ) -> tuple[TrajectoryStore, list[Ball]]:  # TODO: FIX IT
        """Select the trajectories

        :param ball_store: The ball store
        :param hole: The hole
        :param number_of_bounce: The number number of bounce (min: 1)
        :param tags: The tags of the trajectories

        :return: tuple[TrajectoryStore, list[Ball]]: The trajectories and the balls used
        """
        # Get departure and arrival
        departure = ball_store.get_white_ball()
        arrival = hole
        trajectory_store = TrajectoryStore()  # The trajectory store

        # If ball_already_use is None, create a new list
        ball_already_use = ball_already_use or []
        ball_already_use.append(departure)  # Add the departure to the ball_already_use
        # Get the nearest ball from the arrival and add it to the trajectory store
        last_ball = ball_store.get_nearest_ball(arrival.x, arrival.y, ball_already_use, ball_store.player_color)
        if last_ball is None:
            return None, ball_already_use
        ball_already_use.append(last_ball)
        trajectory_store.add_trajectory(last_ball, arrival, tags)
        
        if number_of_bounce >=2:
            for bounce in range(1, number_of_bounce):
                if bounce == number_of_bounce - 1:
                    color = ball_store.player_color
                else:
                    color = None
                ball = ball_store.get_nearest_ball(last_ball.x, last_ball.y, ball_already_use, color)
                if ball is None:
                    return None, ball_already_use
                ball_already_use.append(ball)
                trajectory_store.insert_trajectory(0, Trajectory(ball, last_ball, tags))
                last_ball = ball
        
        trajectory_store.insert_trajectory(0, Trajectory(departure, last_ball, tags))
        return trajectory_store, ball_already_use
    
    @classmethod
    def get_difficulty(cls, trajectory: TrajectoryStore, ball_store: BallStore) -> float:
        """Return the difficulty of the trajectory"""
        difficulty = 0
        difficulty += trajectory.get_total_distance() * DIFICULTIES['ONE CENTIMETER']
        difficulty += trajectory.get_total_angle() * DIFICULTIES['ONE DEGREE']
        difficulty += trajectory.get_number_of_bounces() * DIFICULTIES['BOUNCE']
        if trajectory.touch_black_ball(ball_store):
            difficulty += DIFICULTIES['TOUCH BLACK BALL']
        if trajectory.touch_an_opponent_ball():
            difficulty += DIFICULTIES['TOUCH OPPONENT BALL']
        return difficulty

    def __str__(self) -> str:
        return "Trajectories: " + str(self.trajectories)
    
    def __repr__(self) -> str:
        return self.__str__()