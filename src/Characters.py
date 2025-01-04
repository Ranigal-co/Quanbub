class Character:
    def __init__(self, name, speed_move, speed_attack, hp, attack, damage_type, range, cost, recharge):
        self.name = name
        self.speed_move = speed_move
        self.speed_attack = speed_attack
        self.hp = hp
        self.attack = attack
        self.damage_type = damage_type
        self.range = range
        self.cost = cost
        self.recharge = recharge
        self.in_deck = False  # По умолчанию персонаж не в колоде

    def get_data(self):
        return [self.name, self.speed_move, self.speed_attack, self.hp, self.attack, self.damage_type, self.range]