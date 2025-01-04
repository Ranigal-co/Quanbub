import sqlite3

from src.Deck import Deck


class Database:
    def __init__(self, db_name='game_progress.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Инициализация базы данных и создание таблиц, если они не существуют."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS progress
                     (level_id INTEGER PRIMARY KEY, is_unlocked INTEGER, coins INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS deck
                     (slot INTEGER PRIMARY KEY, character_name TEXT)''')
        conn.commit()
        conn.close()

    def load_progress(self, levels, coin):
        """Загрузка прогресса из базы данных."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM progress")
        rows = c.fetchall()
        for row in rows:
            level_id, is_unlocked, coins = row
            if level_id <= len(levels):
                levels[level_id - 1].is_unlocked = bool(is_unlocked)
            coin.coins = coins
        conn.close()

    def save_progress(self, levels, coins):
        """Сохранение прогресса в базу данных."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        for level in levels:
            c.execute("INSERT OR REPLACE INTO progress (level_id, is_unlocked, coins) VALUES (?, ?, ?)",
                      (level.level_id, int(level.is_unlocked), coins))
        conn.commit()
        conn.close()

    def save_deck(self, deck):
        """Сохранение колоды в базу данных."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM deck")  # Очищаем таблицу перед сохранением новой колоды
        for slot, character in enumerate(deck.slots):
            if character:
                c.execute("INSERT INTO deck (slot, character_name) VALUES (?, ?)", (slot, character.name))
        conn.commit()
        conn.close()

    def load_deck(self, characters):
        """Загрузка колоды из базы данных."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM deck")
        rows = c.fetchall()
        deck = Deck()
        for row in rows:
            slot, character_name = row
            for character in characters:
                if character.name == character_name:
                    deck.add_character(character, slot)
                    break
        conn.close()
        return deck