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
        '''
        Отображение hp баз
        '''
        hp_enemy = self.enemy_base.get_hp()
        hp_defender = self.defender_base.get_hp()
        if hp_enemy >= 0:
            hp_render_enemy = FONT_PRESS_ESC.render(str(hp_enemy), True, pygame.Color("white"))
            screen.blit(hp_render_enemy, (self.get_coords_enemy()[0], self.get_coords_enemy()[1] - hp_render_enemy.get_height()))
        else:
            hp_render_enemy = FONT_PRESS_ESC.render('0', True, pygame.Color("white"))
            screen.blit(hp_render_enemy, (self.get_coords_enemy()[0], self.get_coords_enemy()[1] - hp_render_enemy.get_height()))
        if hp_defender >= 0:
            hp_render_defender = FONT_PRESS_ESC.render(str(hp_defender), True, pygame.Color("white"))
            screen.blit(hp_render_defender, (
            self.get_coords_defender()[0], self.get_coords_defender()[1] - hp_render_defender.get_height()))
        else:
            hp_render_defender = FONT_PRESS_ESC.render('0', True, pygame.Color("white"))
            screen.blit(hp_render_defender, (
            self.get_coords_defender()[0], self.get_coords_defender()[1] - hp_render_defender.get_height()))


    def get_coords_enemy(self):
        return [self.enemy_base.rect[0], self.enemy_base.rect[1]]

    def get_coords_defender(self):
        return [self.defender_base.rect[0], self.defender_base.rect[1]]