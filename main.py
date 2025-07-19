import pyxel

# Tamanho de cada célula do grid em pixels
CELL_SIZE = 16
# Quantidade de células do mapa (20x20)
MAP_SIZE = 20
# Tamanho da tela em pixels
SCREEN_WIDTH = CELL_SIZE * MAP_SIZE
SCREEN_HEIGHT = CELL_SIZE * MAP_SIZE + 64  # 64 pixels para a área de interface
# Cor do jogador
PLAYER_COLOR = 8
# Cor das paredes
WALL_COLOR = 7
# Cor de fundo
BG_COLOR = 0
# Área de movimento válida
MOVE_AREA_COLOR = 3
# Distância máxima de movimento
MAX_MOVE_DISTANCE = 3

class App:
    def __init__(self):
        # Inicializa a janela do Pyxel
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Grid Move")
        # Ativa o uso do mouse
        pyxel.mouse(True)
        # Posição inicial do jogador (dentro da sala, não na parede)
        self.player_pos = [1, 1]
        # Inicia o loop principal do Pyxel
        pyxel.run(self.update, self.draw)

    def is_valid_move(self, target_x, target_y):
        """Verifica se o movimento é válido (dentro da área permitida e não é parede)"""
        # Verifica se está dentro da sala (não é parede)
        if target_x < 1 or target_x >= MAP_SIZE-1 or target_y < 1 or target_y >= MAP_SIZE-1:
            return False
        # Calcula a distância Manhattan (mais adequada para grid)
        distance = abs(target_x - self.player_pos[0]) + abs(target_y - self.player_pos[1])
        return distance <= MAX_MOVE_DISTANCE

    def get_valid_moves(self):
        """Retorna lista de posições válidas para movimento"""
        valid_moves = []
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if self.is_valid_move(x, y):
                    valid_moves.append([x, y])
        return valid_moves

    def update(self):
        # Fecha o jogo se apertar Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Move o jogador ao clicar com o mouse
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # Converte coordenadas do mouse para coordenadas do grid
            grid_x = mx // CELL_SIZE
            grid_y = my // CELL_SIZE
            # Só move se o clique for em uma posição válida
            if self.is_valid_move(grid_x, grid_y):
                self.player_pos = [grid_x, grid_y]

    def draw(self):
        # Limpa a tela com a cor de fundo
        pyxel.cls(BG_COLOR)
        
        # Desenha a área de movimento válida
        valid_moves = self.get_valid_moves()
        for pos in valid_moves:
            if pos != self.player_pos:  # Não desenha sobre o jogador
                px = pos[0] * CELL_SIZE
                py = pos[1] * CELL_SIZE
                pyxel.rect(px+1, py+1, CELL_SIZE-2, CELL_SIZE-2, MOVE_AREA_COLOR)
        
        # Desenha as paredes ao redor da sala
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                if x == 0 or x == MAP_SIZE-1 or y == 0 or y == MAP_SIZE-1:
                    px = x * CELL_SIZE
                    py = y * CELL_SIZE
                    pyxel.rect(px, py, CELL_SIZE, CELL_SIZE, WALL_COLOR)
        
        # Desenha o jogador como um quadrado menor dentro da célula
        px = self.player_pos[0] * CELL_SIZE
        py = self.player_pos[1] * CELL_SIZE
        pyxel.rect(px+2, py+2, CELL_SIZE-4, CELL_SIZE-4, PLAYER_COLOR)
        
        # Desenha a área de interface na parte inferior
        interface_y = CELL_SIZE * MAP_SIZE
        interface_height = 64        
        # Área de status (esquerda)
        status_width = SCREEN_WIDTH // 3
        pyxel.rect(0, interface_y, status_width, interface_height, 5)
        
        # Área de ações (meio)
        actions_x = status_width
        actions_width = SCREEN_WIDTH // 3
        pyxel.rect(actions_x, interface_y, actions_width, interface_height, 4)
        
        # Área de inventário (direita)
        inventory_x = actions_x + actions_width
        inventory_width = SCREEN_WIDTH - inventory_x
        pyxel.rect(inventory_x, interface_y, inventory_width, interface_height, 2)

# Cria e executa o jogo
App() 