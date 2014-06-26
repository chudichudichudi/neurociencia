
import trial
import logging
import time
import threading
import configuration

class SliderTrial(trial.Trial):

    def __init__(self, logger, circles, control=None, slider=None, **kwargs):
        
        super(SliderTrial, self).__init__(logger, circles, control)
        if control is None:           
            self.trial_type='slider'
        else:
            self.trial_type='slider'+control
        self.slider = slider
        self.slider_suscription = slider.suscribe('touch', self._choose_slider)
        self.slider.hide()
        
        
        
    def _show_question(self):
        """ Show confidence question. """
        self.slider.show()
        self.logger.begin_time(self.current_trial, self.trial_type)
    
        
    
    def _choose_slider(self, ans):
        print 'lerolero'
        trial_info=self.save_trial(ans)
        self.slider.hide()
        self.slider_suscription.unsuscribe()
        def future():
            self.end_trial(trial_info)
        t = threading.Timer(configuration.TRIAL_INTERVAL, future)
        t.start()

        

    

    def _choose_circle(self, circle):
        """ Saves the circle choosed and shows the question. """
        self.logger.process_circle_choice(circle)
        self.circles.hide()
        self._show_question()
        
        
        
        
