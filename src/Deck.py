class Deck:
    def __init__(self):
        self.slots = [None] * 5  # 5 слотов для персонажей

    def add_character(self, character, slot):
        """Добавляет персонажа в указанный слот, если его еще нет в колоде."""
        if self.slots[slot] is None and not self.is_character_in_deck(character):
            self.slots[slot] = character
            character.in_deck = True
            return True
        return False  # Слот уже занят или персонаж уже в колоде

    def replace_character(self, character, slot):
        """Заменяет персонажа в указанном слоте, если новый персонаж еще не в колоде."""
        if self.is_character_in_deck(character):
            return False  # Персонаж уже в колоде, замена невозможна

        if self.slots[slot] is not None:
            self.slots[slot].in_deck = False  # Убираем текущего персонажа из колоды
        self.slots[slot] = character
        character.in_deck = True  # Добавляем нового персонажа в колоду
        return True

    def remove_character(self, slot):
        """Удаляет персонажа из указанного слота."""
        if self.slots[slot] is not None:
            self.slots[slot].in_deck = False
            self.slots[slot] = None
            return True
        return False  # Слот пуст

    def get_characters(self):
        """Возвращает список персонажей в колоде."""
        return [char for char in self.slots if char is not None]

    def is_character_in_deck(self, character):
        """Проверяет, есть ли персонаж уже в колоде."""
        return character in self.slots