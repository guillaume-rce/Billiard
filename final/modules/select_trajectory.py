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
                         max_bounce: int = MAX_BOUNCE, tags: list = []
                        ) -> None:  # TODO: FIX IT
        """Select the trajectories

        :param ball_store: The ball store
        :param hole: The hole
        :param max_bounce: The maximum number of bounce
        :param tags: The tags of the trajectories

        :return: None
        """
        departure = ball_store.get_white_ball()
        arrival = hole

        for number_of_bounce in range(max_bounce + 1):
            ball_already_touched = [departure]
            trajectory_store = TrajectoryStore()

            final_ball = ball_store.get_nearest_ball(arrival.x, arrival.y,
                                                    ball_already_touched,
                                                     ball_store.player_color)
            if final_ball is None:
                break
            trajectory_store.add_trajectory_by_instance(
                    Trajectory(final_ball, arrival, tags))
            ball_already_touched.append(final_ball)

            last_ball = final_ball
            for bounce in range(number_of_bounce + 1):
                if bounce == number_of_bounce:
                    color = ball_store.player_color
                else:
                    color = None
                other_ball = ball_store.get_nearest_ball(last_ball.x, last_ball.y,
                                                        ball_already_touched,
                                                        color)
                if other_ball is None:
                    break
                trajectory_store.add_trajectory_by_instance(
                        Trajectory(other_ball, last_ball, tags))
                ball_already_touched.append(other_ball)
                last_ball = other_ball
            
            if other_ball is not None or last_ball is not None:
                break                       
            trajectory_store.add_trajectory_by_instance(Trajectory(departure, last_ball, tags))
            self.add_trajectory(trajectory_store, number_of_bounce)

    def __str__(self) -> str:
        return "Trajectories: " + str(self.trajectories)
    
    def __repr__(self) -> str:
        return self.__str__()