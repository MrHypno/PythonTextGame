from game_data import world, itemMessages
from core_codes import move_player, take_item, use_item, save_game, load_game, create_hero
from Characters import Hero
from events import check_locations
from ui_elements import slow_print, print_game_name

currentlocation = "ambush area"
dangerous_locations = ["deep forest", "woods", "deep forest2", "old road", "old road2", "forest2", "forest3", "forest4"]
inventory = []
my_hero = None
            
print_game_name("Save the King!", font="big", color="bold red")
slow_print("\n---- MAIN MENU ----")

choice = input("1. New Game\n2. Load Game\nType 'help' for commands> ")

while choice != "1" and choice != "2":
    if choice == "help":
        slow_print("Available commands are as follows:")
        slow_print(">go north/south/east/west - Allows you to navigate the map")
        slow_print(">look - Checks if there are any items around")
        slow_print(">take 'item name' - Adds the item to your inventory")
        slow_print(">inventory/inv/i - Shows the items in your inventory")
        slow_print(">use - To use the items in your inventory")
        slow_print(">save - Saves and exits the game")
        slow_print(">exit/quit - The game closes, does not save progress, and must be restarted from the beginning")
        slow_print(">help - Lists commands")
    else:
        print("Incorrect selection please type '1', '2' or 'help'.")
    choice = input("1. New Game\n2. Load Game\nType 'help' for commands> ")

if choice == "2":
    loaded_data = load_game()
    if loaded_data:
        h_data = loaded_data["hero_data"]
        
        my_hero = Hero(
            name=h_data["name"],
            hp=h_data["max_hp"],
            attack_power=h_data["attack_power"],
            current_hp=h_data["current_hp"],
            current_armor=h_data["current_armor"]
        )
        
        currentlocation = loaded_data["current_location"]
        inventory = loaded_data["inventory"]
        world = loaded_data["world_state"]
        
        slow_print(f"Welcome back {my_hero.name}!")
        
    else:
        my_hero = create_hero()
else:
    my_hero = create_hero()

slow_print("\nPress enter to start.")
input() #Blank input for starting

if choice == "1":
    slow_print("You were ambushed by bandits and the knights were killed, but the king and you managed to escape successfully. You are very close to the [bold green]ambush area[/bold green] and the bandits are searching for you. You must escape before they find you and successfully reach the [bold green]castle[/bold green].")

slow_print(f"You are currently in the [bold green]{world[currentlocation]["name"]}[/bold green]")

while my_hero.isAlive:
    check_locations(my_hero, world, currentlocation, inventory, dangerous_locations) #Controls events that will be triggered based on the location

    if not my_hero.isAlive: #Second check for hero because without this while loop runs one more time
        print_game_name("GAME OVER!", font="big", color="bold red")
        break

    action = input(">").strip().lower()

    if action == "":
        continue

    actionList = action.split(" ", 1)
    command = actionList[0]
    
    if command == "save":
        save_game(my_hero, currentlocation, inventory, world)
        slow_print("Do you want to exit the game? (yes/no)")
        choice = input(">").strip().lower()

        if choice in ["y", "yes"]:
            slow_print("\nThe game is closed!")
            break
        else:
            slow_print("You're continuing the game")

    elif command in ["exit", "quit"]:
        slow_print("You're a cowardly soldier. The bandits found you, and you fled like a traitor, and the king was killed!")
        print_game_name("GAME OVER!", font="big", color="bold red")
        break
    
    elif command == "go":
        if len(actionList) < 2:
            print("Go where ? (e.g., 'go east')")
            continue
        direction = actionList[1]
        
        currentlocation = move_player(currentlocation, direction, world, inventory)
        if currentlocation == "castle":
            slow_print("Congratulations! You won!")
            break

    elif command == "take":
        if len(actionList) < 2:
            slow_print("Take what? (e.g., 'take key')")
            continue
        targetItem = actionList[1]
        take_item(currentlocation, world, targetItem, inventory)

    elif command in ["inventory", "inv", "i"]:
        if len(inventory) == 0:
            slow_print("\nYour inventory is empty.")
        else:
            item_counts = {}
            for item in inventory:
                if item in item_counts:
                    item_counts[item] += 1
                else:
                    item_counts[item] = 1
            
            slow_print("\n --- INVENTORY ---")
            for item, count in item_counts.items():
                if count > 1:
                    slow_print(f"- {item.capitalize()} ({count}x)")
                else:
                    slow_print(f"- {item.capitalize()}")
            slow_print("---------------------")

    elif command == "look":
        slow_print("\nYou carefully look around you")
        roomItems = world[currentlocation].get("item", [])

        if world[currentlocation].get("chest_found") == True:
            slow_print("There is a large hole dug in the ground, revealing an old wooden chest.")
        elif roomItems:
            for item in roomItems:
                itemDesc = itemMessages.get(item)

                if "look" in itemDesc:
                    slow_print(f"{itemDesc['look']}")
                else:
                    slow_print(f"You see a [loot]{item}[/loot] here.") #Failsafe / Probably will never appear
        else:
            slow_print("This place is empty. Just dust and shadows.")
        
    elif command == "use":
        if len(actionList) < 2:
            slow_print("Use what? (e.g., 'use bandage')")
            continue
        usedItem = actionList[1]
        use_item(usedItem, inventory, my_hero, currentlocation, world)

    elif command == "help":
        slow_print("Available commands are as follows:")
        slow_print(">go north/south/east/west - Allows you to navigate the map")
        slow_print(">look - Checks if there are any items around")
        slow_print(">take 'item name' - Adds the item to your inventory")
        slow_print(">inventory/inv/i - Shows the items in your inventory")
        slow_print(">use - To use the items in your inventory")
        slow_print(">save - Saves and exits the game")
        slow_print(">exit/quit - The game closes, does not save progress, and must be restarted from the beginning")
        slow_print(">help - Lists commands")
        
    # elif command == "location": #for debugging purposes
    #     new_location = actionList[1]
    #     currentlocation = new_location
    #     continue

    else:
        slow_print("I don't understand that command.")
        slow_print("Try: 'go [direction]', 'take [item]', 'exit' or type 'help' for commands.")
        continue