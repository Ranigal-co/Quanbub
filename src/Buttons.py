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

        self.color_cursor = (100, 0, 0)
        self.color_without_cursor = (200, 0, 0)

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
        pygame.draw.rect(screen, color, self.button)
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
