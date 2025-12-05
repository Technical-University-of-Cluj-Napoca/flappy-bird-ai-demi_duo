import pygame
import os

def load_assets():
    """
    Încarcă toate imaginile și sunetele și le returnează într-un dicționar structurat.
    """
    assets = {}

    # --- IMAGINI ---
    # Backgrounds
    assets['bg_day'] = pygame.image.load('assets/sprites/background-day.png').convert()
    assets['bg_night'] = pygame.image.load('assets/sprites/background-night.png').convert()
    
    # Floor
    assets['floor'] = pygame.image.load('assets/sprites/base.png').convert()
    
    # Pipes
    assets['pipe'] = pygame.image.load('assets/sprites/pipe-green.png').convert()

    # Bird Animation Frames
    bird_down = pygame.image.load('assets/sprites/bluebird/bluebird-downflap.png').convert_alpha()
    bird_mid = pygame.image.load('assets/sprites/bluebird/bluebird-midflap.png').convert_alpha()
    bird_up = pygame.image.load('assets/sprites/bluebird/bluebird-upflap.png').convert_alpha()
    assets['bird_frames'] = [bird_down, bird_mid, bird_up]

    # UI Elements
    assets['game_over'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    assets['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()

    # Score Digits (0-9)
    assets['score_sprites'] = {}
    for i in range(10):
        assets['score_sprites'][str(i)] = pygame.image.load(f'assets/sprites/digits/{i}.png').convert_alpha()

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