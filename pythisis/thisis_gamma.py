
from euclid3 import *
from math import sqrt, pi, cos, sin, atan2, degrees

# the 'to do' lists below are based on documentation of syntax in thisis_beta

keyword_list = ['clear', 'put', 'unput', 'draw']
# todo , 'delay', 'set', 'get', 'macro', '{', '}', '{}', 'spawn',
types_of_put = ['at', 'on']  # todo , 'where', 'group'
types_of_on = ['to', 'around']
types_of_draw = ['to', 'around']
# todo , '.', '.o', '.x', '.[]', 'thru', 'spiral'
# types_of_clear = []  # todo 'all', 'put', 'macros', 'namedrgba',
# types_of_set = []
# todo 'delaytime', 'namedrgba', 'dot', 'pen', 'penloc', 'sleep', '_'
# types_of_pen_set = []  # todo 'size', 'rgba', 'namedrgba'
# types_of_penloc_set = []  # todo 'to', 'move'
# types_of_get = []  # todo 'rgba', 'howfar', 'whereis', 'howmany'
# types_of_spiral = []  # todo 'log', 'Archimedes', 'A'
# types_of_macro = []  # todo 'start', 'end', 'run'

# deprecated syntax:
#    keywords that were in _beta, but are dropped:...
#         lcd, thisis, (relpx,rel,relative),
#    ...or changed in _gamma:
#        clearall, colour, dotsize, pensize, (sleep,_),

# idea - maybe collapse all the types_of_... lists into a one nested
#         structure which could then be parsed out to document the syntax

return_types_dict = {
    # parse_line() returns list such as ['/!', 'a', 'return', 'message']
    # beginning with one of these token types:
    '/?': 'error',
    '/>': 'successful put',
    '/<': 'successful unput',
    '/_': 'drawing data',
    '/v': 'vector or value data',
    '/=': 'through-put for un-matched kw'
    #  any of these will also act to comment out a single line if parsed
}

# commenting:
to_comment_line = ['//', '/!'] + list(return_types_dict.keys())
to_start_block_comment = ['/*', '/..']
to_end_block_comment = ['*/', '../']



def degtorad(deg):
    return pi*(deg/180)


def poltocar(r, theta, *args):
    # polar to cartesian:
    #   input  = radius and radians (or degrees if specified in call)
    #   output = x y vector
    if 'deg' in args:
        theta = degtorad(theta)
    x = cos(theta) * r
    y = sin(theta) * r
    return Vector2(x, y)


def cartopol(x, y, *args):
    # cartesian to polar:
    #   input  = x and y
    #   output = r and theta in radians (or degrees if specified in call)
    r = howfar(Point2(x, y))
    theta = atan2(y, x)
    if 'deg' in args:
        theta = degrees(theta)
    return [r, theta]


def howfar(p1=Point2(), p2=Point2()):
    a = p1.x - p2.x
    b = p1.y - p2.y
    h = sqrt(a**2 + b**2)
    return h


class TextBuffer:
    def __init__(self):
        self.buffer = []

    def string_to_buffer(self, text_in, mode='set'):
        if mode == 'set':
            self.buffer = []
        # if mode not 'set' then text_in appends to existing buffer
        for l in text_in.splitlines():
            self.buffer.append(l.split())

    def line(self, num):
        # todo error catching on num
        return self.buffer[num]

    def cut_comments(self):
        print('before cut comments:', self.buffer)
        block_comment_active = False
        ret_buf = []
        for li in self.buffer:
            if len(li) > 0:
                if not block_comment_active:
                    if li[0] in to_start_block_comment:
                        block_comment_active = True
                    elif li[0] not in to_comment_line:
                        ret_buf.append(li)
                else:
                    # is in comment block, so look for end of block
                    if li[0] in to_end_block_comment:
                        block_comment_active = False
        self.buffer = ret_buf
        print('after cut comments:', self.buffer)


class Thisis:
    has_been_put = {'x': Point2(0.50, 0.50), 'z': Point2(0.00, 0.00)}

    text_buffer = TextBuffer()

    def self_buffer_parse(self):
        return self.buffer_parse(self.text_buffer.buffer)

    def buffer_parse(self, input_buffer):
        return_buffer = []
        p = TextBuffer()
        p.buffer = input_buffer
        p.cut_comments()
        for li in p.buffer:
            # fixme
            return_buffer.append(self.parse_line(li))
        return return_buffer

    def parse_line(self, txt_in):
        # txt_in is expected to be a list of strings
        kw = txt_in[0]
        print('kw = ', kw)

        if kw not in keyword_list:
            ret_msg = ['/='].append(txt_in)
            print('ret_msg:', ret_msg)
            return ret_msg

        if kw == 'clear':
            return ['/_', 'clear']

        if kw == 'put':
            # put is the fundamental thisis command with syntax structure:
            #     put
            #     <point name>
            #     <put type [at|on|where|group]>
            #     <(additional info to specify where)>
            # successful put commands make changes to the has_been_put dict
            if len(txt_in) < 5:
                ret_msg = ['/?', 'too short:', '/='].append(txt_in)
                print('ret_msg:', ret_msg)
                return ret_msg

            p_name = txt_in[1]
            put_type = txt_in[2]

            # print('put_type = ', put_type)

            if put_type == 'at':
                x = float(txt_in[3])
                y = float(txt_in[4])
                print("x,y = ", [x, y])
                self.has_been_put[p_name] = Point2(x, y)
                print('has_been_put = ', self.has_been_put)
                return ['/>', p_name, str(x), str(y)]
            # end if put_type is 'at'



            if put_type == 'on':
                # // put C on A $4 B at <value> <unit_type>
                #               ^- $4 specifies the relationship
                #                 between points A and B ($3 and $5)
                #                 which have already been put
                # // put $1 on $3 around $5 at $7 deg
                #                                 ^- 'deg' or 'rad'
                # // put $1 on $3 to $5 at $7 %
                #                             ^\
                #            in version _b the '%-' unit_type was added
                #            to fix the 'reverse slope' bug in version _a.
                #
                #     for _g a new method is implemented.

                if len(txt_in) < 8:
                    # Abort if the message isn't long enough
                    ret_msg = ['/?', 'not enough words', '/='].append(txt_in)
                    print('ret_msg:', ret_msg)
                    return ret_msg

                on_type = txt_in[4]
                if on_type not in types_of_on:
                    return ['/?', 'on', on_type, 'unknown']
                p3 = self.has_been_put[txt_in[3]]
                p5 = self.has_been_put[txt_in[5]]
                distance = howfar(p3, p5)
                f7 = float(txt_in[7])  # f7 is the <value>

                if len(txt_in) > 8:
                    unit_type = txt_in[8]
                else:
                    # Set default unit type:
                    unit_type = 'deg' if on_type == 'around' else '%'

                if on_type == 'around':
                    p = p5 + poltocar(distance, f7, unit_type)
                    return self.parse_line(['put', p_name, 'at', p.x, p.y])
                # end if on_type == 'around'

                if on_type == 'to':
                    v = p5-p3
                    r, theta = cartopol(v.x, v.y)  # theta in radians this time
                    if unit_type == '%':
                        n = float(f7) / 100.
                    else:
                        n = 0.5  # fixme handle error: unit_type not '%'
                    d = r * n
                    temp_x, temp_y = p3 + Point2(d, 0)
                    temp_msg = ['put', '_temp_', 'at', temp_x, temp_y]
                    self.parse_line(temp_msg)

                    temp_msg = ['put', p_name,
                                'on', '_temp_', 'around', txt_in[3],
                                'at', theta, 'rad']
                    ret_msg = self.parse_line(temp_msg)
                    # self.parse_line(['unput', '_temp_'])
                    #  fixme test with unput
                    return ret_msg

                # end if on_type == 'to'
            # end if put_type == 'on':
        # end if kw == 'put'

        if kw == 'unput':
            try:
                p_name = txt_in[1]
            except IndexError:
                print('nothing after', kw)
                return ['/?', 'nothing after', kw]
            if p_name in self.has_been_put:
                del self.has_been_put[p_name]
                ret_msg = ['/<', p_name]
            else:
                ret_msg = ['/?', p_name, 'has not been put']
            return ret_msg
        # end if kw == 'unput'

        if kw == 'draw':
            try:
                p1_name = txt_in[1]
            except IndexError:
                print('nothing after', kw)
                return ['/?', 'nothing after', kw]

            if p1_name not in self.has_been_put:
                ret_msg = ['/?', p1_name, 'has not been put']
                print('ret_msg:', ret_msg)
                return ret_msg

            draw_type = txt_in[2]

            if draw_type in types_of_draw:
                print('draw_type = ', draw_type)
                if draw_type == 'to':
                    p2_name = txt_in[3]

                    if p2_name not in self.has_been_put:
                        ret_msg = ['/?', p2_name, 'has not been put']
                        print('ret_msg:', ret_msg)
                        return ret_msg

                    ret_msg = ['/_',
                               'linesegment',
                               self.has_been_put[p1_name].x,
                               self.has_been_put[p1_name].y,
                               self.has_been_put[p2_name].x,
                               self.has_been_put[p2_name].y,
                               ]
                    print('ret_msg:', ret_msg)
                    return ret_msg
                # end if draw_type == 'to'
                if draw_type == 'around':
                    p2_name = txt_in[3]

                    if p2_name not in self.has_been_put:
                        ret_msg = ['/?', p2_name, 'has not been put']
                        print('ret_msg:', ret_msg)
                        return ret_msg

                    p1 = self.has_been_put[p1_name]
                    p2 = self.has_been_put[p2_name]
                    radius = howfar(p1, p2)

                    ret_msg = ['/_', 'circle', p2.x, p2.y, radius]
                    print('ret_msg:', ret_msg)
                    return ret_msg
                # end if draw_type == 'to'
            # end if draw_type not in types_of_draw:
            else:
                ret_msg = ['/?', draw_type]
                print('ret_msg:', ret_msg)
                return ret_msg

        # end if kw == 'draw'
        else:
            # function shouldn't reach this if keyword_list is correct
            print('? check keyword_list')
            return ['/?', '!']
    # end def parse_line(self, line)


if __name__ == '__main__':
    print('/!\n/! thisis \n/! _gamma \n/!')
    thisis = Thisis()
    done = False
    while not done:
        text = input('/!>>> ')
        if text == 'exit':
            done = True
            break
        thisis.text_buffer.string_to_buffer(text)
        ret_buffer = thisis.self_buffer_parse()
        for li in ret_buffer:
            print('/!\n/!<<<', li, '\n/!')
