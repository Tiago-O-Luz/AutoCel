import time
from copy import deepcopy
from enum import Enum

# Definição dos tipos de partículas presentes no autômato
class ParticleType(Enum):
    AIR = "empty"  # Representa o ar (célula vazia)
    SAND = "yellow"  # Representa a areia (célula com partícula de areia)
    SOLID = "white"  # Representa um obstáculo sólido (célula preenchida)

# Casos de teste para o autômato
CASE_SAND_1 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

CASE_SAND_2 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]

CASE_SAND_3 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0]
]

# Classe principal do autômato de areia
class SandAutomaton:
    def __init__(self, rows=10, cols=10):
        # Inicialização dos parâmetros
        self.rows = rows
        self.cols = cols

        # Criação da grade inicial preenchida com ar
        self.grid = [[ParticleType.AIR for _ in range(self.cols)] for _ in range(self.rows)]

        # Definindo as bordas da grade como sólidas
        for i in range(self.rows):
            if i == 0 or i == self.rows - 1:  # Linha superior e inferior
                for j in range(self.cols):
                    self.grid[i][j] = ParticleType.SOLID
            else:
                self.grid[i][0] = ParticleType.SOLID  # Primeira coluna
                self.grid[i][-1] = ParticleType.SOLID  # Última coluna

        # Armazena o estado inicial da grade
        self.start_grid = deepcopy(self.grid)

    # Adiciona uma partícula de areia na posição especificada (linha e coluna)
    def add_particle(self, row, col):
        # Verifica se a posição está dentro dos limites da grade
        if not (row >= self.rows or row < 0 or col >= self.cols or col < 0):
            # Verifica se a célula está vazia
            if self.grid[row][col] is ParticleType.AIR:
                self.grid[row][col] = ParticleType.SAND  # Adiciona a partícula de areia
                print(f"particle {row},{col} is SAND")  # Mensagem de debug

    # Executa uma iteração de simulação do autômato
    def run_iteration(self):
        # Cria uma cópia da grade atual para atualizar os estados
        new_grid = deepcopy(self.grid)

        # Varre a grade de baixo para cima e da direita para a esquerda, ignorando as bordas
        for i in reversed(range(1, self.rows - 1)):
            for j in reversed(range(1, self.cols - 1)):
                p = self.grid[i][j]  # Partícula atual
                pd = self.grid[i + 1][j]  # Partícula abaixo
                pdl = self.grid[i + 1][j - 1]  # Partícula abaixo à esquerda
                pdr = self.grid[i + 1][j + 1]  # Partícula abaixo à direita

                # Se a partícula atual for areia
                if p == ParticleType.SAND:
                    # Verifica se a célula abaixo está vazia (ar)
                    if pd == ParticleType.AIR:
                        new_grid[i][j] = ParticleType.AIR
                        new_grid[i + 1][j] = ParticleType.SAND

                    # Verifica se a célula abaixo contém areia
                    if pd == ParticleType.SAND:
                        # Verifica se a célula abaixo à esquerda está vazia
                        if pdl == ParticleType.AIR:
                            new_grid[i][j] = ParticleType.AIR
                            new_grid[i + 1][j - 1] = ParticleType.SAND
                        # Verifica se a célula abaixo à direita está vazia
                        elif pdr == ParticleType.AIR:
                            new_grid[i][j] = ParticleType.AIR
                            new_grid[i + 1][j + 1] = ParticleType.SAND

                        # Verificação adicional para evitar colisões com limites
                        elif j > 2 and j < self.cols - 2:
                            pdll = self.grid[i + 1][j - 2]  # Partícula abaixo duas colunas à esquerda
                            pdrr = self.grid[i + 1][j + 2]  # Partícula abaixo duas colunas à direita

                            # Verifica se a célula abaixo duas colunas à esquerda está vazia
                            if pdll == ParticleType.AIR:
                                new_grid[i][j] = ParticleType.AIR
                                new_grid[i + 1][j - 2] = ParticleType.SAND

                            # Verifica se a célula abaixo duas colunas à direita está vazia
                            if pdrr == ParticleType.AIR:
                                new_grid[i][j] = ParticleType.AIR
                                new_grid[i + 1][j + 2] = ParticleType.SAND

        # Atualiza a grade com o novo estado após a iteração
        self.grid = new_grid
        return self.grid

    # Reseta a grade para o estado inicial
    def reset(self):
        self.grid = deepcopy(self.start_grid)
