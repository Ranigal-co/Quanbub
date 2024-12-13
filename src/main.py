import pygame

from Settings import *
from Entities import Enemy, Defender
from Stages import Menu, Game
from Buttons import Button


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

buttons = list()
buttons.append(Button(WIDTH - 40, 0, 40, 40))
buttons[-1].func = B_CLOSE
buttons.append(Button(500, 300, 150, 40, "Start game"))
buttons[-1].func = B_START_GAME

entities = list()
entities.append(Enemy("Enemy", 50, 50, 100, 25))
entities[-1].spawn()
entities.append(Defender("Defender", 50, 200, 100, 25))
entities[-1].spawn()

game = None
menu = Menu()
stage = MENU
bases = list()

money_text = f'Баланс: 0'

MONEY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MONEY_EVENT, 0)

pause = False
clock = pygame.time.Clock()
execute = True
while execute:
    screen.fill((0, 0, 0))
    money_render = FONT_GAME.render(money_text, True, pygame.Color("yellow"))
    for event in pygame.event.get():
        type = event.type
        if type == pygame.QUIT:
            execute = False
        elif type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] == 1:
                if pause is True:
                    pause = False
                else:
                    pause = True
        elif type == MONEY_EVENT:
            if pause is False:
                game.money += 1
    for index, button in enumerate(buttons):
        event = button.render(screen)
        if event == B_CLOSE:
            execute = False
        elif event == B_START_GAME:
            pygame.time.set_timer(MONEY_EVENT, SPEED_MONEY)
            stage = GAME
            game = Game()
            bases = [game.enemy_base, game.defender_base]
            del buttons[index]
            buttons.append(Button(400, HEIGHT - 80, 150, 40, f"{COST_DEFENDER} Buy"))
            buttons[-1].set_color(pygame.Color("yellow"), (0, 100, 100))
            buttons[-1].func = B_BUY_DEFENDER
        elif event == B_BUY_DEFENDER and game.money >= COST_DEFENDER:
            game.money -= COST_DEFENDER
            entities.append(Defender("Defender", 50, 200, 100, 100))
            entities[-1].spawn()
    if stage == GAME:
        game.render(screen)
        screen.blit(money_render, (400, 0))
        for index, entity in enumerate(entities):
            if pause is False:
                game_over = entity.move_attack(entities, bases)
                if 'win' in game_over:
                    stage = MENU
                    print(game_over)
            status_enemy = entity.check_hp()
            if status_enemy == DEATH:
                del entities[index]
            entity.render(screen)
        money_text = f'Money: {game.money}'
    elif stage == MENU:
        buttons = list()
        buttons.append(Button(WIDTH - 40, 0, 40, 40))
        buttons[-1].func = B_CLOSE
        buttons.append(Button(500, 300, 150, 40, "Start game"))
        buttons[-1].func = B_START_GAME

        entities = list()
        entities.append(Enemy("Enemy", 50, 50, 100, 25))
        entities[-1].spawn()
        entities.append(Defender("Defender", 50, 200, 100, 25))
        entities[-1].spawn()
    if pause is True:
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 370, 300))
        screen.blit(TEXT_PAUSE, (200, 200))
        screen.blit(TEXT_PRESS_ESC, (220, 255))

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
