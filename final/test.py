from modules.trajectoryV2 import Trajectory
from modules.elements import Ball, Hole

ball = Ball(3, 4)
hole = Hole(5, 6)

ball2 = Ball(5, 6)
hole2 = Hole(2, 5)

trajectory = Trajectory(ball, hole)
print(trajectory)
print(trajectory.get_vector())

trajectory2 = Trajectory(ball2, hole2)
print(trajectory2)
print(trajectory2.get_vector())

print(trajectory.get_angle(trajectory2))