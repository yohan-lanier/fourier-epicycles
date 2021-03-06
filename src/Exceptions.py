from cgi import test


def is_color_in_accepted_colors(color):
    accepted_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    if color not in accepted_colors:
        raise InvalidColor(color)
    else : return color

def test_a_color(color):
    '''
    test wether the input color is accepted by the program
    '''
    try : 
        is_color_in_accepted_colors(color)
        return color
    except InvalidColor as ic :
        color = ic.ask_for_valid_color()
        test_a_color(color)
        return color

class InvalidColor(Exception):
    '''
    class for Invalid color exception
    '''
    def __init__(self, c):
        super().__init__()
        self._value = c

    def ask_for_valid_color(self):
        print('\n-------------------------------------')
        print(f'Color {self._value} is invalid. Please input an accepted color. Accepted colors are b, g, r, c, m, y, k, w,blue, orange, green, red, purple, brown, pink, gray, olive, cyan')
        print('-------------------------------------\n')
        c = input()
        return c

class NoPathInSVG(Exception):
    def __init__(self):
        super().__init__()
    def __str__(self):
        print('No path was found in the input file. Check if your svg contains a path and try again')
