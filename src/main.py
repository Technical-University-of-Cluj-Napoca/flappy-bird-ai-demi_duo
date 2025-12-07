import pygame
import sys
from settings import *
from assets import load_assets
import random

# Entities
from entities.bird import Bird
from entities.pipe_manager import PipeManager

# AI
from ai.population import Population

# --- SETUP ---
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird - Manual & AI")
clock = pygame.time.Clock()
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# --- ASSETS ---
assets = load_assets()

# --- CONFIG ---
# Change this to "MANUAL" or "AI" to switch modes
GAME_MODE = "MANUAL" 
# GAME_MODE = "AI"

# --- INSTANCES ---
# We initialize BOTH so we can switch if we want
bird = Bird(assets['bird_frames'], assets['sounds'])
population = Population(POPULATION_SIZE, assets)
pipe_manager = PipeManager(assets['pipe'])

# --- EVENTS ---
SPAWNPIPE = pygame.USEREVENT
#pygame.time.set_timer(SPAWNPIPE, PIPE_SPAWN_TIME)

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

def reset_game():
    """Helper function to reset the game state."""
    global game_active, score, fade_alpha, hit_sound_played, die_sound_played
    game_active = True
    pipe_manager.clear()
    score = 0
    fade_alpha = 0
    hit_sound_played = False
    die_sound_played = False
    
    # --- FIX START ---
    # 1. Spawn a pipe IMMEDIATELY so the AI has inputs ($i_0, i_1, i_2$)
    pipe_manager.spawn_pipe()
    
    # 2. Schedule the SECOND pipe to appear after a random delay
    next_spawn_time = random.randint(1400, 2000) # Slightly longer delay for the second pipe
    pygame.time.set_timer(SPAWNPIPE, next_spawn_time) 
    # --- FIX END ---
    
    # Reset specific entities based on mode
    if GAME_MODE == "MANUAL":
        bird.reset()
        assets['sounds']['swoosh'].play()
    elif GAME_MODE == "AI":
        global population
        population = Population(POPULATION_SIZE, assets)

# --- LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- INPUT HANDLING ---
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Allow mode switching if game is NOT active (on menu screen)
            if not game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    GAME_MODE = "MANUAL"
                    print("Switched to MANUAL mode")
                elif event.key == pygame.K_a:
                    GAME_MODE = "AI"
                    print("Switched to AI mode")

            # Handle Gameplay Input
            triggered = (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN)
            
            if triggered:
                if game_active:
                    # Only flap if we are in Manual Mode
                    if GAME_MODE == "MANUAL":
                        bird.flap()
                else:
                    # Start the game (works for both modes)
                    reset_game()

        if event.type == SPAWNPIPE and game_active:
            pipe_manager.spawn_pipe()
            next_spawn_time = random.randint(800, 1300)
            pygame.time.set_timer(SPAWNPIPE, next_spawn_time)

    # --- DRAW & UPDATE ---
    game_surface.blit(assets['bg_day'], (0,0))
    
    # Day/Night Cycle
    target_is_night = (int(score) // 10) % 2 == 1
    if target_is_night and fade_alpha < 255: fade_alpha += FADE_SPEED
    elif not target_is_night and fade_alpha > 0: fade_alpha -= FADE_SPEED
    
    if fade_alpha > 0:
        assets['bg_night'].set_alpha(fade_alpha)
        game_surface.blit(assets['bg_night'], (0,0))

    if game_active:
        pipe_manager.update()
        pipe_manager.draw(game_surface)

        # --- MODE SPECIFIC UPDATES ---
        if GAME_MODE == "MANUAL":
            # 1. Update Single Bird
            bird.move()
            bird.animate()
            bird.draw(game_surface)

            # 2. Check Collision
            if bird.check_collision(pipe_manager):
                game_active = False
                if not hit_sound_played:
                    assets['sounds']['hit'].play()
                    hit_sound_played = True

            # 3. Score Logic (Manual)
            for pipe in pipe_manager.pipes:
                if bird.rect.centerx > pipe.rect_bottom.centerx and not pipe.passed:
                    score += 1
                    pipe.passed = True
                    assets['sounds']['point'].play()

        elif GAME_MODE == "AI":
            # 1. Update Population
            alive_count = population.update(pipe_manager, game_surface)
            
            # 2. Check Extinction
            if alive_count == 0:
                # All birds died - Restart immediately or go to next gen
                # For now (Random AI), just reset the game loop
                reset_game()

            # 3. Score Logic (AI)
            # In AI mode, score is usually generation count or max fitness
            # But we can try to track score based on the 'best' bird alive
            # (Simplification: just increment score if any bird passes a pipe)
            # Note: This is purely visual for AI
            if len(pipe_manager.pipes) > 0:
                first_pipe = pipe_manager.pipes[0]
                # If pipe passed screen center (roughly) and hasn't been marked
                if first_pipe.rect_bottom.centerx < 50 and not first_pipe.passed:
                     score += 1
                     first_pipe.passed = True

        display_score(score, GAME_WIDTH/2, 50)

    else:
        # --- GAME OVER SCREEN ---
        if score > high_score: high_score = score
        
        # Draw the "falling" animation only for Manual bird
        if GAME_MODE == "MANUAL":
            if bird.rect.bottom < 450:
                bird.move()
                bird.draw(game_surface)
            else:
                rotated = pygame.transform.rotozoom(bird.image, -90, 1)
                game_surface.blit(rotated, bird.rect)
                if not die_sound_played:
                    assets['sounds']['die'].play()
                    die_sound_played = True

        # Draw UI
        if score == 0 and not game_active:
             # Start Screen
             game_surface.blit(assets['message'], assets['message'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2)))
             # Optional: Draw Mode Indicator
             # You could add text here saying "Mode: MANUAL (Press A for AI)"
        else:
             # Game Over Screen
             game_surface.blit(assets['game_over'], assets['game_over'].get_rect(center=(GAME_WIDTH/2, 200)))
             display_score(score, GAME_WIDTH/2, 260)

    floor_x_pos -= 1
    if floor_x_pos <= -GAME_WIDTH: floor_x_pos = 0
    draw_floor()

    screen.blit(pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0,0))
    pygame.display.update()
    clock.tick(FPS)