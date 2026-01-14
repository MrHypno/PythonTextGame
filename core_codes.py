import time
import json
import os
import random
from ui_elements import slow_print
from Characters import Hero
from game_data import item_list, useableItems, itemMessages

#Moves the player around
def move_player(currentlocation, direction, world, inventory):
    valid_directions = ["north", "south", "east", "west"]
    
    if direction in valid_directions and direction in world[currentlocation]:
        next_room_key = world[currentlocation][direction]
        next_location_data = world.get(next_room_key)
        
        is_locked = next_location_data.get("locked", False)
        
        if is_locked:
            if "key" in inventory:
                inventory.remove("key")
                world[next_room_key]["locked"] = False
                slow_print("You opened the door with the key!", style="success")
            else:
                slow_print("The door is locked! You need a key.")
                return currentlocation
            
        currentlocation = next_room_key
        slow_print(f"You move to [bold green]{world[currentlocation].get('name')}[/bold green]")
        if "desc" in world[currentlocation]:
            slow_print(world[currentlocation]["desc"])
            
        return currentlocation
    else:
        slow_print("You can't go that way.")
        return currentlocation
        
#Adds the item to inventory
def take_item(currentlocation, world, targetItem, inventory):
    if "item" in world[currentlocation]:
        if targetItem in world[currentlocation]["item"]:
            slow_print(f"Picked up {targetItem}")
            inventory.append(targetItem)
            world[currentlocation]["item"].remove(targetItem)
            print("Inventory:", inventory)
        else:
            print("There is no", targetItem, "here.")
    else:
        slow_print("There are no items in this area.")

#Uses the item in inventory
def use_item(usedItem, inventory, my_hero, currentlocation, world):
    if usedItem in inventory:
        if usedItem in useableItems:
            value = useableItems[usedItem]
            itemUsed = False

            if "heal" in value:
                if my_hero.heal(value["heal"]):
                    itemUsed = True
            elif "armor" in value:
                if my_hero.armor(value["armor"]):
                    itemUsed = True

            if itemUsed:
                inventory.remove(usedItem)
        elif usedItem == "key":
            if "chest_found" in world[currentlocation]:
                if world[currentlocation]["chest_found"] == True:

                    reward = random.choice(item_list)

                    slow_print("You insert the key into the rusted lock...")
                    slow_print("CLICK! The mechanism turns.", style="success")
                    slow_print(f"The chest creaks open! You found a [loot]{reward}[/loot] inside!")
                    inventory.append(reward)
                    inventory.remove("key")

                    del world[currentlocation]["chest_found"]

                    world[currentlocation]["desc"] = "An empty, open chest sits in the hole."
            else:
                desc = itemMessages["key"]["message"]
                slow_print(desc)
        elif usedItem == "shovel":
            if currentlocation == "forest2":
                if world[currentlocation]["chest_found"] == False:
                    slow_print("You start digging into the soft earth...")
                    slow_print("CLUNK! Your shovel hits someting hard.", style="success")
                    slow_print("You found an old chest!")
                    
                    if "key" in inventory:
                        slow_print("You can open the chest using the key.")
                    else:
                        slow_print("You need a key to open the chest.")

                    world[currentlocation]["chest_found"] = True
                    world[currentlocation]["desc"] = "There is a large hole dug in the ground, revealing an old wooden chest."
                else:
                    slow_print("You already dug here, the chest is right there.")
            else:
                slow_print("You dug here, but found nothing but worms and dirt.")
        else:
            desc = itemMessages.get(usedItem)
            if "message" in desc:
                slow_print(desc["message"])
            else:
                slow_print((f"You can't use a {usedItem}.")) #Failsafe / Probably will never appear
    else:
        slow_print("You don't have that item in your inventory.")

#Save Game
def save_game(hero, loc, inv, game_world):
    data = {
        "hero_data": hero.to_dict(),
        "current_location": loc,
        "inventory": inv,
        "world_state": game_world
    }
    
    try:
        with open("savefile.json", "w") as f:
            json.dump(data, f)
        slow_print("\nGame Saved Successfully!", style="success")
    except Exception as e:
        slow_print(f"Save Error: {e}")

#Load Game
def load_game():
    if not os.path.exists("savefile.json"):
        slow_print("Save file not founded", style="danger")
        return None
    
    try:
        with open("savefile.json", "r") as f:
            data = json.load(f)
        slow_print("Loading game...")
        return data
    except Exception as e:
        slow_print(f"Loading fail : {e}", style="danger")
        return None

#Hero Creation
def create_hero():
    slow_print("Choose your class:")
    slow_print("1. Knight (High HP, Moderate Damage)")
    slow_print("2. Archer (Lower HP, High Damage)")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == "1":
            slow_print("\nYou begin as a brave Knight!", style="success")
            return Hero("Knight", hp=100, attack_power=20)
        elif choice == "2":
            slow_print("\nYou begin as a sharpshooting Archer!", style="success")
            return Hero("Archer", hp=85, attack_power=30)
        else:
            slow_print("Please make a valid choice (1 or 2).", style="danger")

#Fighting Script
def start_fight(my_hero, my_enemy):
    slow_print(f"\nA wild {my_enemy.name} appeared! \n", style="danger")
    my_hero.print_status()
    while my_hero.isAlive and my_enemy.isAlive:
        input("Press enter to attack...")
        my_hero.attack(my_enemy)
        
        if my_enemy.isAlive:
            time.sleep(1)
            my_enemy.attack(my_hero)
            slow_print("-" * 30)
        else:
            return True
        
    return False