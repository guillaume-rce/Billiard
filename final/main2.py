from modules.elements import Ball, BallStore, Table
from modules.utils import TrajectoryUtils

Rxs, Rys = [30, 40, 150, 20], [40, 30, 70, 60]
Jxs, Jys = [10, 40, 150], [80, 40, 10]

# Create a new BallStore and add some balls to it
ball_store = BallStore()
ball_store.add_balls(Rxs, Rys, "red")
ball_store.add_balls(Jxs, Jys, "yellow")
ball_store.add_balls([10], [10], "white")

ball_store.get_balls("red")

traj = Trajectory(ball_store)
print(traj.is_valid_move(Ball.get_by_id(1, ball_store.get_balls('red')), 50, 50))

# Create a new Table
table = Table(ball_store)

# Display the balls on the table
table.display_balls()

# Display the table
table.display()
