from Crypto.Util.number import *
import random

class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    
    def _get_y(self, x):
        y_squared = (x * x * x + self.a * x + self.b) % self.p
        y = pow(y_squared, (self.p + 1) // 4, self.p)
        return y
    
    def get_random_point(self):
        while True:
            x = random.randint(0, self.p)
            y = self._get_y(x)
            point = Point(x, y, self)
            assert point._check()
            return point
    
    def __eq__(self, other):
        if not isinstance(other, Curve):
            return NotImplemented
        return (self.a, self.b, self.p) == (other.a, other.b, other.p)
    
class Point:
    def __init__(self, x, y, curve: Curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other: "Point"):
        if self.curve != other.curve:
            raise ValueError("Points are not on the same curve")
        if self.x == other.x and self.y == other.y:
            return self.double()
        else:
            return self.add(other)
    
    def _check(self):
        if self.y**2 % self.curve.p != (self.x**3 + self.curve.a * self.x + self.curve.b) % self.curve.p:
            raise ValueError(f"Point {self} is not on the curve")

    def double(self):
        if self.y == 0:
            return Point(0, 0, self.curve)
        
        m = (3 * self.x * self.x + self.curve.a) * pow(2 * self.y, -1, self.curve.p) % self.curve.p
        x = (m * m - 2 * self.x) % self.curve.p
        y = (-self.y + m * (self.x - x)) % self.curve.p
        return Point(x, y, self.curve)
    
    def add(self, other: "Point"):
        if self.x == other.x:
            return Point(0, 0, self.curve)
        if self == Point(0, 0, self.curve):
            return other
        if other == Point(0, 0, self.curve):
            return self
        
        m = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p) % self.curve.p
        x = (m * m - self.x - other.x) % self.curve.p
        y = (-self.y + m * (self.x - x)) % self.curve.p
        return Point(x, y, self.curve)
    
    def __mul__(self, k):
        if k == 0:
            return Point(0, 0, self.curve)
        elif k < 0:
            return -self * -k
        
        result = Point(0, 0, self.curve)
        addend = self
        
        while k:
            if k & 1:
                result += addend
            addend = addend.double()
            k >>= 1
        
        return result
    
    def __rmul__(self, k):
        return self * k
    
    def __neg__(self):
        return Point(self.x, -self.y % self.curve.p, self.curve)
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y, self.curve) == (other.x, other.y, other.curve)

    
flag = b"flag{invalid_curve_attack}"
m = bytes_to_long(flag)

a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF

c = Curve(a, b, p)

while True:
    x = input("Enter x coordinate:")
    y = input("Enter y coordinate:")
    P = Point(int(x), int(y), c)
    print(m*P)
