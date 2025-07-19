"""
Estado global do jogo
"""

from typing import List, Dict, Optional, Tuple
from .player import Player
from .constants import *
from maps.map_generator import HauntedMansionGenerator

# Constantes da tela (importadas do main.py)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class GameState:
    """Gerencia o estado global do jogo."""
    
    def __init__(self, map_width: int, map_height: int):
        self.map_width = map_width
        self.map_height = map_height
        
        # Gerador de mapa
        self.map_generator = HauntedMansionGenerator(map_width, map_height)
        self.map_data = []
        
        # Jogador
        self.player = None
        
        # Estado do jogo
        self.current_state = GAME_STATE_MENU
        self.current_ui = UI_NORMAL
        self.game_running = True
        
        # Sistema turn-based
        self.current_turn = TURN_PLAYER
        
        # Eventos e mensagens
        self.event_log = []
        self.chat_messages = []
        
        # Inicializa o jogo
        self._initialize_game()
    
    def _initialize_game(self):
        """Inicializa o jogo."""
        # Gera o mapa
        self.map_data = self.map_generator.generate_mansion(
            num_rooms=8,
            max_connection_distance=15,
            corridor_width=3
        )
        
        # Cria o jogador em uma posição válida
        spawn_x, spawn_y = self.map_generator.find_valid_spawn_position()
        self.player = Player(spawn_x, spawn_y)
        
        # Adiciona mensagem inicial
        self.add_chat_message("Mestre da Dungeon", "Bem-vindo à mansão mal assombrada! Explore com cuidado...")
        
        # Inicia o jogo
        self.current_state = GAME_STATE_PLAYING
        self.player.start_turn()
    
    def update(self):
        """Atualiza o estado do jogo."""
        # Verifica se o jogo acabou
        if self.player.hp <= 0:
            self.current_state = GAME_STATE_GAME_OVER
            self.add_chat_message("Sistema", "Você morreu! Game Over!")
            return
        
        # Sistema turn-based
        if self.current_state == GAME_STATE_PLAYING:
            if self.current_turn == TURN_PLAYER:
                # Vez do jogador
                if not self.player.has_actions_remaining():
                    self._end_player_turn()
            else:
                # Vez do mestre (será implementado depois)
                self._master_turn()
    
    def handle_mouse_action(self, action: str, x: int, y: int) -> bool:
        """Processa ações do mouse."""
        if self.current_state == GAME_STATE_MENU:
            return self._handle_menu_mouse(x, y)
        elif self.current_state == GAME_STATE_PLAYING:
            return self._handle_playing_mouse(action, x, y)
        elif self.current_state == GAME_STATE_PAUSE:
            return self._handle_pause_mouse(x, y)
        elif self.current_state == GAME_STATE_GAME_OVER:
            return self._handle_game_over_mouse(x, y)
        
        return False
    
    def _handle_menu_mouse(self, x: int, y: int) -> bool:
        """Processa cliques no menu inicial."""
        # Botão para começar o jogo (área central da tela)
        if (SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and
            SCREEN_HEIGHT // 2 + 10 <= y <= SCREEN_HEIGHT // 2 + 50):
            self.current_state = GAME_STATE_PLAYING
            self.player.start_turn()
            return True
        return False
    
    def _handle_playing_mouse(self, action: str, x: int, y: int) -> bool:
        """Processa cliques durante o jogo."""
        if self.current_turn != TURN_PLAYER:
            return False
        
        # Processa ações dos botões
        if action == ACTION_MOVE:
            return self._try_move_to_position(x, y)
        elif action == ACTION_ATTACK:
            return self._try_attack()
        elif action == ACTION_USE_ITEM:
            return self._try_use_item()
        elif action == ACTION_REST:
            return self._try_rest()
        elif action == ACTION_OPEN_INVENTORY:
            self.current_ui = UI_INVENTORY
            return True
        
        return False
    
    def _handle_pause_mouse(self, x: int, y: int) -> bool:
        """Processa cliques no menu de pausa."""
        # Botão continuar
        if (SCREEN_WIDTH // 2 - 50 <= x <= SCREEN_WIDTH // 2 + 50 and
            SCREEN_HEIGHT // 2 + 5 <= y <= SCREEN_HEIGHT // 2 + 25):
            self.current_state = GAME_STATE_PLAYING
            return True
        # Botão sair
        elif (SCREEN_WIDTH // 2 - 50 <= x <= SCREEN_WIDTH // 2 + 50 and
              SCREEN_HEIGHT // 2 + 25 <= y <= SCREEN_HEIGHT // 2 + 45):
            self.current_state = GAME_STATE_MENU
            return True
        return False
    
    def _handle_game_over_mouse(self, x: int, y: int) -> bool:
        """Processa cliques no game over."""
        # Botão recomeçar
        if (SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and
            SCREEN_HEIGHT // 2 - 10 <= y <= SCREEN_HEIGHT // 2 + 30):
            self.restart_game()
            return True
        # Botão sair
        elif (SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and
              SCREEN_HEIGHT // 2 + 30 <= y <= SCREEN_HEIGHT // 2 + 70):
            self.game_running = False
            return True
        return False
    
    def _try_move_to_position(self, screen_x: int, screen_y: int) -> bool:
        """Tenta mover o jogador para uma posição clicada na tela."""
        if not self.player.can_perform_action(ACTION_MOVE):
            return False
        
        # Converte coordenadas da tela para coordenadas do mundo
        # Assumindo que a área do jogo está na esquerda da tela
        game_area_width = SCREEN_WIDTH - UI_PANEL_WIDTH
        game_area_height = SCREEN_HEIGHT - STATUS_HEIGHT
        
        # Calcula offset da câmera
        player_x, player_y = self.player.get_position()
        camera_x = max(0, min(player_x - game_area_width // 2, len(self.map_data[0]) - game_area_width))
        camera_y = max(0, min(player_y - game_area_height // 2, len(self.map_data) - game_area_height))
        
        # Converte coordenadas da tela para coordenadas do mapa
        map_x = camera_x + screen_x
        map_y = camera_y + screen_y
        
        # Verifica se a posição é válida
        if (0 <= map_x < self.map_width and 
            0 <= map_y < self.map_height and
            not self.map_generator.is_wall(map_x, map_y)):
            
            if self.player.move(map_x, map_y):
                self.add_chat_message("Sistema", f"Você se move para ({map_x}, {map_y})")
                return True
        
        return False
    
    def _try_move_player(self, dx: int, dy: int) -> bool:
        """Tenta mover o jogador."""
        if not self.player.can_perform_action(ACTION_MOVE):
            return False
        
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Verifica se a posição é válida
        if (0 <= new_x < self.map_width and 
            0 <= new_y < self.map_height and
            not self.map_generator.is_wall(new_x, new_y)):
            
            if self.player.move(new_x, new_y):
                self.add_chat_message("Sistema", f"Você se move para ({new_x}, {new_y})")
                return True
        
        return False
    
    def _try_attack(self) -> bool:
        """Tenta atacar."""
        if not self.player.can_perform_action(ACTION_ATTACK):
            return False
        
        self.player.actions_remaining -= 1
        self.add_chat_message("Sistema", "Você ataca o ar!")
        return True
    
    def _try_use_item(self) -> bool:
        """Tenta usar um item."""
        if not self.player.can_perform_action(ACTION_USE_ITEM):
            return False
        
        # TODO: Implementar seleção de item
        self.add_chat_message("Sistema", "Você usa um item!")
        self.player.actions_remaining -= 1
        return True
    
    def _try_rest(self) -> bool:
        """Tenta descansar."""
        if not self.player.can_perform_action(ACTION_REST):
            return False
        
        if self.player.hp < self.player.max_hp:
            heal_amount = min(10, self.player.max_hp - self.player.hp)
            self.player.heal(heal_amount)
            self.player.actions_remaining -= 1
            self.add_chat_message("Sistema", f"Você descansa e recupera {heal_amount} HP!")
        else:
            self.add_chat_message("Sistema", "Você já está com HP máximo!")
        return True
    
    def _end_player_turn(self):
        """Finaliza o turno do jogador."""
        self.player.end_turn()
        self.current_turn = TURN_MASTER
        self.add_chat_message("Sistema", "Turno do Mestre da Dungeon!")
    
    def _master_turn(self):
        """Executa o turno do mestre."""
        # TODO: Implementar IA do mestre
        self.add_chat_message("Mestre da Dungeon", "O mestre observa seus movimentos...")
        
        # Por enquanto, apenas passa o turno de volta para o jogador
        self.current_turn = TURN_PLAYER
        self.player.start_turn()
        self.add_chat_message("Sistema", "Seu turno!")
    
    def add_chat_message(self, sender: str, message: str):
        """Adiciona uma mensagem ao chat."""
        self.chat_messages.append({
            'sender': sender,
            'message': message,
            'timestamp': len(self.chat_messages)
        })
        
        # Limita o número de mensagens
        if len(self.chat_messages) > 50:
            self.chat_messages.pop(0)
    
    def add_event(self, event_type: str, description: str):
        """Adiciona um evento ao log."""
        self.event_log.append({
            'type': event_type,
            'description': description,
            'timestamp': len(self.event_log)
        })
    
    def get_map_data(self) -> List[List[int]]:
        """Retorna os dados do mapa."""
        return self.map_data
    
    def get_player_status(self) -> Dict[str, any]:
        """Retorna o status do jogador."""
        return self.player.get_status_summary()
    
    def get_recent_chat_messages(self, count: int = 10) -> List[Dict]:
        """Retorna as mensagens mais recentes do chat."""
        return self.chat_messages[-count:]
    
    def get_recent_events(self, count: int = 10) -> List[Dict]:
        """Retorna os eventos mais recentes."""
        return self.event_log[-count:]
    
    def is_game_over(self) -> bool:
        """Verifica se o jogo acabou."""
        return not self.player.is_alive()
    
    def restart_game(self):
        """Reinicia o jogo."""
        self._initialize_game()
        self.current_state = GAME_STATE_PLAYING
        self.current_ui = UI_NORMAL
        self.current_turn = TURN_PLAYER
        self.game_running = True 