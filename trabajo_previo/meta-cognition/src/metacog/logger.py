'''
Created on Jan 10, 2012

@author: mariano
'''

import time
import logging

class Logger(object):
    '''
    Class that saves the answers
    '''


    def __init__(self):
        self.active = False
        self.time = 0

    def start(self, filename):
        logging.debug("Start to measure.")
        self.active = True
        tstamp = str(int(time.time()))
        self.file = open(tstamp + ' - ' + filename + '.out', 'wr')
        columns = ['trial_num', 'trial_type', 'circle_rt', 'circle_correct', 'circle_number',
                   'confidence', 'confidence_rt', 'scale', 'c1', 'c2', 'c3', 'c4', 'c5',
                   'c6', 'c7', 'c8', 'c9']
        header = "#%s\n" % '\t'.join(columns)
        self.file.write(header)

    def begin_time(self, current_trial, trial_type):
        self.current_trial = current_trial
        self.trial_type = trial_type
        self.time = time.time()

    def process_answer(self, ans):
        self.answer_time = time.time() - self.time
        self.current_answer = ans

    def process_circle_choice(self, circle):
        if self.time is None:
            logging.warn("Self time is None for trial %d!!!!", self.current_trial)
            self.time = 0
        self.circle_time = time.time() - self.time
        self.current_circle = circle


    def __persist_trial(self, trial):
        if self.active:
            self.file.write(str(trial) + '\n')
            self.file.flush()

    def save_trial(self, circles):
        trial = TrialRecord(trial_num=self.current_trial,
                      trial_type=self.trial_type,
                      circle=self.current_circle,
                      circle_time=self.circle_time,
                      circles=circles,
                      answer=self.current_answer,
                      answer_time=self.answer_time)
        self.__persist_trial(trial)
        return trial

    def dump_answers(self):
        self.file.close()


class TrialRecord(object):

    def __init__(self, trial_num, trial_type, circles, circle_time, circle,
                 answer, answer_time):
        self.trial_num = trial_num
        self.trial_type = trial_type
        self.answer = answer
        self.answer_time = answer_time
        self.circle_time = circle_time
        self.circles_size = [c.size for c in circles]
        self.quest = 1 - circles.scale
        self.position = circle.position
        self.correct = circle.is_correct()

    def get_score(self):
        """
        Return score according to the answer.
        """
        score = 1
        if self.answer:
            score = 3
            if not self.correct:
                score *= -1
        return score

    score = property(get_score)

    def __str__(self):
        to_persist = [self.trial_num,
                      self.trial_type,
                      self.circle_time,
                      self.correct,
                      self.position,
                      self.answer,
                      self.answer_time,
                      self.quest
                      ]
        assert all([x is not None for x in to_persist])
        res = '\t'.join([str(x) for x in to_persist])
        res += '\t' + ' '.join([str(x) for x in self.circles_size])
        return res

