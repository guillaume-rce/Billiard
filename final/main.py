from modules.elements import BallStore, Table, HoleStore
from modules.trajectory import TrajectoryStore, SelectTrajectories


Rxs, Rys = [30, 40, 150, 20], [40, 30, 70, 60]
Yxs, Yys = [10, 40, 150], [80, 40, 10]
Wx, Wy = [100], [60]
Bx, By = [80], [90]

# Create a new BallStore and add some balls to it
ball_store = BallStore()
ball_store.add_balls(Rxs, Rys, "red")
ball_store.add_balls(Yxs, Yys, "yellow")
ball_store.add_balls(Bx, By, "black")
ball_store.add_balls(Wx, Wy, "white")
ball_store.set_players("red", "yellow")

hole_store = HoleStore()  # Create a new HoleStore

trajectory_store = TrajectoryStore()
trajectory_store.add_trajectories(ball_store, hole_store)

# Create a new Table
table = Table(hole_store)

# Display the balls on the table
table.draw_balls(ball_store)

trajectories = SelectTrajectories()
trajectories.select_trajectories(trajectory_store, ball_store)

table.draw_liaison(
    ball_store.get_white_ball(),
    trajectories.get_easiest().get_ball(),
    'black',
)
table.draw_liaison_by_coords(
    trajectories.get_easiest().get_ball().x,
    trajectories.get_easiest().get_ball().y,
    trajectories.get_easiest().get_hole().x,
    trajectories.get_easiest().get_hole().y,
    'black',
)

table.draw_liaison(
    ball_store.get_white_ball(),
    trajectories.get_hardest().get_ball(),
    'red',
)
table.draw_liaison_by_coords(
    trajectories.get_hardest().get_ball().x,
    trajectories.get_hardest().get_ball().y,
    trajectories.get_hardest().get_hole().x,
    trajectories.get_hardest().get_hole().y,
    'red',
)

# Display the table
table.display()
