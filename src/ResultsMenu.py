from src.Buttons import Button
from src.Settings import *

class ResultsMenu:
    def __init__(self, is_victory, coins_earned, current_level, levels, button_manager):
        self.is_victory = is_victory  # Победа или поражение
        self.coins_earned = coins_earned  # Количество заработанных монет
        self.current_level = current_level  # Текущий уровень
        self.levels = levels  # Список всех уровней
        self.button_manager = button_manager  # Ссылка на ButtonManager
        self.button_manager.create_results_buttons(is_victory, current_level, levels)

    def render(self, screen):
        """Отрисовывает меню результатов."""
        # Отображаем текст в зависимости от победы или поражения
        if self.is_victory:
            result_text = FONT_GAME.render("Victory!", True, (0, 255, 0))
            coins_text = FONT_PRESS_ESC.render(f"Coins earned: {self.coins_earned}", True, (255, 255, 255))
        else:
            result_text = FONT_GAME.render("Defeat!", True, (255, 0, 0))
            coins_text = FONT_PRESS_ESC.render("Try again!", True, (255, 255, 255))

        # Отрисовка текста
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))
        screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, 150))