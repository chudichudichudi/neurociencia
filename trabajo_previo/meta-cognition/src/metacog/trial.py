from multineuro.sprite.textsprite import TextSprite
import logging

class Trial(object):

    def __init__(self, logger, circles, control=None):
        self.logger = logger
        self.circles = circles
        self.suscription=dict()
        for circle in circles:
            self.suscription[circle]=circle.suscribe('touch', self._choose_circle)
        #if control in ['easy', 'hard']:
        self.control=control


        #self.splash = TextSprite('', self.show_circles)
        
        
        
    def run(self, scale, current_trial, trial_ended):
        self.current_trial = current_trial
        #self.hard = hard
        self.scale = scale
        #self.splash.show()
        self.show_circles()
        self.trial_ended = trial_ended

    def save_trial(self, ans):
        self.logger.process_answer(ans)
        logging.debug('Saving Trial.')
        trial_info = self.logger.save_trial(self.circles)
        logging.debug('Saved.')
        return trial_info

    def show_circles(self):
        self.circles.renew_circles(self.scale, self.control)
        self.logger.begin_time(self.current_trial, self.trial_type)
        self.circles.show()
        print "waiting here"

    #~ def _choose_circle(self, circle):
        #~ """ Saves the circle choosed and shows the question. """
        #~ self.logger.process_circle_choice(circle)
        #~ self.circles.hide()
        #~ self._show_question()

    def end_trial(self, trial_info):
        for circle in self.circles:
            self.suscription[circle].unsuscribe()
        self.trial_ended(trial_info)
            
        
        
