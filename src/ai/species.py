import random

class Species:
    def __init__(self, representative_bird, skin_name="blue"):
        # The representative is the brain pattern that defines this species
        self.representative = representative_bird.brain.clone()
        self.birds = [representative_bird]
        self.average_fitness = 0
        self.best_fitness = 0
        self.champion = None
        
        # Threshold for how different a brain can be to still belong here
        # You can tweak this number (e.g., 0.5 to 2.0) based on testing
        self.threshold = 1.0 
        self.skin_name = skin_name

    def belongs_to_species(self, bird_brain):
        """
        Calculates the distance between the bird's weights and the representative's weights.
        Returns True if the difference is smaller than the threshold.
        """
        diff = 0
        for i in range(len(self.representative.weights)):
            diff += abs(self.representative.weights[i] - bird_brain.weights[i])
        return diff < self.threshold

    def sort_birds(self):
        """Sorts the birds in this species by fitness (descending)."""
        self.birds.sort(key=lambda b: b.fitness, reverse=True)
        if self.birds:
            self.champion = self.birds[0]
            self.best_fitness = self.champion.fitness

    def calculate_average_fitness(self):
        """Calculates the average score of this species."""
        total = sum(b.fitness for b in self.birds)
        if self.birds:
            self.average_fitness = total / len(self.birds)
        else:
            self.average_fitness = 0

    def give_birth(self, clone_champion=True):
        """
        Produces a new brain.
        - If clone_champion is True, returns an exact copy of the best bird.
        - Otherwise, picks a random parent from this species and mutates the brain.
        """
        if clone_champion and self.champion:
            return self.champion.brain.clone()
        
        # Select a random parent from the current species
        parent = random.choice(self.birds)
        child_brain = parent.brain.clone()
        
        # Apply mutation
        child_brain.mutate(mutation_rate=0.1) 
        return child_brain