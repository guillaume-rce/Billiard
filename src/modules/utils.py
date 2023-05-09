from numpy import stack, sqrt, floor, ceil, arccos as acos

def convert_coordinates(xs: tuple, ys: tuple) -> tuple:
    """Converts coordinates from the simulator to the map."""
    points = stack((xs, ys), axis=-1)
    return points


class Vector2D:
    """2D vector class."""
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def orthogonal(self) -> "Vector2D":
        return Vector2D(-self.y, self.x)
    
    @property
    def normalize(self) -> "Vector2D":
        return self / abs(self)
    
    def dot(self, other: "Vector2D") -> float:
        return self.x * other.x + self.y * other.y
    
    def get_angle(self, other: "Vector2D") -> float:
        return acos(self.dot(other) / (abs(self) * abs(other)))

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(self.x / other, self.y / other)

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: "Vector2D") -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __len__(self) -> int:
        return 2

    def __getitem__(self, item) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, key, value) -> None:
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    def __pos__(self) -> "Vector2D":
        return Vector2D(self.x, self.y)

    def __round__(self, n=None) -> "Vector2D":
        return Vector2D(round(self.x, n), round(self.y, n))

    def __floor__(self) -> "Vector2D":
        return Vector2D(floor(self.x), floor(self.y))

    def __ceil__(self) -> "Vector2D":
        return Vector2D(ceil(self.x), ceil(self.y))

    def __lt__(self, other: "Vector2D") -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other: "Vector2D") -> bool:
        return self.x <= other.x and self.y <= other.y