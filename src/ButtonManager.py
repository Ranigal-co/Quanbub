from src.Buttons import Button
from src.Settings import *


class ButtonManager:
    def __init__(self, heroes_menu=None, enhance_menu=None):
        self.buttons = []  # Список кнопок
        self.heroes_menu = heroes_menu  # Ссылка на объект HeroesMenu
        self.enhance_menu = enhance_menu  # Ссылка на объект DefenderBase

    def create_menu_buttons(self):
        """Создает кнопки для главного меню."""
        self.buttons.clear()

        self.buttons.append(Button(WIDTH - 40, 0, 40, 40))
        self.buttons[-1].func = B_CLOSE

        self.buttons.append(Button(WIDTH // 2 - 75, HEIGHT // 2 - 60, 150, 40, "Levels"))
        self.buttons[-1].func = B_LEVELS

        self.buttons.append(Button(WIDTH // 2 - 75, HEIGHT // 2, 150, 40, "Heroes"))
        self.buttons[-1].func = B_HEROES

        self.buttons.append(Button(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 40, "Enhance"))
        self.buttons[-1].func = B_ENHANCE

    def create_level_menu_buttons(self, levels):
        """Создает кнопки для меню уровней."""
        self.buttons.clear()

        # Кнопки для уровней
        for i, level in enumerate(levels):
            if level.is_unlocked:
                button = Button(425, 280 + i * 60, 210, 40, f"Level {level.level_id}")
                button.set_color((200, 0, 0), (100, 0, 0))  # Цвета для разблокированного уровня
            else:
                button = Button(425, 280 + i * 60, 210, 40, f"Level {level.level_id} (Locked)")
                button.set_color((100, 100, 100), (100, 100, 100))  # Серый цвет для заблокированного уровня
            button.func = f"SELECT_LEVEL_{level.level_id}"
            self.buttons.append(button)

        # Кнопка "Back"
        back_button = Button(WIDTH - 160, 0, 100, 40, "Back")
        back_button.func = MENU
        self.buttons.append(back_button)

    def create_heroes_menu_buttons(self, characters, deck):
        """Создает кнопки для меню героев."""
        self.buttons.clear()

        # Кнопки для персонажей
        for i, character in enumerate(characters):
            button_text = f"{character.name}" if character.in_deck else character.name
            button = Button(WIDTH - 240, 100 + i * 60, 200, 40, button_text)
            button.func = f"SELECT_CHARACTER_{i}"
            if self.heroes_menu.selected_character == character:
                button.set_color((0, 255, 0), (0, 200, 0))  # Зеленый цвет для выбранного персонажа
            else:
                button.set_color((200, 0, 0), (100, 0, 0))  # Красный цвет для остальных
            self.buttons.append(button)

        # Кнопки для слотов колоды
        for i in range(5):
            slot_character = deck.slots[i]
            button_text = f"{slot_character.name}" if slot_character else f""
            button = Button(40 + i * 180, HEIGHT - 80, 150, 40, button_text)
            button.func = f"SELECT_SLOT_{i}"
            if self.heroes_menu.selected_slot == i:
                button.set_color((0, 0, 255), (0, 0, 200))  # Синий цвет для выбранного слота
            else:
                button.set_color((200, 0, 0), (100, 0, 0))  # Красный цвет для остальных
            self.buttons.append(button)

        # Кнопка "Delete" (появляется только при выборе слота с персонажем)
        if self.heroes_menu.selected_slot is not None and deck.slots[self.heroes_menu.selected_slot] is not None:
            delete_button = Button(40, HEIGHT - 180, 100, 40, "Delete")
            delete_button.func = "DELETE_CHARACTER"
            delete_button.set_color((255, 0, 0), (200, 0, 0))  # Красный цвет для кнопки удаления
            self.buttons.append(delete_button)

        # Кнопка "Back"
        back_button = Button(WIDTH - 160, 0, 100, 40, "Back")
        back_button.func = MENU
        self.buttons.append(back_button)

    def create_enhance_menu_buttons(self, characters):
        """Создает кнопки для меню улучшений."""
        self.buttons.clear()

        # Кнопки для улучшения персонажей
        for i, character in enumerate(characters):
            button_text = f"{character.name}"
            button = Button(WIDTH - 330, 100 + i * 60, 160, 40, button_text)
            button.func = f"UPGRADE_CHARACTER_{i}"
            self.buttons.append(button)

        # Кнопка для улучшения здоровья базы
        button_text = f"Base HP"
        button = Button(60, 100, 200, 40, button_text)
        button.func = "UPGRADE_BASE_HP"
        self.buttons.append(button)

        # Кнопка для улучшения лимита денег базы
        button_text = f"Limit Money"
        button = Button(60, 160, 200, 40, button_text)
        button.func = "UPGRADE_BASE_LIMIT_MONEY"
        self.buttons.append(button)

        # Кнопка для улучшения скорости накопления денег базы
        button_text = f"Speed Money"
        button = Button(60, 220, 200, 40, button_text)
        button.func = "UPGRADE_BASE_SPEED_MONEY"
        self.buttons.append(button)

        # Кнопка "Back"
        back_button = Button(WIDTH - 160, 0, 100, 40, "Back")
        back_button.func = MENU
        self.buttons.append(back_button)

    def create_pause_buttons(self):
        """Создает кнопки для паузы."""
        self.buttons.clear()

        # Кнопка "Close" (закрыть игру)
        close_button = Button(WIDTH - 40, 0, 40, 40)
        close_button.func = B_CLOSE
        self.buttons.append(close_button)

        # Кнопка "Menu" (вернуться в главное меню)
        menu_button = Button(WIDTH - 160, 0, 100, 40, "Menu")
        menu_button.func = MENU_PAUSE
        self.buttons.append(menu_button)

    def create_results_buttons(self, is_victory, current_level, levels):
        """Создает кнопки для меню результатов."""
        self.buttons.clear()

        # Кнопка "Меню"
        menu_button = Button(WIDTH // 2 - 75, HEIGHT - 150, 150, 40, "Menu")
        menu_button.func = MENU
        self.buttons.append(menu_button)

        # Кнопка "Перепройти уровень"
        retry_button = Button(WIDTH // 2 - 75, HEIGHT - 100, 150, 40, "Retry Level")
        retry_button.func = "RETRY_LEVEL"
        self.buttons.append(retry_button)

        # Кнопка "Следующий уровень" (только если победа и есть следующий уровень)
        if is_victory and current_level.level_id < len(levels):
            next_level_button = Button(WIDTH // 2 - 75, HEIGHT - 50, 150, 40, "Next Level")
            next_level_button.func = "NEXT_LEVEL"
            self.buttons.append(next_level_button)

    def handle_events(self, event):
        """Обрабатывает события кнопок."""
        for button in self.buttons:
            event_result = button.render(screen)
            if event_result:
                return event_result
        return None

    def render_buttons(self, screen):
        """Отрисовывает кнопки на экране."""
        for button in self.buttons:
            button.render(screen)