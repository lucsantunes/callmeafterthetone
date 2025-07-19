"""
Map Generator Module
====================

Este módulo é responsável pela geração de mapas para o jogo.
Futuramente será expandido para incluir geração procedural de dungeons
estilo Dungeons & Dragons.

Estrutura do mapa:
- 0: Vazio (área transitável)
- 1: Parede (bloqueia movimento)
- 2: Porta
- 3: Área especial (futuro)
"""

import random
from typing import List, Tuple, Optional


class MapGenerator:
    """
    Classe responsável pela geração de mapas.
    """
    
    def __init__(self, map_width: int, map_height: int):
        """
        Inicializa o gerador de mapas.
        
        Args:
            map_width: Largura do mapa em células
            map_height: Altura do mapa em células
        """
        self.map_width = map_width
        self.map_height = map_height
        self.map_data = []
        
    def generate_simple_map(self) -> List[List[int]]:
        """
        Gera um mapa simples com paredes nas bordas.
        Esta é a implementação atual do main.py.
        
        Returns:
            Lista 2D representando o mapa (0 = vazio, 1 = parede)
        """
        # Inicializa o mapa com zeros (vazio)
        self.map_data = [[0 for _ in range(self.map_width)] 
                        for _ in range(self.map_height)]
        
        # Adiciona paredes nas bordas
        for x in range(self.map_width):
            self.map_data[0][x] = 1  # Parede superior
            self.map_data[self.map_height - 1][x] = 1  # Parede inferior
            
        for y in range(self.map_height):
            self.map_data[y][0] = 1  # Parede esquerda
            self.map_data[y][self.map_width - 1] = 1  # Parede direita
            
        return self.map_data
    
    def get_map_data(self) -> List[List[int]]:
        """
        Retorna os dados do mapa atual.
        
        Returns:
            Lista 2D representando o mapa
        """
        return self.map_data
    
    def is_wall(self, x: int, y: int) -> bool:
        """
        Verifica se a posição (x, y) é uma parede.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            
        Returns:
            True se é parede, False caso contrário
        """
        if not self.is_valid_position(x, y):
            return True  # Posições fora do mapa são consideradas paredes
        return self.map_data[y][x] == 1
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Verifica se a posição está dentro dos limites do mapa.
        
        Args:
            x: Coordenada X
            y: Coordenada Y
            
        Returns:
            True se a posição é válida, False caso contrário
        """
        return 0 <= x < self.map_width and 0 <= y < self.map_height
    
    def get_map_size(self) -> Tuple[int, int]:
        """
        Retorna as dimensões do mapa.
        
        Returns:
            Tupla (largura, altura) do mapa
        """
        return self.map_width, self.map_height


# Funções auxiliares para uso futuro
def create_dungeon_generator(map_width: int, map_height: int) -> MapGenerator:
    """
    Factory function para criar um gerador de dungeons.
    Futuramente será expandida para diferentes tipos de geração.
    
    Args:
        map_width: Largura do mapa
        map_height: Altura do mapa
        
    Returns:
        Instância de MapGenerator configurada
    """
    return MapGenerator(map_width, map_height)


# Constantes para tipos de células (futuro)
CELL_EMPTY = 0
CELL_WALL = 1
CELL_DOOR = 2
CELL_FLOOR = 3
CELL_CORRIDOR = 4
CELL_ROOM = 5 