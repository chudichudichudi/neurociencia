
import trial
import logging
import time
import threading
import configuration

class WageTrial(trial.Trial):

    def __init__(self, logger, circles, control=None, buttons=None, score=None, **kwargs):
        
        super(WageTrial, self).__init__(logger, circles, control)
        if control is None:               
            self.trial_type='wage'
        else:
            self.trial_type='wage'+control
        self.buttons = buttons
        self.button_suscription={}
        for button in buttons:
            self.button_suscription[button]=button.suscribe('touch', self._choose_button)
        self.score = score
        self.hide_buttons()
        
        
        
    def _show_question(self):
        """ Show confidence question. """
        self.score.sprite.show()
        for button in self.buttons:
            button.show()
        self.logger.begin_time(self.current_trial, self.trial_type)    
    
        
    def hide_buttons(self):
        """ Hide buttons. """
        self.score.sprite.hide()
        for button in self.buttons:
            button.hide()

    def _choose_button(self, ans):
        trial_info=self.save_trial(ans)
        self.score.save_score(trial_info.score)
        for button in self.buttons:
            button.hide()
            self.button_suscription[button].unsuscribe()
        def future():
            self.score.sprite.hide()
            self.end_trial(trial_info)
        t = threading.Timer(configuration.SCORE_TIMEOUT, future)
        t.start() 

    

    def _choose_circle(self, circle):
        """ Saves the circle choosed and shows the question. """
        self.logger.process_circle_choice(circle)
        self.circles.hide()
        self._show_question()
        
        
        
        
