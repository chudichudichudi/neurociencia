'''
Created on Mar 25, 2012

@author: mariano
'''

#TIMEOUTs
TRIAL_TIMEOUT = 10
SCORE_TIMEOUT = 0.5
TRIAL_INTERVAL = 0.5

#Maximo de niveles total
#MAX_PELLETS = 10

#Maximo de trials total
MAX_TRIALS = 150

#Puntos rojos para pasar nivel
#POINTS_PER_PELLET = 20

#Puntos iniciales al comenzar nivel
#POINTS_RESTART = 0

#Button positions"
BUTTON_POSITION = [(350, 600), (500, 600), (360, 620)]

#Circles sizes
MAX_SIZE = 100
SIZE_FOR_EASY = [int(MAX_SIZE * x) for x in [0.22, 0.3, 0.4,
                                        0.5, 0.54, 0.6,
                                        0.7, 0.74, 1.0]]

#Circles positions:
INITIAL_POINT = (200, 30)
OFFSET_X = [int(MAX_SIZE * x) for x in [0.5, 0.7, 1]]
OFFSET_Y = [int(x * 0.8) for x in OFFSET_X]

#Image resources
#MEDIA = '/home/mate/teaching-brain/multi-game/meta-cognition/media/'
MEDIA = '/home/chudi/trabajo/neuro/metacognition/trabajo_previo/meta-cognition/media/'

#GREEN_TICK_FILE = MEDIA + "green-tick.png"
#RED_CROSS_FILE = MEDIA + "red-cross.png"
HIGH_CONFIDENCE_FILE = MEDIA + "yellow_box.png"
LOW_CONFIDENCE_FILE = MEDIA + "purple_box.png"
SCORE_CONTAINER_FILE = MEDIA + 'score_container.png'
CONGRATS_PICTURE = MEDIA + 'congrats.jpg'
SLIDER_FILE = MEDIA + 'slider2.png'

#Tuio configuration
TUIO_ENABLE = False

#Game Configuration
FULLSCREEN = True

#Trial Types
#TRIAL_TYPES = ['plain', 'wage', 'plain', 'wage']
TRIAL_TYPES = ['wage', 'plain', 'wage']
#TRIAL_TYPES = ['plain', 'plain']
TRIAL_TYPES = ['wage', 'wage']


#Trial Amount
N_TRIALS = len(TRIAL_TYPES)

