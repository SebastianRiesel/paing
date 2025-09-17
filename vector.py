import math
from typing import Sized


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'({self.x}, {self.y})'

    def scaled(self, scalar):
        return Vector2(self.x*scalar, self.y*scalar)

    def normalized(self):
        return self.scaled(1/abs(self))




