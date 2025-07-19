"""
Classe do jogador
"""

from typing import Tuple, List, Dict, Optional
from .constants import *


class Player:
    """Representa o jogador no jogo."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = PLAYER_START_HP
        self.max_hp = PLAYER_MAX_HP
        self.attack_damage = PLAYER_ATTACK_DAMAGE
        self.defense = PLAYER_DEFENSE
        self.level = 1
        self.experience = 0
        self.gold = 0
        
        # Status temporários
        self.status_effects = {}
        
        # Inventário (será expandido)
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        
        # Sistema turn-based
        self.actions_remaining = 1  # Ações restantes no turno
        self.max_actions_per_turn = 1
    
    def move(self, new_x: int, new_y: int) -> bool:
        """Move o jogador para uma nova posição."""
        if self.actions_remaining > 0:
            self.x = new_x
            self.y = new_y
            self.actions_remaining -= 1
            return True
        return False
    
    def take_damage(self, damage: int) -> int:
        """Aplica dano ao jogador."""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """Cura o jogador."""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def is_alive(self) -> bool:
        """Verifica se o jogador está vivo."""
        return self.hp > 0
    
    def get_hp_percentage(self) -> float:
        """Retorna a porcentagem de HP."""
        return self.hp / self.max_hp
    
    def get_position(self) -> Tuple[int, int]:
        """Retorna a posição atual do jogador."""
        return (self.x, self.y)
    
    def add_experience(self, amount: int):
        """Adiciona experiência ao jogador."""
        self.experience += amount
        # TODO: Implementar sistema de level up
    
    def add_gold(self, amount: int):
        """Adiciona ouro ao jogador."""
        self.gold += amount
    
    def get_status_summary(self) -> Dict[str, any]:
        """Retorna um resumo do status do jogador."""
        return {
            'hp': self.hp,
            'max_hp': self.max_hp,
            'hp_percentage': self.get_hp_percentage(),
            'level': self.level,
            'experience': self.experience,
            'gold': self.gold,
            'attack_damage': self.attack_damage,
            'defense': self.defense,
            'is_alive': self.is_alive(),
            'actions_remaining': self.actions_remaining,
            'max_actions_per_turn': self.max_actions_per_turn
        }
    
    def can_perform_action(self, action: str) -> bool:
        """Verifica se o jogador pode realizar uma ação."""
        if not self.is_alive():
            return False
        
        # Verifica se tem ações restantes
        if self.actions_remaining <= 0:
            return False
        
        # Verificações específicas por ação
        if action == ACTION_MOVE:
            return True
        elif action == ACTION_ATTACK:
            return True
        elif action == ACTION_USE_ITEM:
            return len(self.inventory) > 0
        elif action == ACTION_REST:
            return self.hp < self.max_hp
        elif action == ACTION_OPEN_INVENTORY:
            return True  # Sempre pode abrir inventário
        
        return True
    
    def get_available_actions(self) -> List[str]:
        """Retorna as ações disponíveis para o jogador."""
        actions = [ACTION_OPEN_INVENTORY]  # Sempre disponível
        
        if self.is_alive() and self.actions_remaining > 0:
            actions.extend([ACTION_MOVE, ACTION_ATTACK])
            
            if len(self.inventory) > 0:
                actions.append(ACTION_USE_ITEM)
            
            if self.hp < self.max_hp:
                actions.append(ACTION_REST)
        
        return actions
    
    def start_turn(self):
        """Inicia o turno do jogador."""
        self.actions_remaining = self.max_actions_per_turn
    
    def end_turn(self):
        """Finaliza o turno do jogador."""
        self.actions_remaining = 0
    
    def has_actions_remaining(self) -> bool:
        """Verifica se o jogador ainda tem ações restantes."""
        return self.actions_remaining > 0 