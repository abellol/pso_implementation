from algorithm.particle import Particle

class Swarm:
  """
  A class to represent a swarm of particles in the Particle Swarm Optimization algorithm.
  """
  def __init__(self, bounds: tuple, c1: float, c2: float, w: float, n_particles: int, optimization: str, objective_function):
    self.optimization = optimization
    self.particles = [Particle(bounds, c1, c2, w, objective_function) for _ in range(n_particles)]
    self.gbest = self.particles[0].position
    self.objective_function = objective_function

  def update_gbest(self):
    """
    Update the global best position of the swarm.
    """
    for particle in self.particles:
      if self.optimization == "min":
        if particle.evaluate() < self.objective_function(self.gbest):
          self.gbest = particle.position.copy()
      elif self.optimization == "max":
        if particle.evaluate() > self.objective_function(self.gbest):
          self.gbest = particle.position.copy()