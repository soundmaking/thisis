
import turtle



turtle_shapes = ['classic', 'arrow', 'turtle', 'circle', 'square', 'triangle']


trtl = turtle.Pen()

trtl.shape('circle')

trtl.shapesize(0.1, 0.1)

trtl.speed(5)

x = 1
z = 0

while True:
    if x < 4:
        trtl.fd(24)
        x +=1
        z += 1
    else:
        trtl.left(27)
        x = 0

    if z == 7:
        trtl.right(130)
        z = 0
