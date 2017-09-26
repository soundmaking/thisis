import thisis_gamma
from euclid3 import Point2  # , Vector2
from math import pi

thisis = thisis_gamma.Thisis()


v = thisis_gamma.poltocar(4, pi/2)
print(v)

v2 = thisis_gamma.poltocar(4, -90, 'deg')
print(v2)


v3 = thisis_gamma.poltocar(4, 45, 'deg')
print(v3)

p1 = Point2(v)
p2 = Point2(v3)


print(v3.xy)

x1, y1 = v3.xy

print(x1, y1)

d = thisis_gamma.howfar(v, v2)
print(d)


