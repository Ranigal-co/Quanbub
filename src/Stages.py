import pygame
from Settings import *
from Base import EnemyBase, DefenderBase


class Menu:
    def render(self, screen):
        pass


class Game:
    def __init__(self):
        self.money = 0
        self.enemy_base = EnemyBase()
        self.defender_base = DefenderBase()

    def render(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.enemy_base.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.defender_base.rect)