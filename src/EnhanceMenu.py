from src.Buttons import Button
from Settings import *


class EnhanceMenu:
    def __init__(self, characters, defender_base, coin, db, levels):
        self.db = db
        self.levels = levels
        self.characters = characters
        self.defender_base = defender_base
        self.coin = coin
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        """Создаем кнопки для улучшения персонажей и базы."""
        self.buttons.clear()

        # Кнопки для улучшения персонажей
        for i, character in enumerate(self.characters):
            button_text = f"Upgrade {character.name} (Cost: {character.upgrade_cost})"
            button = Button(380, 100 + i * 60, 300, 40, button_text)
            button.func = f"UPGRADE_CHARACTER_{i}"
            self.buttons.append(button)

        # Кнопка для улучшения здоровья базы
        button_text = f"Base HP (Cost: {self.defender_base.hp_upgrade_cost})"
        button = Button(40, 400, 300, 40, button_text)
        button.func = "UPGRADE_BASE_HP"
        self.buttons.append(button)

        # Кнопка для улучшения лимита денег базы
        button_text = f"Limit Money (Cost: {self.defender_base.limit_money_upgrade_cost})"
        button = Button(40, 460, 300, 40, button_text)
        button.func = "UPGRADE_BASE_LIMIT_MONEY"
        self.buttons.append(button)

        # Кнопка для улучшения скорости накопления денег базы
        button_text = f"Speed Money (Cost: {self.defender_base.speed_money_upgrade_cost})"
        button = Button(40, 520, 300, 40, button_text)
        button.func = "UPGRADE_BASE_SPEED_MONEY"
        self.buttons.append(button)

        # Кнопка "Back"
        button = Button(WIDTH - 160, 0, 100, 40, "Back")
        button.func = MENU
        self.buttons.append(button)

    def handle_event(self, event):
        """Обрабатываем события в меню улучшений."""
        if event == "CLICK_OUTSIDE":
            # Сбрасываем выбор, если игрок нажал вне кнопок
            self.selected_character = None
            self.update_buttons()
        elif event.startswith("UPGRADE_CHARACTER_"):
            character_index = int(event.split("_")[-1])
            self.upgrade_character(character_index)
        elif event == "UPGRADE_BASE_HP":
            self.defender_base.upgrade_hp()
            self.db.save_base_upgrades(self.defender_base)
            self.db.save_progress(self.levels, self.coin.coins)
            self.update_buttons()
        elif event == "UPGRADE_BASE_LIMIT_MONEY":
            self.defender_base.upgrade_limit_money()
            self.db.save_base_upgrades(self.defender_base)
            self.db.save_progress(self.levels, self.coin.coins)
            self.update_buttons()
        elif event == "UPGRADE_BASE_SPEED_MONEY":
            self.defender_base.upgrade_speed_money()
            self.db.save_base_upgrades(self.defender_base)
            self.db.save_progress(self.levels, self.coin.coins)
            self.update_buttons()
        elif event == "UPGRADE_BASE":
            self.upgrade_base()

    def upgrade_character(self, character_index):
        """Улучшаем персонажа."""
        character = self.characters[character_index]
        if self.coin.coins >= character.upgrade_cost:
            self.coin.coins -= character.upgrade_cost
            character.upgrade()
            self.update_buttons()
            print(f"{character.name} upgraded to level {character.level}!")
            # Сохраняем данные о прокачке персонажа
            self.db.save_character_upgrades(self.characters)
            # Сохраняем текущее количество монет
            self.db.save_progress(self.levels, self.coin.coins)  # levels нужно передать, если оно доступно в EnhanceMenu
        else:
            print("Not enough coins!")

    def upgrade_base(self):
        """Улучшаем базу."""
        if self.coin.coins >= self.defender_base.upgrade_cost:
            self.coin.coins -= self.defender_base.upgrade_cost
            self.defender_base.upgrade()
            self.update_buttons()
            print(f"Base upgraded to level {self.defender_base.lvl}!")
            # Сохраняем данные о прокачке базы
            self.db.save_base_upgrades(self.defender_base)
            # Сохраняем текущее количество монет
            self.db.save_progress(self.levels, self.coin.coins)  # levels нужно передать, если оно доступно в EnhanceMenu
        else:
            print("Not enough coins!")

    def update_buttons(self):
        """Обновляем текст кнопок после улучшений."""
        self.buttons.clear()
        self.create_buttons()

    def render(self, screen):
        """Отрисовываем меню улучшений."""
        for button in self.buttons:
            button.render(screen)