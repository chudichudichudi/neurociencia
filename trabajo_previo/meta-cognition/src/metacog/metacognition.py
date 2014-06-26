'''
Created on Jan 4, 2012

@author: mariano
'''
from configuration import SIZE_FOR_EASY, BUTTON_POSITION, INITIAL_POINT, OFFSET_X, OFFSET_Y
from logger import Logger
import logging
from metacog.configuration import FULLSCREEN, \
    HIGH_CONFIDENCE_FILE, LOW_CONFIDENCE_FILE, \
    TUIO_ENABLE, TRIAL_TIMEOUT, MAX_TRIALS, CONGRATS_PICTURE, SLIDER_FILE
    #GREEN_TICK_FILE, RED_CROSS_FILE, 
    #MAX_PELLETS, 
    #POINTS_PER_PELLET, POINTS_RESTART, 
    #TRIAL_TYPES, N_TRIALS
from multineuro import game
from multineuro.sprite import ButtonSprite
from multineuro.sprite.button import Button
from psychopy import data
from score import Score
from sprite.circles import Circles
from sprite.slider import Slider
from metacog.trial import Trial
from metacog.wage_trial import WageTrial
from metacog.slider_trial import SliderTrial
from metacog.plain_trial import PlainTrial
from multineuro.forms.forms import Form
from multineuro.forms.input import Input
import sys
import pygame
import time
import random

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')


class Metacognition(game.Game):
    ''' A '''


    def _initialize(self):
        self.logger = Logger()
        self.pellets = 0
        self._initialize_circles()
        self._initialize_buttons()
        self._initialize_score()
        self._initialize_quest()
        self.initialize_form()
        self.initialize_trials()


    def start_experiment(self):
        logging.debug('Start Experiment') #Start measuring
        self.logger.start(self.log_file) #Restart trial count and mark beginning
        self.current_trial = 0
        #~ self.trial = WageTrial(self.logger, self.circles, [self.button_not_know, self.button_know])
        #self.add_active_sprite(self.trial.splash)
        self._start_trial()


    def process_form(self, form_result):
        self.log_file = form_result['Name'] + '.meta'
        self.start_experiment()#trials()

    def initialize_trials(self):
        
        real_trial_types=40*['wage']+40*['slider']+20*['plain']
        random.shuffle(real_trial_types)
        #self.trial_types=real_trial_types
        self.trial_types=['wage_easy']+['slider_easy']+\
                        real_trial_types[:5]+['wage_easy']+\
                        real_trial_types[5:15]+['slider_easy']+\
                        real_trial_types[15:25]+['wage_hard']+\
                        real_trial_types[25:35]+['slider_hard']+\
                        real_trial_types[35:45]+['wage_easy']+\
                        real_trial_types[45:55]+['slider_easy']+\
                        real_trial_types[55:65]+['wage_hard']+\
                        real_trial_types[65:75]+['slider_hard']+\
                        real_trial_types[75:85]+['wage_easy']+\
                        real_trial_types[85:95]+['slider_easy']+\
                        real_trial_types[95:105]+['wage_hard']+\
                        real_trial_types[105:115]+['slider_hard']
        
        print self.trial_types
        test=True
        test=False
        if test:
            self.trial_types=['wage', 'wage']
            self.trial_types=['plain', 'slider', 'wage', 'plain', 'plain']
            self.trial_types=['wage', 'wage', 'wage', 'wage', 'wage', 'wage', 'wage', 'wage', 'wage', 'wage',]
            
        
        self.number_of_trials = len(self.trial_types)
        

    def initialize_form(self):
        form = Form(True)
        form.add_object('Name', Input('Nombre', '',
                                      label_size=18,
                                      input_border_color=(255, 100, 100),
                                      input_border_width=0,
                                      input_bg_color=(0, 0, 0, 0)))
        self.registerForm(form, self.process_form)

    def __init__(self):
        logging.log(logging.DEBUG, 'Welcome to Metacog')
        super(Metacognition, self).__init__("Metacognition",
                                            fullscreen=FULLSCREEN,
                                            tuio=TUIO_ENABLE)
        self.trial_types_const = {
            'wage': WageTrial,
            'plain': PlainTrial,
            'slider': SliderTrial
        }
        self._initialize()
        

    def _initialize_circles(self):
        """ Initialize and register circles. """
        self.circles = Circles(INITIAL_POINT, OFFSET_X, OFFSET_Y, SIZE_FOR_EASY)
        for circle in self.circles:
            self.add_active_sprite(circle)
            #circle.suscribe('touch', self._choose_circle)
            circle.hide()


    def _initialize_quest(self):
        """ Initialize Staircase handler used to choose hard level. """
        self.quest = data.QuestHandler(startVal=0.5, #0.12,
                                       startValSd=.2,
                                       pThreshold=0.6,
                                       gamma=0.5,
                                       grain=0.005,
                                       nTrials=MAX_TRIALS,
                                       minVal=0,
                                       maxVal=1, #0.49,
                                       stepType='lin')

    def _initialize_score(self):
        """ Initialize and register the score. """
        self.score = Score()
        self.add_background_sprite(self.score.sprite)
        self.score.sprite.hide()

    def _initialize_buttons(self):
        """ Initialize and register the butttons. """
        self.button_know = Button(BUTTON_POSITION[0],
                                  #self.end_trial,#self._process_trial,
                                  resource=HIGH_CONFIDENCE_FILE,
                                  val=True
                                  )
        self.button_not_know = Button(BUTTON_POSITION[1],
                                      #self.end_trial,#self._process_trial,
                                      resource=LOW_CONFIDENCE_FILE,
                                      val=False)
        self.slider = Slider(BUTTON_POSITION[2], resource=SLIDER_FILE)
        #self.finnish_button = ButtonSprite('bottom-left')
        #self.finnish_button.suscribe('pressed', lambda _ : self._show_prize())
        self.congrats = Button((0, 0), lambda _:self.callback(), CONGRATS_PICTURE)
        self.congrats.center()
        self.add_active_sprite(self.button_know)
        self.add_active_sprite(self.button_not_know)
        self.add_active_sprite(self.slider)
        #self.add_active_sprite(self.finnish_button)
        self.add_active_sprite(self.congrats)
        self.congrats.hide()
        self.button_know.hide()
        self.button_not_know.hide()
        self.slider.hide()
        
 


    def _start_trial(self):
        
        current_trial_type = str.split(self.trial_types[self.current_trial], '_')
        current_trial_class = current_trial_type[0]
        self.current_trial_control = None
        if len(current_trial_type) > 1:
            self.current_trial_control = current_trial_type[1]

        #print ['Start with '] + current_trial_type
        #print self.current_trial
        args = {
            'buttons': [self.button_not_know, self.button_know],
            'slider': self.slider,
            'score': self.score,
            'control': self.current_trial_control
        }
        trial = self.trial_types_const[current_trial_class](self.logger, self.circles, **args)
             
        quest = self.quest.next()
        scale = 1 - quest
        
        trial.run(scale, self.current_trial+1, self.end_trial)
        
        


    def end_trial(self, trial_information):
        #print 'Ending with ' + self.current_trial_type
        #self.score.save_score(trial_information.score)
        self._update_quest(trial_information.correct
                            and trial_information.circle_time < TRIAL_TIMEOUT)
                            
        if self.current_trial == self.number_of_trials-1: #N_TRIALS-1:
            self.do_callback = self.game_over
            self.congrats.show()
        else:
            self.current_trial += 1
            self._start_trial()
            
      

    def _update_quest(self, success):
        if self.current_trial_control is None:
            self.quest.addData(success)

    def _show_prize(self):
        """ Hides everything and shows only the score. """
        puntaje = 'Estas en el nivel  ' + str(self.pellets + 1) + '.'
        self.do_callback = self.next_trial
        if self.pellets >= MAX_PELLETS or self.current_trial >= MAX_TRIALS:
        #if self.current_trial == N_TRIALS-1:
            self.do_callback = self._show_final_score
        self.score.sprite.hide()
        self.congrats.show()
        self.show_message(puntaje, callback=lambda : None)

    def callback(self):
        self.do_callback()

    def _show_final_score(self):
        self.show_message('Estas en el nivel ' + str(self.pellets + 1) + '.', callback=self.game_over)

    def game_over(self):
        self.logger.dump_answers()
        super(Metacognition, self).game_over()

    def close(self):
        self.logger.dump_answers()
        super(self.__class__, self).close()

def main():
    """ Metacognition Game"""
    exp = None
    error = False
    try:
        exp = Metacognition()
        exp.start()
    except Exception as e:
        print e
        error = True
        raise
    finally:
        game.Game.kill()


if __name__ == '__main__':
    main()
    sys.exit(0)
