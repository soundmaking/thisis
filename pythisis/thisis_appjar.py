
# experiment to test out appjar

from appJar import gui
import thisis_gamma
import turtle


turtle_shapes = ['classic', 'arrow', 'turtle', 'circle', 'square', 'triangle']


app = gui("test", "600x400")
app.setFont(20)

thisis = thisis_gamma.Thisis()

trtl = turtle.Pen()
trtl.shape('square')
trtl.shapesize(0.1, 0.1)
trtl.speed(10)


def press(what):
    print(what)


def text_bttn(_arg):
    thisis.text_buffer.string_to_buffer(app.getTextArea('textbox'))
    ret_msg_list = thisis.self_buffer_parse()

    for msg in ret_msg_list:
        msg_type = msg[0]
        
        if '/_' == msg_type:
            # drawing...
            del msg[0]
            draw_type = msg.pop(0)
            
            if 'clear' == draw_type:
                trtl.clear()
                
            if 'linesegment' == draw_type:
                p1x, p1y, p2x, p2y = msg
                trtl.penup()
                trtl.goto(p1x, p1y)
                trtl.pendown()
                trtl.begin_poly()
                trtl.goto(p2x, p2y)
                trtl.end_poly()
                
            if 'poly' == draw_type:
                p1x, p1y, p2x, p2y = msg[0:4]
                trtl.penup()
                trtl.goto(p1x, p1y)
                trtl.pendown()
                trtl.begin_poly()
                trtl.goto(p2x, p2y)
                for n in range(4, len(msg), 2):
                    nx, ny = msg[n:n+2]
                    trtl.goto(nx, ny)
                trtl.end_poly()
                
            if 'circle' == draw_type:
                x, y, r = msg
                trtl.penup()
                trtl.goto(x, y - r)
                trtl.setheading(0)
                trtl.pendown()
                trtl.circle(r)

        elif '/>' == msg_type:
            # point(s) has(ve) been put...
            info = msg.pop(0)
            for n in range(0, len(msg), 3):
                info += ' '+str(msg[n])
            print(info)
            
        else:
            print('other:', msg)
        
# end def text_bttn(_arg)


def update_settings():
    pass


app.addTextArea('textbox').config(font="Courier 20")

app.addButton("txt", text_bttn)

# app.addLabelOptionBox('turtle shape', turtle_shapes)
# app.addButton('update', update_settings)

app.setTextArea('textbox', '''/!
/*
  drawing with thisis_gamma
    'on slippers'
    by sdf 2017-09-24
*/

clear
put x at 123 123 

put L on x around z at -180 deg
put R on x around z at 0 deg

put aR on x around z at 15 deg
put bR on x around z at -15 deg
put aL on x around z at 165 deg
put bL on x around z at -165 deg

put acL on aL to aR at 40 %
put acR on aR to aL at 40 %
put bcR on bR to bL at 40 %
put bcL on bL to bR at 40 %

put bbcR on acR to bcR at 150 %
put bbcL on acL to bcL at 150 %
put aacR on bcR to acR at 150 %
put aacL on bcL to acL at 150 %

put LaacL on aacR to aacL at 175 %
put RaacR on aacL to aacR at 175 %
put LbbcL on bbcR to bbcL at 175 %
put RbbcR on bbcL to bbcR at 175 %

put c group 24 on x around z

//


draw aL to acL
draw acL to aacL
draw aacL to LaacL

draw bL to bcL
draw bcL to bbcL
draw bbcL to LbbcL

draw aR to acR
draw acR to aacR
draw aacR to RaacR

draw bR to bcR
draw bcR to bbcR
draw bbcR to RbbcR

draw L to R

// draw x around z

draw aR thru c2 c3 c4 c5 c6 c7 c8 c9 c10 aL
draw bL thru c14 c15 c16 c17 c18 c19 c20 c21 c22 bR
''')


app.go()
