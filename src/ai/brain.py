import random
import math

class Brain:
    def __init__(self,weights =None):
        if weights:
            self.weights = list(weights)
        else:
            self.weights = [random.uniform(-1, 1) for _ in range(4)]

    def sigmoid(self,x):
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0 if x < 0 else 1
    
    def decide(self, inputs):
        total = 0
        for i in range(3):
            total += inputs[i] * self.weights[i]
        
        total += self.weights[3] * 1  # bias
        return self.sigmoid(total)
    
    def mutate(self, mutation_rate):
        """
        Modifies weights randomly based on a mutation rate.
        Ref: 'apply smaller random mutations on its weights' [cite: 301]
        """
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                # Add a small random value to the weight
                self.weights[i] += random.gauss(0, 0.2)
                # Clamp weights between -1 and 1 (optional but recommended)
                self.weights[i] = max(-1, min(1, self.weights[i]))

    def clone(self):
        """Returns a deep copy of this brain."""
        return Brain(list(self.weights))