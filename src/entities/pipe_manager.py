import pygame
from settings import *
from entities.pipe import Pipe

class PipeManager:
    def __init__(self, pipe_img):
        self.pipe_img = pipe_img
        self.pipes = [] # Listă de obiecte Pipe
    
    def spawn_pipe(self):
        # Creăm un nou obiect Pipe la marginea dreaptă a ecranului
        new_pipe = Pipe(self.pipe_img, GAME_WIDTH + 50)
        self.pipes.append(new_pipe)

    def update(self):
        for pipe in self.pipes:
            pipe.move()
        
        # Ștergem țevile care au ieșit din ecran pentru a economisi memorie
        # Păstrăm doar țevile unde marginea dreaptă > -50
        self.pipes = [pipe for pipe in self.pipes if pipe.rect_bottom.right > -50]

    def draw(self, surface):
        for pipe in self.pipes:
            pipe.draw(surface)
    
    def clear(self):
        self.pipes.clear()