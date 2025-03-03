## PSO ALGORITHM IMPLEMENTATION

### Contributors: 
| Name | ID |
|---|---|
| Alejandro Bello | 1013037759 |
| Malcolm Carrillo | 1010962608 |
| Rafael Chirivi | 1034661580 |

<details><summary>Get ready to see the great logo: </summary><p>
<div align='center'>
<figure> <img src="https://i.postimg.cc/NFbwf57S/logo-def.png" alt="logo" width="400" height="auto"/></br>
<figcaption><b> "we're programmers, not designers" </b></figcaption></figure>
</div>
</p></details><br>

### Installation

To install and run this project, follow these steps:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/abellol/pso_implementation.git
   cd pso_implementation/
   ```

2. **Create and activate a virtual environment (optional but recommended)**  
   - On Windows:  
     ```bash
     python -m venv my_venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:  
     ```bash
     python -m venv my_venv
     source venv/bin/activate
     ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with:

```bash
python main.py
```


## Configuration

The file contains adjustable parameters such as:
- Number of particles
- Inertia weight
- Cognitive and social coefficients (listed as c1 and c2)
- Number of iterations
- Objective function (taken from some presets)

Modify these parameters to suit your optimization problem.


## Class diagram
```mermaid

classDiagram
Particle --* Swarm : A swarm has particles
Swarm ..> Optimization : Optimization depends on a swarm
Optimization --> Visualizer : Optimization works with a Visualizer
Visualizer --* UserInterface : User Interface has a Visualizer 
FunctionValueError <--> UserInterface : Custom Error works over User Interface
class Particle{
    + bounds : tuple
    + c1 : float
    + c2 : float
    + w : float
    + objective_function
    + __init__(self, bounds, c1, c2, w, objective_function) self.position, self.pbest, self.max_velocity, self.velocity, self.c1, self.c2, self.w, self.objective_function
    + evaluate(self) : self.objective_function(self.position)
    + update_velocity(self, gbest) r1, r2, cognitive, social, self.velocity
    + update_position(self, bounds) self.position
}
class Swarm{
    + bounds : tuple
    + c1 : float
    + c2 : float
    + w : float
    + n_particles : int
    + optimization : str
    + objective_function
    + __init__(self, bounds, c1, c2, w, n_particles, optimization, objective_function) self.optimization, self.particles, self.gbest, self.objective_function
    + update_gbest(self) self.gbest
}
class Optimization{
    + bounds : tuple
    + c1 : float
    + c2 : float
    + w : float
    + n_particles : int
    + optimization : str
    + iterations : str
    + objective_function
    + canvas
    + figure
    + ax
    + root 
    + ui
    + __init__(self, bounds, c1, c2, w, n_particles, optimization, iterations, objective_function, canvas, figure, ax, root, ui) self.bounds, self.iterations, self.swarm, self.vizualizer, self.objective_function, self.ui
    + optimize(self) self.swarm.gbest, best_value
}
class Visualizer{
    + objective_function
    + bounds : tuple
    + canvas
    + figure
    + ax
    + root 
    + ui
    + resolution : int
    + __init__(self, objective_function, bounds, canvas, figure, ax, root, ui, resolution) self.objective_function, self.bounds, self.resolution, self.canvas, self.figure, self.ax, self.root, self.ui, self.create_background()
    + create_background(self) x, y, X, Y, Z, self.X, self.Y, self.Z
    + plot(self, particles, gbest, iteration) levels, positions
    + show_final(self, gbest, best_value) gbest, best_value
}
class UserInterface{
    + __init__(self) self.root, self.lim_x, self.lim_y, self.c1, self.c2, self.w, self.particles, self.iterations, self.selected_function, functions_list, self.Error, self.trigger
    + create_plot(self) self.fig, self.ax, self.canvas, self.canvas_widget
    + init_optimization(self) bounds, c1, c2, w, n_particles, iterations, function_name, pso
    + loop(self)
}
class FunctionValueError{
    + message : str
    + __init__(self, message)
}

```

