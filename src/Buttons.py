import pygame
from Settings import *


'''

    Данный файл реализован для инициализации кнопок и взаимодействие с ними
    В будущем вместо цветов будут картинки, а значит будет круто
    
'''


class Button:
    def __init__(self, x, y, width, height, text=None):
        self.WIDTH = width
        self.HEIGHT = height
        self.x = x
        self.y = y
        self.text = FONT_PRESS_ESC.render(text, True, (255, 255, 255))

        self.button = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

        self.activate = False

        '''
        
            Функция кнопки - это то как она будет взаимодейстовать с игрой
            Все фунции распологаются в файле Settings и помечены в начале как B_*
            
        '''
        self.func = B_NONE

        self.color_cursor = (0, 100, 0)
        self.color_without_cursor = (0, 200, 0)

    '''
        Делаем отрисовку объекта класса
    '''
    def render(self, screen):
        x, y = pygame.mouse.get_pos()
        color = self.color_without_cursor
        '''
            Пересечение прямоугольника и курсора
        '''
        collide = self.button.collidepoint(x, y)
        if collide and pygame.mouse.get_pressed()[0] is True:
            return self.func
        elif collide:
            color = self.color_cursor
        pygame.draw.rect(screen, color, self.button, border_radius=10)
        if self.text is not None:
            screen.blit(self.text, (self.x, self.y))

    '''
        Установить цвет кнопок в разных состояниях, где
            without - цвет кнопки в обычном состоянии
            cursor  - цвет кнопки при наведении на нее
    '''

    def set_color(self, without, cursor):
        self.color_without_cursor = without
        self.color_cursor = cursor


class Button_game(Button):
    def __init__(self, x, y, width, height, text, recharge=TICK):
        super().__init__(x, y, width, height, text)
        self.recharge = recharge
        self.const_rech = recharge
        self.color_enable = (50, 50, 50)

    def recharge_func(self, money, cost):
        if self.recharge <= 0 and money >= cost:
            self.activate = True
            return self.activate
        else:
            self.activate = False
            return self.activate

    def recharge_func_tick(self):
        if self.recharge <= 0:
            return True
        else:
            return False

    def render_b(self, screen, pause):
        if pause is False:
            if self.activate:
                x, y = pygame.mouse.get_pos()
                color = self.color_without_cursor
                '''
                    Пересечение прямоугольника и курсора
                '''
                collide = self.button.collidepoint(x, y)
                if collide and pygame.mouse.get_pressed()[0] is True:
                    return self.func
                elif collide:
                    color = self.color_cursor
                pygame.draw.rect(screen, color, self.button, border_radius=10)
                if self.text is not None:
                    screen.blit(self.text, (self.x, self.y))
            else:
                color = self.color_enable
                pygame.draw.rect(screen, color, self.button, border_radius=10)
                if self.text is not None:
                    screen.blit(self.text, (self.x, self.y))
        else:
            if self.activate:
                color = self.color_without_cursor
                '''
                    Пересечение прямоугольника и курсора
                '''
                pygame.draw.rect(screen, color, self.button, border_radius=10)
                if self.text is not None:
                    screen.blit(self.text, (self.x, self.y))
            else:
                color = self.color_enable
                pygame.draw.rect(screen, color, self.button, border_radius=10)
                if self.text is not None:
                    screen.blit(self.text, (self.x, self.y))

    def color_enable_f(self, color):
        self.color_enable = color