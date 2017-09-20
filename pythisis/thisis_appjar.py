
# experiment to test out appjar

from appJar import gui
import thisis_gamma
import turtle
import euclid as eu
from math import pi, degrees, sqrt

turtle_shapes = ['classic', 'arrow', 'turtle', 'circle', 'square', 'triangle']



app = gui("test", "600x400")
app.setFont(20)

thisis = thisis_gamma.Thisis()
pen = turtle.Pen()
pen.shape('square')
pen.shapesize(0.1, 0.1)



def press(what):
    print(what)




def text_bttn(_arg):
    thisis.text_buffer.string_to_buffer(app.getTextArea('textbox'))
    ret_buffer = thisis.self_buffer_parse()
    for li in ret_buffer:
        if li[0] == '/_':
            del li[0]
            draw_type = li.pop(0)
            if draw_type == 'linesegment':
                p1 = eu.Point2(li[0], li[1])
                p2 = eu.Point2(li[2], li[3])

                pen.penup()
                pen.goto(p1.x, p1.y)
                pen.pendown()
                pen.begin_poly()
                pen.goto(p2.x, p2.y)
                pen.end_poly()

    # print(ret_buffer)



def update_settings(*args):
    pass


app.addTextArea('textbox').config(font="Courier 20")

app.addButton("txt", text_bttn)

# app.addLabelOptionBox('turtle shape', turtle_shapes)
# app.addButton('update', update_settings)

app.setTextArea('textbox', '''/!
put n at 0 111
put e at 111 0
put s at 0 -111
put w at -111 0

draw n to e
draw e to s
draw s to w
draw w to n
''')


app.go()