import random
import time
from ui_elements import slow_print
from Characters import create_bandit_leader, create_random_enemy, Enemy
from core_codes import start_fight

def guard_encounter():
    slow_print("\n" + "="*40)
    slow_print("Guard Commander: HALT! To pass, you must answer my riddle.", style="dialogue")
    slow_print("Guard Commander: I will ask you ONE question.", style="dialogue")
    slow_print("Guard Commander: If you fail 3 times, you will be executed!", style="dialogue")
    slow_print("(Type your answer directly. Example: 'map', 'darkness')")

    
    question_pool = [
        { "q": "If you speak my name, you break me. What am I?", "valid_answers": ["silence"] }, 
        { "q": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "valid_answers": ["map"] }, 
        { "q": "The more you take, the more you leave behind. What are they?", "valid_answers": ["footsteps","steps"] },
        { "q": "The maker doesn't want it; the buyer doesn't use it; the user doesn't see it. What is it?", "valid_answers": ["coffin"] },
        { "q": "If you have me, you want to share me. If you share me, you haven't got me. What am I?", "valid_answers": ["secret"] } 
    ]

    selected_question = random.choice(question_pool) #Random question picker
    mistakes = 0
    
    slow_print(f"\n[RIDDLE]")
    slow_print(selected_question["q"])
    
    while mistakes < 3: #3 mistake right.
        user_answer = input("\n Your Answer:").strip().lower()
        
        if user_answer in selected_question["valid_answers"]:
            slow_print("Guard Commander: ... Correct. You are wiser than you look.", style="dialogue")
            return True
        else:
            mistakes += 1
            slow_print(f"Guard Commander: WRONG! You have {3-mistakes} chances left.", style="dialogue")
    return False

def merchant_event(my_hero, inventory):
    slow_print("\n" + "="*30)
    slow_print("MERCHANT: Greetings, traveler! I have rare goods for sale.", style="dialogue")
    
    if "gold coin" in inventory:
        slow_print("MERCHANT: Ah, I see you have a shiny Gold Coin! I can trade it for something special.", style="dialogue")
        slow_print("1. Sharpen Sword (+15 Attack Power)")
        slow_print("2. Reinforced Armor (+50 Armor)")
        slow_print("3. Vitality Elixir (Increase Max HP & Full Heal)")
        slow_print("4. Leave")
        
        choice = input("Merchant: What is your choice? (1-4): ").strip()
        
        if choice == "1":
            my_hero.AttackPower += 15
            slow_print("Merchant: Your weapon is now razor sharp!", style="success")
            inventory.remove("gold coin")
        elif choice == "2":
            my_hero.armor(50)
            slow_print("Merchant: This armor will protect you from many blows.", style="success")
            inventory.remove("gold coin")
        elif choice == "3":
            my_hero._Hero__MaxHP += 50
            my_hero.heal(999)
            slow_print("Merchant: You feel stronger than ever before!", style="success")
            inventory.remove("gold coin")
        elif choice == "4":
            slow_print("Merchant: Come back if you change your mind.", style="dialogue")
        else:
            slow_print("Merchant: Stop wasting my time.", style="dialogue")
    else:
        slow_print("MERCHANT: Wait... You have no gold! Come back when you can pay!", style="dialogue")
    slow_print("="*30 + "\n")

def villager_talk(my_hero, world):
    slow_print("\n" + "-"*20)
    
    if world.get("bandit camp", {}).get("cleared", False) == True:
        hero_dialogues = [
            "VILLAGER: You killed the Bandit Leader! You are our hero!",
            "VILLAGER: We are finally free! Please, take whatever you need from my house.",
            "VILLAGER: I knew you were a savior the moment I saw you!",
            "VILLAGER: The King will surely reward you for this!"
        ]
        slow_print(f"{random.choice(hero_dialogues)}", style="dialogue")
        
    else:
        chance = random.randint(1, 100)
        
        if chance <= 10: #Low chance of villager attacking us
            slow_print("VILLAGER: I won't let you hurt anyone else! DIE TRAITOR!", style="danger")
            slow_print("(The villager grabs a pitchfork and attacks you in a blind panic!)")
        
            angry_villager = Enemy("Angry Villager", 40, 5)

            fight_result = start_fight(my_hero, angry_villager)
            
            if fight_result:
                slow_print("You knocked the villager unconscious. You feel bad about hurting an innocent...")
        
        if chance <= 40:
            suspicious_dialogues = [
                "VILLAGER: Get out! You look just like those bandits!",
                "VILLAGER: Did you kill the knights? Stay away from my family!",
                "VILLAGER: I don't trust you. You have blood on your hands.",
                "VILLAGER: Don't hurt me! Take what you want and leave!",
                "VILLAGER: You're one of them, aren't you? A traitor!",
                "VILLAGER: My husband went to the woods and never came back. Was it YOU?!"
            ]
            slow_print(f"{random.choice(suspicious_dialogues)}", style="danger")
            slow_print("(The villager backs away slowly, holding a kitchen knife.)")

        elif chance <= 70:
            info_dialogues = [
                "VILLAGER: I saw smoke rising from the deep forest. The bandit camp must be there.",
                "VILLAGER: The Mayor hid something in the archives before he fled. But it's locked.",
                "VILLAGER: Be careful on the cliffs. The ground is unstable.",
                "VILLAGER: I heard the merchant in the town square likes gold coins.",
                "VILLAGER: Those bandits... they have heavy armor. You'll need a strong weapon."
            ]
            slow_print(f"{random.choice(info_dialogues)}", style="dialogue")

        else:
            friendly_dialogues = [
                "VILLAGER: Please help us... We have no food left.",
                "VILLAGER: May the gods protect you, traveler.",
                "VILLAGER: It's dangerous to go alone. Watch your back.",
                "VILLAGER: If you see the King, tell him we are still loyal."
            ]
            slow_print(f"{random.choice(friendly_dialogues)}", style="dialogue")

    slow_print("-" * 20 + "\n")

            
def archives_puzzle():
    slow_print("\n" + "="*40)
    slow_print("You found an ancient locked chest in the Archives.")
    slow_print("There is a note attached to it, written in old ink:")
    slow_print("-" * 30)
    slow_print("'To open the wisdom box, you must know the numbers of nature:'")
    slow_print("1. The number of legs on a Spider.")
    slow_print("2. The number of moons orbiting the Earth.")
    slow_print("3. The number of seasons in a year.")
    slow_print("-" * 30)
    slow_print("(Enter the 3-digit code together. Example: 123)")

    correct_code = "814" # Spider(8), Moon(1), Seasons(4)
    attempts = 3

    while attempts > 0:
        guess = input("\nEnter Code: ").strip()

        if guess == correct_code:
            slow_print("\nCLICK! The mechanism turns and the chest opens!", style="success")
            return True
        else:
            attempts -= 1
            if attempts > 0:
                slow_print(f"Wrong code. You have {attempts} tries left before it seals forever.")
            else:
                slow_print("\nThe mechanism completely jams. You can never open this chest.", style="danger")
                return False
    return False

def check_locations(my_hero, world, currentlocation, inventory, dangerous_locations):
    
    # Merchant Check
    if currentlocation == "town square":
        merchant_event(my_hero, inventory)

    # Villager Check
    elif currentlocation in ["town house", "middle house", "big house"]:
        villager_talk(my_hero, world)

    # Cliffs Check
    elif currentlocation == "cliffs":
        time.sleep(1)
        chance = random.randint(1, 100)
        if chance <=40:
            slow_print("\nCRACK! The ground beneath your feet gives way!", style="danger")
            slow_print("Your try to grab a rock but it's too late...", style="danger")
            slow_print("You fall into the abyss to your death.", style="danger")
            my_hero.isAlive = False
        else:
            slow_print("You stumble slightly but manage to keep your balance. That was close!")
        
    # Guards Check
    elif currentlocation == "guards":
        quiz_results = guard_encounter()
        if quiz_results == True:
            slow_print("\nGuard Commander: You possess great wisdom. The gates are open for you!", style="dialogue")
            slow_print("You can enter the Castle safely!, Go north!!")
        else:
            slow_print("\n[bold red]Guard Comander:[/bold red] You are a fool and spy! EXECUTE HIM!", style="dialogue")
            slow_print("The guards seize you. The last thing you see is the commander's sword...")
            my_hero.isAlive = False
    
    # Random Fight Check
    elif currentlocation in ["forest3", "road4"]:
        slow_print("\nThere is a Bandit waiting for you in the shadows!")
        my_enemy = create_random_enemy()
        fight_result = start_fight(my_hero, my_enemy)

    # Archives Check
    elif currentlocation == "archives":
        if world["archives"].get("chest_found") == True:
            puzzle_result = archives_puzzle()

            if puzzle_result == True:
                slow_print("Inside the chest, you find a [loot]Masterwork Sword[/loot]!")
                slow_print("You equipped the sword. It gives you more attack power!")
                
                my_hero.AttackPower += 15 
                
                del world["archives"]["chest_found"]
                world["archives"]["desc"] = "The room smells of old paper and decaying parchment. An empty chest stands open in the corner."
            else:
                slow_print("You kick the chest in frustration, but it won't budge.")
        else:
            slow_print("The chest in the corner is empty and open.")

    #Random encounters
    elif currentlocation in dangerous_locations and random.randint(1, 100) <= 20:
            my_enemy = create_random_enemy() 
            fight_result = start_fight(my_hero, my_enemy)
                
            if fight_result:
                slow_print("You can continue on your journey.", style="success")
                
    # Boss Check
    elif currentlocation == "bandit camp":
        if world["bandit camp"].get("cleared", False) == False:
            slow_print("\n!!! IT'S A TRAP !!!")
            slow_print("You walked straight into the Bandit Camp! There is no escape!")
            
            my_enemy = create_bandit_leader()
            fight_result = start_fight(my_hero, my_enemy)
            
            if not fight_result:
                slow_print("The Bandit Leader crushed you... ")
                my_hero.isAlive = False
            else:
                slow_print("\n*** VICTORY ***")
                slow_print("You have defeated the Bandit Leader! The remaning bandits flee in terror. Don't forget that they can still attack you!")
                slow_print("You found the Leader's [loot]Heavy Armor[/loot] and put it on!")
                my_hero.armor(50)
                world["bandit camp"]["cleared"] = True
        else:
            slow_print("You see the defeated bandits scattered around. The camp is safe now.")