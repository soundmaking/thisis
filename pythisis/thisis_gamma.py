#
from euclid import *
# for euclid docs see: https://github.com/ezag/pyeuclid/blob/master/euclid.rst
# for "euclid.py with updated raise error calls for python 3." see https://github.com/makemate/euclid_package


keyword_list = ['put', 'draw']

# parse_line() returns list as
#     ['/!', 'a', 'return', 'message']
# with one of these types:
return_types_dict = {
    '/?': 'error',
    '/>': 'successful put',
    '/<': 'successful unput',
    '/_': 'drawing data',
    '/v': 'vector or value data'
}

class Thisis:
    has_been_put = {'x': Vector2(0.50, 0.50), 'z': Vector2(0.00, 0.00)}


    def parse_line(self, txt_in):
        # line_in should be a pre-processed list of strings that make up a command line of text



        kw = txt_in[0]
        print('kw = ', kw)

        if kw not in keyword_list:
            ret_msg = ['/?', kw]
            return ret_msg

        if kw == 'put':
            # put is the fundamental thisis command with syntax structure:
            #     put <point name> <put type [at|on|where|group]> <(additional info to specify where)>
            # successful put commands result in new or altered items in the has_been_put dict

            v_name = txt_in[1]
            put_type = txt_in[2]

            print('put_type = ', put_type)

            if put_type == 'at':
                x = float(txt_in[3])
                y = float(txt_in[4])
                print("x,y = ",[x,y])
                self.has_been_put[v_name] = Vector2(x,y)
                print('has_been_put = ', self.has_been_put)
                return ['/>', v_name]
            # end if put_type is 'at'
            elif put_type == 'on':
                pass



        # end if kw is 'put'

        if kw == 'draw':
            # fixme test for length of the command

            v1_name = txt_in[1]
            draw_type = txt_in[2]
            print('draw_type = ', draw_type)
            if draw_type == 'to':
                v2_name = txt_in[3]
                ret_msg = ['/_',
                           'linesegment',
                           self.has_been_put[v1_name].x,
                           self.has_been_put[v1_name].y,
                           self.has_been_put[v2_name].x,
                           self.has_been_put[v2_name].y,
                           ]
                print('ret_msg:', ret_msg)
                return ret_msg

            # end if draw_type == 'to'

        # end if kw is 'draw'
        else:
            print('?')
    # end def parse_line(self, line)