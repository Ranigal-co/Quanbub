import random
import pygame
from Settings import *
from random import *


'''

    Данный файл реализован для инициализации сущностей для игры и взаиомдействия с ними
    В будущем вместо кубов будут нормальные картинки
    Предпологаю что на первом плане экрана будет Defender, а после него Enemy
    
'''


'''
    Интерфейс для Enemy и Defender
'''
class Entity:
    def __init__(self, name=NONE, speed_move=10, speed_attack=500,
                 hp=100, attack=10, type=NONE, color=(0, 0, 0), direction=0, damage_type=SINGLE):
        self.name = name

        self.speed_move = speed_move
        self.speed_attack = speed_attack
        self.hp, self.attack = hp, attack
        self.type = type
        self.damage_type = damage_type

        self.color = color

        self.x, self.y = 0, 0
        self.tick = 0

        self.direction = direction

        self.WIDTH, self.HEIGHT = 50, 50
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def set_coords(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    '''
        где-то здесь логика, что один чел один удар по кому либо наносит, а не массивный урон
    '''

    def move_attack(self, entities, bases):
        collide = 0
        if self.rect.collidelist(bases) > -1:
            for base in bases:
                if self.rect.colliderect(base.rect):
                    collide += 1
                    if self.tick >= self.speed_attack:
                        win = base.attack_me(self.attack)
                        if 'win' in win:
                            return win
        else:
            for entity in entities:
                if entity.type != self.type:
                    if self.rect.colliderect(entity.rect):
                        collide += 1
                        if self.tick >= self.speed_attack:
                            if self.damage_type == SINGLE:
                                entity.hp -= self.attack
                                break
                            else:
                                entity.hp -= self.attack
        if collide > 0:
            if self.tick >= self.speed_attack:
                self.tick = 0
                return PLAY
            else:
                self.tick += 1
        else:
            self.x += self.speed_move / FPS * self.direction
            self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        return NONE

    def check_hp(self):
        if self.hp <= 0:
            return DEATH

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        '''
        Отображение hp юнитов
        '''
        if self.hp >= 0:
            hp_render = FONT_HP_ENTITIES.render(str(self.hp), True, pygame.Color("white"))
            screen.blit(hp_render, (self.x, self.y - hp_render.get_height()))
        else:
            hp_render = FONT_HP_ENTITIES.render('0', True, pygame.Color("white"))
            screen.blit(hp_render, (self.x, self.y - hp_render.get_height()))


class Enemy(Entity):
    def __init__(self, name, speed_move, speed_attack, hp, attack, cost, damage_type):
        super().__init__(name=name, speed_move=speed_move,
                         speed_attack=speed_attack, hp=hp, attack=attack, type=ENEMY, color=(255, 0, 0), direction=-1, damage_type=damage_type)
        self.cost = cost

    def spawn(self):
        self.set_coords(WIDTH - 150, HEIGHT - 200 + randint(-15, 15))
'''
здесь cost - это сколько выпадает с врага монет
крч хз баг это или оставим, типо если денег и так 100/100, но с врага выпадает, то типо там 110/100 получается бабла
можно оставить можно нет
'''
class Monster:
    def __init__(self):
        name = 'Monster'
        speed_move = 50
        speed_attack = 200
        hp = 50
        attack = 25
        cost = 10
        damage_type = SINGLE
        # charge = 1000 крч надо сделать чтобы не всегда можно было купить, а нужно подождать пока воин перезарядится, тогда снова заспавнить можно

        self.name = name
        self.data = (name, speed_move, speed_attack, hp, attack, cost, damage_type)
        self.cost = cost


class Boss:
    def __init__(self):
        name = 'Boss'
        speed_move = 20
        speed_attack = 300
        hp = 200
        attack = 40
        cost = 100
        damage_type = AREA
        # charge = 1000

        self.name = name
        self.data = (name, speed_move, speed_attack, hp, attack, cost, damage_type)
        self.cost = cost


class Defender(Entity):
    def __init__(self, name, speed_move, speed_attack, hp, attack, damage_type):
        super().__init__(name=name, speed_move=speed_move,
                         speed_attack=speed_attack, hp=hp, attack=attack, type=DEFENDER, color=(0, 255, 0), direction=1, damage_type=damage_type)

    def spawn(self):
        self.set_coords(100, HEIGHT - 200 + randint(-15, 15))


class Hero:
    def __init__(self):
        name = "Hero"
        speed_move = 50
        speed_attack = 200
        hp = 50
        attack = 25
        cost = 50
        damage_type = AREA
        # charge = 5000

        self.name = name
        self.data = (name, speed_move, speed_attack, hp, attack, damage_type)
        self.cost = cost


class Shit:
    def __init__(self):
        name = "Shit"
        speed_move = 25
        speed_attack = 100
        hp = 100
        attack = 10
        cost = 25
        damage_type = SINGLE

        self.name = name
        self.data = (name, speed_move, speed_attack, hp, attack, damage_type)
        self.cost = cost
