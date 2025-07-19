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
import math
from typing import List, Tuple, Optional, Set


class Room:
    """Representa uma sala no dungeon."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def get_center(self) -> Tuple[int, int]:
        """Retorna o centro da sala."""
        return (self.x + self.width // 2, self.y + self.height // 2)
        
    def get_random_point(self) -> Tuple[int, int]:
        """Retorna um ponto aleatório dentro da sala."""
        return (
            random.randint(self.x + 1, self.x + self.width - 2),
            random.randint(self.y + 1, self.y + self.height - 2)
        )
        
    def intersects(self, other: 'Room') -> bool:
        """Verifica se esta sala intersecta com outra."""
        return not (self.x + self.width <= other.x or 
                   other.x + other.width <= self.x or
                   self.y + self.height <= other.y or 
                   other.y + other.height <= self.y)
    
    def distance_to(self, other: 'Room') -> int:
        """Calcula a distância mínima entre duas salas."""
        # Calcula a distância horizontal
        if self.x + self.width <= other.x:
            dx = other.x - (self.x + self.width)
        elif other.x + other.width <= self.x:
            dx = self.x - (other.x + other.width)
        else:
            dx = 0  # Salas se sobrepõem horizontalmente
        
        # Calcula a distância vertical
        if self.y + self.height <= other.y:
            dy = other.y - (self.y + self.height)
        elif other.y + other.height <= self.y:
            dy = self.y - (other.y + other.height)
        else:
            dy = 0  # Salas se sobrepõem verticalmente
        
        # Retorna a distância mínima (Manhattan)
        return dx + dy


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
        cell_type = self.map_data[y][x]
        # Apenas paredes bloqueiam movimento (corredores e pisos são transitáveis)
        return cell_type == CELL_WALL
    
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
    
    def find_valid_spawn_position(self) -> Tuple[int, int]:
        """
        Encontra uma posição válida para spawn do jogador.
        
        Returns:
            Tupla (x, y) com posição válida
        """
        # Procura por uma posição transitável
        for y in range(1, self.map_height - 1):
            for x in range(1, self.map_width - 1):
                if not self.is_wall(x, y):
                    return (x, y)
        
        # Fallback: posição central se não encontrar
        return (self.map_width // 2, self.map_height // 2)
    
    def generate_dungeon(self, num_rooms: int = 8, min_room_size: int = 5, 
                        max_room_size: int = 12, corridor_width: int = 2) -> List[List[int]]:
        """
        Gera um dungeon estilo D&D com salas e corredores.
        
        Args:
            num_rooms: Número de salas a gerar
            min_room_size: Tamanho mínimo das salas
            max_room_size: Tamanho máximo das salas
            corridor_width: Largura dos corredores (2, 3 ou 4)
            
        Returns:
            Lista 2D representando o mapa do dungeon
        """
        # Inicializa o mapa com paredes
        self.map_data = [[CELL_WALL for _ in range(self.map_width)] 
                        for _ in range(self.map_height)]
        
        # Gera salas
        rooms = self._generate_rooms(num_rooms, min_room_size, max_room_size, min_distance=3)
        
        # Conecta as salas com corredores
        self._connect_rooms(rooms, corridor_width)
        
        return self.map_data
    
    def _generate_rooms(self, num_rooms: int, min_size: int, max_size: int, min_distance: int = 3) -> List[Room]:
        """Gera salas aleatórias que não se intersectam e mantêm distância mínima."""
        rooms = []
        attempts = 0
        max_attempts = num_rooms * 300  # Aumenta tentativas para compensar a restrição
        
        while len(rooms) < num_rooms and attempts < max_attempts:
            # Gera sala aleatória
            width = random.randint(min_size, max_size)
            height = random.randint(min_size, max_size)
            x = random.randint(1, self.map_width - width - 1)
            y = random.randint(1, self.map_height - height - 1)
            
            new_room = Room(x, y, width, height)
            
            # Verifica se não intersecta e mantém distância mínima
            failed = False
            for room in rooms:
                if new_room.intersects(room):
                    failed = True
                    break
                # Verifica distância mínima
                if new_room.distance_to(room) < min_distance:
                    failed = True
                    break
            
            if not failed:
                rooms.append(new_room)
                # Desenha a sala no mapa
                self._carve_room(new_room)
            
            attempts += 1
        
        # Se não conseguiu gerar todas as salas, tenta com tamanhos menores
        if len(rooms) < num_rooms:
            remaining = num_rooms - len(rooms)
            smaller_rooms = self._generate_rooms(remaining, min_size - 1, max_size - 2, min_distance)
            rooms.extend(smaller_rooms)
        
        return rooms
    
    def _carve_room(self, room: Room):
        """Cava uma sala no mapa."""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if self.is_valid_position(x, y):
                    self.map_data[y][x] = CELL_FLOOR
    
    def _connect_rooms(self, rooms: List[Room], corridor_width: int = 2):
        """Conecta as salas com corredores usando algoritmo simples."""
        if len(rooms) < 2:
            return
        
        # Conecta cada sala com a próxima
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            
            # Pega pontos aleatórios em cada sala
            point1 = room1.get_random_point()
            point2 = room2.get_random_point()
            
            # Cria corredor entre os pontos
            self._create_corridor(point1, point2, corridor_width)
    
    def _create_corridor(self, start: Tuple[int, int], end: Tuple[int, int], corridor_width: int = 2):
        """Cria um corredor entre dois pontos."""
        x1, y1 = start
        x2, y2 = end
        
        # Cria corredor em L (primeiro horizontal, depois vertical)
        if random.random() < 0.5:
            # Primeiro horizontal, depois vertical
            self._carve_horizontal_corridor(x1, x2, y1, corridor_width)
            self._carve_vertical_corridor(y1, y2, x2, corridor_width)
        else:
            # Primeiro vertical, depois horizontal
            self._carve_vertical_corridor(y1, y2, x1, corridor_width)
            self._carve_horizontal_corridor(x1, x2, y2, corridor_width)
    
    def _carve_horizontal_corridor(self, x1: int, x2: int, y: int, width: int = 2):
        """Cava um corredor horizontal com largura especificada."""
        start_x = min(x1, x2)
        end_x = max(x1, x2) + 1
        
        # Calcula o offset para centralizar o corredor
        offset = width // 2
        
        for x in range(start_x, end_x):
            for w in range(width):
                corridor_y = y - offset + w
                if self.is_valid_position(x, corridor_y):
                    self.map_data[corridor_y][x] = CELL_CORRIDOR
    
    def _carve_vertical_corridor(self, y1: int, y2: int, x: int, width: int = 2):
        """Cava um corredor vertical com largura especificada."""
        start_y = min(y1, y2)
        end_y = max(y1, y2) + 1
        
        # Calcula o offset para centralizar o corredor
        offset = width // 2
        
        for y in range(start_y, end_y):
            for w in range(width):
                corridor_x = x - offset + w
                if self.is_valid_position(corridor_x, y):
                    self.map_data[y][corridor_x] = CELL_CORRIDOR


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


# Constantes para tipos de células
CELL_EMPTY = 0
CELL_WALL = 1
CELL_DOOR = 2
CELL_FLOOR = 3
CELL_CORRIDOR = 4
CELL_ROOM = 5 