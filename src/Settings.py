import pygame
pygame.init()

"""

    Данный файл отвечает за настройку игры в целом
    Не рекомендуется изменять данный файл, так как могут появиться баги
    Данный файл обязательно импортировать

    Здесь находятся константы, они обозначаются заглавными буквами

"""

WIDTH, HEIGHT = 1000, 600
FPS = 60
SPEED_MONEY = 200
SPEED_SPAWN_ENEMY = 7500
SPEED_SPAWN_BOSS = 60000
COST_DEFENDER_1 = 20
COST_DEFENDER_2 = 30

STANDARD_BASE_HP = 100
STANDARD_BASE_HP_ENEMY = 500

TICK = 1000
'''
    Константы для игры
'''
NONE = "None"
ENEMY = "Enemy"
DEFENDER = "Defender"
MENU = "Menu"
GAME = "Game"
DEATH = "Death"
ENEMY_WIN = "Enemy win"
DEFENDER_WIN = "Defender win"
PLAY = "play"
SINGLE = "Single"
AREA = "Area"

'''
    Функции кнопок
'''
B_NONE = None
B_CLOSE = "CLOSE"
B_START_GAME = "START GAME"
B_BUY_DEFENDER_1 = "BUY DEFENDER 1"
B_BUY_DEFENDER_2 = "BUY DEFENDER 2"
B_LVL_UP = "Lvl up"

'''
    Шрифты константы
'''
FONT_GAME = pygame.font.Font("../fonts/bit.ttf", 50)
FONT_PRESS_ESC = pygame.font.Font("../fonts/bit.ttf", 20)
FONT_HP_ENTITIES = pygame.font.Font("../fonts/bit.ttf", 16)

'''
    Текстовые константы
'''
TEXT_PAUSE = FONT_GAME.render("PAUSE", True, (255, 255, 255))
TEXT_PRESS_ESC = FONT_PRESS_ESC.render("Press esc", True, (255, 255, 255))
TEXT_START_GAME = FONT_PRESS_ESC.render("Start game", True, (255, 255, 255))