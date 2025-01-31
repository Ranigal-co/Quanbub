import random

from Entities import Enemy, Defender
from Stages import Menu, Game
from Buttons import Button_game
from src.Entities import Monster, Boss
from Volume_editor import Rail, Slider
from Levels import Level
from LevelMenu import LevelMenu
from Database import Database
from Coins import Coins
from Characters import Character
from ButtonManager import *
from src.ResultsMenu import ResultsMenu

buttons_game = list()

USE_ENEMY = Monster(), Boss()
enemy1, enemy2 = USE_ENEMY

Rail = Rail(650, 13, 150, 4)

slider = Slider(725, 15, 5)

entities = list()

game = None
results_menu = None
base_def_game = Game()
current_music = None
current_menu_music = 0
current_game_music = 0
menu = Menu()
stage = MENU
bases = [base_def_game.defender_base]
LVL = 1

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
pygame.time.set_timer(TICK_EVENT, 0) # 0.1 секунда в Settings прописано

pause = False
clock = pygame.time.Clock()
execute = True

db = Database()
levels = [
    Level(1, 7500, 60000, 200, 0, 100 + random.randint(0, 100)),
    Level(2, 5000, 45000, 200, 0, 100 + random.randint(25, 150), 750),
    Level(3, 2000, 20000, 200, 0, 100 + random.randint(50, 200), 1000),
    Level(4, 1000, 10000, 200, 0, 300 + random.randint(200, 600), 3000),
    Level(5, 500, 3000, 200, 0, 1000 + random.randint(1000, 5000), 10000)
]

characters = [
    Character("Wall", 10, 230, 404, 5, AREA, 20, 19, 40),
    Character("Shit", 25, 100, 101, 20, SINGLE, 40, 24, 20),
    Character("Archer", 20, 350, 37, 90, SINGLE, 150, 38, 60),
    Character("Hero", 50, 200, 52, 36, AREA, 80, 52, 50),
    Character("Uber", 60, 220, 469, 170, AREA, 70, 213, 300),
    Character("Alpha", 80, 140, 2469, 160, AREA, 73, 690, 600)
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

# Создаем экземпляры ButtonManager для каждого меню
menu_button_manager = ButtonManager()
level_button_manager = ButtonManager()
heroes_button_manager = ButtonManager(heroes_menu)
enhance_button_manager = ButtonManager(heroes_menu, enhance_menu)
pause_button_manager = ButtonManager()
results_button_manager = ButtonManager()

while execute:
    screen.fill((0, 0, 0))
    if stage == GAME:
        screen.blit(bg, (0, 0))
    # Загрузка и воспроизведение музыки для разных стадий
    if stage != GAME and stage != RESULTS:
        if current_music != "menu_music":
            pygame.mixer_music.fadeout(500)
            pygame.mixer_music.load(f'../music/music_menu/menu_{current_menu_music}')  # Путь к музыке для меню
            current_menu_music = (current_menu_music + 1) % 5
            pygame.mixer_music.play(loops=1, fade_ms=500)
            pygame.mixer_music.set_volume(1)
            current_music = "menu_music"
        elif not pygame.mixer_music.get_busy():
            current_menu_music = (current_menu_music + 1) % 5
            pygame.mixer_music.fadeout(500)
            pygame.mixer_music.load(f'../music/music_menu/menu_{current_menu_music}')  # Путь к музыке для меню
            pygame.mixer_music.play(loops=1, fade_ms=500)
            pygame.mixer_music.set_volume(1)
    elif stage == RESULTS:
        if current_music != "results_music":
            pygame.mixer_music.fadeout(500)
            if results_menu.is_victory:
                pygame.mixer_music.load('../music/music_pause/mus_main.mp3')  # Путь к музыке победы
                pygame.mixer_music.play(loops=-1, fade_ms=15000)
            else:
                pygame.mixer_music.load('../music/music_pause/mus_main.mp3')  # Путь к музыке поражения
                pygame.mixer_music.play(loops=-1, fade_ms=7000)
            pygame.mixer_music.set_volume(1)
            current_music = "results_music"
    elif stage == GAME:
        if current_music != "game_music":
            pygame.mixer_music.fadeout(500)
            pygame.mixer_music.load(f'../music/music_game/battle_{current_game_music}.mp3')  # Путь к музыке для игры
            pygame.mixer_music.play(loops=-1, fade_ms=500)
            pygame.mixer_music.set_volume(0.6)
            current_music = "game_music"
    money_render = FONT_GAME.render(money_text, True, pygame.Color("yellow"))
    for event in pygame.event.get():
        type = event.type
        if type == pygame.QUIT:
            execute = False
        elif type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, было ли нажатие вне кнопок
            clicked_outside = True
            for button in heroes_button_manager.buttons:
                if button.button.collidepoint(event.pos):
                    clicked_outside = False
                    break
            if clicked_outside:
                # Сбрасываем выбор, если игрок нажал вне кнопок
                heroes_menu.selected_character = None
                heroes_menu.selected_slot = None
                heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
        elif type == pygame.KEYDOWN and stage == GAME:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] == 1:
                sound_game['pause'].play()
                if pause is True:
                    pos_music_pause = pygame.mixer_music.get_pos() / 1000
                    pygame.mixer_music.fadeout(500)
                    pygame.mixer_music.load(f'../music/music_game/battle_{current_game_music}.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=500)
                    pygame.mixer_music.set_volume(0.6)
                    pause = False
                    pause_button_manager.buttons.clear()  # Очищаем кнопки паузы
                else:
                    pos_music_game = pygame.mixer_music.get_pos() / 1000
                    pygame.mixer_music.fadeout(500)
                    pygame.mixer_music.load('../music/music_pause/mus_main.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_pause, fade_ms=500)
                    pygame.mixer_music.set_volume(1)
                    pause = True
                    pause_button_manager.create_pause_buttons()  # Создаем кнопки паузы
        elif type == MONEY_EVENT:
            if pause is False:
                if game.money < game.limit_money:
                    game.money += 1
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
    for index, button in enumerate(menu_button_manager.buttons):
        event = button.render(screen)
        if event == B_CLOSE:
            execute = False
        elif event == B_HEROES:
            stage = HEROES_MENU
            sound_game['button'].play()
        elif event == MENU:
            stage = MENU
            sound_game['button'].play()
        elif event == MENU_PAUSE:
            stage = MENU
            pause = False
            sound_game['button'].play()
        elif event == B_ENHANCE:
            stage = ENHANCE_MENU
            sound_game['button'].play()
        elif event == B_LEVELS:
            stage = LEVEL_MENU
            sound_game['button'].play()

    for index, button in enumerate(buttons_game):
        for char in characters_game:
            if button.func == char.name:
                button.recharge_func(game.money, char.cost)
        if button.func == B_LVL_UP:
            button.recharge_func(game.money, bases[0].cost_lvl)
        event = button.render_b(screen, pause)
        if pause is False:
            if event == B_LVL_UP:
                game.money -= bases[0].cost_lvl  # bases[0] ссылается на defender_base
                buttons_game[-1].func = B_LVL_UP
                bases[0].lvl_up()
                LVL = bases[0].lvl
                game.limit_money = bases[0].limit_money * LVL
                sound_game['buy'].play()
                buttons_game[index].recharge = buttons_game[index].const_rech
                del buttons_game[index]
                buttons_game.append(
                    Button_game(10, HEIGHT - 80, 150, 40, f"Base Lvl: {bases[0].lvl}", 2,
                                bases[0].cost_lvl))
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
        buttons_game.clear()
        if len(menu_button_manager.buttons) < 2:  # Создаем кнопки только если они еще не созданы
            menu_button_manager.create_menu_buttons()
        entities.clear()
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))

    elif stage == LEVEL_MENU:
        for j in range(len(menu_button_manager.buttons) - 1, 0, -1):
            del menu_button_manager.buttons[j]
        # Создаем кнопки для меню уровней, если они еще не созданы
        if not level_button_manager.buttons:
            level_button_manager.create_level_menu_buttons(levels)
        # Отрисовка кнопок уровней и кнопки "Back"
        for button in level_button_manager.buttons:
            event = button.render(screen)
            if event == MENU:
                stage = MENU  # Возвращаемся в главное меню при нажатии на кнопку "Back"
                sound_game['button'].play()
            elif event and event.startswith("SELECT_LEVEL_"):
                level_id = int(event.split("_")[-1])  # Получаем ID уровня из события
                selected_level = levels[level_id - 1]  # Получаем выбранный уровень
                if selected_level.is_unlocked:
                    pygame.time.set_timer(MONEY_EVENT, int(selected_level.money_speed / bases[0].speed_money))
                    pygame.time.set_timer(ENEMY_SPAWN_Monster, selected_level.enemy_spawn_interval)
                    pygame.time.set_timer(ENEMY_SPAWN_Boss, selected_level.boss_spawn_interval)
                    pygame.time.set_timer(TICK_EVENT, TICK)
                    stage = GAME
                    game = Game(selected_level.enemy_hp_base)
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
                            button = Button_game(170 + i * 160, HEIGHT - 80, 150, 40,
                                                 f"{character.name}", character.recharge, character.cost)
                            button.set_color(pygame.Color("grey"), (0, 100, 100))
                            button.func = str(character.name)
                            buttons_game.append(button)

                    buttons_game.append(
                        Button_game(10, HEIGHT - 80, 150, 40, f"Base Lvl: {bases[0].lvl}", 2, bases[0].cost_lvl))
                    buttons_game[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                    buttons_game[-1].func = B_LVL_UP

                    sound_game['button'].play()

                    pos_music_game = 0
                    pos_music_pause = 0
                    pygame.mixer_music.fadeout(1000)
                    pygame.mixer_music.load('../music/music_game/battle_3.mp3')
                    pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=1000)
                    pygame.mixer_music.set_volume(0.6)

                    current_game_music = (current_game_music + 1) % 7  # смена игровой музыки
                else:
                    print(f"Level {level_id} is locked!")  # Уровень заблокирован
        # Отрисовка текста с количеством монет (если нужно)
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))

    elif stage == HEROES_MENU:
        for j in range(len(menu_button_manager.buttons) - 1, 0, -1):
            del menu_button_manager.buttons[j]
        if not heroes_button_manager.buttons:  # Создаем кнопки только если они еще не созданы
            heroes_button_manager.create_heroes_menu_buttons(characters, deck)
        for index, button in enumerate(heroes_button_manager.buttons):
            event = button.render(screen)
            if event == MENU:
                stage = MENU  # Возвращаемся в главное меню при нажатии на кнопку "Back"
                sound_game['button'].play()
            elif event and event.startswith("SELECT_CHARACTER_"):
                character_index = int(event.split("_")[-1])
                heroes_menu.selected_character = characters[character_index]
                heroes_menu.selected_slot = None  # Сбрасываем выбор слота
                heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
                sound_game['button'].play()
            elif event and event.startswith("SELECT_SLOT_"):
                slot_index = int(event.split("_")[-1])
                if heroes_menu.selected_character:
                    # Если выбран персонаж, добавляем его в слот
                    if deck.slots[slot_index] is None:
                        if deck.add_character(heroes_menu.selected_character, slot_index):
                            heroes_menu.selected_slot = slot_index
                            heroes_menu.selected_character = None
                            heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
                            db.save_deck(deck)  # Сохраняем колоду
                            sound_game['button'].play()
                        else:
                            print("Character is already in deck!")
                    else:
                        if deck.replace_character(heroes_menu.selected_character, slot_index):
                            heroes_menu.selected_slot = slot_index
                            heroes_menu.selected_character = None
                            heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
                            db.save_deck(deck)  # Сохраняем колоду
                            sound_game['button'].play()
                        else:
                            print("Character is already in deck!")
                else:
                    # Если персонаж не выбран, просто выбираем слот
                    heroes_menu.selected_slot = slot_index
                    heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
                    sound_game['button'].play()
            elif event == "DELETE_CHARACTER":
                if heroes_menu.selected_slot is not None and deck.slots[heroes_menu.selected_slot] is not None:
                    # Удаляем персонажа из выбранного слота
                    deck.remove_character(heroes_menu.selected_slot)
                    heroes_menu.selected_slot = None
                    heroes_menu.selected_character = None
                    heroes_button_manager.create_heroes_menu_buttons(characters, deck)  # Обновляем кнопки
                    db.save_deck(deck)  # Сохраняем колоду
                    sound_game['button'].play()
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))

    elif stage == ENHANCE_MENU:
        for j in range(len(menu_button_manager.buttons) - 1, 0, -1):
            del menu_button_manager.buttons[j]
        # Создаем кнопки для меню улучшений, если они еще не созданы
        if not enhance_button_manager.buttons:
            enhance_button_manager.create_enhance_menu_buttons(characters)
        # Обработка событий кнопок
        for index, button in enumerate(enhance_button_manager.buttons):
            event = button.render(screen)
            if event == MENU:
                stage = MENU  # Возвращаемся в главное меню при нажатии на кнопку "Back"
                sound_game['button'].play()
            elif event and event.startswith("UPGRADE_CHARACTER_"):
                character_index = int(event.split("_")[-1])
                character = characters[character_index]
                if coin.coins >= character.upgrade_cost:
                    coin.coins -= character.upgrade_cost
                    character.upgrade()
                    db.save_character_upgrades(characters)  # Сохраняем данные о прокачке персонажей
                    db.save_progress(levels, coin.coins)  # Сохраняем текущее количество монет
                    enhance_button_manager.create_enhance_menu_buttons(characters)  # Обновляем кнопки
                    sound_game['buy'].play()
            elif event == "UPGRADE_BASE_HP":
                bases[0].upgrade_hp()
                db.save_base_upgrades(bases[0])  # Сохраняем данные о прокачке базы
                db.save_progress(levels, coin.coins)  # Сохраняем текущее количество монет
                enhance_button_manager.create_enhance_menu_buttons(characters)  # Обновляем кнопки
            elif event == "UPGRADE_BASE_LIMIT_MONEY":
                bases[0].upgrade_limit_money()
                db.save_base_upgrades(bases[0])  # Сохраняем данные о прокачке базы
                db.save_progress(levels, coin.coins)  # Сохраняем текущее количество монет
                enhance_button_manager.create_enhance_menu_buttons(characters)  # Обновляем кнопки
            elif event == "UPGRADE_BASE_SPEED_MONEY":
                bases[0].upgrade_speed_money()
                db.save_base_upgrades(bases[0])  # Сохраняем данные о прокачке базы
                db.save_progress(levels, coin.coins)  # Сохраняем текущее количество монет
                enhance_button_manager.create_enhance_menu_buttons(characters)  # Обновляем кнопки

        # Отрисовка кнопок
        enhance_button_manager.render_buttons(screen)

        # Отрисовка текста с количеством монет
        coins_render = FONT_GAME.render(f'Coins: {coin.coins}', True, pygame.Color("yellow"))
        screen.blit(coins_render, (WIDTH / 2 - coins_render.get_width() / 2, 0))

    elif stage == GAME:
        pygame.mixer_music.set_volume(slider.Volume_digit())
        sound_game['buy'].set_volume(slider.Volume_digit())
        sound_game['hit_defender'].set_volume(slider.Volume_digit())
        game.render(screen)
        base_def_game.render_def_base(screen)
        screen.blit(money_render, (0, 0))
        menu_button_manager.buttons.clear()

        # Отображение текущего уровня
        level_text = FONT_PRESS_ESC.render(f"Level: {selected_level.level_id}", True, (255, 255, 255))
        screen.blit(level_text, (WIDTH - level_text.get_width(), 0))  # Позиция в верхнем правом углу

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
                            level_button_manager.create_level_menu_buttons(levels)
                        # Создаем меню результатов для победы
                        results_menu = ResultsMenu(True, levels[selected_level.level_id - 1].coins, selected_level, levels, results_button_manager)
                        sound_game['victory.mp3'].play()
                    else:
                        # Создаем меню результатов для поражения
                        results_menu = ResultsMenu(False, 0, selected_level, levels, results_button_manager)
                        sound_game['lose.mp3'].play()
                    db.save_progress(levels, coin.coins)
                    level_menu.update_buttons()
                    stage = RESULTS  # Переходим на стадию результатов
                    bases[0].hp = bases[0].hp_select
                    pygame.mixer_music.fadeout(500)
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

    elif stage == RESULTS:
        buttons_game.clear()
        if results_menu:
            # Отрисовываем меню результатов
            results_menu.render(screen)
            for index, button in enumerate(results_button_manager.buttons):
                event = button.render(screen)
                if event == MENU:
                    stage = MENU  # Возвращаемся в главное меню
                    results_menu = None  # Сбрасываем меню результатов
                    sound_game['button'].play()
                elif event == "RETRY_LEVEL":
                    # Перезапускаем текущий уровень
                    entities.clear()
                    results_menu = None
                    if selected_level.is_unlocked:
                        pygame.time.set_timer(MONEY_EVENT, int(selected_level.money_speed / bases[0].speed_money))
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
                                button = Button_game(170 + i * 160, HEIGHT - 80, 150, 40,
                                                     f"{character.name}", character.recharge, character.cost)
                                button.set_color(pygame.Color("grey"), (0, 100, 100))
                                button.func = str(character.name)
                                buttons_game.append(button)

                        buttons_game.append(
                            Button_game(10, HEIGHT - 80, 150, 40, f"Base Lvl: {bases[0].lvl}", 2, bases[0].cost_lvl))
                        buttons_game[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                        buttons_game[-1].func = B_LVL_UP

                        pos_music_game = 0
                        pos_music_pause = 0
                        pygame.mixer_music.fadeout(1000)
                        pygame.mixer_music.load('../music/music_game/battle_3.mp3')
                        pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=1000)
                        pygame.mixer_music.set_volume(0.6)
                    sound_game['button'].play()
                elif event == "NEXT_LEVEL":
                    # Переходим на следующий уровень
                    entities.clear()
                    results_menu = None
                    if selected_level.level_id < len(levels):
                        level_id = selected_level.level_id
                        selected_level = levels[level_id]
                        if selected_level.is_unlocked:
                            pygame.time.set_timer(MONEY_EVENT, int(selected_level.money_speed / bases[0].speed_money))
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
                                    button = Button_game(170 + i * 160, HEIGHT - 80, 150, 40,
                                                         f"{character.name}", character.recharge, character.cost)
                                    button.set_color(pygame.Color("grey"), (0, 100, 100))
                                    button.func = str(character.name)
                                    buttons_game.append(button)

                            buttons_game.append(
                                Button_game(10, HEIGHT - 80, 150, 40, f"Base Lvl: {bases[0].lvl}", 2,
                                            bases[0].cost_lvl))
                            buttons_game[-1].set_color(pygame.Color("grey"), (0, 100, 100))
                            buttons_game[-1].func = B_LVL_UP

                            pos_music_game = 0
                            pos_music_pause = 0
                            pygame.mixer_music.fadeout(1000)
                            pygame.mixer_music.load('../music/music_game/battle_3.mp3')
                            pygame.mixer_music.play(loops=-1, start=pos_music_game, fade_ms=1000)
                            pygame.mixer_music.set_volume(0.6)
                        sound_game['button'].play()

    if pause is True:
        if stage == GAME:
            # Отрисовка элементов паузы
            Rail.Render_rail(screen)
            slider.Render_slider(screen)
            screen.blit(TEXT_PAUSE, (200, 200))
            screen.blit(TEXT_PRESS_ESC, (220, 255))

            # Создаем кнопки для паузы, если они еще не созданы
            if not pause_button_manager.buttons:
                pause_button_manager.create_pause_buttons()

            # Обработка событий кнопок паузы
            for index, button in enumerate(pause_button_manager.buttons):
                event = button.render(screen)
                if event == B_CLOSE:
                    execute = False  # Закрываем игру
                elif event == MENU_PAUSE:
                    stage = MENU  # Возвращаемся в главное меню
                    pause = False  # Снимаем паузу
                    sound_game['button'].play()

            # Отрисовка кнопок паузы
            pause_button_manager.render_buttons(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()