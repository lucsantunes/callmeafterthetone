"""
Interface principal do jogo
"""

import pyxel
from typing import List, Dict, Tuple
from core.constants import *


class GameInterface:
    """Interface principal do jogo."""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Áreas da interface
        self.game_area_width = screen_width - UI_PANEL_WIDTH  # Área do jogo (esquerda)
        self.game_area_height = screen_height - STATUS_HEIGHT  # Área do jogo (superior)
        
        # Chat (lado direito)
        self.chat_x = self.game_area_width
        self.chat_y = 0
        self.chat_width = UI_PANEL_WIDTH
        self.chat_height = screen_height
        
        # Status (inferior esquerda)
        self.status_x = 0
        self.status_y = self.game_area_height
        self.status_width = self.game_area_width // 3
        self.status_height = STATUS_HEIGHT
        
        # Ações (inferior meio)
        self.actions_x = self.status_width
        self.actions_y = self.game_area_height
        self.actions_width = self.game_area_width // 3
        self.actions_height = STATUS_HEIGHT
        
        # Inventário resumido (inferior direita)
        self.inventory_x = self.actions_x + self.actions_width
        self.inventory_y = self.game_area_height
        self.inventory_width = self.game_area_width // 3
        self.inventory_height = STATUS_HEIGHT
        
        # Botões de ação
        self.action_buttons = [
            {"text": "Mover", "key": "M", "action": ACTION_MOVE},
            {"text": "Atacar", "key": "A", "action": ACTION_ATTACK},
            {"text": "Usar Item", "key": "I", "action": ACTION_USE_ITEM},
            {"text": "Descansar", "key": "R", "action": ACTION_REST},
            {"text": "Inventário", "key": "TAB", "action": ACTION_OPEN_INVENTORY}
        ]
    
    def draw(self, game_state):
        """Desenha a interface completa."""
        # Limpa a tela
        pyxel.cls(COLOR_BLACK)
        
        # Desenha área do jogo
        self._draw_game_area(game_state)
        
        # Desenha chat
        self._draw_chat(game_state)
        
        # Desenha status
        self._draw_status(game_state)
        
        # Desenha ações
        self._draw_actions(game_state)
        
        # Desenha inventário resumido
        self._draw_inventory_summary(game_state)
    
    def _draw_game_area(self, game_state):
        """Desenha a área principal do jogo."""
        # Desenha o mapa
        map_data = game_state.get_map_data()
        player_x, player_y = game_state.player.get_position()
        
        # Calcula offset da câmera para centralizar o jogador
        camera_x = max(0, min(player_x - self.game_area_width // 2, len(map_data[0]) - self.game_area_width))
        camera_y = max(0, min(player_y - self.game_area_height // 2, len(map_data) - self.game_area_height))
        
        # Desenha o mapa visível
        for y in range(self.game_area_height):
            for x in range(self.game_area_width):
                map_x = camera_x + x
                map_y = camera_y + y
                
                if (0 <= map_x < len(map_data[0]) and 
                    0 <= map_y < len(map_data)):
                    
                    cell = map_data[map_y][map_x]
                    
                    if cell == CELL_WALL:
                        pyxel.pset(x, y, COLOR_GRAY)
                    elif cell == CELL_FLOOR:
                        pyxel.pset(x, y, COLOR_BROWN)
                    elif cell == CELL_CORRIDOR:
                        pyxel.pset(x, y, COLOR_BROWN)
        
        # Desenha o jogador
        player_screen_x = player_x - camera_x
        player_screen_y = player_y - camera_y
        
        if (0 <= player_screen_x < self.game_area_width and 
            0 <= player_screen_y < self.game_area_height):
            pyxel.pset(player_screen_x, player_screen_y, COLOR_RED)
    
    def _draw_chat(self, game_state):
        """Desenha o chat de eventos."""
        # Fundo do chat
        pyxel.rect(self.chat_x, self.chat_y, self.chat_width, self.chat_height, COLOR_DARK_BLUE)
        
        # Título do chat
        pyxel.text(self.chat_x + 5, 5, "Chat do Mestre", COLOR_WHITE)
        
        # Linha separadora
        pyxel.line(self.chat_x, 15, self.chat_x + self.chat_width - 1, 15, COLOR_WHITE)
        
        # Mensagens do chat
        messages = game_state.get_recent_chat_messages(15)
        y_offset = 20
        
        for message in messages:
            sender = message['sender']
            text = message['message']
            
            # Nome do remetente
            pyxel.text(self.chat_x + 5, y_offset, f"{sender}:", COLOR_YELLOW)
            
            # Quebra o texto em linhas
            words = text.split()
            line = ""
            line_y = y_offset + 8
            
            for word in words:
                if len(line + word) < 25:  # Limite de caracteres por linha
                    line += word + " "
                else:
                    pyxel.text(self.chat_x + 5, line_y, line, COLOR_WHITE)
                    line = word + " "
                    line_y += 8
            
            if line:
                pyxel.text(self.chat_x + 5, line_y, line, COLOR_WHITE)
            
            y_offset = line_y + 12
            
            if y_offset > self.chat_height - 20:
                break
    
    def _draw_status(self, game_state):
        """Desenha o status do jogador."""
        # Fundo do status
        pyxel.rect(self.status_x, self.status_y, self.status_width, self.status_height, COLOR_NAVY)
        
        # Informações do jogador
        status = game_state.get_player_status()
        
        # HP
        hp_text = f"HP: {status['hp']}/{status['max_hp']}"
        pyxel.text(self.status_x + 5, self.status_y + 5, hp_text, COLOR_WHITE)
        
        # Barra de HP
        hp_percentage = status['hp_percentage']
        hp_bar_width = int((self.status_width - 10) * hp_percentage)
        pyxel.rect(self.status_x + 5, self.status_y + 15, hp_bar_width, 8, COLOR_RED)
        pyxel.rect(self.status_x + 5, self.status_y + 15, self.status_width - 10, 8, COLOR_GRAY)
        
        # Level e XP
        level_text = f"Level: {status['level']}"
        pyxel.text(self.status_x + 5, self.status_y + 30, level_text, COLOR_WHITE)
        
        xp_text = f"XP: {status['experience']}"
        pyxel.text(self.status_x + 5, self.status_y + 40, xp_text, COLOR_WHITE)
        
        # Ouro
        gold_text = f"Ouro: {status['gold']}"
        pyxel.text(self.status_x + 5, self.status_y + 50, gold_text, COLOR_YELLOW)
    
    def _draw_actions(self, game_state):
        """Desenha as ações disponíveis."""
        # Fundo das ações
        pyxel.rect(self.actions_x, self.actions_y, self.actions_width, self.actions_height, COLOR_PURPLE)
        
        # Título
        pyxel.text(self.actions_x + 5, self.actions_y + 5, "Ações", COLOR_WHITE)
        
        # Botões de ação
        button_y = self.actions_y + 20
        for i, button in enumerate(self.action_buttons):
            if i < 3:  # Mostra apenas 3 botões por vez
                # Fundo do botão
                button_color = COLOR_GREEN if game_state.player.can_perform_action(button["action"]) else COLOR_GRAY
                pyxel.rect(self.actions_x + 5, button_y, self.actions_width - 10, 20, button_color)
                
                # Texto do botão
                pyxel.text(self.actions_x + 10, button_y + 5, button["text"], COLOR_WHITE)
                pyxel.text(self.actions_x + 10, button_y + 15, f"({button['key']})", COLOR_WHITE)
                
                button_y += 25
    
    def _draw_inventory_summary(self, game_state):
        """Desenha o resumo do inventário."""
        # Fundo do inventário
        pyxel.rect(self.inventory_x, self.inventory_y, self.inventory_width, self.inventory_height, COLOR_BROWN)
        
        # Título
        pyxel.text(self.inventory_x + 5, self.inventory_y + 5, "Inventário", COLOR_WHITE)
        
        # Itens disponíveis (simulação - será implementado depois)
        items = ["Espada", "Poção"]  # Placeholder
        
        item_y = self.inventory_y + 20
        for i, item in enumerate(items[:2]):  # Mostra apenas 2 itens
            pyxel.text(self.inventory_x + 5, item_y, f"{i+1}. {item}", COLOR_WHITE)
            item_y += 15
        
        # Botão para abrir inventário completo
        pyxel.rect(self.inventory_x + 5, self.inventory_y + 50, self.inventory_width - 10, 20, COLOR_GREEN)
        pyxel.text(self.inventory_x + 10, self.inventory_y + 55, "Abrir Inventário", COLOR_WHITE)
    
    def handle_click(self, x: int, y: int) -> str:
        """Processa cliques na interface."""
        # Verifica cliques na área do jogo (movimento)
        if (0 <= x < self.game_area_width and 0 <= y < self.game_area_height):
            return ACTION_MOVE
        
        # Verifica cliques nos botões de ação
        if (self.actions_y <= y <= self.actions_y + self.actions_height and
            self.actions_x <= x <= self.actions_x + self.actions_width):
            
            button_y = self.actions_y + 20
            for i, button in enumerate(self.action_buttons[:3]):
                if (button_y <= y <= button_y + 20 and
                    self.actions_x + 5 <= x <= self.actions_x + self.actions_width - 5):
                    return button["action"]
                button_y += 25
        
        # Verifica clique no botão do inventário
        if (self.inventory_y + 50 <= y <= self.inventory_y + 70 and
            self.inventory_x + 5 <= x <= self.inventory_x + self.inventory_width - 5):
            return ACTION_OPEN_INVENTORY
        
        return None 