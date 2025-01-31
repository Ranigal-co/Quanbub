import pygame
from Settings import *


'''

    Данный класс нужен для инициализации башен и взаимодействия с ними!
    Класс требуется в улучшениях

'''

class Base:
    def __init__(self, x, y, width, height):
        self.hp = STANDARD_BASE_HP
        self.hp_select = 50

        self.x, self.y = x, y
        self.WIDTH, self.HEIGHT = width, height

        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def get_hp(self):
        return self.hp


class EnemyBase(Base):
    def __init__(self, hp=STANDARD_BASE_HP_ENEMY):
        super().__init__(WIDTH - 50, HEIGHT - 200, 50, 50)
        self.hp = hp
        self.type = ENEMY

    def attack_me(self, attack):
        if self.hp > 0:
            self.hp -= attack
        else:
            return DEFENDER_WIN
        return NONE


class DefenderBase(Base):
    def __init__(self, cost_lvl=50, lvl=1, limit_money=100, speed_money=1):
        super().__init__(0, HEIGHT - 200, 50, 50)
        self.cost_lvl = cost_lvl
        self.lvl = lvl
        self.lvl_main = 1
        self.type = DEFENDER
        self.upgrade_cost = 100  # Стоимость улучшения базы
        self.limit_money = limit_money
        self.speed_money = speed_money  # Скорость накопления денег

        self.hp_upgrade_cost = 50  # Стоимость улучшения здоровья
        self.limit_money_upgrade_cost = 50  # Стоимость улучшения лимита денег
        self.speed_money_upgrade_cost = 50  # Стоимость улучшения скорости накопления денег
        self.coin = None

    def lvl_up(self):
        self.lvl += 1
        self.hp += self.hp_select * self.lvl
        self.cost_lvl = 50 * self.lvl

    def attack_me(self, attack):
        if self.hp > 0:
            self.hp -= attack
        else:
            return ENEMY_WIN
        return NONE
    '''
    def upgrade(self):
        """Улучшаем базу."""
        self.lvl_main += 1
        self.hp = 100 * self.lvl_main  # Увеличиваем здоровье базы
        self.hp_select = 100 * self.lvl_main
        self.upgrade_cost += 50 * self.lvl_main  # Увеличиваем стоимость следующего улучшения
        self.limit_money = 100 * self.lvl_main
    '''

    def upgrade_hp(self):
        """Улучшаем здоровье базы."""
        if self.coin.coins >= self.hp_upgrade_cost:
            self.coin.coins -= self.hp_upgrade_cost
            self.hp += 100  # Увеличиваем здоровье на 100
            self.hp_select += 100
            self.hp_upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            sound_game['buy'].play()
            print(f"Base HP upgraded to {self.hp}!")

    def upgrade_limit_money(self):
        """Улучшаем лимит денег."""
        if self.coin.coins >= self.limit_money_upgrade_cost:
            self.coin.coins -= self.limit_money_upgrade_cost
            self.limit_money += 100 # Увеличиваем лимит денег на 100
            self.limit_money_upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            sound_game['buy'].play()
            print(f"Base limit money upgraded to {self.limit_money}!")

    def upgrade_speed_money(self):
        """Улучшаем скорость накопления денег."""
        if self.coin.coins >= self.speed_money_upgrade_cost:
            self.coin.coins -= self.speed_money_upgrade_cost
            self.speed_money += 0.2  # Увеличиваем скорость накопления денег на 0.2
            self.speed_money_upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            sound_game['buy'].play()
            print(f"Base speed money upgraded to {self.speed_money}!")