import pygame
from settings import *

class Bird:
    def __init__(self, frames, sounds):
        self.frames = frames
        self.sounds = sounds
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(50, GAME_HEIGHT / 2))
        self.movement = 0
        self.index = 0
        
    def flap(self):
        self.movement = FLAP_STRENGTH
        self.sounds['wing'].play()

    def move(self):
        self.movement += GRAVITY
        self.rect.centery += self.movement

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def draw(self, surface):
        rotated_bird = pygame.transform.rotozoom(self.image, -self.movement * ROTATION_SPEED, 1)
        surface.blit(rotated_bird, self.rect)

    def check_collision(self, pipe_manager):
        # Verificăm fiecare țeavă din manager
        for pipe in pipe_manager.pipes:
            # O țeavă are două rect-uri: top și bottom
            if self.rect.colliderect(pipe.rect_top) or self.rect.colliderect(pipe.rect_bottom):
                return True
        
        # Coliziune podea/tavan
        if self.rect.top <= -50 or self.rect.bottom >= 450:
            return True
            
        return False

    def reset(self):
        self.rect.center = (50, GAME_HEIGHT / 2)
        self.movement = 0