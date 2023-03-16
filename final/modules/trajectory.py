from modules.elements import *
from modules.utils import Vector2D

class Trajectory:
    """A class to represent a trajectory between two points"""

    def __init__(self, departure: Ball|Hole, arrival: Ball|Hole, tags: list = []) -> None:
        """Initialise a new Trajectory object"""
        self.departure = departure  # The departure point of the trajectory
        self.arrival = arrival  # The arrival point of the trajectory
        self.tags = tags  # The tags of the trajectory
    
    def get_tags(self) -> list:
        """Return the tags of the trajectory"""
        return self.tags

    def add_tags(self, tags: list):
        """Add the given tags to the trajectory"""
        self.tags.extend(tags)

    def remove_tags(self, tags: list):
        """Remove the given tags from the trajectory"""
        for tag in tags:
            self.tags.remove(tag)

    def get_departure(self) -> Ball|Hole:
        """Return the departure point of the trajectory"""
        return self.departure
    
    def get_arrival(self) -> Ball|Hole:
        """Return the arrival point of the trajectory"""
        return self.arrival
    
    def get_balls(self) -> list[Ball]:
        """Return the balls of the trajectory"""
        balls = []
        if isinstance(self.departure, Ball):
            balls.append(self.departure)
        if isinstance(self.arrival, Ball):
            balls.append(self.arrival)
        return balls
    
    def get_distance(self) -> float:
        """Return the distance of the trajectory"""
        return self.departure.distance_to(self.arrival)

    def get_vector(self) -> Vector2D:
        """Return the vector of the trajectory"""
        return Vector2D(self.arrival.x - self.departure.x, self.arrival.y - self.departure.y)
    
    def get_orthogonal_vector(self) -> Vector2D:
        """Return the orthogonal vector of the trajectory"""
        return self.get_vector().orthogonal
    
    def get_angle(self, other: "Trajectory") -> float:
        """Return the angle between two trajectories"""
        return self.get_vector().get_angle(other.get_vector())

    def is_blocked(self, obstacles: BallStore) -> bool:
        """Return True if the trajectory is blocked by an obstacle"""
        return Trajectory.check_for_obstacle(self, obstacles)  
    
    @classmethod
    def check_for_obstacle(cls, trajectory: "Trajectory", obstacles: BallStore) -> bool:
        """Return True if the trajectory is blocked by an obstacle"""
        for obstacle in obstacles.get_all():
            if obstacle == trajectory.get_departure() or obstacle == trajectory.get_arrival():
                continue
            if obstacle.is_in_trajectory(
                trajectory.get_departure().get_position(),
                trajectory.get_arrival().get_position(),
            ):
                return True
        return False
    
    @classmethod
    def from_vector(cls,
                    departure: Ball|Hole, vector: Vector2D,
                    store: BallStore|HoleStore, tags: list = [],
                ) -> "Trajectory":
        """Return a trajectory from a departure point and a vector"""
        if type(store) == HoleStore:
            arrival = Hole.get_by_position(departure.x + vector.x, departure.y + vector.y, store)
        elif type(store) == BallStore:
            arrival = Ball.get_by_position(departure.x + vector.x, departure.y + vector.y, store)
        else:
            raise TypeError("The store must be a BallStore or a HoleStore")
        return cls(departure, arrival, tags)
    
    @classmethod
    def get_by_tags(cls, tags: list, trajectories: list["Trajectory"]) -> list["Trajectory"]:
        """Return the trajectories with the given tags"""
        return [trajectory for trajectory in trajectories if set(tags).issubset(trajectory.tags)]
    
    @classmethod
    def add_tags_to_trajectories(cls, tags: list, trajectories: list["Trajectory"]):
        """Add the given tags to the given trajectories"""
        for trajectory in trajectories:
            trajectory.add_tags(tags)
    
    @classmethod
    def get_by_departure_and_arrival(self, departure: Ball|Hole, arrival: Ball|Hole, trajectories: list["Trajectory"]) -> "Trajectory":
        """Return the trajectory with the given departure and arrival"""
        for trajectory in trajectories:
            if trajectory.departure == departure and trajectory.arrival == arrival:
                return trajectory
        return None

    def __eq__(self, other: "Trajectory") -> bool:
        """Return True if the two trajectories are equal"""
        return self.departure == other.departure and self.arrival == other.arrival
    
    def __abs__(self) -> float:
        """Return the absolute value of the trajectory"""
        return abs(self.get_vector())

    def __repr__(self) -> str:
        """Return a string representation of the instance trajectory"""
        return "Trajectory({self.departure}, {self.arrival})".format(self=self)
    
    def __str__(self) -> str:
        """Return a string representation of the trajectory"""
        return "({self.departure}, {self.arrival})".format(self=self)

class TrajectoryStore:
    """A class to represent a store of trajectories"""

    def __init__(self) -> None:
        """Initialise a new TrajectoryStore object"""
        self.trajectories = []  # The list of trajectories
    
    def add_trajectory(self,
                       departure: Ball|Hole, arrival: Ball|Hole,
                       obstacles: BallStore = None, tags: list = []
                    ) -> bool:
        """Add a new trajectory to the store"""        
        self.trajectories.append(Trajectory(departure, arrival, tags))
        return 'ADDED'
    
    def add_trajectory_by_instance(self, trajectory: Trajectory) -> None:
        """Add a new trajectory to the store"""
        self.trajectories.append(trajectory)
    
    def add_trajectories_by_instance(self, trajectories: list[Trajectory]) -> None:
        """Add new trajectories to the store"""
        self.trajectories.extend(trajectories)
    
    def insert_trajectory(self, index: int, trajectory: Trajectory) -> None:
        """Insert a new trajectory to the store"""
        self.trajectories.insert(index, trajectory)

    def remove_trajectory(self, departure: Ball|Hole, arrival: Ball|Hole) -> None:
        """Remove a trajectory from the store"""
        self.trajectories.remove(
            Trajectory.get_by_departure_and_arrival(departure, arrival, self.trajectories)
        )

    def get_all(self) -> list[Trajectory]:
        """Return all the trajectories in the store"""
        return self.trajectories

    def is_in_trajectory_store(self, object: Ball|Hole) -> bool:
        """Return True if the object is in the trajectory store"""
        for trajectory in self.trajectories:
            if trajectory.departure == object or trajectory.arrival == object:
                return True
        return False
    
    def is_possible(self) -> bool:
        """Return True if the trajectory store is possible"""
        for trajectory in self.get_all():
            if trajectory.is_blocked():
                return False
        return True

    def touch_an_opponent_ball(self) -> bool:
        """Return True if the trajectory store touch an opponent ball"""
        for trajectory in self.get_all():
            for ball in trajectory.get_balls():
                if not ball.is_player:
                    return True
        return False
    
    def touch_black_ball(self, ball_store: BallStore) -> bool:
        """Return True if the trajectory store touch a black ball"""
        for trajectory in self.get_all():
            for ball in trajectory.get_balls():
                if ball_store.get_black_ball() == ball:
                    return True
        return False

    @classmethod
    def already_exist(cls, 
                      trajectory_store: "TrajectoryStore", trajectory_stores: list["TrajectoryStore"]
    ) -> bool:
        """Return True if the trajectory store already exists"""
        for other_trajectory_store in trajectory_stores:
            if trajectory_store == other_trajectory_store:
                return True
        return False
    
    def __eq__(self, other: "TrajectoryStore") -> bool:
        """Return True if the two trajectory stores are equal"""
        return self.trajectories == other.trajectories
    
    def __len__(self):
        return len(self.get_all())
    
    def __str__(self) -> str:
        return str(self.get_all())
    
    def __repr__(self) -> str:
        return "TrajectoryStore({self.trajectories})".format(self=self)