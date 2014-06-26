


import trial
import logging
import configuration
import threading

class PlainTrial(trial.Trial):

    def __init__(self, logger, circles, control=None, **kwargs):
        
        super(PlainTrial, self).__init__(logger, circles, control)
        self.running=True
        if control is None:
            self.trial_type='plain'
        else:
            self.trial_type='plain'+control
       

            
    def _choose_circle(self, circle):
        """ Saves the circle choosed and shows the question. """
        self.logger.process_circle_choice(circle)
        self.circles.hide()
        trial_info=self.save_trial('Plain')
        def future():
            self.end_trial(trial_info)
        t = threading.Timer(configuration.TRIAL_INTERVAL, future)
        t.start()

        
