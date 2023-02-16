from modules.trajectory import Trajectory
from modules.select_trajectory import SelectTrajectory
from modules.elements import *

Rxs, Rys = [30, 40, 150, 20], [40, 30, 70, 60]
Yxs, Yys = [10, 40, 150], [80, 40, 10]
Wx, Wy = [100], [60]
Bx, By = [80], [90]

ball = Ball(3, 4)
hole = Hole(5, 6)

ball2 = Ball(5, 6)
hole2 = Hole(2, 5)

ball_store = BallStore()
ball_store.add_balls(Rxs, Rys, "red")
ball_store.add_balls(Yxs, Yys, "yellow")
ball_store.add_balls(Bx, By, "black")
ball_store.add_balls(Wx, Wy, "white")
ball_store.set_players("red", "yellow")

hole_store = HoleStore()

print(ball_store.get_white_ball())

select_trajectories = SelectTrajectory()
select_trajectories.enumerate_all_trajectories(ball_store, hole_store, 1)
for trajectory_store in select_trajectories.get_trajectories():
    print(trajectory_store)
    print("\n")