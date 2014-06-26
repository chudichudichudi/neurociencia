'''
Created on Apr 2, 2012

@author: mariano
'''
#from metacog.configuration import POINTS_PER_PELLET

class ScoreSpriteUtility(object):
    '''
    Function to generate every Score position
    '''


    def __init__(self):
        '''
        Builds the utility
        '''
        #self.offset = 0
        #self.max_column = 3

        self.column_number = 6
        self.row_number = 23
        self.max_points = self.column_number*self.row_number

        self.initial_position = (66, 700)

        self.current_column = 0
        self.current_row = 0

    def _calc_position(self):
        #initial_position = (66, 660)
        column = self.initial_position[0] + 24 * self.current_column #+ self.offset
        row = self.initial_position[1] - 30 * self.current_row
        return  column, row

    def generate_initial_positions(self):
        """ Creates every posible position for the score. """
        initial_positions = []
        #for _ in range(POINTS_PER_PELLET):
        for _ in range(self.max_points):
            initial_positions.append(self._generate_next_position())
        return initial_positions



    def _update_next_position(self):
        self.current_column += 1
        if self.current_column >= self.column_number:
            self.current_column = 0
            self.current_row += 1
        
            # if self.max_column == 2:
            #     self.max_column = 1
            #     self.offset = 13
            # else:
            #     self.max_column = 2
            #     self.offset = 0

    def _generate_next_position(self):
        result = self._calc_position()
        self._update_next_position()
        return result
