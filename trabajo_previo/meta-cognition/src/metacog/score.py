'''
Created on Jan 15, 2012

@author: mariano
'''
from sprite.score import ScoreSprite
#from metacog.configuration import POINTS_PER_PELLET

class Score(object):
    '''
    Models the Score of the game
    '''


    def __init__(self):
        '''
        Starts with 0 and creates a sprite
        '''
        self.score = 0
        self.sprite = ScoreSprite()


    def save_score(self, count):
        """ Save score and update view. """
        prev = self.score
        self.score = max(self.score + count, 0) #min(max(self.score + count, 0), POINTS_PER_PELLET)
        if prev != self.score:
            self.sprite.change_score(self.score)

    def restart(self, points=0):
        """ Restart current score to 0. """
        if self.score != points:
            self.sprite.change_score(points)
            self.score = points

