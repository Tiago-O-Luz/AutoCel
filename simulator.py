"""
Para rodar salve o código em um arquivo "main.py" e use o comando:
    python3 main.py

É necessário ter instalado a biblioteca tkinter do python:
    pip install python
ou
    python3 -m pip install python

O simulador possui botões de start (inicia interações), stop (pausa interações) e reset (elimina todas as celulas)
Para desenhar células basta clicar com o botão esquerdo do mouse e arrastar pela tela
"""


import time
import tkinter as tk
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
                        if new_grid[i+1][j] == ParticleType.AIR:
                            new_grid[i][j] = ParticleType.AIR
                            new_grid[i + 1][j] = ParticleType.SAND    
                        # Verifica se a célula abaixo à esquerda está vazia
                        elif pdl == ParticleType.AIR:
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

# Classe responsável pela interface gráfica do autômato de areia
class Display:
    def __init__(self, root, rows=10, cols=10, cell_size=40):
        # Inicialização dos parâmetros
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        
        # Instância do autômato de areia
        self.simulator = SandAutomaton(rows, cols)
        self.running = False  # Flag para controle do estado de execução
        
        # Configuração dos elementos da interface
        self.btn_frame = tk.Frame(root)
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, background="black")
        
        # Botões de controle
        self.start_btn = tk.Button(self.btn_frame, text="START", command=self.start, background="green", foreground="white")
        self.stop_btn = tk.Button(self.btn_frame, text="STOP", command=self.stop, background="red", foreground="white")
        self.reset_btn = tk.Button(self.btn_frame, text="RESET", command=self.reset, background="blue", foreground="white")
        
        # Posicionamento dos botões
        self.start_btn.pack(side="left")
        self.stop_btn.pack(side="left")
        self.reset_btn.pack(side="left")
        self.btn_frame.pack()
        self.canvas.pack()
        
        # Eventos de clique e movimento do mouse
        self.b1bind = self.canvas.bind("<Button-1>", self.set_b1_pressed)  # Clique esquerdo
        self.b1bind = self.canvas.bind("<ButtonRelease-1>", self.set_b1_released)  # Soltar clique esquerdo
        self.b2bind = self.canvas.bind("<Button-2>", self.reset_canvas)  # Clique do meio para resetar o canvas
        self.mbind = self.canvas.bind("<Motion>", self.set_add_particle_pos)  # Movimento do mouse
        
        self.b1_pressed = False  # Flag para controle do clique esquerdo
        self.draw_particles(self.simulator.grid)  # Desenha as partículas iniciais
        self.loop()  # Inicia o loop de atualização

    # Desenha um quadrado na posição especificada com a cor definida
    def draw_square(self, row, col, color):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    # Desenha todas as partículas presentes na grade do autômato
    def draw_particles(self, grid):
        self.reset_canvas()  # Limpa o canvas antes de desenhar
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] != ParticleType.AIR:  # Desenha apenas partículas diferentes de ar
                    self.draw_square(i, j, grid[i][j].value)

    # Limpa o canvas removendo todos os elementos desenhados
    def reset_canvas(self):
        self.canvas.delete("all")

    # Loop de atualização contínua
    def loop(self):
        if self.running:  # Se o autômato estiver em execução
            grid = self.simulator.run_iteration()  # Executa uma iteração do autômato
            self.draw_particles(grid)  # Atualiza o desenho das partículas
            print(f"finished interaction")  # Mensagem de debug
        if self.b1_pressed:  # Se o botão esquerdo do mouse estiver pressionado
            self.handle_add_particle()  # Adiciona uma partícula na posição do mouse
        self.canvas.after(16, self.loop)  # Atualiza a cada 16ms (~60 FPS)

    # Inicia a execução do autômato
    def start(self):
        self.running = True

    # Para a execução do autômato
    def stop(self):
        self.running = False

    # Reseta o canvas e o estado do autômato, se não estiver em execução
    def reset(self):
        if not self.running:
            self.reset_canvas()
            self.simulator.reset()
            self.draw_particles(self.simulator.grid)

    # Adiciona uma partícula de areia na posição atual do mouse
    def handle_add_particle(self):
        x = self.add_particle_pos.x
        y = self.add_particle_pos.y
        row = x // self.cell_size  # Calcula a linha correspondente na grade
        col = y // self.cell_size  # Calcula a coluna correspondente na grade
        self.simulator.add_particle(col, row)  # Adiciona a partícula no autômato
        self.draw_square(col, row, ParticleType.SAND.value)  # Desenha a partícula no canvas
    
    # Define o estado de clique esquerdo como pressionado
    def set_b1_pressed(self, e):
        self.set_add_particle_pos(e)  # Atualiza a posição para adição de partícula
        self.b1_pressed = True

    # Define o estado de clique esquerdo como solto
    def set_b1_released(self, e):
        self.b1_pressed = False
    
    # Atualiza a posição do mouse para adicionar uma partícula
    def set_add_particle_pos(self, e):
        self.add_particle_pos = e

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulator")
    app = Display(root, 100, 100, 5)
    root.mainloop()