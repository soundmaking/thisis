#
from euclid import *
# for euclid docs see: https://github.com/ezag/pyeuclid/blob/master/euclid.rst
# for "euclid.py with updated raise error calls for python 3." see https://github.com/makemate/euclid_package

from math import sqrt, pow

keyword_list = ['clear', 'put', 'draw']  # get set macro spawn
types_of_put = ['at']  # 'on' 'where' 'group'
types_of_draw = ['to', 'around']  # . .o .x .[] thru spiral

# parse_line() returns list as
#     ['/!', 'a', 'return', 'message']
# with one of these types:
return_types_dict = {
    '/?': 'error',
    '/>': 'successful put',
    '/<': 'successful unput',
    '/_': 'drawing data',
    '/v': 'vector or value data',
    '/=': 'through-put for un-matched kw'
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
            ret_msg = ['/?', kw, '<= not a keyword']
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

            v_name = txt_in[1]
            put_type = txt_in[2]

            print('put_type = ', put_type)

            if put_type == 'at':
                x = float(txt_in[3])
                y = float(txt_in[4])
                print("x,y = ", [x, y])
                self.has_been_put[v_name] = Point2(x, y)
                print('has_been_put = ', self.has_been_put)
                return ['/>', v_name]
            # end if put_type is 'at'
            elif put_type == 'on':
                pass

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

                    x1 = self.has_been_put[p1_name].x
                    y1 = self.has_been_put[p1_name].y
                    x2 = self.has_been_put[p2_name].x
                    y2 = self.has_been_put[p2_name].y
                    radius = sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))

                    ret_msg = ['/_', 'circle', x2, y2, radius]
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
            print('? check keyword_list')  # shouldn't reach this
            return ['/?', '!']
    # end def parse_line(self, line)
