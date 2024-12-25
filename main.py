import tkinter as tk
from tkinter import messagebox

# Enum for Item Types
class ItemType:
    HEAL = "Heal"
    DAMAGE_BOOST = "Damage Boost"
    DEFENSE_BOOST = "Defense Boost"

# Abstract Character Class
class Character:
    def __init__(self, name, health, attack_power, defense):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense

    def take_damage(self, damage):
        effective_damage = max(damage - self.defense, 0)
        self.health -= effective_damage
        print(f"{self.name} takes {effective_damage} damage. Remaining health: {self.health}")

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        print(f"{self.name} attacks {target.name}!")
        target.take_damage(self.attack_power)

    def take_turn(self, target):
        raise NotImplementedError("Subclasses must implement take_turn")

# Player Class
class Player(Character):
    def __init__(self, name, health, attack_power, defense):
        super().__init__(name, health, attack_power, defense)
        self.inventory = {ItemType.HEAL: 3, ItemType.DAMAGE_BOOST: 3, ItemType.DEFENSE_BOOST: 3}

    def use_item(self, item_type):
        if self.inventory[item_type] > 0:
            self.inventory[item_type] -= 1
            if item_type == ItemType.HEAL:
                self.health += 20
                print(f"{self.name} heals for 20 HP. Current health: {self.health}")
            elif item_type == ItemType.DAMAGE_BOOST:
                self.attack_power += 5
                print(f"{self.name} gains +5 Attack Power. Current attack: {self.attack_power}")
            elif item_type == ItemType.DEFENSE_BOOST:
                self.defense += 5
                print(f"{self.name} gains +5 Defense. Current defense: {self.defense}")
        else:
            print("No items of this type left.")

    def take_turn(self, target):
        # Player actions handled through GUI
        pass

# Enemy Class
class Enemy(Character):
    def take_turn(self, target):
        self.attack(target)

# Battle Class
class Battle:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.initialize_gui()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.title("RPG.IO")

        # Combat Log
        self.log = tk.Text(self.root, state="disabled", width=50, height=20)
        self.log.pack()

        # Action Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Attack", command=self.attack_action).pack(side="left")
        tk.Button(button_frame, text="Use Item", command=self.use_item_action).pack(side="left")

        self.update_log("Battle begins!")
        self.root.mainloop()

    def update_log(self, message):
        self.log.config(state="normal")
        self.log.insert("end", message + "\n")
        self.log.config(state="disabled")

    def attack_action(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                self.player.attack(enemy)
                self.update_log(f"{self.player.name} attacks {enemy.name}!")
                if not enemy.is_alive():
                    self.update_log(f"{enemy.name} is defeated!")
                break
        self.enemy_turn()

    def use_item_action(self):
        options = [ItemType.HEAL, ItemType.DAMAGE_BOOST, ItemType.DEFENSE_BOOST]
        choice = messagebox.askquestion("Choose an item", "Choose Heal, Damage Boost, or Defense Boost?")
        
        if choice == 'yes':
            # For this example, we assume the item selection is Heal.
            item_type = ItemType.HEAL
        elif choice == 'no':
            # For this example, we assume the item selection is Damage Boost.
            item_type = ItemType.DAMAGE_BOOST
        else:
            item_type = None

        if item_type and item_type in options:
            self.player.use_item(item_type)
            self.update_log(f"{self.player.name} uses {item_type}!")
        else:
            self.update_log("Invalid item selection.")
        self.enemy_turn()

    def enemy_turn(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.take_turn(self.player)
                self.update_log(f"{enemy.name} attacks {self.player.name}!")
        
        if not self.player.is_alive():
            self.update_log("Game Over! You died.")
            self.root.quit()

        if all(not enemy.is_alive() for enemy in self.enemies):
            self.update_log("You win! All enemies defeated!")
            self.root.quit()

# Example Game Setup
if __name__ == "__main__":
    player = Player("Junior", 100, 15, 5)
    enemies = [
        Enemy("Goblin", 30, 10, 2),
        Enemy("Mr. Big Chungus", 50, 12, 3)
    ]
    Battle(player, enemies)
