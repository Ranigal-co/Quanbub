import pygame

from Settings import *
from Entities import Enemy, Defender, Hero, Shit
from Stages import Menu, Game
from Buttons import Button
from src.Entities import Monster, Boss

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

buttons = list()
buttons.append(Button(WIDTH - 40, 0, 40, 40))
buttons[-1].func = B_CLOSE
buttons.append(Button(500, 300, 150, 40, "Start game"))
buttons[-1].func = B_START_GAME

USE_FIGHTER = Hero(), Shit()
fighter1, fighter2 = USE_FIGHTER
USE_ENEMY = Monster(), Boss()
enemy1, enemy2 = USE_ENEMY

entities = list()
# entities.append(Enemy(*fighter2.data))
# entities[-1].spawn()
# entities.append(Defender(*fighter2.data))
# entities[-1].spawn()

clicked = False
game = None
menu = Menu()
stage = MENU
bases = list()
LVL = 1

music_game = [pygame.mixer.Sound('../music/music_game/battle_6.mp3')]
music_pause = [pygame.mixer.Sound('../music/music_pause/mus_main.mp3')]
sound_game = {'buy':pygame.mixer.Sound('../music/sounds_game/buy.mp3'),
              'pause':pygame.mixer.Sound('../music/sounds_game/pause.mp3'),
              'hit_defender':pygame.mixer.Sound('../music/sounds_game/hit.mp3')}
current_index_music_game = 0
current_index_music_pause = 0

money_text = f'Баланс: 0'

MONEY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MONEY_EVENT, 0)

ENEMY_SPAWN_Monster = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SPAWN_Monster, 0)

ENEMY_SPAWN_Boss = pygame.USEREVENT + 3
pygame.time.set_timer(ENEMY_SPAWN_Boss, 0)

CLICKED_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(CLICKED_EVENT, 120)

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
                    for _ in music_pause:
                        _.set_volume(0)
                    music_game[current_index_music_game].set_volume(0.6)
                    current_index_music_game = (current_index_music_game + 1) % len(music_game)
                    pause = False
                else:
                    for _ in music_game:
                        _.set_volume(0)
                    music_pause[current_index_music_pause].set_volume(1)
                    current_index_music_pause = (current_index_music_pause + 1) % len(music_pause)
                    pause = True
        elif type == MONEY_EVENT:
            if pause is False and game.money < game.limit_money:
                game.money += 1
        elif type == ENEMY_SPAWN_Monster:
            if pause is False:
                entities.append(Enemy(*enemy1.data))
                entities[-1].spawn()
        elif type == ENEMY_SPAWN_Boss:
            if pause is False:
                entities.append(Enemy(*enemy2.data))
                entities[-1].spawn()
        elif type == CLICKED_EVENT:
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
    for index, button in enumerate(buttons):
        event = button.render(screen)
        if event == B_CLOSE:
            execute = False
        elif event == B_START_GAME:
            pygame.time.set_timer(MONEY_EVENT, SPEED_MONEY)
            pygame.time.set_timer(ENEMY_SPAWN_Monster, SPEED_SPAWN_ENEMY)
            pygame.time.set_timer(ENEMY_SPAWN_Boss, SPEED_SPAWN_BOSS)
            stage = GAME
            game = Game()
            bases = [game.enemy_base, game.defender_base]

            del buttons[index]
            buttons.append(Button(300, HEIGHT - 80, 150, 40, f"{fighter1.cost} {fighter1.name}"))
            buttons[-1].set_color(pygame.Color("grey"), (0, 100, 100))
            buttons[-1].func = B_BUY_DEFENDER_1
            buttons.append(Button(500, HEIGHT - 80, 150, 40, f"{fighter2.cost} {fighter2.name}"))
            buttons[-1].set_color(pygame.Color("grey"), (0, 100, 100))
            buttons[-1].func = B_BUY_DEFENDER_2
            buttons.append(Button(50, HEIGHT - 80, 150, 40, f"Lvl: {bases[1].lvl} up: {bases[1].cost_lvl}"))
            buttons[-1].set_color(pygame.Color("grey"), (0, 100, 100))
            buttons[-1].func = B_LVL_UP

            music_pause[current_index_music_pause].stop()
            music_game[current_index_music_game].stop()
            music_pause[current_index_music_pause].play(-1)
            music_game[current_index_music_game].play(-1)
            music_pause[current_index_music_pause].set_volume(0)
            music_game[current_index_music_game].set_volume(0.6)
        if pause is False:
            if event == B_BUY_DEFENDER_1 and game.money >= fighter1.cost and clicked:
                game.money -= fighter1.cost
                entities.append(Defender(*fighter1.data))
                entities[-1].spawn()
                sound_game['buy'].play()
                clicked = False
            if event == B_BUY_DEFENDER_2 and game.money >= fighter2.cost and clicked:
                game.money -= fighter2.cost
                entities.append(Defender(*fighter2.data))
                entities[-1].spawn()
                sound_game['buy'].play()
                clicked = False
            if event == B_LVL_UP and game.money >= bases[1].cost_lvl and clicked:
                game.money -= bases[1].cost_lvl
                buttons[-1].func = B_LVL_UP
                buttons[-1].text = f"Lvl: {bases[1].lvl} up: {bases[1].cost_lvl}"
                bases[1].lvl_up()
                LVL = bases[1].lvl
                game.limit_money = 100 * LVL
                sound_game['buy'].play()
                del buttons[index]
                buttons.append(Button(50, HEIGHT - 80, 175, 40, f"Lvl: {bases[1].lvl} up: {bases[1].cost_lvl}"))
                buttons[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                buttons[-1].func = B_LVL_UP
    if stage == GAME:
        game.render(screen)
        screen.blit(money_render, (0, 0))
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
                if entities[index].type == ENEMY and game.limit_money > game.money + entities[index].cost:
                    game.money += entities[index].cost
                del entities[index]
            entity.render(screen)
        money_text = f'Money: {game.money}/{game.limit_money}'
    elif stage == MENU:
        pygame.time.set_timer(ENEMY_SPAWN_Monster, 0)
        pygame.time.set_timer(ENEMY_SPAWN_Boss, 0)
        pygame.time.set_timer(MONEY_EVENT, 0)
        buttons = list()
        buttons.append(Button(WIDTH - 40, 0, 40, 40))
        buttons[-1].func = B_CLOSE
        buttons.append(Button(500, 300, 150, 40, "Start game"))
        buttons[-1].func = B_START_GAME
        for _ in music_game:
            _.set_volume(0)

        entities = list()
        # entities.append(Enemy(*fighter2.data))
        # entities[-1].spawn()
        # entities.append(Defender(*fighter2.data))
        # entities[-1].spawn()
    if pause is True:
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 370, 250))
        screen.blit(TEXT_PAUSE, (200, 200))
        screen.blit(TEXT_PRESS_ESC, (220, 255))

    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
