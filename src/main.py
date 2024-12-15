import pygame

from Settings import *
from Entities import Enemy, Defender, Hero, Shit
from Stages import Menu, Game
from Buttons import Button


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

buttons = list()
buttons.append(Button(WIDTH - 40, 0, 40, 40))
buttons[-1].func = B_CLOSE
buttons.append(Button(500, 300, 150, 40, "Start game"))
buttons[-1].func = B_START_GAME

USE_FIGHTER = Hero(), Shit()
fighter1, fighter2 = USE_FIGHTER

entities = list()
entities.append(Enemy(*fighter2.data))
entities[-1].spawn()
entities.append(Defender(*fighter2.data))
entities[-1].spawn()

game = None
menu = Menu()
stage = MENU
bases = list()

'''
загрузка музыки в списки
'''

music_game = [pygame.mixer.Sound('../music/music_game/battle_1.mp3')]
music_pause = [pygame.mixer.Sound('../music/music_pause/mus_main.mp3')]
sound_game = {'buy':pygame.mixer.Sound('../music/sounds_game/buy.mp3'),
              'pause':pygame.mixer.Sound('../music/sounds_game/pause.mp3'),
              'hit_defender':pygame.mixer.Sound('../music/sounds_game/hit_1.mp3')}
current_index_music_game = 0
current_index_music_pause = 0

money_text = f'Баланс: 0'

MONEY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MONEY_EVENT, 0)

ENEMY_SPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SPAWN, 0)

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
                sound_game['pause'].play()
                if pause is True:
                    '''
                    музыка игры
                    '''
                    for _ in music_pause:
                        _.set_volume(0)
                    music_game[current_index_music_game].set_volume(1)
                    current_index_music_game = (current_index_music_game + 1) % len(music_game)
                    pause = False
                else:
                    '''
                    музыка паузы
                    '''
                    for _ in music_game:
                        _.set_volume(0)
                    music_pause[current_index_music_pause].set_volume(1)
                    current_index_music_pause = (current_index_music_pause + 1) % len(music_pause)
                    pause = True
        elif type == MONEY_EVENT:
            if pause is False:
                game.money += 1
        elif type == ENEMY_SPAWN:
            if pause is False:
                entities.append(Enemy(*fighter1.data))
                entities[-1].spawn()
    for index, button in enumerate(buttons):
        event = button.render(screen)
        if event == B_CLOSE:
            execute = False
        elif event == B_START_GAME:
            pygame.time.set_timer(MONEY_EVENT, SPEED_MONEY)
            pygame.time.set_timer(ENEMY_SPAWN, SPEED_SPAWN_ENEMY)
            stage = GAME
            game = Game()
            bases = [game.enemy_base, game.defender_base]
            del buttons[index]
            buttons.append(Button(300, HEIGHT - 80, 150, 40, f"{fighter1.cost} {fighter1.name}"))
            buttons[-1].set_color(pygame.Color("yellow"), (0, 100, 100))
            buttons[-1].func = B_BUY_DEFENDER_1
            buttons.append(Button(500, HEIGHT - 80, 150, 40, f"{fighter2.cost} {fighter2.name}"))
            buttons[-1].set_color(pygame.Color("yellow"), (0, 100, 100))
            buttons[-1].func = B_BUY_DEFENDER_2
            '''
            музыка игры
            '''
            music_pause[current_index_music_pause].stop()
            music_game[current_index_music_game].stop()
            music_pause[current_index_music_pause].play(-1)
            music_game[current_index_music_game].play(-1)
            music_pause[current_index_music_pause].set_volume(0)
            music_game[current_index_music_game].set_volume(1)
        elif event == B_BUY_DEFENDER_1 and game.money >= fighter1.cost:
            game.money -= fighter1.cost
            entities.append(Defender(*fighter1.data))
            entities[-1].spawn()
            sound_game['buy'].play()
        elif event == B_BUY_DEFENDER_2 and game.money >= fighter2.cost:
            game.money -= fighter2.cost
            entities.append(Defender(*fighter2.data))
            entities[-1].spawn()
            sound_game['buy'].play()
    if stage == GAME:
        game.render(screen)
        screen.blit(money_render, (400, 0))
        for index, entity in enumerate(entities):
            if pause is False:
                game_over = entity.move_attack(entities, bases)
                if 'win' in game_over:
                    stage = MENU
                    print(game_over)
                elif 'play' in game_over:
                    sound_game['hit_defender'].play()
            status_enemy = entity.check_hp()
            if status_enemy == DEATH:
                del entities[index]
            entity.render(screen)
        money_text = f'Money: {game.money}'
    elif stage == MENU:
        pygame.time.set_timer(ENEMY_SPAWN, 0)
        pygame.time.set_timer(MONEY_EVENT, 0)
        buttons = list()
        buttons.append(Button(WIDTH - 40, 0, 40, 40))
        buttons[-1].func = B_CLOSE
        buttons.append(Button(500, 300, 150, 40, "Start game"))
        buttons[-1].func = B_START_GAME
        for _ in music_game:
            _.set_volume(0)

        entities = list()
        entities.append(Enemy(*fighter2.data))
        entities[-1].spawn()
        entities.append(Defender(*fighter2.data))
        entities[-1].spawn()
    if pause is True:
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 370, 250))
        screen.blit(TEXT_PAUSE, (200, 200))
        screen.blit(TEXT_PRESS_ESC, (220, 255))

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
