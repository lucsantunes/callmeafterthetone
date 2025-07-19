import pyxel

# Tamanho de cada célula do grid em pixels
CELL_SIZE = 16
# Quantidade de células visíveis na tela
VISIBLE_CELLS_X = 20
VISIBLE_CELLS_Y = 20
# Tamanho total do mapa (maior que a tela)
MAP_SIZE_X = 60  # 3x maior que a tela
MAP_SIZE_Y = 60  # 3x maior que a tela
# Tamanho da tela em pixels
SCREEN_WIDTH = CELL_SIZE * VISIBLE_CELLS_X
SCREEN_HEIGHT = CELL_SIZE * VISIBLE_CELLS_Y + 64  # 64 pixels para a área de interface
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
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Grid Move - Mapa Maior")
        # Ativa o uso do mouse
        pyxel.mouse(True)
        # Posição inicial do jogador (dentro da sala, não na parede)
        self.player_pos = [1, 1]
        # Posição da câmera (inicialmente no canto superior esquerdo)
        self.camera_x = 0
        self.camera_y = 0
        # Inicia o loop principal do Pyxel
        pyxel.run(self.update, self.draw)

    def world_to_screen(self, world_x, world_y):
        """Converte coordenadas do mundo para coordenadas da tela"""
        screen_x = (world_x - self.camera_x) * CELL_SIZE
        screen_y = (world_y - self.camera_y) * CELL_SIZE
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        """Converte coordenadas da tela para coordenadas do mundo"""
        world_x = (screen_x // CELL_SIZE) + self.camera_x
        world_y = (screen_y // CELL_SIZE) + self.camera_y
        return world_x, world_y

    def update_camera(self):
        """Atualiza a posição da câmera para seguir o jogador"""
        # Calcula a posição ideal da câmera (jogador no centro da tela)
        target_camera_x = self.player_pos[0] - VISIBLE_CELLS_X // 2
        target_camera_y = self.player_pos[1] - VISIBLE_CELLS_Y // 2
        
        # Limita a câmera para não mostrar áreas vazias além do mapa
        self.camera_x = max(0, min(target_camera_x, MAP_SIZE_X - VISIBLE_CELLS_X))
        self.camera_y = max(0, min(target_camera_y, MAP_SIZE_Y - VISIBLE_CELLS_Y))

    def is_valid_move(self, target_x, target_y):
        """Verifica se o movimento é válido (dentro da área permitida e não é parede)"""
        # Verifica se está dentro do mapa (não é parede)
        if target_x < 1 or target_x >= MAP_SIZE_X-1 or target_y < 1 or target_y >= MAP_SIZE_Y-1:
            return False
        # Calcula a distância Manhattan (mais adequada para grid)
        distance = abs(target_x - self.player_pos[0]) + abs(target_y - self.player_pos[1])
        return distance <= MAX_MOVE_DISTANCE

    def get_valid_moves(self):
        """Retorna lista de posições válidas para movimento"""
        valid_moves = []
        # Só verifica células visíveis na tela para otimização
        start_x = max(0, self.camera_x)
        end_x = min(MAP_SIZE_X, self.camera_x + VISIBLE_CELLS_X)
        start_y = max(0, self.camera_y)
        end_y = min(MAP_SIZE_Y, self.camera_y + VISIBLE_CELLS_Y)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.is_valid_move(x, y):
                    valid_moves.append([x, y])
        return valid_moves

    def update(self):
        # Fecha o jogo se apertar Q
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # Atualiza a câmera para seguir o jogador
        self.update_camera()
        
        # Move o jogador ao clicar com o mouse
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # Converte coordenadas do mouse para coordenadas do mundo
            world_x, world_y = self.screen_to_world(mx, my)
            # Só move se o clique for em uma posição válida
            if self.is_valid_move(world_x, world_y):
                self.player_pos = [world_x, world_y]

    def draw(self):
        # Limpa a tela com a cor de fundo
        pyxel.cls(BG_COLOR)
        
        # Desenha as paredes ao redor do mapa (apenas as visíveis)
        for y in range(self.camera_y, self.camera_y + VISIBLE_CELLS_Y):
            for x in range(self.camera_x, self.camera_x + VISIBLE_CELLS_X):
                if x == 0 or x == MAP_SIZE_X-1 or y == 0 or y == MAP_SIZE_Y-1:
                    screen_x, screen_y = self.world_to_screen(x, y)
                    pyxel.rect(screen_x, screen_y, CELL_SIZE, CELL_SIZE, WALL_COLOR)
        
        # Desenha a área de movimento válida (apenas as visíveis)
        valid_moves = self.get_valid_moves()
        for pos in valid_moves:
            if pos != self.player_pos:  # Não desenha sobre o jogador
                screen_x, screen_y = self.world_to_screen(pos[0], pos[1])
                pyxel.rect(screen_x+1, screen_y+1, CELL_SIZE-2, CELL_SIZE-2, MOVE_AREA_COLOR)
        
        # Desenha o jogador como um quadrado menor dentro da célula
        player_screen_x, player_screen_y = self.world_to_screen(self.player_pos[0], self.player_pos[1])
        pyxel.rect(player_screen_x+2, player_screen_y+2, CELL_SIZE-4, CELL_SIZE-4, PLAYER_COLOR)
        
        # Desenha a área de interface na parte inferior
        interface_y = CELL_SIZE * VISIBLE_CELLS_Y
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