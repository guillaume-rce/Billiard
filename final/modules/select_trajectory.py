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
    
    def get_easiest(self) -> Trajectory:
        """Return the easiest trajectory"""
        return self._easiest
    
    def get_hardest(self) -> Trajectory:
        """Return the hardest trajectory"""
        return self._hardest
    
    def get_trajectories(self, number_of_bounce: int = None) -> list[TrajectoryStore]:
        """Return the trajectories"""
        if number_of_bounce is None:
            trajectories = []
            for number_of_bounce in self.trajectories:
                trajectories.extend(self.trajectories[number_of_bounce])
            return trajectories
        else:
            return self.trajectories[number_of_bounce]
    
    def add_trajectory(self, trajectory_store, number_of_bounce: int = 0):
        """Add the trajectory to the trajectories"""
        if number_of_bounce not in self.trajectories:
            self.trajectories[number_of_bounce] = []
        self.trajectories[number_of_bounce].append(trajectory_store)
        
    def select_trajectories(self,
                         ball_store: BallStore, hole: Hole,
                         number_of_bounce: int = 1,
                         tags: list = []
                        ) -> tuple[TrajectoryStore, list[Ball]]:  # TODO: FIX IT
        """Select the trajectories

        :param ball_store: The ball store
        :param hole: The hole
        :param number_of_bounce: The number number of bounce (min: 1, max: 4)
        :param tags: The tags of the trajectories

        :return: tuple[TrajectoryStore, list[Ball]]: The trajectories and the balls used
        """
        departure = ball_store.get_white_ball()
        arrival = hole
        trajectory_store = TrajectoryStore()

        ball_already_use = [departure]
        last_ball = ball_store.get_nearest_ball(arrival.x, arrival.y, ball_already_use)
        ball_already_use.append(last_ball)
        trajectory_store.add_trajectory(last_ball, arrival, tags)
        
        if number_of_bounce >=2:
            for bounce in range(1, number_of_bounce):
                ball = ball_store.get_nearest_ball(last_ball.x, last_ball.y, ball_already_use)
                ball_already_use.append(ball)
                trajectory_store.insert_trajectory(0, Trajectory(ball, last_ball, tags))
                last_ball = ball
        
        trajectory_store.insert_trajectory(0, Trajectory(departure, last_ball, tags))
        return trajectory_store, ball_already_use

    def __str__(self) -> str:
        return "Trajectories: " + str(self.trajectories)
    
    def __repr__(self) -> str:
        return self.__str__()