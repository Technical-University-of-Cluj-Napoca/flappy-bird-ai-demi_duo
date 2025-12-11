import pygame
from settings import *
from entities.pipe import Pipe

class PipeManager:
    def __init__(self, pipe_img):
        self.pipe_img = pipe_img
        self.pipes = [] # List of Pipe objects
    
    def spawn_pipe(self):
        # Create a new pipe just outside the right edge of the screen
        new_pipe = Pipe(self.pipe_img, GAME_WIDTH + 50)
        self.pipes.append(new_pipe)

    def update(self):
        for pipe in self.pipes:
            pipe.move()
        
        # Remove pipes that have moved off the left edge of the screen
        # Keep only pipes that are still visible
        self.pipes = [pipe for pipe in self.pipes if pipe.rect_bottom.right > -50]

    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)
    
    def clear(self):
        self.pipes.clear()