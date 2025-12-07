from entities.bird import Bird

class Population:
    def __init__(self,size, assets):
        self.size = size
        self.assets = assets
        # Spawn N birds
        self.birds = [Bird(assets['bird_frames'], assets['sounds']) for _ in range(size)]
        #self.generation = 1

    def update(self, pipe_manager, game_surface):
        alive_count = 0
        for bird in self.birds:
            if bird.alive:
                bird.think(pipe_manager)
                bird.move()
                bird.animate()
                bird.draw(game_surface)
                alive_count += 1

                if bird.check_collision(pipe_manager):
                    bird.alive = False
                else:
                    alive_count += 1
        return alive_count