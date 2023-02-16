from modules.elements import Ball, BallStore, Hole, HoleStore, Table
from numpy import arccos, array, degrees, dot
from numpy.linalg import norm

_DIFICULTIES_LEVEL = {
    'ONE CENTIMETER': 0.2,
    'ONE DEGREE': 0.1,
    'BOUNCE': 10,
    'TOUCH OPPONENT BALL': 20,
    'TOUCH BLACK BALL': 50,
}  # TODO: Define the level    

def check_intersection(ball:Ball, x: int, y: int, ball_store: BallStore):
    """
    Check if the ball is on the trajectory.
    """
    if x < 0 or x > Table.TABLE_DIMENSION[0] or y < 0 or y > Table.TABLE_DIMENSION[1]:
        return True
    
    for other in ball_store.get_all():
        diameter = (ball.radius + other.radius)
        if other != ball:
            '''distance = ball.distance_to_position(x, y)
            distance_obs_p1 = ball.distance_to(other)
            distance_obs_p2 = norm(array([x, y]) - other.get_position())

            if ((distance_obs_p1 + distance_obs_p2) <= distance or
                distance_obs_p1 <= diameter or distance_obs_p2 <= diameter
            ):
                return True
        '''
            if other.is_in_trajectory(ball.get_position().tolist(), (x, y)):
                return True
    return False


def check_angle(white_ball: Ball, ball: Ball, hole: Hole) -> bool:
    """
    Check if the angle is correct.
    """
    ba = hole.get_position() - ball.get_position()
    bc = white_ball.get_position() - ball.get_position()

    cosine_angle = dot(ba, bc) / (norm(ba) * norm(bc))
    angle = arccos(cosine_angle)
    angle = degrees(angle)
    if angle > 100. and angle < 260.:
        return True
    return False


class Trajectory:
    next_id = 0
    max_bounce = 0

    def __init__(self, ball: Ball, hole: Hole, tags: list = []) -> None:
        self.id = Trajectory.next_id  # Assign the next available ID to this ball
        Trajectory.next_id += 1  # Increment the next available ID

        self.ball = ball
        self.hole = hole
        self.tags = tags
        self.bounce = 0
        self.touch_black_ball = False
        self.touch_opponent_ball = False
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
 
    def get_points(self) -> tuple[Ball, Hole]:
        """
        Return a tuple containing the starting ball and final hole.
        """
        return self.ball, self.hole
    
    def get_ball(self) -> Ball:
        """
        Return the starting ball.
        """
        return self.ball
    
    def get_hole(self) -> Hole:
        """
        Return the final ball.
        """
        return self.hole
    
    def get_total_distance(self, white_ball: Ball) -> float:
        return white_ball.distance_to(self.ball) + self.ball.distance_to_position(self.hole.x, self.hole.y)
    
    def get_angle(self, white_ball: Ball) -> float:
        ba = self.hole.get_position() - self.ball.get_position()
        bc = white_ball.get_position() - self.ball.get_position()

        cosine_angle = dot(ba, bc) / (norm(ba) * norm(bc))
        angle = arccos(cosine_angle)
        angle = degrees(angle)
        return angle
    
    def get_difficulty(self, white_ball: Ball) -> float:
        """
        Return the difficulty of the trajectory.
        """
        if self.difficulty == 0:
            self.difficulty = _DIFICULTIES_LEVEL['ONE CENTIMETER'] * self.get_total_distance(white_ball)
            self.difficulty += _DIFICULTIES_LEVEL['BOUNCE'] * self.bounce
            if self.get_angle(white_ball) > 180.:
                self.difficulty += _DIFICULTIES_LEVEL['ONE DEGREE'] * self.get_angle(white_ball)
            if self.get_angle(white_ball) < 180.:
                self.difficulty += _DIFICULTIES_LEVEL['ONE DEGREE'] * (180. - self.get_angle(white_ball))
            if self.touch_black_ball:
                self.difficulty += _DIFICULTIES_LEVEL['TOUCH BLACK BALL']
            if self.touch_opponent_ball:
                self.difficulty += _DIFICULTIES_LEVEL['TOUCH OPPONENT BALL']
        return self.difficulty

    @classmethod
    def is_possible(cls, white_ball: Ball, ball: Ball, hole: Hole, ball_store: BallStore) -> bool:
        """
        Check if a trajectory is possible.
        A trajectory is possible if the white ball can reach the ball and the ball can reach the hole.
        """       
        if (not check_intersection(ball, hole.x, hole.y, ball_store)  # TODO: Add for white_ball
            and check_angle(white_ball, ball, hole)):
                return True
        return False
    
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
        """
        Set the maximum number of bounces for all balls.
        """
        Trajectory.max_bounce = value        


class TrajectoryStore:
    """
    A store for balls.
    """
    def __init__(self) -> None:
        """
        Create a new BallStore.
        """
        self.trajectories = {}
    
    def add_trajectories(self, ball_store: BallStore, holes: HoleStore, tags: list = []) -> None:
        """
        Add all balls in the given BallStore to this store.
        """
        white_ball = ball_store.get_white_ball()
        for ball in ball_store.get_all(ball_store.get_player_color()):
            for hole in holes.get_all():
                if Trajectory.is_possible(white_ball, ball, hole, ball_store):
                    self.add_trajectory(ball, hole, tags)

    
    def add_trajectory(self, ball: Ball, hole: Hole, tags: list = []) -> None:
        """
        Add a ball to the store.
        """
        if ball.id not in self.trajectories:
            self.trajectories[ball.id] = {}
        self.trajectories[ball.id][hole.id] = Trajectory(ball, hole, tags)
    
    def remove_trajectory(self, id: int) -> None:
        """
        Remove the trajectory with the given ID.
        """
        for ball_id in list(self.trajectories.keys()):
            for hole_id in list(self.trajectories[ball_id].keys()):
                if self.trajectories[ball_id][hole_id].id == id:
                    del self.trajectories[ball_id][hole_id]
    
    def remove_ball(self, ball: Ball) -> None:
        """
        Remove all trajectories with the given ball.
        """
        del self.trajectories[ball.id]
    
    def update_trajectories(self, ball_store: BallStore, holes: HoleStore, tags: list = []) -> None:
        """
        Update all trajectories.
        """
        for i in self.get_ids():
            self.remove_trajectory(i)
        
        self.add_trajectories(ball_store, holes, tags)
    
    def get_trajectories(self, ball: Ball) -> list[Trajectory]:
        """
        Return a list of all trajectories with the given ball.
        """
        return self.trajectories[ball.id]
    
    def is_possible(self, ball: Ball, ball_store: BallStore) -> list:
        """
        Return all ids of trajectories that are possible for the given ball.
        """
        ids = []
        for id, trajectory in enumerate(self.trajectories[ball.id]):
            if trajectory.check_intersection(ball_store):
                ids.append(id)
        return ids
    
    def enumerate(self) -> list[tuple[int, int, Trajectory]]:
        trajectories = []
        for ball_id in list(self.trajectories.keys()):
            for hole_id in list(self.trajectories[ball_id].keys()):
                trajectories.append((ball_id, hole_id, self.trajectories[ball_id][hole_id]))
        return trajectories

    def get_ids(self) -> list[int]:
        """
        Return a list of all IDs.
        """
        ids = []
        for ball_id in list(self.trajectories.keys()):
            for hole_id in list(self.trajectories[ball_id].keys()):
                ids.append(self.trajectories[ball_id][hole_id].id)
        return ids


class SelectTrajectories:
    """
    A class for selecting trajectories.
    """
    def __init__(self) -> None:
        """
        Create a new SelectTrajectories.
        """
        self.trajectories = {}

    def select_trajectories(self, trajectories: TrajectoryStore, ball_store: BallStore) -> None:
        """
        Select the best trajectories.
        """
        white_ball = ball_store.get_white_ball()
        for ball_id, hole_id, trajectory in trajectories.enumerate():
            self.trajectories[trajectory.get_difficulty(white_ball)] = trajectory
    
    def update_trajectories(self, trajectories: TrajectoryStore, ball_store: BallStore) -> None:
        """
        Update the selected trajectories.
        """
        self.trajectories = {}
        self.select_trajectories(trajectories, ball_store)
    
    def get_trajectory(self, difficulty: float = None) -> Trajectory:
        """
        Return the trajectory with the given difficulty, or the easiest if no difficulty is given.
        """
        if difficulty is None:
            return self.get_easiest()
        
        if difficulty not in self.trajectories:
            difficulty = min(self.trajectories.keys(), key=lambda x: abs(x - difficulty))
        return self.trajectories[difficulty]

    def get_easiest(self) -> Trajectory:
        """
        Return the easiest trajectory.
        """
        return self.trajectories[min(self.trajectories.keys())]
    
    def get_hardest(self) -> Trajectory:
        """
        Return the hardest trajectory.
        """
        return self.trajectories[max(self.trajectories.keys())]
