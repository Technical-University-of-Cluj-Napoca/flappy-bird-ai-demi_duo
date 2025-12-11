import pygame
from settings import *
from ai.brain import Brain

class Bird:
    def __init__(self, frames, sounds, brain = None):
        self.frames = frames
        self.sounds = sounds
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(BIRD_START_X, BIRD_START_Y))
        self.movement = 0
        self.index = 0

        self.brain = brain if brain else Brain()
        self.alive = True
        self.fitness = 0
        
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
        if self.alive:
            rotated_bird = pygame.transform.rotozoom(self.image, -self.movement * ROTATION_SPEED, 1)
            surface.blit(rotated_bird, self.rect)

    def check_collision(self, pipe_manager):
        # Check each pipe from manager
        for pipe in pipe_manager.pipes:
            # A pipe has 2 rects: top and bottom
            if self.rect.colliderect(pipe.rect_top) or self.rect.colliderect(pipe.rect_bottom):
                return True
        
        # Colision with ground or ceiling
        if self.rect.top <= -50 or self.rect.bottom >= 450:
            return True
            
        return False

    def reset(self):
        self.rect.center = (BIRD_START_X, BIRD_START_Y)
        self.movement = 0
        self.alive = True
        self.fitness = 0

    def think(self, pipe_manager):
        closest_pipe = None
        closest_dist = float('inf')

        for pipe in pipe_manager.pipes:
            if pipe.rect_bottom.right >= self.rect.left:
                dist = pipe.rect_bottom.x - self.rect.x
                if dist < closest_dist:
                    closest_dist = dist
                    closest_pipe = pipe

        if closest_pipe:
            # i0: distance to top pipe
            # i1: distance to next pipe (horizontal)
            # i2: distance to bottom pipe
            
            i0 = (closest_pipe.rect_top.bottom - self.rect.top) / GAME_HEIGHT
            i1 = (closest_pipe.rect_bottom.left - self.rect.right) / GAME_WIDTH
            i2 = (closest_pipe.rect_bottom.top - self.rect.bottom) / GAME_HEIGHT

            inputs = [i0, i1, i2]
            output = self.brain.decide(inputs)

            if output > THRESHOLD_FLAP:
                self.flap()