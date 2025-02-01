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
        self.level = 1  # Уровень персонажа
        self.upgrade_cost = 50  # Стоимость улучшения

    def get_data(self):
        return [self.name, self.speed_move, self.speed_attack, self.hp, self.attack, self.damage_type, self.range]

    def upgrade(self):
        """Улучшаем персонажа."""
        if self.name == "Hero":
            self.hp += (18 + self.level)  # Увеличиваем здоровье
            self.attack += (15 * self.level)  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            if self.recharge > 25:
                self.recharge -= 5
            self.level += 1
        elif self.name == "Shit":
            self.hp += (20 * self.level)  # Увеличиваем здоровье
            self.attack += 15  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            self.speed_move += 4
            if self.recharge > 10:
                self.recharge -= 5
            self.level += 1
        elif self.name == "Archer":
            self.hp += (12 + self.level)  # Увеличиваем здоровье
            self.attack += (12 * self.level)  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            if self.speed_attack > 220:
                self.speed_attack -= (10 + self.level)
            if self.recharge > 10:
                self.recharge -= 5
            self.level += 1
        elif self.name == "Uber":
            self.hp += (30 + self.level)  # Увеличиваем здоровье
            self.attack += (23 * self.level)  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            if self.recharge > 150:
                self.recharge -= (2 * self.level)
            self.level += 1
        elif self.name == "Alpha":
            self.hp += (103 + self.level * 5)  # Увеличиваем здоровье
            self.attack += (40 * self.level)  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            if self.speed_attack > 80:
                self.speed_attack -= (10 + self.level)
            if self.recharge > 300:
                self.recharge -= 5 * self.level
            self.level += 1
        elif self.name == "Wall":
            self.hp += (103 + self.level)  # Увеличиваем здоровье
            self.attack += self.level  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            self.speed_move += 3
            self.level += 1
        else:
            self.hp += (103 + self.level * 5)  # Увеличиваем здоровье
            self.attack += (40 * self.level)  # Увеличиваем урон
            self.upgrade_cost += 25  # Увеличиваем стоимость следующего улучшения
            if self.speed_attack > 80:
                self.speed_attack -= (10 + self.level)
            if self.recharge > 300:
                self.recharge -= 5 * self.level
            self.level += 1