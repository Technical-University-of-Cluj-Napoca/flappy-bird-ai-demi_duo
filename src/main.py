import pygame
import sys
from settings import *
from assets import load_assets

# Importuri din noul pachet entities
from entities.bird import Bird
from entities.pipe_manager import PipeManager

# --- SETUP ---
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird AI Structure")
clock = pygame.time.Clock()
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# --- ASSETS ---
assets = load_assets()

# --- INSTANCES ---
bird = Bird(assets['bird_frames'], assets['sounds'])
pipe_manager = PipeManager(assets['pipe'])

# --- EVENTS ---
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, PIPE_SPAWN_TIME)

# --- VARS ---
game_active = False
score = 0
high_score = 0
floor_x_pos = 0
fade_alpha = 0
hit_sound_played = False
die_sound_played = False

# --- UTILS ---
def draw_floor():
    game_surface.blit(assets['floor'], (floor_x_pos, 450)) 
    game_surface.blit(assets['floor'], (floor_x_pos + GAME_WIDTH, 450))

def display_score(val, x, y):
    score_str = str(int(val))
    total_width = sum([assets['score_sprites'][digit].get_width() for digit in score_str])
    current_x = x - (total_width / 2)
    for digit in score_str:
        game_surface.blit(assets['score_sprites'][digit], (current_x, y))
        current_x += assets['score_sprites'][digit].get_width()

# --- LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            triggered = (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN)
            if triggered:
                if game_active:
                    bird.flap()
                else:
                    game_active = True
                    assets['sounds']['swoosh'].play()
                    pipe_manager.clear()
                    bird.reset()
                    score = 0
                    fade_alpha = 0
                    hit_sound_played = False
                    die_sound_played = False

        if event.type == SPAWNPIPE and game_active:
            pipe_manager.spawn_pipe()

    # --- DRAW & UPDATE ---
    game_surface.blit(assets['bg_day'], (0,0))
    
    # Day/Night
    target_is_night = (int(score) // 10) % 2 == 1
    if target_is_night and fade_alpha < 255: fade_alpha += FADE_SPEED
    elif not target_is_night and fade_alpha > 0: fade_alpha -= FADE_SPEED
    
    if fade_alpha > 0:
        assets['bg_night'].set_alpha(fade_alpha)
        game_surface.blit(assets['bg_night'], (0,0))

    if game_active:
        bird.move()
        bird.animate()
        bird.draw(game_surface)

        pipe_manager.update()
        pipe_manager.draw(game_surface)

        # Collision (pasăm pipe_manager întreg pentru a accesa lista de țevi)
        if bird.check_collision(pipe_manager):
            game_active = False
            if not hit_sound_played:
                assets['sounds']['hit'].play()
                hit_sound_played = True

        # Score Logic (mult mai curat acum)
        for pipe in pipe_manager.pipes:
            # Verificăm dacă centrul păsării a trecut de centrul țevii
            if bird.rect.centerx > pipe.rect_bottom.centerx and not pipe.passed:
                score += 1
                pipe.passed = True # Marcăm țeava ca "trecută"
                assets['sounds']['point'].play()
        
        display_score(score, GAME_WIDTH/2, 50)

    else:
        if score > high_score: high_score = score
        
        if bird.rect.bottom < 450:
            bird.move()
            bird.draw(game_surface)
        else:
            rotated = pygame.transform.rotozoom(bird.image, -90, 1)
            game_surface.blit(rotated, bird.rect)
            if not die_sound_played:
                assets['sounds']['die'].play()
                die_sound_played = True

        if score == 0 and bird.rect.centery == GAME_HEIGHT/2:
             game_surface.blit(assets['message'], assets['message'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2)))
        else:
             game_surface.blit(assets['game_over'], assets['game_over'].get_rect(center=(GAME_WIDTH/2, 200)))
             display_score(score, GAME_WIDTH/2, 260)

    floor_x_pos -= 1
    if floor_x_pos <= -GAME_WIDTH: floor_x_pos = 0
    draw_floor()

    screen.blit(pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0,0))
    pygame.display.update()
    clock.tick(FPS)