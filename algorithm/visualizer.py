import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Visualizer:
  def __init__(self, objective_function, bounds, canvas, figure, ax, root, ui, resolution=150):
    self.objective_function = objective_function
    self.bounds = bounds
    self.resolution = resolution
    self.canvas = canvas  # Tkinter canvas
    self.figure = figure  # Matplotlib figure
    self.ax = ax  # Matplotlib axis
    self.root = root  # Tkinter root window
    self.ui = ui  # Store reference to UI
    self.create_background()

  def create_background(self):
    """
    Creates the background of the plot
    """
    x = np.linspace(self.bounds[0], self.bounds[1], self.resolution)
    y = np.linspace(self.bounds[0], self.bounds[1], self.resolution)
    X, Y = np.meshgrid(x, y)
    Z = self.objective_function([X, Y])
    self.X, self.Y, self.Z = X, Y, Z

  def plot(self, particles, gbest, iteration):
    """
    Plots the objective function and particles in the search space
    """
    self.ax.clear()
    levels = np.logspace(np.log10(self.Z.min() + 1e-10), np.log10(self.Z.max()), num=30)
    self.ax.contourf(self.X, self.Y, self.Z, levels=levels, cmap="magma", norm=LogNorm())
    positions = np.array([particle.position for particle in particles])
    self.ax.scatter(positions[:, 0], positions[:, 1], color="green", label="Partículas", zorder=3)
    self.ax.scatter(gbest[0], gbest[1], color="yellow", marker="*", s=100, label="Mejor global", zorder=4)
    self.ax.set_xlim(self.bounds[0], self.bounds[1])
    self.ax.set_ylim(self.bounds[0], self.bounds[1])
    self.ax.set_xlabel("x", fontsize=12)
    self.ax.set_ylabel("y", fontsize=12)
    self.ax.set_title(f"Iteración {iteration + 1}", fontsize=14, fontweight="bold")
    self.ax.legend(loc="upper right", bbox_to_anchor=(1.05, 1), fontsize=10)
    self.ax.grid(True, linestyle="--", alpha=0.6)
    self.canvas.draw()  # Redraw on Tkinter canvas
    self.root.update_idletasks()  # Allow Tkinter to process events
    self.root.update()  # Force UI refresh

  def show_final(self, gbest, best_value):
    """Shows the result of the optimization"""
    self.ax.text(0.02, 0.02,  
      f"Best solution: ({gbest[0]:.4f}, {gbest[1]:.4f})\nOptimal Value: {best_value:.6f}",
      fontsize=9, color="black", bbox=dict(facecolor="white", alpha=0.8),
      transform=self.ax.transAxes,
      verticalalignment='bottom', horizontalalignment='left')
    self.canvas.draw()
    
    print(f"Best solution found: ({gbest[0]:.4f}, {gbest[1]:.4f})")
    print(f"Optimal Value: {best_value:.6f}")

    # Ensure button gets re-enabled
    self.ui.trigger.config(state="normal")