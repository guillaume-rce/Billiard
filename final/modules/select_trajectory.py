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
    
    def get_trajectory(self, number_of_bounce: int, id: int) -> Trajectory:
        """Return the trajectory"""
        return self.trajectories[number_of_bounce].get_by_id(id)
    
    def add_trajectory(self, trajectory_store, number_of_bounce: int = 0):
        """Add the trajectory to the trajectories"""
        if number_of_bounce not in self.trajectories:
            self.trajectories[number_of_bounce] = []
        self.trajectories[number_of_bounce].append(trajectory_store)
        
    def enumerate_all_trajectories(self,
                         ball_store: BallStore, hole_store: HoleStore,
                         number_of_bounce: int = MAX_BOUNCE, tags: list = []
                        ) -> None:  # TODO : FIX IT...
        """Add the trajectories to the trajectories"""
        departure = ball_store.get_white_ball()  # The departure point of the trajectory
        for arrival in hole_store.get_all():  # The arrival point of the trajectory
            for bounce in range(number_of_bounce+1):  # The number of bounce
                trajectory_store = TrajectoryStore()  # Create a new TrajectoryStore

                for first_ball in ball_store.get_all(ball_store.get_player_color()):
                    # The first ball of the trajectory (the ball of the player)
                    if first_ball == departure:  # If the first ball is the departure ball
                        continue  # Skip the ball
                    first_trajectory = Trajectory(departure, first_ball, tags)  # Create the first trajectory
                    trajectory_store.add_trajectory_by_instance(first_trajectory)  # Add the trajectory to the TrajectoryStore   
                    last_ball = first_ball  # Save the fist ball as the last ball         

                    for i in range(bounce):  # The number of bounce
                        for ball in ball_store.get_all():  # The next ball of the trajectory
                            if ball == departure or ball == arrival:
                                continue  # Skip the ball
                            if trajectory_store.is_in_trajectory_store(ball):
                                continue  # Skip the ball
                            other_trajectory = Trajectory(last_ball, ball, tags)
                            trajectory_store.add_trajectory_by_instance(other_trajectory)
                            last_ball = ball  # Save the ball as the last ball

                    final_trajectory = Trajectory(last_ball, arrival, tags)  # Create the final trajectory
                    trajectory_store.add_trajectory_by_instance(final_trajectory)  # Add the trajectory to the TrajectoryStore

                if len(trajectory_store) > 0:
                    # If the TrajectoryStore is not empty and the trajectory is not blocked
                    self.add_trajectory(trajectory_store, bounce)  # Add the TrajectoryStore to the trajectories
    
    def __str__(self) -> str:
        return "Trajectories: " + str(self.trajectories)
    
    def __repr__(self) -> str:
        return self.__str__()