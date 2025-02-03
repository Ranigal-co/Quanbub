from Settings import *
from Buttons import Button


class HeroesMenu:
    def __init__(self, characters, deck, db):
        self.characters = characters
        self.deck = deck
        self.db = db
        self.selected_character = None
        self.selected_slot = None  # Выбранный слот
        self.buttons = []
        self.delete_button = None  # Кнопка для удаления персонажа
        self.create_buttons()

    def create_buttons(self):
        """Создает кнопки для персонажей и слотов колоды."""
        self.buttons.clear()  # Очищаем старые кнопки

        # Кнопки для персонажей
        for i, character in enumerate(self.characters):
            button_text = f"{character.name}" if character.in_deck else character.name
            button = Button(WIDTH - 240, 100 + i * 60, 200, 40, button_text)
            button.func = f"SELECT_CHARACTER_{i}"
            character_text = FONT_RECHARGE.render("(In Deck)", True, pygame.Color("yellow"))
            screen.blit(character_text, (WIDTH - 240 - character_text.get_width(), 100 + i * 60))
            if self.selected_character == character:
                button.set_color((0, 255, 0), (0, 200, 0))  # Зеленый цвет для выбранного персонажа
            else:
                button.set_color((200, 0, 0), (100, 0, 0))  # Красный цвет для остальных
            self.buttons.append(button)

        # Кнопки для слотов колоды
        for i in range(5):
            slot_character = self.deck.slots[i]
            button_text = f"{slot_character.name}" if slot_character else f""
            button = Button(40 + i * 180, HEIGHT - 80, 150, 40, button_text)
            button.func = f"SELECT_SLOT_{i}"
            slot_text = FONT_RECHARGE.render(f"Slot {i + 1}: ", True, pygame.Color("yellow"))
            screen.blit(slot_text, (40 + i * 180, HEIGHT - 80 - slot_text.get_height()))
            if self.selected_slot == i:
                button.set_color((0, 0, 255), (0, 200, 0))  # Зеленый цвет для выбранного слота
            else:
                button.set_color((200, 0, 0), (100, 0, 0))  # Красный цвет для остальных
            self.buttons.append(button)

        # Кнопка "Delete" (появляется только при выборе слота с персонажем)
        if self.selected_slot is not None and self.deck.slots[self.selected_slot] is not None:
            self.delete_button = Button(40, HEIGHT - 240, 200, 40, "Delete")
            self.delete_button.func = "DELETE_CHARACTER"
            self.delete_button.set_color((255, 0, 0), (200, 0, 0))  # Красный цвет для кнопки удаления
        else:
            self.delete_button = None

    def update_buttons(self):
        """Обновляет текст и состояние кнопок."""
        self.create_buttons()

    def handle_event(self, event):
        """Обрабатывает события выбора персонажа и слота."""
        if event == "CLICK_OUTSIDE":
            # Сбрасываем выбор, если игрок нажал вне кнопок
            self.selected_character = None
            self.selected_slot = None
            self.update_buttons()  # Обновляем кнопки
        elif event.startswith("SELECT_CHARACTER_"):
            character_index = int(event.split("_")[-1])
            self.selected_character = self.characters[character_index]
            self.selected_slot = None  # Сбрасываем выбор слота при выборе персонажа
            self.update_buttons()  # Обновляем кнопки
        elif event.startswith("SELECT_SLOT_"):
            slot_index = int(event.split("_")[-1])
            if self.selected_character:
                # Если выбран персонаж, добавляем его в слот
                if self.deck.slots[slot_index] is None:
                    # Если слот пуст, добавляем персонажа
                    if self.deck.add_character(self.selected_character, slot_index):
                        self.selected_slot = slot_index  # Выбираем слот после добавления персонажа
                        self.selected_character = None  # Сбрасываем выбор персонажа
                        self.update_buttons()  # Обновляем кнопки
                        self.db.save_deck(self.deck)  # Сохраняем колоду после добавления персонажа
                    else:
                        print("Character is already in deck!")
                else:
                    # Если в слоте уже есть персонаж, заменяем его
                    if self.deck.replace_character(self.selected_character, slot_index):
                        self.selected_slot = slot_index  # Выбираем слот после замены персонажа
                        self.selected_character = None  # Сбрасываем выбор персонажа
                        self.update_buttons()  # Обновляем кнопки
                        self.db.save_deck(self.deck)  # Сохраняем колоду после добавления персонажа
                    else:
                        print("Character is already in deck!")
            else:
                # Если персонаж не выбран, просто выбираем слот
                self.selected_slot = slot_index
                self.update_buttons()  # Обновляем кнопки
        elif event == "DELETE_CHARACTER":
            if self.selected_slot is not None and self.deck.slots[self.selected_slot] is not None:
                # Удаляем персонажа из выбранного слота
                self.deck.remove_character(self.selected_slot)
                self.selected_character = None  # Сбрасываем выбор персонажа
                self.update_buttons()  # Обновляем кнопки
                self.db.save_deck(self.deck)  # Сохраняем колоду после удаления персонажа

    def render(self, screen):
        """Отрисовывает меню."""
        for button in self.buttons:
            button.render(screen)

        # Отрисовка кнопки "Delete", если она есть
        if self.delete_button:
            self.delete_button.render(screen)

        # Отрисовка персонажей в колоде
        for i, character in enumerate(self.deck.slots):
            if character:
                # Отображаем имя персонажа и его изображение (если есть)
                text = FONT_PRESS_ESC.render(character.name, True, (255, 255, 255))
                screen.blit(text, (40 + i * 180, HEIGHT - 120))
                # Здесь можно добавить отрисовку изображения персонажа, если оно есть

    def info(self, screen, characters):
        if self.selected_character:
            select_character_text_tth = FONT_RECHARGE.render(f"Character {self.selected_character.name}:",
                                                            True, pygame.Color("yellow"))
            screen.blit(select_character_text_tth, (140, 120))
            select_character_text_attack = FONT_RECHARGE.render(f"Attack: {self.selected_character.attack}",
                                                                True, pygame.Color("yellow"))
            screen.blit(select_character_text_attack, (140, 140))
            select_character_text_cost = FONT_RECHARGE.render(f"Cost: {self.selected_character.cost}",
                                                              True, pygame.Color("yellow"))
            screen.blit(select_character_text_cost, (140, 160))
            select_character_text_hp = FONT_RECHARGE.render(f"Hp: {self.selected_character.hp}",
                                                              True, pygame.Color("yellow"))
            screen.blit(select_character_text_hp, (140, 180))
            select_character_text_speed_move = FONT_RECHARGE.render(f"Speed move: {self.selected_character.speed_move}",
                                                            True, pygame.Color("yellow"))
            screen.blit(select_character_text_speed_move, (140, 200))
            select_character_text_recharge = FONT_RECHARGE.render(
                f"Recharge: {self.selected_character.recharge}",
                True, pygame.Color("yellow"))
            screen.blit(select_character_text_recharge, (140, 220))
            select_character_text_range = FONT_RECHARGE.render(
                f"Range: {self.selected_character.range}",
                True, pygame.Color("yellow"))
            screen.blit(select_character_text_range, (140, 240))
            select_character_text_damage_type = FONT_RECHARGE.render(f"Damage type: {self.selected_character.damage_type}",
                                                            True, pygame.Color("yellow"))
            screen.blit(select_character_text_damage_type, (140, 260))
            select_character_text_level = FONT_RECHARGE.render(f"Level: {self.selected_character.level}",
                                                            True, pygame.Color("yellow"))
            screen.blit(select_character_text_level, (140, 280))

        for i in range(5):
            slot_text = FONT_RECHARGE.render(f"Slot {i + 1}: ", True, pygame.Color("yellow"))
            screen.blit(slot_text, (40 + i * 180, HEIGHT - 80 - slot_text.get_height()))
        for i, character in enumerate(characters):
            if character.in_deck:
                character_text = FONT_RECHARGE.render("(In Deck)", True, pygame.Color("yellow"))
                screen.blit(character_text, (WIDTH - 240 - character_text.get_width(), 100 + i * 60))