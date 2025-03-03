from algorithm.visualizer import Visualizer
from algorithm.swarm import Swarm

class Optimization:
  """
  A class to represent the optimization process of the PSO algorithm.
  """
  def __init__(self, bounds, c1, c2, w, n_particles, optimization, iterations, objective_function, canvas, figure, ax, root, ui):
    self.bounds, self.iterations = bounds, iterations
    self.swarm = Swarm(bounds, c1, c2, w, n_particles, optimization, objective_function)
    self.visualizer = Visualizer(objective_function, bounds, canvas, figure, ax, root, ui)  # Pass UI instance
    self.objective_function = objective_function
    self.ui = ui  
  def optimize(self):
    """
    Optimize the objective function using the PSO algorithm.
    """
    for _ in range(self.iterations):
      for particle in self.swarm.particles:
        particle.update_velocity(self.swarm.gbest)
        particle.update_position(self.bounds)
        if self.objective_function(particle.position) < self.objective_function(particle.pbest):
          particle.pbest = particle.position.copy()
      self.swarm.update_gbest()
      self.visualizer.plot(self.swarm.particles, self.swarm.gbest, _)
    best_value = self.objective_function(self.swarm.gbest)
    self.visualizer.show_final(self.swarm.gbest, best_value)
    return self.swarm.gbest, best_value
