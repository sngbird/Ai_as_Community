import rule_engine
from social import Social
from utils import load_characters_from_xml, load_sck_from_xml


characters = load_characters_from_xml('characters.xml')
# Create the Social engine
social_engine = Social(characters)

# Everything below here is interface stuff

# Main menu setup
print("-------- Weclome to Tavern Week! --------")
print("Influence the relationships between characters")
print("in order to form parties to complete quests.")
print("-----------------------------------------")
print("(Type 'start' to begin the game, 'exit' to quit)")
while True:
        user_input = input("Enter a command: ")
        
        if user_input == 'exit':
            print("Exiting...")
            exit(0)
        elif user_input == 'start':
            print("The game has begun!")
            break
        else:
            print("Unknown command.")

# Tavern main options
print("You have entered the tavern...")
char_names = ['BucketKnight', 'SheepGirl', 'StarboFantastica', 'VanessaConfessa', 'GrumblarTheDestructor', 'BarklerTrobbofield', 'WillabeeFreaky', 'DJWizard', 'TamberGauzeman', 'MossaWillows']
while True:
    print("\n")
    print("What would you like to do?")
    print("COMMAND LIST")
    print("--------------------------")
    print("char - View info on adventurers")
    print("suggest - Make a suggestion")
    print("quest - View available quests")
    print("exit - Quit the game")
    print("--------------------------")
    user_input = input("Enter a command: ")
        
    if user_input == 'exit':
        print("Exiting...")
        print("Come visit the tavern again soon!")
        exit(0)
    elif user_input == 'char':
        print("\n")
        # Loop allowing player to select character
        while True:
            print("Which adventurer?")
            print("NAME LIST")
            print("--------------------------")
            print("BucketKnight")
            print("SheepGirl")
            print("StarboFantastica")
            print("VanessaConfessa")
            print("GrumblarTheDestructor")
            print("BarklerTrobbofield")
            print("WillabeeFreaky")
            print("DJWizard")
            print("TamberGauzeman")
            print("MossaWillows")
            print("exit - Return to previous menu")
            print("--------------------------")
            user_input = input("Enter a name or command: ")

            if user_input == 'exit':
                break
            elif user_input not in char_names:
                print("Unknown command.")
                continue

            adv_name = user_input
            # Loop to access character info
            while True:
                print("\n")
                print("What would you like to know about " + adv_name + "?")
                print("COMMAND LIST")
                print("--------------------------")
                print("trait - Class and Personality traits")
                print("history - Social History")
                print("relation - Relationships with other characters")
                print("sck - Shared Cultural Knowledge (likes/dislikes)")
                print("exit - Return to previous menu")
                print("--------------------------")
                user_input = input("Enter a command: ")

                if user_input == 'exit':
                    break
                elif user_input == 'trait':
                    print(social_engine.get_traits(adv_name))
                elif user_input == 'history':
                    print("gets social history, too tired to do this rn")
                elif user_input == 'relation':
                    print("player enters character name and gets relationship, too tired to do this rn")
                elif user_input == 'sck':
                    print(social_engine.get_sck_opinions(adv_name))
                else:
                    print("Unknown command.")
    elif user_input == 'suggest':
        print("Here are available suggestions!")
        # add loop allowing player to select suggestion
    elif user_input == 'quest':
        print("Here are available quests!")
        # add loop allowing player to select quest
    else:
        print("Unknown command.")
