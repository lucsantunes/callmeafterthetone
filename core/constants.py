"""
Constantes do jogo
"""

# Cores
COLOR_BLACK = 0
COLOR_NAVY = 1
COLOR_PURPLE = 2
COLOR_GREEN = 3
COLOR_BROWN = 4
COLOR_DARK_BLUE = 5
COLOR_LIGHT_BLUE = 6
COLOR_WHITE = 7
COLOR_RED = 8
COLOR_ORANGE = 9
COLOR_YELLOW = 10
COLOR_LIME = 11
COLOR_CYAN = 12
COLOR_GRAY = 13
COLOR_PINK = 14
COLOR_PEACH = 15

# Tipos de célula do mapa
CELL_WALL = 1
CELL_FLOOR = 3
CELL_CORRIDOR = 4

# Estados do jogo
GAME_STATE_MENU = "menu"           # Menu inicial
GAME_STATE_PAUSE = "pause"          # Menu de pausa
GAME_STATE_PLAYING = "playing"      # Jogo ativo
GAME_STATE_GAME_OVER = "game_over"  # Game over ou vitória

# Interfaces/UI (não são estados)
UI_NORMAL = "normal"                # Interface normal do jogo
UI_INVENTORY = "inventory"          # Interface do inventário
UI_SKILLS = "skills"                # Interface de habilidades
UI_MONSTER = "monster"              # Interface de monstro
UI_CHAT = "chat"                    # Chat de eventos

# Sistema turn-based
TURN_PLAYER = "player"              # Vez do jogador
TURN_MASTER = "master"              # Vez do mestre

# Ações do jogador
ACTION_MOVE = "move"
ACTION_ATTACK = "attack"
ACTION_USE_ITEM = "use_item"
ACTION_OPEN_INVENTORY = "open_inventory"
ACTION_CAST_SPELL = "cast_spell"
ACTION_REST = "rest"

# Tipos de itens
ITEM_TYPE_WEAPON = "weapon"
ITEM_TYPE_ARMOR = "armor"
ITEM_TYPE_POTION = "potion"
ITEM_TYPE_SCROLL = "scroll"
ITEM_TYPE_GOLD = "gold"

# Configurações do jogador
PLAYER_MAX_HP = 100
PLAYER_START_HP = 100
PLAYER_ATTACK_DAMAGE = 10
PLAYER_DEFENSE = 5

# Configurações da interface
UI_PANEL_WIDTH = 200
UI_PANEL_HEIGHT = 600
CHAT_HEIGHT = 150
STATUS_HEIGHT = 100

# Configurações de combate
COMBAT_RANGE = 2
COMBAT_ACCURACY = 0.8