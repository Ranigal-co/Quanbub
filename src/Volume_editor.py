from Settings import *


# рисую саму дорожку по которой будет двигаться ползунок


class Rail:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = (128, 128, 128)  # grey
        self.rail = pygame.Rect(self.x, self.y, self.width, self.height)

    def Render_rail(self, screen):
        pygame.draw.rect(screen, self.color, self.rail, 1, 4)


# рисую ползунок который будет бегать по дорожке


class Slider:
    def __init__(self, x, y, radius):
        self.radius = radius
        self.x = x
        self.y = y
        self.color_no_cursor = (128, 128, 128)  # grey
        self.color_with_cursor = (169, 169, 169)  # grey_posvetlee
        self.slider = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        self.func = B_NONE

        self.flag = 0

    def Render_slider(self, screen):
        x, y = pygame.mouse.get_pos()
        color = self.color_no_cursor
        self.slider = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        collide = self.slider.collidepoint(x, y)
        if collide and pygame.mouse.get_pressed()[0] is True:
            self.flag = 1
        if pygame.mouse.get_pressed()[0] is False:
            self.flag = 0
        if self.flag:
            color = self.color_with_cursor
            if 650 < x < 800:
                self.x = x
        if collide:
            color = self.color_with_cursor
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

    def Volume_digit(self):
        return (150 - (800 - self.x)) / 150
    # возвращает значение звука на котором стоит ползунок
