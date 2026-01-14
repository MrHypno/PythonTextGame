import random
from ui_elements import slow_print

class Hero:
    def __init__(self, name, hp, attack_power, current_hp=None, current_armor=0):
        self.name = name
        self.__MaxHP = hp
        
        if current_hp is not None:
            self.__CurrentHP = current_hp
        else:
            self.__CurrentHP = hp
            
        self.__MaxArmor = 50
        self.__CurrentArmor = current_armor 
        self.AttackPower = attack_power
        self.isAlive = True
    
    
    def to_dict(self):
        return {
            "name": self.name,
            "max_hp": self.__MaxHP,
            "current_hp": self.__CurrentHP,
            "attack_power": self.AttackPower,
            "current_armor": self.__CurrentArmor
        }   

    def print_status(self):
        print(f"\n--- {self.name} Status ---")
        print(f"HP: {self.__CurrentHP} / {self.__MaxHP}")
        print(f"Armor: {self.__CurrentArmor}")
        print(f"Attack Power: {self.AttackPower}")
        print("-----------------------")

    def heal(self, healAmount):
        if self.__CurrentHP >= self.__MaxHP:
            slow_print(f"{self.name} is already at full health!")
            return False
        
        self.__CurrentHP += healAmount
        if self.__CurrentHP > self.__MaxHP:
            self.__CurrentHP = self.__MaxHP
        slow_print(f"{self.name} [green]healed[/green]. New HP: [green]{self.__CurrentHP}[/green]")
        return True

    def armor(self, armorAmount):
        if self.__CurrentArmor >= self.__MaxArmor:
            slow_print(f"{self.name} is already at full armor!")
            return False

        self.__CurrentArmor += armorAmount
        if self.__CurrentArmor > self.__MaxArmor:
            self.__CurrentArmor = self.__MaxArmor
        slow_print(f"{self.name} [green]repaired[/green] armor. New Armor: [green]{self.__CurrentArmor}[/green]")
        return True

    def take_damage(self, damage):
        if self.__CurrentArmor > 0:
            if self.__CurrentArmor >= damage:
                self.__CurrentArmor -= damage
                damage = 0
                slow_print(f"Armor absorbed the hit! Armor left: [green]{self.__CurrentArmor}[/green]")
            else:
                damage -= self.__CurrentArmor
                self.__CurrentArmor = 0
                slow_print("Armor broken!", style="danger")
        if damage > 0:
            self.__CurrentHP -= damage
            if self.__CurrentHP <= 0:
                self.__CurrentHP = 0
                self.isAlive = False
            slow_print(f"{self.name} took [red]{damage} damage![/red] Remaining HP: [green]{self.__CurrentHP}[/green]")
        
        if not self.isAlive:
            slow_print(f"You are dead!", style="danger")
            
    def attack(self, enemy):
        print(f"{self.name} attacks!")
        enemy.take_damage(self.AttackPower)


class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.__MaxHP = hp
        self.__CurrentHP = hp
        self.AttackPower = attack_power
        self.isAlive = True

    def take_damage(self, damage):
        self.__CurrentHP -= damage
        if self.__CurrentHP <= 0:
            self.__CurrentHP = 0
            self.isAlive = False
        
        slow_print(f"{self.name} (Enemy) took [red]{damage} damage![/red] Remaining HP: [green]{self.__CurrentHP}[/green]")
        
        if not self.isAlive:
            slow_print(f"{self.name} is defeated! You won!", style="success")

    def attack(self, hero):
        print(f"{self.name} attacks!")
        hero.take_damage(self.AttackPower)

def create_random_enemy():
    enemy_types = [
        {"name": "Bandit", "hp": 90, "ap": 10},
        {"name": "Archer Bandit", "hp": 60, "ap": 15},
        {"name": "Enemy Knight", "hp": 100, "ap": 20}
    ]
    data = random.choice(enemy_types)
    return Enemy(data["name"], data["hp"], data["ap"])

def create_bandit_leader():
    slow_print("\n*** WARNING: A MASSIVE ENEMY APPROACHES ***", style="danger")
    slow_print("The ground shakes as the Bandit Leader steps out of his throne!", style="danger")
    return Enemy("Bandit Leader",hp=200 ,attack_power=35)