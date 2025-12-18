import pygame
import random
from settings import *

class Pipe:
    def __init__(self, pipe_img, x_pos):
        self.image = pipe_img
        self.x = x_pos
        self.passed = False # Flag util for score and AI logic
        self.height = random.randint(170, 430)
        
        # Initializing rectangles for the top and bottom pipes
        # Bottom pipe
        self.rect_bottom = self.image.get_rect(midtop=(self.x, self.height))
        # Top pipe
        self.rect_top = self.image.get_rect(midbottom=(self.x, self.height - 150))

    def move(self):
        self.rect_bottom.centerx -= PIPE_MOVE_SPEED
        self.rect_top.centerx -= PIPE_MOVE_SPEED

    # Draw both pipes (top and bottom)
    def draw(self, surface):
        surface.blit(self.image, self.rect_bottom)        
        flip_pipe = pygame.transform.flip(self.image, False, True)
        surface.blit(flip_pipe, self.rect_top)