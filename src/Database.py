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
        c.execute('''CREATE TABLE IF NOT EXISTS character_upgrades
                     (character_name TEXT PRIMARY KEY, level INTEGER, upgrade_cost INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS base_upgrades
                     (base_level INTEGER PRIMARY KEY, hp INTEGER, upgrade_cost INTEGER, limit_money INTEGER, speed_money INTEGER,
                     hp_upgrade_cost INTEGER, limit_money_upgrade_cost INTEGER, speed_money_upgrade_cost INTEGER)''')
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

    def save_character_upgrades(self, characters):
        """Сохранение данных о прокачке персонажей."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        for character in characters:
            c.execute(
                "INSERT OR REPLACE INTO character_upgrades (character_name, level, upgrade_cost) VALUES (?, ?, ?)",
                (character.name, character.level, character.upgrade_cost))
        conn.commit()
        conn.close()

    def save_base_upgrades(self, defender_base):
        """Сохранение данных о прокачке базы."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO base_upgrades (base_level, hp, upgrade_cost, limit_money, speed_money, hp_upgrade_cost, limit_money_upgrade_cost, speed_money_upgrade_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (defender_base.lvl_main, defender_base.hp, defender_base.upgrade_cost, defender_base.limit_money,
             defender_base.speed_money,
             defender_base.hp_upgrade_cost, defender_base.limit_money_upgrade_cost,
             defender_base.speed_money_upgrade_cost))
        conn.commit()
        conn.close()

    def load_character_upgrades(self, characters):
        """Загрузка данных о прокачке персонажей."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM character_upgrades")
        rows = c.fetchall()
        for row in rows:
            character_name, level, upgrade_cost = row
            for character in characters:
                if character.name == character_name:
                    for i in range(level - 1):
                        character.upgrade()
                    break
        conn.close()

    def load_base_upgrades(self, defender_base):
        """Загрузка данных о прокачке базы."""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM base_upgrades")
        row = c.fetchone()
        if row:
            base_level, hp, upgrade_cost, limit_money, speed_money, hp_upgrade_cost, limit_money_upgrade_cost, speed_money_upgrade_cost = row
            defender_base.lvl_main = base_level
            defender_base.hp = hp
            defender_base.upgrade_cost = upgrade_cost
            defender_base.limit_money = limit_money
            defender_base.speed_money = speed_money
            defender_base.hp_upgrade_cost = hp_upgrade_cost  # Загружаем стоимость улучшения здоровья
            defender_base.limit_money_upgrade_cost = limit_money_upgrade_cost  # Загружаем стоимость улучшения лимита денег
            defender_base.speed_money_upgrade_cost = speed_money_upgrade_cost  # Загружаем стоимость улучшения скорости накопления денег
        conn.close()