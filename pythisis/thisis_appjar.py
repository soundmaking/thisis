
# experiment to test out appjar

from appJar import gui
import thisis_gamma
import turtle

turtle_shapes = ['classic', 'arrow', 'turtle', 'circle', 'square', 'triangle']



app = gui("test", "600x400")
app.setFont(20)

thisis = thisis_gamma.Thisis()
pen = turtle.Pen()



def press(what):
    print(what)




def text_bttn(_arg):
    thisis.text_buffer.string_to_buffer(app.getTextArea('textbox'))
    ret_buffer = thisis.self_buffer_parse()
    print(ret_buffer)



def update_settings(*args):
    pen.shape(app.getOptionBox('turtle shape'))


app.addTextArea('textbox').config(font="Courier 20")

app.addButton("txt", text_bttn)

app.addLabelOptionBox('turtle shape', turtle_shapes)
app.addButton('update', update_settings)




app.go()