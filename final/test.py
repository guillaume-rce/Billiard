from modules.trajectory import Trajectory
from modules.select_trajectory import SelectTrajectory
from modules.elements import *

Rxs, Rys = [30, 40, 150, 20], [40, 30, 70, 60]
Yxs, Yys = [10, 40, 150], [80, 40, 10]
Wx, Wy = [100], [60]
Bx, By = [80], [90]

ball_store = BallStore()
ball_store.add_balls(Rxs, Rys, "red")
ball_store.add_balls(Yxs, Yys, "yellow")
ball_store.add_balls(Bx, By, "black")
ball_store.add_balls(Wx, Wy, "white")
ball_store.set_players("red", "yellow")

hole_store = HoleStore()

trajectories = SelectTrajectory()
for i in range(1, 4):
    ball_not_use = []
    while True:
        trajectory, balls = SelectTrajectory.select_trajectories(
            ball_store,
            hole_store.get_hole(0),
            number_of_bounce=i,
            )
        if type(trajectory) != type(None) and trajectory.is_possible(ball_store)[0]:
            trajectories.add_trajectory(trajectory, i)
            break
        else:
            if type(trajectory) != type(None):
                break
            else:
                for inpossible_trajectory in trajectory.is_possible(ball_store)[1]:
                    ball_not_use.append(inpossible_trajectory.get_arrival())
                    ball_not_use.append(inpossible_trajectory.get_departure())

table = Table()
table.draw_table()
table.draw_holes(hole_store)
table.draw_balls(ball_store)
easiest_trajectories, difficulty = trajectories.get_easiest(ball_store)
hardest_trajectories, difficulty = trajectories.get_hardest(ball_store)

for trajectory in easiest_trajectories[0].get_all():
    print(trajectory.get_departure(), trajectory.get_arrival(), '\n')
    table.draw_line(
        trajectory.get_departure(),
        trajectory.get_arrival(),
        'white',
    )

for trajectory in hardest_trajectories[0].get_all():
    print(trajectory.get_departure(), trajectory.get_arrival(), '\n')
    table.draw_line(
        trajectory.get_departure(),
        trajectory.get_arrival(),
        'black',
    )

table.display()