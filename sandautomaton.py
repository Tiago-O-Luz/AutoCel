import time
from copy import deepcopy
from enum import Enum


class ParticleType(Enum):
    AIR = "empty"
    SAND = "yellow"
    SOLID = "white"


CASE_SAND_1 = [
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 1, 0, 0],
[0, 0, 0, 0, 0]]

CASE_SAND_2 = [
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 1, 0, 0],
[0, 0, 1, 0, 0]]

CASE_SAND_3 = [
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 1, 0, 0],
[0, 1, 1, 0, 0]]


class SandAutomaton:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.grid = [[ParticleType.AIR for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            if i == 0 or i == self.rows-1:
                for j in range(self.cols):
                    self.grid[i][j] = ParticleType.SOLID
            else:
                self.grid[i][0] = ParticleType.SOLID
                self.grid[i][-1] = ParticleType.SOLID
        self.start_grid = deepcopy(self.grid)


    def add_particle(self, row, col):
        # Calcular a célula clicada
        # col = event.x // self.cell_size
        # row = event.y // self.cell_size
        if self.grid[row][col] is ParticleType.AIR:  # Verifica se a célula já não está preenchida
            # Desenhar o quadrado
            self.grid[row][col] = ParticleType.SAND
            print(f"particle {row},{col} is SAND")


    def run_iteration(self):
        new_grid = deepcopy(self.grid)
        # new_grid = [[ParticleType.AIR for _ in range(self.cols)] for _ in range(self.rows)]
        for i in reversed(range(self.rows)[1:-1]):
            for j in reversed(range(self.cols)[1:-1]):
                p = self.grid[i][j]
                pd = self.grid[i+1][j]
                pdl = self.grid[i+1][j-1]
                pdr = self.grid[i+1][j+1]
                # pdll = self.grid[i+1][j-2]
                # pdrr = self.grid[i+1][j+2]
                if p == ParticleType.SAND:
                    if pd == ParticleType.AIR:
                        new_grid[i][j] = ParticleType.AIR
                        new_grid[i+1][j] = ParticleType.SAND
                    if pd == ParticleType.SAND:
                        if pdl == ParticleType.AIR:
                            new_grid[i][j] = ParticleType.AIR
                            new_grid[i+1][j-1] = ParticleType.SAND
                        elif pdr == ParticleType.AIR:
                            new_grid[i+1][j+1] = ParticleType.SAND
                            new_grid[i][j] = ParticleType.AIR
                        # elif pdll == ParticleType.AIR:
                        #     new_grid[i][j] = ParticleType.AIR
                        #     new_grid[i+1][j-2] = ParticleType.SAND
                        # elif pdrr == ParticleType.AIR:
                        #     new_grid[i][j] = ParticleType.AIR
                        #     new_grid[i+1][j+2] = ParticleType.SAND

        self.grid = new_grid
    
        return self.grid
    
    def reset(self):
        self.grid = deepcopy(self.start_grid)
