from modules.trajectory import Trajectory
from modules.select_trajectory import SelectTrajectory
from modules.elements import *

Rxs, Rys = [50, 40, 150, 20, 100], [40, 30, 70, 60, 50]
Yxs, Yys = [10, 40, 100, 150], [80, 40, 10, 50]
Wx, Wy = [100], [60]
Bx, By = [80], [90]

player = "red"
opponent = "yellow"

ball_store = BallStore()
ball_store.add_balls(Rxs, Rys, "red")
ball_store.add_balls(Yxs, Yys, "yellow")
ball_store.add_balls(Bx, By, "black")
ball_store.add_balls(Wx, Wy, "white")
ball_store.set_players(player, opponent)

hole_store = HoleStore()

for count, hole in enumerate(hole_store.get_all()):
    if count == 4 or count == 5:
        continue
    trajectories = SelectTrajectory()
    trajectories.select_trajectories_by_bounce(ball_store, hole_store, hole)

    table = Table()
    table.draw_table()
    table.draw_holes(hole_store)
    table.draw_balls(ball_store)
    easiest_trajectories, difficulty = trajectories.get_easiest(ball_store)

    for trajectory in easiest_trajectories[0].get_all():
        print(trajectory.get_departure(), trajectory.get_arrival(), '\n')
        table.draw_line(
            trajectory.get_departure(),
            trajectory.get_arrival(),
            'white',
        )
    table.display()
