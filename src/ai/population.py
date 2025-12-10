from entities.bird import Bird
from ai.species import Species  # <--- Import your new class
import random

class Population:
    def __init__(self, size, assets):
        self.size = size
        self.assets = assets
        self.generation = 1
        self.species = []
        
        # Define the available skins for visual differentiation
        self.available_skins = ['blue', 'red', 'yellow']
        
        # Initialize first generation (defaulting to Blue)
        # Note: Ensure you have updated assets.py to include 'bird_skins'
        self.birds = [Bird(assets['bird_skins']['blue'], assets['sounds']) for _ in range(size)]

    def update(self, pipe_manager, game_surface):
        alive_count = 0
        for bird in self.birds:
            if bird.alive:
                bird.fitness += 1  # Reward for surviving
                
                bird.think(pipe_manager)
                bird.move()
                bird.animate()
                bird.draw(game_surface)
                
                if bird.check_collision(pipe_manager):
                    bird.alive = False
                else:
                    alive_count += 1
        return alive_count

    def natural_selection(self):
        """Called when all birds die."""
        print(f"--- Generation {self.generation} Complete ---")
        
        self.speciate()
        self.calculate_fitness()
        self.sort_species()
        self.next_generation()
        
        self.generation += 1
        print(f"--- Generation {self.generation} Started ---")

    def speciate(self):
        for s in self.species:
            s.birds = []
        
        for bird in self.birds:
            found = False
            for s in self.species:
                if s.belongs_to_species(bird.brain):
                    s.birds.append(bird)
                    found = True
                    break
            
            if not found:
                # Assign a color based on the new species count (Cycle: Blue -> Red -> Yellow -> Blue...)
                skin_idx = len(self.species) % len(self.available_skins)
                new_skin = self.available_skins[skin_idx]
                
                self.species.append(Species(bird, skin_name=new_skin))
        
        self.species = [s for s in self.species if len(s.birds) > 0]

    def calculate_fitness(self):
        for s in self.species:
            s.sort_birds()
            s.calculate_average_fitness()

    def sort_species(self):
        # Best species (highest average fitness) comes first
        self.species.sort(key=lambda s: s.average_fitness, reverse=True)

    def next_generation(self):
        new_birds = []
        
        # Calculate global fitness sum to determine offspring count
        total_fitness = sum(s.average_fitness for s in self.species)
        
        for s in self.species:
            # Calculate how many babies this species is allowed to have
            if total_fitness > 0:
                amount = (s.average_fitness / total_fitness) * self.size
            else:
                amount = self.size / len(self.species)
            
            amount = int(amount)
            skin_frames = self.assets['bird_skins'][s.skin_name]
            
            # 1. Clone the champion (Elitism)
            if amount > 0:
                child_brain = s.give_birth(clone_champion=True)
                new_birds.append(Bird(skin_frames, self.assets['sounds'], child_brain))
                amount -= 1
            
            # 2. Fill the rest with mutated offspring
            for _ in range(amount):
                 child_brain = s.give_birth(clone_champion=False)
                 new_birds.append(Bird(skin_frames, self.assets['sounds'], child_brain))
        
        # Fill any remaining slots (due to rounding) with offspring from the best species
        while len(new_birds) < self.size:
             s = self.species[0]
             skin_frames = self.assets['bird_skins'][s.skin_name]
             new_birds.append(Bird(skin_frames, self.assets['sounds'], s.give_birth(clone_champion=False)))

        self.birds = new_birds