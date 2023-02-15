from modules.elements import *
from modules.utils import Vector2D

class Trajectory:
    def __init__(self, departure: Ball|Hole, arrival: Ball|Hole) -> None:
        self.departure = departure
        self.arrival = arrival
    
    def get_departure(self) -> Ball|Hole:
        return self.departure
    
    def get_arrival(self) -> Ball|Hole:
        return self.arrival
    
    def get_vector(self) -> Vector2D:
        return Vector2D(self.arrival.x - self.departure.x, self.arrival.y - self.departure.y)
    
    def get_angle(self, other: "Trajectory") -> float:
        return self.get_vector().get_angle(other.get_vector())
    
    def __abs__(self) -> float:
        return abs(self.get_vector())

    def __repr__(self) -> str:
        return "Trajectory({self.departure}, {self.arrival})".format(self=self)
    
    def __str__(self) -> str:
        return "({self.departure}, {self.arrival})".format(self=self)