import tkinter as tk
import time
from enum import Enum
from sandautomaton import SandAutomaton, ParticleType

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
