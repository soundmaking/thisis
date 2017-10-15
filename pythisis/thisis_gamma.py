
from euclid3 import Point2, Vector2
from math import sqrt, pi, cos, sin, atan2, degrees


# # #
# # # # # # Syntax Stuff # # # # # #
# # #

syntax_key = {
    'clear': (
        'all',
        'put',
        'macros',
        'rgba'),
    'clearall': None,
    'put': {
        'at': None,
        'on': ('to', 'around'),
        'where': (),
        'group': None},
    'unput': None,
    'draw': {
        'line': {
            'to': None,
            'around': None,
            'thru': None,
            'arc': None,  # todo
            'spiral': (  # todo
                'log',
                'Archimedes',
                'A')},
        'dot': (
            '.',
            '.o',
            '.x',
            '.[]'),
        'group': ()},  # todo
    'set': {  # todo
        'world': {
            'ltrb': '(todo)',
            'pixels': '(todo)',
            'theta': (  # todo
                '+cw',
                '-cw')},
        'sizes': (  # todo
            'world',
            'pixels'),
        'legacy': (
            'colour',
            'sleep',
            '_'),
        'dotsize': '(todo)',
        'pensize': '(todo)',
        'penloc': {
            '(todo)': '(todo)',
            'move': (
                '(todo)',
                'relpx',
                'rel',
                'relative'),
            'to': '(todo)'},
        'rgba': '(todo)',
        'delaytime': '(todo)',
        'sleeptime': '(todo)'},
    'get': (  # todo
        'rgba',
        'howfar',
        'whereis',
        'howmany'),
    'macro': {  # todo
        'braces': {
            '{': 'start',
            '}': 'end',
            '{}': 'run'},
        'start': '(todo)',
        'end': '(todo)',
        'run': '(todo)'},
    'delay': None,  # todo
    'spawn': '(todo)'
}  # end of syntax_key dict


return_types_dict = {
    # parse_line() returns list such as ['/!', 'a', 'return', 'message']
    # beginning with one of these token types:
    '/?': 'error',
    '/!': 'info',
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
to_comment_line.extend(to_end_block_comment)

default_settings = {
    'world': {
        'ltrb': (-1, -1, 1, 1),
        'pixels': (0, 0, 400, 400),
        'theta': '+cw'}
    'sizes': 'pixels'
}


# # #
# # # # # # Utility Functions # # # # # #
# # #


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


# # #
# # # # # # Object Classes # # # # # #
# # #


class TextBuffer:
    def __init__(self):
        self.text_lines_list = []
        # self.prev_line = -1

    def string_to_buffer(self, text_in, mode='set'):
        if mode == 'set':
            self.text_lines_list = []
        # if mode not 'set' then text_in appends to existing lines
        for l in text_in.splitlines():
            self.text_lines_list.append(l.split())

    def line(self, num):
        # todo error catching on num + add option to call 'next' line
        return self.text_lines_list[num]

    def cut_comments(self):
        # print('before cut comments:', self.text_lines_list)
        block_comment_active = False
        sans_comment_lines = []
        for l in self.text_lines_list:
            if len(l) > 0:
                if not block_comment_active:
                    if l[0] in to_start_block_comment:
                        block_comment_active = True
                    elif l[0] not in to_comment_line:
                        sans_comment_lines.append(l)
                else:
                    # is in comment block, so look for end of block
                    if l[0] in to_end_block_comment:
                        block_comment_active = False
        self.text_lines_list = sans_comment_lines
        # print('after cut comments:', self.text_lines_list)


class Thisis:
    has_been_put = {'x': Point2(0.50, 0.50), 'z': Point2(0.00, 0.00)}
    put_groups = {}
    named_rgba = {}
    macros = {}

    text_buffer = TextBuffer()

    def self_buffer_parse(self):
        return self.multi_line_parse(self.text_buffer.text_lines_list)

    def multi_line_parse(self, input_text_lines_list):
        ret_msg_list = []
        buffer = TextBuffer()
        buffer.text_lines_list = input_text_lines_list
        buffer.cut_comments()
        for l in buffer.text_lines_list:
            ret_msg_list.append(self.parse_line(l))
        return ret_msg_list

    def parse_line(self, txt_in):
        # txt_in is expected to be a list of strings
        kw = txt_in[0]
        # print('kw = ', kw)

        if kw not in syntax_key:
            return ['/=', ' '.join(txt_in)]

        if kw in ('clear', 'clearall'):
            ret_msg = ['/!']
            try:
                clear_type = txt_in[1]
            except IndexError:
                clear_type = 'all'
                ret_msg.append('clear all')

            if clear_type not in syntax_key['clear']:
                return ['/?', 'unknown clear_type: {}'.format(clear_type)]

            if clear_type in ('put', 'all'):
                ret_msg.append(
                    '/< unput {} points'.format(len(self.has_been_put)))
                self.has_been_put = {}
                self.put_groups = {}

            if clear_type in ('rgba', 'all'):
                ret_msg.append(
                    '- cleared {} named rgba'.format(len(self.named_rgba)))
                self.named_rgba = {}

            if clear_type in ('macros', 'all'):
                ret_msg.append(
                    '- cleared {} macros'.format(len(self.macros)))
                self.macros = {}

            return ret_msg
        # end kw 'clear' or 'clearall'

        if 'put' == kw:
            # put is the fundamental thisis command with syntax structure:
            #     put
            #     <point name>
            #     <put type [at|on|where|group]>
            #     <(additional info to specify where)>
            # successful put commands make changes to the has_been_put dict
            if len(txt_in) < 5:
                return ['/?', ' '.join(txt_in)]

            p_name = txt_in[1]
            put_type = txt_in[2]

            if put_type not in syntax_key['put']:
                return ['/?', 'cannot put with "{}"'.format(put_type)]

            if 'at' == put_type:
                x = float(txt_in[3])
                y = float(txt_in[4])
                self.has_been_put[p_name] = Point2(x, y)
                return ['/>', p_name, str(x), str(y)]
            # end if put_type is 'at'

            if 'on' == put_type:
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
                    return ['/?', ' '.join(txt_in)]

                on_type = txt_in[4]
                if on_type not in syntax_key['put']['on']:
                    return ['/?', 'on', on_type, 'unknown']
                p3 = self.has_been_put[txt_in[3]]
                p5 = self.has_been_put[txt_in[5]]
                distance = howfar(p3, p5)
                f7 = float(txt_in[7])  # f7 is the positional <value>

                if len(txt_in) > 8:
                    unit_type = txt_in[8]
                else:
                    unit_type = 'deg' if on_type == 'around' else '%'

                if 'around' == on_type:
                    p = p5 + poltocar(distance, f7, unit_type)
                    return self.parse_line(['put', p_name, 'at', p.x, p.y])
                # end if on_type == 'around'

                if 'to' == on_type:
                    v = p5-p3
                    r, theta = cartopol(v.x, v.y)

                    if unit_type == '%':
                        n = f7 / 100.
                    else:
                        n = f7 / 100.
                        # is same as '%' for now. todo: add unit_type option

                    x, y = p3 + Point2(r * n, 0)
                    self.parse_line(['put', '_temp_', 'at', x, y])

                    ret_msg = \
                        self.parse_line(['put', p_name,
                                         'on', '_temp_',
                                         'around', txt_in[3],
                                         'at', theta, 'rad']
                                        )
                    self.parse_line(['unput', '_temp_'])
                    return ret_msg

                # end if on_type == 'to'
            # end if put_type == 'on':

            if 'where' == put_type:
                # // put $1 where $3 is
                p3_name = txt_in[3]
                if p3_name in self.has_been_put:
                    self.has_been_put[p_name] = self.has_been_put[p3_name]
                    x, y = self.has_been_put[p3_name].xy
                    ret_msg = ['/>', p_name, x, y]
                else:
                    ret_msg = ['/?', p3_name, 'has not been put']
                return ret_msg
            # end if put_type == 'where'

            if 'group' == put_type:
                # // put p_name group $i3 on $p5 [around||to] $p7
                if not txt_in[4] == 'on':
                    err = "found [{}] where [on] should be in group put"
                    return ['/?', err.format(txt_in[4])]

                if len(txt_in) < 8:
                    ret_msg = ['/?', 'too short:', '/='].append(txt_in)
                    # print('ret_msg:', ret_msg)
                    return ret_msg

                on_type = txt_in[6]

                if on_type not in syntax_key['put']['on']:
                    return ['/?', 'unknown on_type: "{}"'.format(on_type)]

                group_size = int(txt_in[3])
                p5 = txt_in[5]
                p7 = txt_in[7]
                put = ['put', '[1]', 'on',
                       p5, on_type, p7,
                       'at', 7, '[8]'
                       ]  # [1] is new_name, [7] is value, [8] is unit_type

                put_ret_list = []
                ret_msg = ['/>']

                for n in range(group_size):
                    # print(n, '/', group_size)
                    put[1] = p_name + str(n)
                    # print(put[1])
                    if on_type == 'around':
                        put[7] = (n/group_size) * 360
                        put[8] = 'deg'
                    elif on_type == 'to':
                        put[7] = (n/group_size) * 100
                        put[8] = '%'
                    else:
                        put_ret_list.append(
                            ['/?', 'wrong on_type:', '/='].append(txt_in)
                        )
                    put_ret = self.parse_line(put)
                    put_ret_list.append(put_ret[1:])
                # end for n in range(group_size)

                ret_msg.extend(msg for msg in put_ret_list)
                self.put_groups[p_name] = group_size
                return ret_msg
            # end if put_type == 'group'
            return ['/?', txt_in]
        # end if kw == 'put'

        if 'unput' == kw:
            try:
                p_name = txt_in[1]
            except IndexError:
                return ['/?', 'unput what?']

            if p_name in self.has_been_put:
                del self.has_been_put[p_name]
                ret_msg = ['/<', p_name]
            else:
                ret_msg = ['/?', p_name, 'has not been put']
            return ret_msg
        # end if kw == 'unput'

        if 'draw' == kw:
            # do some error catching and var setup for draw commands
            try:
                p1_name = txt_in[1]
            except IndexError:
                return ['/?', 'draw what?']

            if p1_name not in self.has_been_put:
                ret_msg = ['/?', p1_name, 'has not been put']
                # print('ret_msg:', ret_msg)
                return ret_msg
            else:
                p1 = self.has_been_put[p1_name]

            try:
                draw_type = txt_in[2]
            except IndexError:
                return ['/?', 'draw {} how?'.format(p1_name)]

            type_ok = draw_type in syntax_key['draw']['line']
            type_ok = type_ok or draw_type in syntax_key['draw']['dot']
            if not type_ok:
                return ['/?', 'unknown draw_type: {}'.format(draw_type)]

            # having made it to this far in the function,
            # these vars are ready to use:
            #    p1_name, p1, draw_type
            #
            # first look for draw_types that only use p1,
            # and then do for draw_types that also use p2...

            if '.' == draw_type:
                return ['/_', 'dot', p1.x, p1.y]

            if '.o' == draw_type:
                return ['/_', 'dot_open', p1.x, p1.y]

            if '.x' == draw_type:
                return ['/_', 'dot_x', p1.x, p1.y]

            if '.[]' == draw_type:
                return ['/_', 'dot_box', p1.x, p1.y]

            # do some error checking for using p2...
            # (things need refactoring when adding spiral and group draw)

            if len(txt_in) < 4:
                return ['/?',
                        'draw {} {} what?'.format(p1_name, draw_type)]
            if txt_in[3] not in self.has_been_put:
                return ['/?', '{} has not been put'.format(txt_in[3])]

            p2_name = txt_in[3]
            p2 = self.has_been_put[p2_name]

            if 'to' == draw_type:
                ret_msg = ['/_', 'linesegment', p1.x, p1.y, p2.x, p2.y]
                return ret_msg
            # end if draw_type == 'to'

            if 'around' == draw_type:
                radius = howfar(p1, p2)
                ret_msg = ['/_', 'circle', p2.x, p2.y, radius]
                return ret_msg
            # end if draw_type == 'to'

            if 'thru' == draw_type:
                # // draw p1 thru p2 p3 ... pn
                ret_msg = ['/_', 'poly', p1.x, p1.y, p2.x, p2.y]
                num_extra_points = len(txt_in)-4

                if num_extra_points < 1:
                    return ret_msg

                for pn_name in txt_in[4:]:

                    if pn_name not in self.has_been_put:
                        return ['/?', '{} has not been put'.format(pn_name)]
                    
                    ret_msg.append(self.has_been_put[pn_name].x)
                    ret_msg.append(self.has_been_put[pn_name].y)
                    
                return ret_msg
            # end if 'thru' == draw_type
            return ['/?', txt_in]
        # end if kw == 'draw'
        else:
            # function shouldn't reach this if syntax_key is correct
            print('? check syntax_key')
            return ['/?', 'syntax_key error']
    # end def parse_line(self, line)


# # #
# # # # # # Command Line Interface style main function # # # # # #
# # #

def thisis_cli():
    print('/! \n/! thisis_gamma\n/!  ')
    print('/! interface to parser -')
    print('/!     please enter a thisis command line or "exit"')
    thisis = Thisis()
    done = False
    while not done:
        text = input('/!\n/! >>> ')
        if text == 'exit':
            # done = True
            break
        thisis.text_buffer.string_to_buffer(text)
        ret_buffer = thisis.self_buffer_parse()
        for li in ret_buffer:
            print(li)

if __name__ == '__main__':
    thisis_cli()
