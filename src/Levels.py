class Level:
    def __init__(self, level_id, enemy_spawn_interval, boss_spawn_interval, money_speed,
                 initial_money, coins):
        self.level_id = level_id
        self.enemy_spawn_interval = enemy_spawn_interval
        self.boss_spawn_interval = boss_spawn_interval
        self.money_speed = money_speed
        self.initial_money = initial_money
        self.coins = coins
        self.is_unlocked = level_id == 1