import pygame
import os

def load_assets():
    """
    Încarcă toate imaginile și sunetele și le returnează într-un dicționar structurat.
    """
    assets = {}

    # --- ICON ---
    assets['icon'] = pygame.image.load('assets/sprites/ui/icon.png')

    # --- IMAGINI ---
    # Backgrounds
    assets['bg_day'] = pygame.image.load('assets/sprites/environment/background-day.png').convert()
    assets['bg_night'] = pygame.image.load('assets/sprites/environment/background-night.png').convert()
    
    # Floor
    assets['floor'] = pygame.image.load('assets/sprites/environment/base.png').convert()
    
    # Pipes
    assets['pipe'] = pygame.image.load('assets/sprites/environment/pipe-green.png').convert()

    # --- Bird Skins ---
    # We will store them in a dictionary: 'blue', 'red', 'yellow'
    assets['bird_skins'] = {}
    
    colors = ['blue', 'red', 'yellow']
    for color in colors:
        path = f'assets/sprites/bird/{color}bird/'
        frames = [
            pygame.image.load(path + f'{color}bird-downflap.png').convert_alpha(),
            pygame.image.load(path + f'{color}bird-midflap.png').convert_alpha(),
            pygame.image.load(path + f'{color}bird-upflap.png').convert_alpha()
        ]
        assets['bird_skins'][color] = frames

    # Keep default for manual mode compatibility if needed
    assets['bird_frames'] = assets['bird_skins']['blue']

    # Bird Animation Frames
    bird_down = pygame.image.load('assets/sprites/bird/bluebird/bluebird-downflap.png').convert_alpha()
    bird_mid = pygame.image.load('assets/sprites/bird/bluebird/bluebird-midflap.png').convert_alpha()
    bird_up = pygame.image.load('assets/sprites/bird/bluebird/bluebird-upflap.png').convert_alpha()
    assets['bird_frames'] = [bird_down, bird_mid, bird_up]

    # UI & MENUS
    assets['game_over'] = pygame.image.load('assets/sprites/ui/gameover.png').convert_alpha()
    assets['message'] = pygame.image.load('assets/sprites/ui/message.png').convert_alpha()

    # 1. Title Label
    assets['label_flappy_bird'] = pygame.image.load('assets/sprites/ui/label_flappy_bird.png').convert_alpha()
    
    # 2. Buttons
    assets['button_play'] = pygame.image.load('assets/sprites/ui/button_play_normal.png').convert_alpha()
    assets['button_play_pressed'] = pygame.image.load('assets/sprites/ui/button_play_pressed.png').convert_alpha()

    # --- MODE SELECTION BUTTONS ---
    raw_ai = pygame.image.load('assets/sprites/ui/button_ai.png').convert_alpha()
    raw_classic = pygame.image.load('assets/sprites/ui/button_classic.png').convert_alpha()
    raw_highest = pygame.image.load('assets/sprites/ui/button_highest.png').convert_alpha()
    
    # Le scalăm la fel ca pe celelalte (ex: 2x)
    SCALE_BTN = 2.0 
    new_size_ai = (int(raw_ai.get_width() * SCALE_BTN), int(raw_ai.get_height() * SCALE_BTN))
    new_size_classic = (int(raw_classic.get_width() * SCALE_BTN), int(raw_classic.get_height() * SCALE_BTN))
    new_size_highest = (int(raw_highest.get_width() * SCALE_BTN), int(raw_highest.get_height() * SCALE_BTN))

    assets['button_ai'] = pygame.transform.scale(raw_ai, new_size_ai)
    assets['button_classic'] = pygame.transform.scale(raw_classic, new_size_classic) 
    assets['button_highest'] = pygame.transform.scale(raw_highest, new_size_highest)
    
    raw_restart = pygame.image.load('assets/sprites/ui/button_restart.png').convert_alpha()
    new_size_restart = (int(raw_restart.get_width() * SCALE_BTN), int(raw_restart.get_height() * SCALE_BTN))
    assets['button_restart'] = pygame.transform.scale(raw_restart, new_size_restart)

    assets['button_menu'] = pygame.image.load('assets/sprites/ui/button_menu.png').convert_alpha()
   # --- PAUSE & RESUME (Mărite) ---
    # 1. Încărcăm imaginea originală
    raw_pause = pygame.image.load('assets/sprites/ui/button_pause.png').convert_alpha()
    raw_resume = pygame.image.load('assets/sprites/ui/button_resume.png').convert_alpha()
    
    # 2. Definim dimensiunea dorită (ex: 26x28, dublu față de originalul 13x14)
    # Poți pune valori fixe (ex: (40, 40)) sau un factor de scalare
    new_size_pause = (int(raw_pause.get_width() * SCALE_BTN), int(raw_pause.get_height() * SCALE_BTN))
    new_size_resume = (int(raw_resume.get_width() * SCALE_BTN), int(raw_resume.get_height() * SCALE_BTN))
    
    # 3. Salvăm versiunea mărită în dicționar
    assets['button_pause'] = pygame.transform.scale(raw_pause, new_size_pause)
    assets['button_resume'] = pygame.transform.scale(raw_resume, new_size_resume)

    
    # 3. Score Panel
    assets['panel_score'] = pygame.image.load('assets/sprites/ui/panel_score.png').convert_alpha()
    
    # 4. Medals
    assets['medals'] = {
        'bronze': pygame.image.load('assets/sprites/ui/medal_bronze.png').convert_alpha(),
        'silver': pygame.image.load('assets/sprites/ui/medal_silver.png').convert_alpha(),
        'gold': pygame.image.load('assets/sprites/ui/medal_gold.png').convert_alpha(),
        'platinum': pygame.image.load('assets/sprites/ui/medal_platinum.png').convert_alpha()
    }

    # SCORE DIGITS (BIG)
    assets['score_sprites'] = {}
    for i in range(10):
        assets['score_sprites'][str(i)] = pygame.image.load(f'assets/sprites/digits/{i}.png').convert_alpha()

    # --- SCORE DIGITS (SMALL) ---
    assets['score_small_sprites'] = {}
    for i in range(10):
        assets['score_small_sprites'][str(i)] = pygame.image.load(f'assets/sprites/small_digits/number_small_{i}.png').convert_alpha()

    # --- AUDIO ---
    # Verificăm dacă mixerul este inițializat pentru a evita erori
    if pygame.mixer.get_init():
        assets['sounds'] = {
            'wing': pygame.mixer.Sound('assets/audio/wing.wav'),
            'hit': pygame.mixer.Sound('assets/audio/hit.wav'),
            'point': pygame.mixer.Sound('assets/audio/point.wav'),
            'die': pygame.mixer.Sound('assets/audio/die.wav'),
            'swoosh': pygame.mixer.Sound('assets/audio/swoosh.wav')
        }
    else:
        assets['sounds'] = {}
        print("Warning: Audio mixer not initialized")

    return assets