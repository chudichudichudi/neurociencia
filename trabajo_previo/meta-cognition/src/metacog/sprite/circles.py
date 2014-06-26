'''
Created on Mar 30, 2012

@author: mariano
'''
from random import shuffle, gauss
from metacog.configuration import MAX_SIZE
from metacog.sprite.circle import Circle

def rotate_list(l, n=1):
    return l[-n:] + l[:-n]

class Circles(object):
    '''
    Class to handle the circles shown in the Metacognition experiment
    '''



    def build_circle_positions(self, initial_point, offset_x, offset_y):
        x_rows = [rotate_list(offset_x, i) for i in xrange(3)]
        x_rows = [ sum(row[:i]) + MAX_SIZE * 2 * i + initial_point[0]
                  for row in x_rows for i in xrange(3)]
        y_columns = [rotate_list(offset_y, -i) for i in xrange(3)]
        y_columns = [ sum(column[:i]) + MAX_SIZE * 2 * i + initial_point[1]
                     for i in xrange(3) for column in y_columns]
        return zip(x_rows, y_columns)



    def __init__(self, initial_point, offset_x, offset_y, size_for_easy):
        '''
        Initialize 9 circles positions and sizes
        '''
        self.size_easy = size_for_easy
        self.circles = []
        positions = self.build_circle_positions(initial_point,
                                                offset_x, offset_y)
        for i in range(len(positions)):
            self.circles.append(Circle(positions[i], i, MAX_SIZE))

        #self.size_pattern = [100, 95, 90, 80, 50, 20, 10, 5, 1]
        self.size_pattern = [96, 92, 88, 80, 75, 70, 60, 50]



    def hide(self):
        """ Hide all circles. """
        for circle in self.circles:
            circle.hide()

    def show(self):
        """ Show all circles. """
        for circle in self.circles:
            circle.show()

    def size_factor(self):
        """ Doblo una gaussiana a la mitad y se lo resto a 1. """
        return 0.5 + max(1 - abs(gauss(0, 0.5)) ** 1.5, 0.1) / 2


    # def _get_size(self, scale):
    #     scale_factor = ((scale - 0.51) * 2.0408163265306123)
    #     scale_factor = scale_factor * 0.5 + 0.5
    #     result = int(MAX_SIZE * self.size_factor() * scale_factor)
    #     return result

    # def _get_size_for_hard(self, scale):
    #     ''' Get size for the circles according to the user level. '''
    #     sizes = [MAX_SIZE] + [max(1, min(self._get_size(scale), MAX_SIZE - 1))
    #                           for _ in range(8)]
    #     return sizes


    def _get_test_sizes(self, scale):
        ''' Get size for the circles according to the user level. '''
        #sizes = [MAX_SIZE] + [max(1, min(self._get_size(scale), MAX_SIZE - 1))
                              #for _ in range(8)]
        sizes = [MAX_SIZE] + [int(max(1, min(1.5*scale*size, MAX_SIZE-1))) for size in self.size_pattern]                      

        return sizes

    def _get_control_sizes(self, scale, control):
        if control == 'easy':
            return [MAX_SIZE, MAX_SIZE-30, 50, 45, 40, 35, 30, 25, 20]
        elif control == 'hard':
            return [MAX_SIZE, MAX_SIZE-1, MAX_SIZE-1, MAX_SIZE-1, MAX_SIZE-2, MAX_SIZE-2, MAX_SIZE-3, MAX_SIZE-4, MAX_SIZE-6]

    def _get_sizes(self, scale, control):
        ''' Get circle sizes. '''
        if control is None:
            sizes = self._get_test_sizes(scale)
        elif control in ['easy', 'hard']:
            sizes = self._get_control_sizes(scale, control)#size_easy
        else:
            print 'Unknown control type, use easy/hard.'
            raise

        shuffle(sizes)
        return sizes

    def renew_circles(self, scale, control):
        """
        Resizes circles with the current trial circle sizes
        """
        self.scale = scale
        current_sizes = self._get_sizes(scale, control)
        for i in range(len(current_sizes)):
            self.circles[i].change_size(current_sizes[i])

    def __iter__(self):
        return CirclesIterator(self.circles)

    #def __next__(self):
    #    return None

class CirclesIterator(object):

    def __init__(self, circles):
        self.circles = circles
        self.current = 0

    # pylint: disable = C0112
    def next(self): #@ReservedAssignment
        # pylint: enable = C0112
        if self.current == len(self.circles):
            raise StopIteration
        else:
            self.current += 1
            return self.circles[self.current - 1]
