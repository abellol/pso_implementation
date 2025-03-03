import tkinter as tk
from tkinter import PhotoImage
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm.optimization import Optimization
from algorithm.errors import FunctionValueError


#Dictionary of saved functions to use
functions = {
  "Goldstein_price": {
    "optimization": "min",
    "function": lambda x, y: (1 + (x + y + 1)**2 * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)) * 
                             (30 + (2*x - 3*y)**2 * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2))
  },
  "Himmelblau": {
    "optimization": "min",
    "function": lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2
  },
  "Three_hump_camel": {
    "optimization": "min",
    "function": lambda x, y: 2*x**2 - 1.05*x**4 + (x**6)/6 + x*y + y**2
  },
  "Beale": {
    "optimization": "min",
    "function": lambda x, y: (1.5 - x + x * y) ** 2 + (2.25 - x + x * y ** 2) ** 2 + (2.625 - x + x * y ** 3) ** 2
  },
  "Booth": {
    "optimization": "min",
    "function": lambda x, y: ((x + 2 * y - 7) ** 2) + ((2 * x + y - 5) ** 2)
  },
  "Matyas": {
    "optimization": "min",
    "function": lambda x, y: 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
  }
}

def objective_function(position, function_name): 
  
  """ 
  This function gets the lambda function correspondent to the function name selected in the UI

  Args:
    position, function_name

  Returns:
    The lambda function  in the right format
  """

  x, y = position
  return functions[function_name]["function"](x, y)

class UserInterface:
  
  def __init__(self):
    self.root = tk.Tk() #Creates window
    self.root.title("PSO Algorithm")
    self.root.geometry("1280x720")
    self.root.resizable(False, False) #Unables the resizing of the window
    self.bg = PhotoImage(file = "algorithm/assets/Bg1.png") 
    self.bgcanvas = tk.Canvas( self.root, width = 1280, height = 720) # Creates a canvas to contain the elements of the UI
    self.bgcanvas.pack(fill = "both", expand = True) 
    self.bgcanvas.create_image( 0, 0, image = self.bg, anchor = "nw")
    
    # Text 
    tk.Label(self.root, text="Bounds", font=("Consolas", 15), fg="black", bg="white").place(x=190, y=50)
    tk.Label(self.root, text="C1", font=("Consolas", 15), fg="black", bg="white").place(x=100, y=150)
    tk.Label(self.root, text="C2", font=("Consolas", 15), fg="black", bg="white").place(x=254, y=150)
    tk.Label(self.root, text="w", font=("Consolas", 15), fg="black", bg="white").place(x=408, y=150)
    tk.Label(self.root, text="# Particles", font=("Consolas", 15), fg="black", bg="white").place(x=100, y=250)
    tk.Label(self.root, text="Iterations", font=("Consolas", 15), fg="black", bg="white").place(x=254, y=250)
    tk.Label(self.root, text="Function", font=("Consolas", 15), fg="black", bg="white").place(x=100, y=350)

    # Entries 
    self.lim_x = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.lim_x.place(x=100, y=80, height=30)

    self.lim_y = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.lim_y.place(x=254, y=80, height=30)

    self.c1 = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.c1.place(x=100, y=180, height=30)

    self.c2 = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.c2.place(x=254, y=180, height=30)

    self.w = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.w.place(x=408, y=180, height=30)

    self.particulas = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.particulas.place(x=100, y=280, height=30)

    self.iterations = tk.Entry(self.root, bg="#cfcfcf", fg="black", width=16, relief="flat")
    self.iterations.place(x=254, y=280, height=30)

    self.selected_function = tk.StringVar()
    self.selected_function.set("Seleccionar función")

    # Dropdown function list
    functions_list = list(functions.keys())
    self.dropdown = tk.OptionMenu(self.root, self.selected_function, *functions_list)
    self.dropdown.config(width=20, relief="flat", font=("Consolas", 12))
    self.dropdown.place(x=100, y=380)

    # Error label placeholder
    self.Error = tk.Label(self.root, text="", font=("Consolas", 15), fg="red", bg="white", wraplength=250, justify="center")
    self.Error.place(x=150, y=600, width=300)

    # Start Button 
    self.trigger = tk.Button(self.root, text="Start Optimization", command=self.init_optimization, 
                             bg="#808080", relief="flat", font=("Consolas", 18))
    self.trigger.place(x=150, y=500, width=300, height=50)

    # Create Matplotlib Plot 
    self.create_plot()

  def create_plot(self):
    """
    This function creates the plot for the data into the tkinter window
    """
    self.fig = Figure(figsize=(6, 6), dpi=100)
    self.ax = self.fig.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.fig, master=self.root) #Creates the matplotlob canvas to place the plotted graph
    self.canvas_widget = self.canvas.get_tk_widget()
    self.canvas_widget.place(relx=0.75, rely=0.45, anchor="center")

  def init_optimization(self):
    """
    This function catches the data input into the entries and dropdown list from the UI, and
    """
    self.trigger.config(state="disabled")  #Unables the button while the optimization is currently occurring 

    try:
      try:
        self.Error.config(text="")
        bounds = (float(self.lim_x.get()), float(self.lim_y.get()))
        c1 = float(self.c1.get())
        c2 = float(self.c2.get())
        w = float(self.w.get())
        n_particles = int(self.particulas.get())
        iterations = int(self.iterations.get())
        function_name = self.selected_function.get()
      except ValueError:

        """Raises an exception turning the general 
        ValueError into the custom FunctionError to display the message and not break the UI loop"""

        raise FunctionValueError("Error occured when handling data, check value types")


      #Sets of conditionals to raise the exception
      if function_name not in functions:
        raise FunctionValueError("Select function")
      if c1 > 2 or c1 < 1:
        raise FunctionValueError("Coefficent c1 is not valid")
      if c2 > 2 or c2 < 1:
        raise FunctionValueError("Coefficents c2 is not valid")
      if w > 1 or w < 0:
        raise FunctionValueError("Weight not valid")

      optimization = functions[function_name]["optimization"]

      print(f"\tStarting optimization with function: {function_name}")
      print(f"Bounds: {bounds}, C1: {c1}, C2: {c2}, w: {w}, Particles: {n_particles}, Iterations: {iterations}")

      pso = Optimization(
        bounds, c1, c2, w, n_particles, optimization, iterations, 
        lambda pos: objective_function(pos, function_name),
        self.canvas, self.fig, self.ax, self.root, self  # Pasamos self para manejar la UI
      )
      pso.optimize()

    except FunctionValueError as error:
      self.Error.config(text=error)
      self.root.after(4000, lambda: self.Error.config(text=""))
      self.trigger.config(state="normal")  # Re-enables the button if there's an error

  def loop(self):
    #Starts and keeps the application loop running
    self.root.mainloop()