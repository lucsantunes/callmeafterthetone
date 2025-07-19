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
        pyxel.text(SCREEN_WIDTH // 2 - len(title) * 3, SCREEN_HEIGHT // 2 - 50, title, COLOR_WHITE)
        pyxel.text(SCREEN_WIDTH // 2 - len(subtitle) * 3, SCREEN_HEIGHT // 2 - 30, subtitle, COLOR_YELLOW)
        
        # Botão para começar
        button_x = SCREEN_WIDTH // 2 - 100
        button_y = SCREEN_HEIGHT // 2 + 10
        button_width = 200
        button_height = 40
        
        pyxel.rect(button_x, button_y, button_width, button_height, COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH // 2 - 30, button_y + 15, "COMEÇAR", COLOR_WHITE)
        
        # Instruções
        instructions = "Clique no botão para começar"
        pyxel.text(SCREEN_WIDTH // 2 - len(instructions) * 3, button_y + 60, instructions, COLOR_WHITE)
    
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
        pyxel.text(SCREEN_WIDTH // 2 - len(pause_text) * 3, SCREEN_HEIGHT // 2 - 20, pause_text, COLOR_WHITE)
        
        # Botão continuar
        button_x = SCREEN_WIDTH // 2 - 50
        button_y = SCREEN_HEIGHT // 2 + 5
        pyxel.rect(button_x, button_y, 100, 20, COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH // 2 - 25, button_y + 5, "Continuar", COLOR_WHITE)
        
        # Botão sair
        button_y2 = SCREEN_HEIGHT // 2 + 25
        pyxel.rect(button_x, button_y2, 100, 20, COLOR_RED)
        pyxel.text(SCREEN_WIDTH // 2 - 15, button_y2 + 5, "Sair", COLOR_WHITE)
    
    def _draw_game_over(self):
        """Desenha a tela de game over."""
        pyxel.cls(COLOR_BLACK)
        
        # Título
        game_over_text = "GAME OVER"
        pyxel.text(SCREEN_WIDTH // 2 - len(game_over_text) * 3, SCREEN_HEIGHT // 2 - 50, game_over_text, COLOR_RED)
        
        # Botão recomeçar
        button_x = SCREEN_WIDTH // 2 - 100
        button_y = SCREEN_HEIGHT // 2 - 10
        pyxel.rect(button_x, button_y, 200, 40, COLOR_GREEN)
        pyxel.text(SCREEN_WIDTH // 2 - 40, button_y + 15, "Recomeçar", COLOR_WHITE)
        
        # Botão sair
        button_y2 = SCREEN_HEIGHT // 2 + 30
        pyxel.rect(button_x, button_y2, 200, 40, COLOR_RED)
        pyxel.text(SCREEN_WIDTH // 2 - 20, button_y2 + 15, "Sair", COLOR_WHITE)

if __name__ == "__main__":
    App() 