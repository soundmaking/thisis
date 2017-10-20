
import turtle

turtle_shapes = [
    'classic',  # 0
    'arrow',  #1
    'turtle',  #2
    'circle',  #3
    'square',  #4
    'triangle']  #5

speed = 10
size = 0.25
shape = turtle_shapes[5]

t1 = turtle.Pen()
t1.shape(shape)
t1.shapesize(size)
t1.speed(speed)

t2 = turtle.Pen()
t2.shape(shape)
t2.shapesize(size)
t2.speed(speed)

t3 = turtle.Pen()
t3.shape(shape)
t3.shapesize(size)
t3.speed(speed)

t4 = turtle.Pen()
t4.shape(shape)
t4.shapesize(size)
t4.speed(speed)

x = 0
x_max = 2

z = 0
z_max = 9

# a and b are used with x to set step
a = 5
b = 4

turn = 52

count = 0

while True:
    count += 1
    if count % 10 == 0:
        print('count = ', count)

    if x <= x_max:
        step = a*(x+b)
        
        t1.fd(step)
        t2.bk(step)
        t3.fd(step)
        t4.bk(step)
        
        x +=1
        z += 1
    else:
        x = 0
        
        
        t1.left(turn)
        t2.rt(turn)
        t3.rt(turn)
        t4.left(turn)

    if z == z_max:
        t1.right(turn)
        t2.left(turn)
        t3.lt(turn)
        t4.rt(turn)
        z = 0

