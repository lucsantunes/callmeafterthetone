import pyxel
from core.game_state import GameState
from ui.interface import GameInterface
from core.constants import *

# Configurações da tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Call Me After The Tone - D&D Haunted Mansion")
        pyxel.mouse(True)
        
        # Inicializa o estado do jogo
        self.game_state = GameState(60, 60)
        
        # Inicializa a interface
        self.interface = GameInterface(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # Atualiza o estado do jogo
        self.game_state.update()
        
        # Processa apenas cliques do mouse
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            action = self.interface.handle_click(x, y)
            if action:
                self.game_state.handle_mouse_action(action, x, y)
    
    def draw(self):
        # Desenha a interface baseada no estado atual
        if self.game_state.current_state == GAME_STATE_MENU:
            self._draw_menu()
        elif self.game_state.current_state == GAME_STATE_PLAYING:
            self._draw_game()
        elif self.game_state.current_state == GAME_STATE_PAUSE:
            self._draw_pause()
        elif self.game_state.current_state == GAME_STATE_GAME_OVER:
            self._draw_game_over()
    
    def _draw_menu(self):
        """Desenha o menu inicial."""
        pyxel.cls(COLOR_BLACK)
        
        # Título
        title = "Call Me After The Tone"
        subtitle = "D&D Haunted Mansion"
        
        # Desenha título maior
        title_x = SCREEN_WIDTH // 2 - len(title) * 6 // 2
        subtitle_x = SCREEN_WIDTH // 2 - len(subtitle) * 6 // 2
        
        for i, char in enumerate(title):
            pyxel.text(title_x + i * 6, SCREEN_HEIGHT // 2 - 50, char, COLOR_WHITE)
        
        for i, char in enumerate(subtitle):
            pyxel.text(subtitle_x + i * 6, SCREEN_HEIGHT // 2 - 30, char, COLOR_YELLOW)
        
        # Botão para começar
        button_x = SCREEN_WIDTH // 2 - 100
        button_y = SCREEN_HEIGHT // 2 + 10
        button_width = 200
        button_height = 40
        
        pyxel.rect(button_x, button_y, button_width, button_height, COLOR_GREEN)
        
        # Texto do botão maior
        button_text = "COMEÇAR"
        button_text_x = SCREEN_WIDTH // 2 - len(button_text) * 6 // 2
        for i, char in enumerate(button_text):
            pyxel.text(button_text_x + i * 6, button_y + 15, char, COLOR_WHITE)
        
        # Instruções
        instructions = "Clique no botão para começar"
        instructions_x = SCREEN_WIDTH // 2 - len(instructions) * 6 // 2
        for i, char in enumerate(instructions):
            pyxel.text(instructions_x + i * 6, button_y + 60, char, COLOR_WHITE)
    
    def _draw_game(self):
        """Desenha o jogo."""
        self.interface.draw(self.game_state)
    
    def _draw_pause(self):
        """Desenha o menu de pausa."""
        # Desenha o jogo em segundo plano
        self.interface.draw(self.game_state)
        
        # Overlay de pausa
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLACK)
        pyxel.rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, COLOR_DARK_BLUE)
        
        # Texto de pausa
        pause_text = "PAUSA"
        pause_x = SCREEN_WIDTH // 2 - len(pause_text) * 6 // 2
        for i, char in enumerate(pause_text):
            pyxel.text(pause_x + i * 6, SCREEN_HEIGHT // 2 - 20, char, COLOR_WHITE)
        
        # Botão continuar
        button_x = SCREEN_WIDTH // 2 - 50
        button_y = SCREEN_HEIGHT // 2 + 5
        pyxel.rect(button_x, button_y, 100, 25, COLOR_GREEN)
        
        continue_text = "Continuar"
        continue_x = SCREEN_WIDTH // 2 - len(continue_text) * 6 // 2
        for i, char in enumerate(continue_text):
            pyxel.text(continue_x + i * 6, button_y + 8, char, COLOR_WHITE)
        
        # Botão sair
        button_y2 = SCREEN_HEIGHT // 2 + 30
        pyxel.rect(button_x, button_y2, 100, 25, COLOR_RED)
        
        quit_text = "Sair"
        quit_x = SCREEN_WIDTH // 2 - len(quit_text) * 6 // 2
        for i, char in enumerate(quit_text):
            pyxel.text(quit_x + i * 6, button_y2 + 8, char, COLOR_WHITE)
    
    def _draw_game_over(self):
        """Desenha a tela de game over."""
        pyxel.cls(COLOR_BLACK)
        
        # Título
        game_over_text = "GAME OVER"
        game_over_x = SCREEN_WIDTH // 2 - len(game_over_text) * 6 // 2
        for i, char in enumerate(game_over_text):
            pyxel.text(game_over_x + i * 6, SCREEN_HEIGHT // 2 - 50, char, COLOR_RED)
        
        # Botão recomeçar
        button_x = SCREEN_WIDTH // 2 - 100
        button_y = SCREEN_HEIGHT // 2 - 10
        pyxel.rect(button_x, button_y, 200, 40, COLOR_GREEN)
        
        restart_text = "Recomeçar"
        restart_x = SCREEN_WIDTH // 2 - len(restart_text) * 6 // 2
        for i, char in enumerate(restart_text):
            pyxel.text(restart_x + i * 6, button_y + 15, char, COLOR_WHITE)
        
        # Botão sair
        button_y2 = SCREEN_HEIGHT // 2 + 30
        pyxel.rect(button_x, button_y2, 200, 40, COLOR_RED)
        
        quit_text = "Sair"
        quit_x = SCREEN_WIDTH // 2 - len(quit_text) * 6 // 2
        for i, char in enumerate(quit_text):
            pyxel.text(quit_x + i * 6, button_y2 + 15, char, COLOR_WHITE)

if __name__ == "__main__":
    App() 