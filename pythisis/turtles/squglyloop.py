
import turtle



turtle_shapes = ['classic', 'arrow', 'turtle', 'circle', 'square', 'triangle']


trtl = turtle.Pen()

trtl.shape('circle')

trtl.shapesize(0.1, 0.1)

trtl.speed(10)

step_start = 1
step = step_start
step_inc = 1
step_max = 20


turn = 0
turn_inc = 103.4


while 1 == 1:
    trtl.fd(step)
    trtl.left(turn)
    
    step += step_inc
    if step > step_max:
        turn += 45
        step = step_start
    
    turn += turn_inc
    if turn > 360:
        turn = turn % 360


