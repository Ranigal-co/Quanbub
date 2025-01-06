import random

from Settings import *
from Entities import Enemy, Defender, Hero, Shit
from Stages import Menu, Game
from Buttons import Button, Button_game
from src.Entities import Monster, Boss
from Volume_editor import Rail, Slider
from Levels import Level
from LevelMenu import LevelMenu
from Database import Database
from Coins import Coins
from HeroesMenu import HeroesMenu
from Characters import Character
from EnhanceMenu import EnhanceMenu
from Base import DefenderBase


buttons = list()
buttons_game = list()
buttons.append(Button(WIDTH - 40, 0, 40, 40))
buttons[-1].func = B_CLOSE

USE_FIGHTER = Hero(), Shit()
fighter1, fighter2 = USE_FIGHTER
USE_ENEMY = Monster(), Boss()
enemy1, enemy2 = USE_ENEMY

Rail = Rail(650, 13, 150, 4)

slider = Slider(725, 15, 5)

entities = list()

game = None
base_def_game = Game()
menu = Menu()
stage = MENU
bases = [base_def_game.defender_base]
LVL = 1

pygame.mixer_music.load('../music/music_game/battle_3.mp3')
sound_game = {'buy':pygame.mixer.Sound('../music/sounds_game/buy.mp3'),
              'pause':pygame.mixer.Sound('../music/sounds_game/pause.mp3'),
              'hit_defender':pygame.mixer.Sound('../music/sounds_game/hit.mp3')}
pos_music_game = 0
pos_music_pause = 0

bg = pygame.image.load("../sprites/backgrounds/background.png")

money_text = f'Balance: 0'

MONEY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MONEY_EVENT, 0)

ENEMY_SPAWN_Monster = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SPAWN_Monster, 0)

ENEMY_SPAWN_Boss = pygame.USEREVENT + 3
pygame.time.set_timer(ENEMY_SPAWN_Boss, 0)

'''
Тик это единица времени для игры, в ней будем измерять всё
'''

TICK_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(TICK_EVENT, 0) # 1 секунда в Settings прописано

pause = False
clock = pygame.time.Clock()
execute = True

db = Database()
levels = [
    Level(1, 7500, 60000, 200, 0, 100 + random.randint(0, 100)),
    Level(2, 5000, 45000, 200, 0, 100 + random.randint(25, 150)),
    Level(3, 3000, 30000, 200, 0, 100 + random.randint(50, 200))
]

characters = [
    Character("Hero", 50, 200, 52, 36, AREA, 80, 50, 5),
    Character("Shit", 25, 100, 100, 20, SINGLE, 40, 25, 2)
]

deck = db.load_deck(characters)
heroes_menu = HeroesMenu(characters, deck, db)

coin = Coins(0)
db.load_progress(levels, coin)
bases[0].coin = coin

# Загружаем данные о прокачке персонажей и базы
db.load_character_upgrades(characters)
db.load_base_upgrades(bases[0])  # bases[0] - это defender_base

enhance_menu = EnhanceMenu(characters, bases[0], coin, db, levels)
enhance_menu.update_buttons()  # Обновляем кнопки после загрузки данных

level_menu = LevelMenu(levels)

selected_level = levels[0]

while execute:
    screen.fill((0, 0, 0))
    if stage == GAME:
        screen.blit(bg, (0, 0))
    money_render = FONT_GAME.render(money_text, True, pygame.Color("yellow"))
    for event in pygame.event.get():
        type = event.type
        if type == pygame.QUIT:
            execute = False
        elif type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, было ли нажатие вне кнопок
            clicked_outside = True
            for button in heroes_menu.buttons:
                if button.button.collidepoint(event.pos):
                    clicked_outside = False
                    break
            if heroes_menu.delete_button:
                if heroes_menu.delete_button.button.collidepoint(event.pos):
                    clicked_outside = False
                    break
            if clicked_outside:
                heroes_menu.handle_event("CLICK_OUTSIDE")  # Сбрасываем выбор
        elif type == pygame.KEYDOWN and stage == GAME:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] == 1:
                sound_game['pause'].play()
                if pause is True:
                    pos_music_pause = pygame.mixer_music.get_pos() / 1000
                    pygame.mixer_music.fadeout(500)
                    pygame.mixer_music.load('../music/music_game/battle_3.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=500)
                    pygame.mixer_music.set_volume(0.6)
                    pause = False
                else:
                    pos_music_game = pygame.mixer_music.get_pos() / 1000
                    pygame.mixer_music.fadeout(500)
                    pygame.mixer_music.load('../music/music_pause/mus_main.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_pause, fade_ms=500)
                    pygame.mixer_music.set_volume(1)
                    pause = True
        elif type == MONEY_EVENT:
            if pause is False:
                if game.money + bases[0].speed_money <= game.limit_money:
                    game.money += bases[0].speed_money  # Увеличиваем деньги на скорость накопления
                elif game.money + bases[0].speed_money >= game.limit_money:
                    game.money = game.limit_money
        elif type == ENEMY_SPAWN_Monster:
            if pause is False:
                entities.append(Enemy(*enemy1.data))
                entities[-1].spawn()
        elif type == ENEMY_SPAWN_Boss:
            if pause is False:
                entities.append(Enemy(*enemy2.data))
                entities[-1].spawn()
        elif type == TICK_EVENT:
            if pause is False:
                for button in buttons_game:
                    if button.recharge_func_tick() is False:
                        button.recharge -= 1
    for index, button in enumerate(buttons):
        event = button.render(screen)
        if event == B_CLOSE:
            execute = False
        elif event == B_HEROES:
            stage = HEROES_MENU
        elif event == MENU:
            stage = MENU
        elif event == MENU_PAUSE:
            stage = MENU
            pause = False
        elif event == B_ENHANCE:
            stage = ENHANCE_MENU  # Переходим в меню улучшений

    for index, button in enumerate(buttons_game):
        for char in characters_game:
            if button.func == char.name:
                button.recharge_func(game.money, char.cost)
        if button.func == B_LVL_UP:
            button.recharge_func(game.money, bases[0].cost_lvl)
        event = button.render_b(screen, pause)
        if pause is False:
            if event == B_LVL_UP:
                game.money -= bases[0].cost_lvl  # Теперь bases[0] ссылается на defender_base
                buttons_game[-1].func = B_LVL_UP
                bases[0].lvl_up()
                LVL = bases[0].lvl
                game.limit_money = bases[0].limit_money * LVL
                sound_game['buy'].play()
                buttons_game[index].recharge = buttons_game[index].const_rech
                del buttons_game[index]
                buttons_game.append(Button_game(50, HEIGHT - 80, 175, 40, f"Lvl: {bases[0].lvl} up: {bases[0].cost_lvl}", 2))
                buttons_game[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                buttons_game[-1].func = B_LVL_UP
            for char in characters_game:
                if event == char.name:
                    game.money -= char.cost
                    entities.append(Defender(*char.get_data()))
                    entities[-1].spawn()
                    sound_game['buy'].play()
                    buttons_game[index].recharge = buttons_game[index].const_rech

    if stage == MENU:
        pygame.time.set_timer(ENEMY_SPAWN_Monster, 0)
        pygame.time.set_timer(ENEMY_SPAWN_Boss, 0)
        pygame.time.set_timer(MONEY_EVENT, 0)
        pygame.time.set_timer(TICK_EVENT, 0)
        buttons.clear()
        buttons_game.clear()
        buttons.append(Button(WIDTH - 40, 0, 40, 40))
        buttons[-1].func = B_CLOSE
        buttons.append(Button(40, 40, 150, 40, "Levels"))
        buttons[-1].func = B_LEVELS
        buttons.append(Button(40, 100, 150, 40, "Heroes"))
        buttons[-1].func = B_HEROES
        buttons.append(Button(40, 160, 150, 40, "Enhance"))
        buttons[-1].func = B_ENHANCE
        pygame.mixer_music.fadeout(1000)
        entities.clear()
        for index, button in enumerate(buttons):
            event = button.render(screen)
            if event == B_CLOSE:
                execute = False
            elif event == B_LEVELS:
                stage = LEVEL_MENU
                for j in range(len(buttons) - 1, 0, -1):
                    del buttons[j]
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))

    elif stage == LEVEL_MENU:
        level_menu.render(screen)
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))
        buttons.append(Button(WIDTH - 160, 0, 100, 40, "Back"))
        buttons[-1].func = MENU
        for button in level_menu.buttons:
            event = button.render(screen)
            if event and event.startswith("SELECT_LEVEL_"):
                level_id = int(event.split("_")[-1])
                selected_level = levels[level_id - 1]
                if selected_level.is_unlocked:
                    pygame.time.set_timer(MONEY_EVENT, selected_level.money_speed)
                    pygame.time.set_timer(ENEMY_SPAWN_Monster, selected_level.enemy_spawn_interval)
                    pygame.time.set_timer(ENEMY_SPAWN_Boss, selected_level.boss_spawn_interval)
                    pygame.time.set_timer(TICK_EVENT, TICK)
                    stage = GAME
                    game = Game()
                    game.money = selected_level.initial_money
                    if len(bases) > 1:
                        del bases[-1]
                    bases[0].hp = bases[0].hp_select
                    bases[0].lvl = 1
                    bases[0].cost_lvl = 50
                    game.limit_money = bases[0].limit_money
                    bases.append(game.enemy_base)  # Теперь defender_base идет первым, а enemy_base вторым

                    buttons_game.clear()
                    # Создание кнопок для персонажей из колоды
                    characters_game = deck.get_characters()

                    for i, character in enumerate(characters_game):
                        if character:
                            button = Button_game(250 + i * 200, HEIGHT - 80, 150, 40,f"{character.cost} {character.name}", character.recharge)
                            button.set_color(pygame.Color("grey"), (0, 100, 100))
                            button.func = str(character.name)
                            buttons_game.append(button)

                    buttons_game.append(
                        Button_game(50, HEIGHT - 80, 150, 40, f"Lvl: {bases[0].lvl} up: {bases[0].cost_lvl}", 2))
                    buttons_game[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                    buttons_game[-1].func = B_LVL_UP

                    pos_music_game = 0
                    pos_music_pause = 0
                    pygame.mixer_music.fadeout(1000)
                    pygame.mixer_music.load('../music/music_game/battle_3.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=1000)
                    pygame.mixer_music.set_volume(0.6)

    elif stage == HEROES_MENU:
        for j in range(len(buttons) - 1, 0, -1):
            del buttons[j]
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))
        buttons.append(Button(WIDTH - 160, 0, 100, 40, "Back"))
        buttons[-1].func = MENU
        heroes_menu.render(screen)
        for button in heroes_menu.buttons:
            event = button.render(screen)
            if event:
                heroes_menu.handle_event(event)
        if heroes_menu.delete_button:
            delete_event = heroes_menu.delete_button.render(screen)
            if delete_event == "DELETE_CHARACTER":
                heroes_menu.handle_event("DELETE_CHARACTER")

    elif stage == ENHANCE_MENU:
        # Создаем EnhanceMenu только при переходе в меню улучшений
        enhance_menu = EnhanceMenu(characters, bases[0], coin, db, levels)
        for j in range(len(buttons) - 1, 0, -1):
            del buttons[j]
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))
        buttons.append(Button(WIDTH - 160, 0, 100, 40, "Back"))
        buttons[-1].func = MENU
        enhance_menu.render(screen)
        for button in enhance_menu.buttons:
            event = button.render(screen)
            if event:
                enhance_menu.handle_event(event)

    elif stage == GAME:
        pygame.mixer_music.set_volume(slider.Volume_digit())
        sound_game['buy'].set_volume(slider.Volume_digit())
        sound_game['hit_defender'].set_volume(slider.Volume_digit())
        game.render(screen)
        base_def_game.render_def_base(screen)
        screen.blit(money_render, (0, 0))
        buttons.clear()

        # Отрисовка игровых кнопок
        for button in buttons_game:
            button.render_b(screen, pause)

        for index, entity in enumerate(entities):
            if pause is False:
                game_over = entity.move_attack(entities, bases)
                if 'win' in game_over:
                    if game_over == DEFENDER_WIN:
                        # Начисляем награду за прохождение уровня
                        coin.coins += levels[selected_level.level_id - 1].coins
                        # Открываем следующий уровень
                        if selected_level.level_id < len(levels):
                            levels[selected_level.level_id].is_unlocked = True
                            level_menu.update_buttons()
                    db.save_progress(levels, coin.coins)
                    stage = MENU
                    print(game_over)
                elif 'play' in game_over:
                    sound_game['hit_defender'].play()
            status_enemy = entity.check_hp()
            if status_enemy == DEATH:
                if entities[index].type == ENEMY:
                    if game.limit_money > game.money + entities[index].cost:
                        game.money += entities[index].cost
                    else:
                        game.money = game.limit_money
                del entities[index]
            entity.render(screen)
            entity.render_font(screen)
        money_text = f'Money: {game.money}/{game.limit_money}'

    if pause is True:
        if stage == GAME:
            Rail.Render_rail(screen)
            slider.Render_slider(screen)
            buttons.append(Button(WIDTH - 40, 0, 40, 40))
            buttons[-1].func = B_CLOSE
            buttons.append(Button(WIDTH - 160, 0, 100, 40, "Menu"))
            buttons[-1].func = MENU_PAUSE
            screen.blit(TEXT_PAUSE, (200, 200))
            screen.blit(TEXT_PRESS_ESC, (220, 255))
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()