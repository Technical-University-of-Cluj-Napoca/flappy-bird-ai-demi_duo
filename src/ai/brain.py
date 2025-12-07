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