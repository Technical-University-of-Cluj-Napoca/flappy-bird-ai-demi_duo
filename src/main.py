import pygame
import sys
import random
from settings import *
from assets import load_assets

# Entities
from entities.bird import Bird
from entities.pipe_manager import PipeManager
from ai.population import Population

# --- SETUP ---
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird AI 2025")

# Setează iconița
assets = load_assets()
if 'icon' in assets:
    pygame.display.set_icon(assets['icon'])

clock = pygame.time.Clock()
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

# --- RECTS FOR UI ---
play_btn_rect = assets['button_play'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2 + 30))
title_rect = assets['label_flappy_bird'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2 - 50))
panel_rect = assets['panel_score'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2))
pause_btn_rect = assets['button_pause'].get_rect(topleft=(30, 30))
restart_btn_rect = assets['button_restart'].get_rect(topright=(pause_btn_rect.right + 230, 30))
# Butonul Classic (Stânga)
classic_btn_rect = assets['button_classic'].get_rect(center=(GAME_WIDTH/2 - 50, GAME_HEIGHT/2 + 90))
# Butonul AI (Dreapta)
ai_btn_rect = assets['button_ai'].get_rect(center=(GAME_WIDTH/2 + 50, GAME_HEIGHT/2 + 90))

# Imaginea de Tutorial (Get Ready)
message_rect = assets['message'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2.5))

# --- CONFIG ---
GAME_MODE = "MANUAL" 

# --- INSTANCES ---
bird = Bird(assets['bird_frames'], assets['sounds'])
population = Population(POPULATION_SIZE, assets)
pipe_manager = PipeManager(assets['pipe'])

# --- EVENTS ---
SPAWNPIPE = pygame.USEREVENT

# --- STATE VARIABLES ---
# States: "MENU", "GET_READY", "PLAYING", "GAMEOVER"
game_state = "MENU" 

score = 0
high_score = 0
floor_x_pos = 0
fade_alpha = 0
hit_sound_played = False
die_sound_played = False
is_play_btn_pressed = False

# --- UTILS ---
def draw_floor():
    game_surface.blit(assets['floor'], (floor_x_pos, 450)) 
    game_surface.blit(assets['floor'], (floor_x_pos + GAME_WIDTH, 450))

def display_score(val, x, y, sprite_dict):
    score_str = str(int(val))
    total_width = 0
    
    # Calculăm lățimea folosind imaginile din dicționarul primit
    for digit in score_str:
        total_width += sprite_dict[digit].get_width()

    current_x = x - (total_width / 2)
    for digit in score_str:
        img = sprite_dict[digit]
        game_surface.blit(img, (current_x, y))
        current_x += img.get_width()

def reset_game():
    global game_state, score, fade_alpha, hit_sound_played, die_sound_played
    
    # MODIFICARE: Trecem în GET_READY, nu direct în PLAYING
    game_state = "GET_READY"
    
    pipe_manager.clear()
    score = 0
    fade_alpha = 0
    hit_sound_played = False
    die_sound_played = False
    
    # Resetăm pasărea la poziția de start
    bird.reset()

    # Dacă e AI, îl resetăm
    if GAME_MODE == "AI":
        #population = Population(POPULATION_SIZE, assets)
        # AI-ul nu are nevoie de tutorial, poate începe direct
        game_state = "PLAYING"
        pipe_manager.spawn_pipe()
        pygame.time.set_timer(SPAWNPIPE, 1200)

def start_playing():
    """Funcție nouă care pornește efectiv jocul (țevile)"""
    global game_state
    game_state = "PLAYING"
    
    # Prima săritură
    if GAME_MODE == "MANUAL":
        bird.flap()
        
    # Pornim țevile
    pipe_manager.spawn_pipe()
    pygame.time.set_timer(SPAWNPIPE, 1200)

def draw_menu():
    game_surface.blit(assets['label_flappy_bird'], title_rect)
    game_surface.blit(assets['button_play'], play_btn_rect)

    # Butonul Play
    if is_play_btn_pressed:
        game_surface.blit(assets['button_play_pressed'], play_btn_rect)
    else:
        game_surface.blit(assets['button_play'], play_btn_rect)

    # --- DESENARE BUTOANE MOD ---
    
    # 1. Desenăm butonul CLASSIC
    # Dacă modul e MANUAL, e complet vizibil (255). Dacă nu, e transparent (100)
    alpha_classic = 255 if GAME_MODE == "MANUAL" else 100
    assets['button_classic'].set_alpha(alpha_classic)
    game_surface.blit(assets['button_classic'], classic_btn_rect)

    # 2. Desenăm butonul AI
    alpha_ai = 255 if GAME_MODE == "AI" else 100
    assets['button_ai'].set_alpha(alpha_ai)
    game_surface.blit(assets['button_ai'], ai_btn_rect)

def draw_get_ready():
    """Desenează ecranul de tutorial"""
    game_surface.blit(assets['message'], message_rect)

def draw_game_over_ui():
    game_surface.blit(assets['game_over'], assets['game_over'].get_rect(center=(GAME_WIDTH/2, GAME_HEIGHT/2 - 80)))
    game_surface.blit(assets['panel_score'], panel_rect)
    
    medal_img = None
    if score >= MEDAL_SCORES['platinum']: medal_img = assets['medals']['platinum']
    elif score >= MEDAL_SCORES['gold']: medal_img = assets['medals']['gold']
    elif score >= MEDAL_SCORES['silver']: medal_img = assets['medals']['silver']
    elif score >= MEDAL_SCORES['bronze']: medal_img = assets['medals']['bronze']
    
    if medal_img:
        medal_rect = medal_img.get_rect(center=(panel_rect.centerx - 32, panel_rect.centery + 5))
        game_surface.blit(medal_img, medal_rect)

    display_score(score, panel_rect.centerx + 36, panel_rect.centery - 10, assets['score_small_sprites'])
    display_score(high_score, panel_rect.centerx + 36, panel_rect.centery + 10, assets['score_small_sprites'])


# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Input Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            game_mouse_pos = (mouse_pos[0] / SCALE_FACTOR, mouse_pos[1] / SCALE_FACTOR)

            if game_state == "MENU":
                # 1. Play Button
                if play_btn_rect.collidepoint(game_mouse_pos):
                    is_play_btn_pressed = True
                    reset_game()
                
                # 2. Classic Mode Select
                if classic_btn_rect.collidepoint(game_mouse_pos):
                    GAME_MODE = "MANUAL"
                    print("Selected: MANUAL")
                
                # 3. AI Mode Select
                if ai_btn_rect.collidepoint(game_mouse_pos):
                    GAME_MODE = "AI"
                    print("Selected: AI")
            
            elif game_state == "GET_READY":
                # Orice click pornește jocul
                start_playing()

            elif game_state == "PLAYING":
                if pause_btn_rect.collidepoint(game_mouse_pos):
                    game_state = "PAUSED"

                if GAME_MODE == "MANUAL":
                    bird.flap()
            
            elif game_state == "PAUSED":
                # Dacă apăsăm oriunde (sau strict pe buton), reluăm jocul
                # De obicei e bine să fie strict pe butonul de Resume:
                if pause_btn_rect.collidepoint(game_mouse_pos):
                    game_state = "PLAYING"

                if restart_btn_rect.collidepoint(game_mouse_pos):
                    reset_game() # Te trimite înapoi la "Get Ready
                    game_state = "MENU"
            
            elif game_state == "GAMEOVER":
                game_state = "MENU"
                is_play_btn_pressed = False

        # Input Tastatură
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "MENU":
                    reset_game()
                elif game_state == "GET_READY":
                    start_playing()
                elif game_state == "PLAYING" and GAME_MODE == "MANUAL":
                    bird.flap()
                elif game_state == "GAMEOVER":
                    game_state = "MENU"
            
            if game_state == "MENU":
                if event.key == pygame.K_m:
                    GAME_MODE = "MANUAL"
                    print("Mode: MANUAL")
                elif event.key == pygame.K_a:
                    GAME_MODE = "AI"
                    print("Mode: AI")

        if event.type == SPAWNPIPE and game_state == "PLAYING":
            pipe_manager.spawn_pipe()
            next_time = random.randint(1000, 1500)
            pygame.time.set_timer(SPAWNPIPE, next_time)

    # --- DRAW & UPDATE ---
    
    # 1. Background
    game_surface.blit(assets['bg_day'], (0,0))
    
    target_is_night = (int(score) // 10) % 2 == 1
    if target_is_night and fade_alpha < 255: fade_alpha += 2
    elif not target_is_night and fade_alpha > 0: fade_alpha -= 2
    if fade_alpha > 0:
        assets['bg_night'].set_alpha(fade_alpha)
        game_surface.blit(assets['bg_night'], (0,0))

    # 2. Logică per State
    if game_state == "MENU":
        draw_floor() 
        floor_x_pos -= 1
        draw_menu()

    elif game_state == "GET_READY":
        draw_floor()
        floor_x_pos -= 1
        
        # Desenăm tutorialul
        draw_get_ready()

    elif game_state == "PLAYING":
        pipe_manager.update()
        pipe_manager.draw(game_surface)
        
        draw_floor()
        floor_x_pos -= 1

        if GAME_MODE == "MANUAL":
            bird.move()
            bird.animate()
            bird.draw(game_surface)
            
            if bird.check_collision(pipe_manager):
                game_state = "GAMEOVER"
                if not hit_sound_played:
                    assets['sounds']['hit'].play()
                    hit_sound_played = True
            
            for pipe in pipe_manager.pipes:
                if bird.rect.centerx > pipe.rect_bottom.centerx and not pipe.passed:
                    score += 1
                    pipe.passed = True
                    assets['sounds']['point'].play()

        elif GAME_MODE == "AI":
            alive_count = population.update(pipe_manager, game_surface)
            if alive_count == 0:
                population.natural_selection()
                reset_game() 
            
            if len(pipe_manager.pipes) > 0:
                if pipe_manager.pipes[0].rect_bottom.centerx < 50 and not pipe_manager.pipes[0].passed:
                    score += 1
                    pipe_manager.pipes[0].passed = True

        game_surface.blit(assets['button_pause'], pause_btn_rect)
        display_score(score, GAME_WIDTH/2, 50, assets['score_sprites'])

    elif game_state == "PAUSED":
        pipe_manager.draw(game_surface)
        draw_floor() # Nu scădem floor_x_pos, deci podeaua stă pe loc
        
        # 2. Pasărea (fără move() sau animate())
        if GAME_MODE == "MANUAL":
            bird.draw(game_surface)
        elif GAME_MODE == "AI":
            # Pentru AI trebuie să desenăm toată populația statică
            for b in population.birds:
                if b.alive: b.draw(game_surface)

        # 3. Scorul
        display_score(score, GAME_WIDTH/2, 50, assets['score_sprites'])

        # 4. Desenăm butonul de RESUME (imaginea >)
        # Folosim același rect, dar altă imagine
        game_surface.blit(assets['button_resume'], pause_btn_rect)

        game_surface.blit(assets['button_restart'], restart_btn_rect)

    elif game_state == "GAMEOVER":
        pipe_manager.draw(game_surface)
        draw_floor()
        
        if bird.rect.bottom < 450:
            bird.move()
            bird.draw(game_surface)
        else:
            rotated = pygame.transform.rotozoom(bird.image, -90, 1)
            game_surface.blit(rotated, bird.rect)
            if not die_sound_played:
                assets['sounds']['die'].play()
                die_sound_played = True
            
            draw_game_over_ui()
        
        if score > high_score:
            high_score = score

    if floor_x_pos <= -GAME_WIDTH:
        floor_x_pos = 0

    screen.blit(pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0,0))
    pygame.display.update()
    clock.tick(FPS)