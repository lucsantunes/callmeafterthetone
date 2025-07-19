"""
Haunted Mansion Generator
=========================

Este módulo gera mansões mal assombradas estilo D&D com:
- Salas de diferentes tamanhos e formatos
- Corredores conectando salas próximas
- Layout realista de mansão
"""

import random
import math
from typing import List, Tuple, Optional, Set


class Room:
    """Representa uma sala na mansão mal assombrada."""
    
    def __init__(self, x: int, y: int, width: int, height: int, room_type: str = "normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type  # normal, large, small, corridor
        
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


class HauntedMansionGenerator:
    """
    Gerador de mansões mal assombradas estilo D&D.
    """
    
    def __init__(self, map_width: int, map_height: int):
        """
        Inicializa o gerador de mansões.
        
        Args:
            map_width: Largura do mapa em células
            map_height: Altura do mapa em células
        """
        self.map_width = map_width
        self.map_height = map_height
        self.map_data = []
        
    def generate_mansion(self, num_rooms: int = 8, max_connection_distance: int = 15, 
                        corridor_width: int = 3) -> List[List[int]]:
        """
        Gera uma mansão mal assombrada.
        
        Args:
            num_rooms: Número de salas a gerar
            max_connection_distance: Distância máxima para conectar salas
            corridor_width: Largura dos corredores
            
        Returns:
            Lista 2D representando o mapa da mansão
        """
        # 1. Inicializa o mapa com paredes
        self.map_data = [[CELL_WALL for _ in range(self.map_width)] 
                        for _ in range(self.map_height)]
        
        # 2. Gera salas com distâncias e tamanhos razoáveis
        rooms = self._generate_rooms(num_rooms)
        
        # 3. Conecta salas que estão até X de distância
        self._connect_nearby_rooms(rooms, max_connection_distance, corridor_width)
        
        return self.map_data
    
    def _generate_rooms(self, num_rooms: int) -> List[Room]:
        """Gera salas com tamanhos e formatos razoáveis."""
        rooms = []
        attempts = 0
        max_attempts = num_rooms * 200
        
        # Define tipos de salas para mansão
        room_types = [
            {"type": "large", "min_size": 12, "max_size": 18, "weight": 2},
            {"type": "normal", "min_size": 8, "max_size": 14, "weight": 5},
            {"type": "small", "min_size": 5, "max_size": 8, "weight": 3}
        ]
        
        while len(rooms) < num_rooms and attempts < max_attempts:
            # Escolhe tipo de sala baseado em peso
            room_type = random.choices(room_types, weights=[r["weight"] for r in room_types])[0]
            
            # Gera dimensões da sala
            width = random.randint(room_type["min_size"], room_type["max_size"])
            height = random.randint(room_type["min_size"], room_type["max_size"])
            
            # Posição aleatória
            x = random.randint(2, self.map_width - width - 2)
            y = random.randint(2, self.map_height - height - 2)
            
            new_room = Room(x, y, width, height, room_type["type"])
            
            # Verifica se não intersecta com salas existentes
            failed = False
            for room in rooms:
                if new_room.intersects(room):
                    failed = True
                    break
                # Mantém distância mínima de 3 células
                if new_room.distance_to(room) < 3:
                    failed = True
                    break
            
            if not failed:
                rooms.append(new_room)
                self._carve_room(new_room)
            
            attempts += 1
        
        return rooms
    
    def _connect_nearby_rooms(self, rooms: List[Room], max_distance: int, corridor_width: int):
        """Conecta salas que estão até X de distância."""
        if len(rooms) < 2:
            return
        
        # Encontra pares de salas próximas
        connections = []
        
        for i in range(len(rooms)):
            for j in range(i + 1, len(rooms)):
                room1 = rooms[i]
                room2 = rooms[j]
                distance = room1.distance_to(room2)
                
                # Conecta se estão próximas o suficiente
                if distance <= max_distance:
                    connections.append((room1, room2, distance))
        
        # Ordena por distância (mais próximas primeiro)
        connections.sort(key=lambda x: x[2])
        
        # Limita o número de conexões para evitar sobrecarga
        max_connections = min(len(connections), len(rooms) - 1)
        selected_connections = connections[:max_connections]
        
        # Cria corredores para as conexões selecionadas
        for room1, room2, distance in selected_connections:
            point1 = room1.get_random_point()
            point2 = room2.get_random_point()
            self._create_corridor(point1, point2, corridor_width)
    
    def _carve_room(self, room: Room):
        """Cava uma sala no mapa."""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if self.is_valid_position(x, y):
                    self.map_data[y][x] = CELL_FLOOR
    
    def _create_corridor(self, start: Tuple[int, int], end: Tuple[int, int], corridor_width: int):
        """Cria um corredor entre dois pontos com largura completa."""
        x1, y1 = start
        x2, y2 = end
        
        # Cria corredor em L (primeiro horizontal, depois vertical)
        if random.random() < 0.5:
            # Primeiro horizontal, depois vertical
            # Garante que o corredor horizontal vai até o ponto de conexão
            self._carve_horizontal_corridor(x1, x2, y1, corridor_width)
            # Garante que o corredor vertical vai desde o ponto de conexão até o destino
            self._carve_vertical_corridor(y1, y2, x2, corridor_width)
            # Preenche o canto do L para garantir largura completa
            self._fill_corner(x2, y1, corridor_width, "horizontal_to_vertical")
        else:
            # Primeiro vertical, depois horizontal
            # Garante que o corredor vertical vai até o ponto de conexão
            self._carve_vertical_corridor(y1, y2, x1, corridor_width)
            # Garante que o corredor horizontal vai desde o ponto de conexão até o destino
            self._carve_horizontal_corridor(x1, x2, y2, corridor_width)
            # Preenche o canto do L para garantir largura completa
            self._fill_corner(x1, y2, corridor_width, "vertical_to_horizontal")
    
    def _carve_horizontal_corridor(self, x1: int, x2: int, y: int, width: int):
        """Cava um corredor horizontal com largura completa."""
        start_x = min(x1, x2)
        end_x = max(x1, x2) + 1
        
        # Calcula o offset para centralizar o corredor
        offset = width // 2
        
        # Cava toda a largura do corredor
        for x in range(start_x, end_x):
            for w in range(width):
                corridor_y = y - offset + w
                if self.is_valid_position(x, corridor_y):
                    self.map_data[corridor_y][x] = CELL_CORRIDOR
    
    def _carve_vertical_corridor(self, y1: int, y2: int, x: int, width: int):
        """Cava um corredor vertical com largura completa."""
        start_y = min(y1, y2)
        end_y = max(y1, y2) + 1
        
        # Calcula o offset para centralizar o corredor
        offset = width // 2
        
        # Cava toda a largura do corredor
        for y in range(start_y, end_y):
            for w in range(width):
                corridor_x = x - offset + w
                if self.is_valid_position(corridor_x, y):
                    self.map_data[y][corridor_x] = CELL_CORRIDOR
    
    def _fill_corner(self, corner_x: int, corner_y: int, width: int, direction: str):
        """Preenche o canto do L para garantir largura completa."""
        offset = width // 2
        
        if direction == "horizontal_to_vertical":
            # Preenche o canto quando o corredor horizontal vira para vertical
            # Preenche apenas as células que faltam no canto interno
            for w in range(width):
                for h in range(width):
                    fill_x = corner_x - offset + w
                    fill_y = corner_y - offset + h
                    if self.is_valid_position(fill_x, fill_y):
                        # Só preenche se não estiver já preenchido
                        if self.map_data[fill_y][fill_x] != CELL_CORRIDOR:
                            self.map_data[fill_y][fill_x] = CELL_CORRIDOR
                        
        elif direction == "vertical_to_horizontal":
            # Preenche o canto quando o corredor vertical vira para horizontal
            # Preenche apenas as células que faltam no canto interno
            for w in range(width):
                for h in range(width):
                    fill_x = corner_x - offset + w
                    fill_y = corner_y - offset + h
                    if self.is_valid_position(fill_x, fill_y):
                        # Só preenche se não estiver já preenchido
                        if self.map_data[fill_y][fill_x] != CELL_CORRIDOR:
                            self.map_data[fill_y][fill_x] = CELL_CORRIDOR
    
    def is_wall(self, x: int, y: int) -> bool:
        """Verifica se a posição é uma parede."""
        if not self.is_valid_position(x, y):
            return True
        return self.map_data[y][x] == CELL_WALL
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Verifica se a posição está dentro dos limites."""
        return 0 <= x < self.map_width and 0 <= y < self.map_height
    
    def find_valid_spawn_position(self) -> Tuple[int, int]:
        """Encontra uma posição válida para spawn."""
        for y in range(1, self.map_height - 1):
            for x in range(1, self.map_width - 1):
                if not self.is_wall(x, y):
                    return (x, y)
        return (self.map_width // 2, self.map_height // 2)
    
    def get_map_data(self) -> List[List[int]]:
        """Retorna os dados do mapa."""
        return self.map_data


# Funções auxiliares
def create_mansion_generator(map_width: int, map_height: int) -> HauntedMansionGenerator:
    """
    Factory function para criar um gerador de mansões mal assombradas.
    
    Args:
        map_width: Largura do mapa
        map_height: Altura do mapa
        
    Returns:
        Instância de HauntedMansionGenerator configurada
    """
    return HauntedMansionGenerator(map_width, map_height)


# Constantes para tipos de células
CELL_EMPTY = 0
CELL_WALL = 1
CELL_DOOR = 2
CELL_FLOOR = 3
CELL_CORRIDOR = 4
CELL_ROOM = 5 