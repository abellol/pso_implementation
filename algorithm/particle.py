import random
import numpy as np

class Particle:
  """
  A class to represent a particle in the swarm.
  """
  def __init__(self, bounds: tuple, c1: float, c2: float, w: float, objective_function):
    self.position = np.random.uniform(bounds[0], bounds[1], size=2)
    self.pbest = self.position.copy()
    self.max_velocity = 0.3 * (bounds[1] - bounds[0])
    self.velocity = np.random.uniform(-self.max_velocity, self.max_velocity, size=2)
    self.c1 = c1
    self.c2 = c2
    self.w = w
    self.objective_function = objective_function

  def evaluate(self):
    """
    Evaluate the particle's position using the objective function.
    """
    return self.objective_function(self.position)

  def update_velocity(self, gbest):
    """
    Update the particle's velocity.
    """
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    cognitive = self.c1 * r1 * (self.pbest - self.position)
    social = self.c2 * r2 * (gbest - self.position)
    self.velocity = self.w * self.velocity + cognitive + social

  def update_position(self, bounds):
    """
    Update the particle's position.
    """
    self.position += self.velocity