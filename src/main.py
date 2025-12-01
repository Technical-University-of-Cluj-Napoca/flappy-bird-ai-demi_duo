import pygame
import sys
import random

# --- CONFIGURATION ---
SCALE_FACTOR = 2
GAME_WIDTH = 288
GAME_HEIGHT = 512
WINDOW_WIDTH = int(GAME_WIDTH * SCALE_FACTOR)
WINDOW_HEIGHT = int(GAME_HEIGHT * SCALE_FACTOR)
FPS = 120

# --- GLOBAL VARIABLES ---
gravity = 0.12
bird_movement = 0
flap_strength = -3.5
pipe_move_speed = 2
score = 0
high_score = 0
game_active = False

# --- FADE VARIABLES ---
fade_alpha = 0
FADE_SPEED = 2

# --- INITIAL SETUP ---
pygame.init()
# Initialize the mixer for audio
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird AI 2025")
clock = pygame.time.Clock()
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# --- LOAD ASSETS ---
# 1. Backgrounds
bg_day = pygame.image.load('assets/sprites/background-day.png').convert()
bg_night = pygame.image.load('assets/sprites/background-night.png').convert()

# 2. Floor
floor_surface = pygame.image.load('assets/sprites/base.png').convert()

# 3. Bird Animation
bird_downflap = pygame.image.load('assets/sprites/bluebird/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/sprites/bluebird/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, GAME_HEIGHT/2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# 4. Pipes
pipe_surface = pygame.image.load('assets/sprites/pipe-green.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [200, 300, 400]

# 5. UI Elements
game_over_surface = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(GAME_WIDTH/2, 200))

message_surface = pygame.image.load('assets/sprites/message.png').convert_alpha()
message_rect = message_surface.get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2))

# 6. Score Sprites
score_sprites = {}
for i in range(10):
    score_sprites[str(i)] = pygame.image.load(f'assets/sprites/digits/{i}.png').convert_alpha()

# 7. AUDIO LOADING
flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')
point_sound = pygame.mixer.Sound('assets/audio/point.wav')
die_sound = pygame.mixer.Sound('assets/audio/die.wav')
swoosh_sound = pygame.mixer.Sound('assets/audio/swoosh.wav')

floor_x_pos = 0

# Audio Flags
hit_sound_played = False 
die_sound_played = False
die_sound_timer = 0 # Counter to delay the die sound

# --- FUNCTIONS ---

def draw_floor():
    game_surface.blit(floor_surface, (floor_x_pos, 450)) 
    game_surface.blit(floor_surface, (floor_x_pos + GAME_WIDTH, 450))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (GAME_WIDTH + 50, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (GAME_WIDTH + 50, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_move_speed
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= GAME_HEIGHT:
            game_surface.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            game_surface.blit(flip_pipe, pipe)

def check_collision(pipes):
    global hit_sound_played
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            if not hit_sound_played:
                hit_sound.play()
                hit_sound_played = True
            return False
            
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        if not hit_sound_played:
            hit_sound.play()
            hit_sound_played = True
        return False
        
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def display_score_sprites(score_value, center_x, center_y):
    score_str = str(int(score_value))
    total_width = 0
    for digit in score_str:
        total_width += score_sprites[digit].get_width()
    start_x = center_x - (total_width / 2)
    current_x = start_x
    for digit in score_str:
        image = score_sprites[digit]
        rect = image.get_rect(topleft = (current_x, center_y))
        game_surface.blit(image, rect)
        current_x += image.get_width()

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = flap_strength
                    flap_sound.play()
                else:
                    game_active = True
                    swoosh_sound.play()
                    pipe_list.clear()
                    bird_rect.center = (50, GAME_HEIGHT/2)
                    bird_movement = 0
                    score = 0
                    fade_alpha = 0 
                    hit_sound_played = False
                    die_sound_played = False
                    die_sound_timer = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                bird_movement = flap_strength
                flap_sound.play()
            else:
                game_active = True
                swoosh_sound.play()
                pipe_list.clear()
                bird_rect.center = (50, GAME_HEIGHT/2)
                bird_movement = 0
                score = 0
                fade_alpha = 0
                hit_sound_played = False
                die_sound_played = False
                die_sound_timer = 0
        
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # --- DRAWING PHASE ---
    
    # Day/Night Cycle
    target_is_night = (int(score) // 10) % 2 == 1
    if target_is_night:
        if fade_alpha < 255:
            fade_alpha += FADE_SPEED
            if fade_alpha > 255: fade_alpha = 255
    else:
        if fade_alpha > 0:
            fade_alpha -= FADE_SPEED
            if fade_alpha < 0: fade_alpha = 0
    
    game_surface.blit(bg_day, (0,0))
    if fade_alpha > 0:
        bg_night.set_alpha(fade_alpha)
        game_surface.blit(bg_night, (0,0))

    if game_active:
        # Physics
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        game_surface.blit(rotated_bird, bird_rect)
        
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score Logic
        for pipe in pipe_list:
            if 50 - pipe_move_speed < pipe.centerx <= 50:
                score += 0.5 
                if score % 1 == 0.5: 
                    point_sound.play()

        display_score_sprites(score, GAME_WIDTH/2, 50)
    
    else:
        # GAME OVER LOGIC
        if score > high_score:
            high_score = score
        
        # Display Game Over & Score
        if score == 0 and bird_rect.centery == GAME_HEIGHT/2:
            game_surface.blit(message_surface, message_rect)
        else:
            game_surface.blit(game_over_surface, game_over_rect)
            display_score_sprites(score, GAME_WIDTH/2, 260) 
            
            # --- DIE SOUND LOGIC ---
            # We increment a timer every frame after death
            if not die_sound_played:
                die_sound_timer += 1
                # Play sound if ~20 frames passed OR if we hit ground immediately
                if die_sound_timer > 4 or bird_rect.bottom >= 450:
                    die_sound.play()
                    die_sound_played = True

            # Fall physics for Game Over
            if bird_rect.bottom < 450:
                bird_movement += gravity
                bird_rect.centery += bird_movement
                rotated_bird = rotate_bird(bird_surface)
                game_surface.blit(rotated_bird, bird_rect)
            else:
                 # Bird is dead on ground
                 rotated_bird = pygame.transform.rotozoom(bird_surface, -90, 1)
                 game_surface.blit(rotated_bird, bird_rect)

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -GAME_WIDTH:
        floor_x_pos = 0

    scaled_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0,0))

    pygame.display.update()
    clock.tick(FPS)