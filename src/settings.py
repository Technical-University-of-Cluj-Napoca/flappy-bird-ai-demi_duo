# settings.py

# Screen Configurations
SCALE_FACTOR = 2
GAME_WIDTH = 288
GAME_HEIGHT = 512
WINDOW_WIDTH = int(GAME_WIDTH * SCALE_FACTOR)
WINDOW_HEIGHT = int(GAME_HEIGHT * SCALE_FACTOR)
FPS = 120

# Bird Physics
GRAVITY = 0.12
FLAP_STRENGTH = -3.5
ROTATION_SPEED = 2

# Pipe Configurations
PIPE_MOVE_SPEED = 2
PIPE_SPAWN_TIME = 1000 # miliseconds
PIPE_HEIGHTS = [200, 300, 400]

FADE_SPEED = 2

# AI
THRESHOLD_FLAP = 0.5
POPULATION_SIZE = 50

# Medal thresholds
MEDAL_SCORES = {
    'bronze': 10,
    'silver': 20,
    'gold': 30,
    'platinum': 40
}

# Bird Coordinates
BIRD_START_X = 50
BIRD_START_Y = GAME_HEIGHT / 2