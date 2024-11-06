import tkinter as tk
import time
from enum import Enum
from sandautomaton import SandAutomaton, ParticleType


class Display:
    def __init__(self, root, rows=10, cols=10, cell_size=40):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.simulator = SandAutomaton(rows, cols)
        self.running = False
        self.btn_frame = tk.Frame(root)
        self.canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size, background="black")
        self.start_btn = tk.Button(self.btn_frame, text="START", command=self.start, background="green", foreground="white")
        self.stop_btn = tk.Button(self.btn_frame, text="STOP", command=self.stop, background="red", foreground="white")
        self.reset_btn = tk.Button(self.btn_frame, text="RESET", command=self.reset, background="blue", foreground="white")

        self.start_btn.pack(side="left")
        self.stop_btn.pack(side="left")
        self.reset_btn.pack(side="left")
        self.btn_frame.pack()
        self.canvas.pack()

        # Adicionar evento de clique
        self.b1bind = self.canvas.bind("<Button-1>", self.set_b1_pressed)
        self.b1bind = self.canvas.bind("<ButtonRelease-1>", self.set_b1_released)
        self.b2bind = self.canvas.bind("<Button-2>", self.reset_canvas)
        self.mbind = self.canvas.bind("<Motion>", self.set_add_particle_pos)
        self.b1_pressed = False
        # self.canvas.bind("<Button-3>", self.run)

        self.draw_particles(self.simulator.grid)
        self.loop()

    def draw_square(self, row, col, color):
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_particles(self, grid):
        self.reset_canvas()
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] != ParticleType.AIR:
                    self.draw_square(i, j, grid[i][j].value)

    def reset_canvas(self):
        self.canvas.delete("all")

    def run(self, event):
        # self.canvas.unbind("<Button-1>", self.b1bind)
        # self.canvas.unbind("<Button-2>", self.b2bind)
        # self.b1bind = self.canvas.bind("<Button-1>", self.stop)
        self.running = True

    def loop(self):
        if self.running:
            grid = self.simulator.run_iteration()
            self.draw_particles(grid)
            # self.running += 1
            print(f"finished interaction {self.running}")
        if self.b1_pressed:
            self.handle_add_particle()
        self.canvas.after(16, self.loop)
    
    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        # self.canvas.unbind("<Button-1>", self.b1bind)
        # self.b1bind = self.canvas.bind("<Button-1>", self.add_particle)
        # self.b2bind = self.canvas.bind("<Button-2>", self.reset_canvas)

    def reset(self):
        if not self.running:
            self.reset_canvas()
            self.simulator.reset()
            self.draw_particles(self.simulator.grid)

    def handle_add_particle(self):
        x = self.add_particle_pos.x
        y = self.add_particle_pos.y
        row = x // self.cell_size
        col = y // self.cell_size
        self.simulator.add_particle(col, row)
        self.draw_square(col, row, ParticleType.SAND.value)
    
    def set_b1_pressed(self, e):
        self.set_add_particle_pos(e)
        self.b1_pressed = True

    def set_b1_released(self, e):
        self.b1_pressed = False
    
    def set_add_particle_pos(self, e):
        self.add_particle_pos = e