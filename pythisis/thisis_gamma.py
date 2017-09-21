
from euclid3 import *
from math import sqrt, pi, cos, sin

keyword_list = ['clear', 'put', 'draw']  # get set macro spawn
types_of_put = ['at']  # 'on' 'where' 'group'
types_of_draw = ['to', 'around']  # . .o .x .[] thru spiral
types_of_on = ['to', 'around']

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
        # txt_in should be a pre-processed list of strings that make up a command line
        kw = txt_in[0]
        print('kw = ', kw)
        # test for length of the command
        # if len(txt_in) < 2:
        #     ret_msg = ['/?', kw, '<= commands need more words']
        #     print('ret_msg:', ret_msg)
        #     return ret_msg

        if kw not in keyword_list:
            ret_msg = ['/='].append(txt_in)
            print('ret_msg:', ret_msg)
            return ret_msg

        if kw == 'clear':
            return ['/_', 'clear']

        if kw == 'put':
            # put is the fundamental thisis command with syntax structure:
            #     put <point name> <put type [at|on|where|group]> <(additional info to specify where)>
            # successful put commands result in new or altered items in the has_been_put dict
            if len(txt_in) < 5:
                ret_msg = ['/?', 'put commands need more words']
                print('ret_msg:', ret_msg)
                return ret_msg

            p_name = txt_in[1]
            put_type = txt_in[2]

            print('put_type = ', put_type)

            if put_type == 'at':
                x = float(txt_in[3])
                y = float(txt_in[4])
                print("x,y = ", [x, y])
                self.has_been_put[p_name] = Point2(x, y)
                print('has_been_put = ', self.has_been_put)
                return ['/>', p_name, str(x), str(y)]
            # end if put_type is 'at'

            if put_type == 'on':
                # // put C on A $4 B at <value> <type>
                #               ^- $4 specifies the relationship
                #                 between points A and B ($3 and $5)
                #                 which have already been put
                on_type = txt_in[4]
                if on_type not in types_of_on:
                    return ['/?', 'on', on_type, 'unknown']
                if on_type == 'around':
                    # put $1 on $3 around $5 at $7 deg
                    p_name = txt_in[1]
                    if len(txt_in) < 8:
                        ret_msg = ['/?', 'something missing?', '/='].append(txt_in)
                        print('ret_msg:', ret_msg)
                        return ret_msg
                    p3 = self.has_been_put[txt_in[3]]
                    p5 = self.has_been_put[txt_in[5]]
                    theta = float(txt_in[7])

                    if len(txt_in) > 8:
                        theta_unit = txt_in[8]
                    else:
                        theta_unit = 'deg'

                    radius = howfar(p3, p5)
                    vector = poltocar(radius, theta, theta_unit)
                    p = vector + p5
                    return self.parse_line(['put', p_name, 'at', p.x, p.y])
            # end if put_type == 'on':
        # end if kw == 'put'

        if kw == 'draw':

            p1_name = txt_in[1]

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


def howfar(p1=Point2(), p2=Point2()):
    a = p1.x - p2.x
    b = p1.y - p2.y
    h = sqrt(a**2 + b**2)
    return h
