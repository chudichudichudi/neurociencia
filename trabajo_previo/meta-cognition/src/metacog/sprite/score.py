'''
Created on Jan 15, 2012

@author: mariano
'''
from multineuro.sprite import ImgSprite
import pygame
from metacog.utilities.score_utilities import ScoreSpriteUtility
from metacog.configuration import SCORE_CONTAINER_FILE #, POINTS_PER_PELLET

class ScoreSprite(ImgSprite):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(ScoreSprite, self).__init__(SCORE_CONTAINER_FILE)
        helper = ScoreSpriteUtility()
        self.available_positions = helper.generate_initial_positions()
        for x in range(len(self.available_positions)):
            self.current_position = x
            self._draw_circle((150, 150, 150))
        self.current_position = 0


    def _draw_circle(self, color):
        """ Draws a circle of the given color in the current position. """
        print self.current_position, self.available_positions[self.current_position]
        pygame.draw.circle(self.image, color,
                           self.available_positions[self.current_position],
                           10)

    def change_score(self, score):
        """ Given a score, this updates the score shown. """
        assert score != self.current_position
        diff = score - self.current_position
        color = (255, 0, 0)
        if diff < 0:
            color = (150, 150, 150)


        i = 0
        while i < abs(diff): # and self.current_position < POINTS_PER_PELLET:
            self._draw_circle(color)
            self.current_position += diff / abs(diff)
            i += 1

        #self.current_position = min(self.current_position, POINTS_PER_PELLET - 1)
        if diff < 0:
            self._draw_circle(color)

        self.dirty = 1




