from Buttons import Button


class LevelMenu:
    def __init__(self, levels):
        self.levels = levels
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        """Создание кнопок для уровней."""
        for i, level in enumerate(self.levels):
            self.add_button(i, level)

    def add_button(self, index, level):
        """Добавление кнопки для уровня."""
        if level.is_unlocked:
            button = Button(425, 280 + index * 60, 150, 40, f"Level {level.level_id}")
            button.set_color((200, 0, 0), (100, 0, 0))  # Цвета для разблокированного уровня
        else:
            button = Button(425, 280 + index * 60, 150, 40, f"Level {level.level_id} (Locked)")
            button.set_color((100, 100, 100), (100, 100, 100))  # Серый цвет для заблокированного уровня
        button.func = f"SELECT_LEVEL_{level.level_id}"
        self.buttons.append(button)

    def update_buttons(self):
        """Обновление кнопок после разблокировки уровней."""
        self.buttons.clear()
        self.create_buttons()

    def render(self, screen):
        """Отрисовка кнопок."""
        for button in self.buttons:
            button.render(screen)