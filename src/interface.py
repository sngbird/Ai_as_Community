import rule_engine
from social import Social
from suggestions import suggestion
from quest import QuestManager
from utils import load_characters_from_xml
import curses

# Create instances of Social and QuestManager classes.
# The Social engine manages character relationships and opinions,
# while the QuestManager handles quests and interactions with the Social engine.
social_engine = Social()
quest_keeper = QuestManager(social_engine)

# Function to draw the menu with selectable options.
# Parameters:
# - stdscr: The curses screen object.
# - selected_row_idx: Index of the currently selected menu item.
# - menu_items: List of strings representing menu options.
def draw_menu(stdscr, selected_row_idx, menu_items):
    # Clear the screen before drawing the menu
    stdscr.clear()
    # Get screen height (h) and width (w)
    h, w = stdscr.getmaxyx()
    # Loop through each menu item and display it on the screen
    for idx, row in enumerate(menu_items):
        # Calculate the x (horizontal) position to center the text
        x = w // 2 - len(row) // 2
        # Calculate the y (vertical) position for each menu item
        y = h // 2 - len(menu_items) // 2 + idx
        # Highlight the selected menu item
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    # Refresh the screen to display the menu
    stdscr.refresh()

# Function to handle the main menu.
# This menu includes options to start the game or exit.
def main_menu(stdscr):
    # Disable the cursor and initialize color pairs for highlighting
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    # Main menu options
    menu = ["Start Game", "Exit"]

    # Infinite loop to keep the menu active until a valid option is selected
    while 1:
        # Draw the main menu
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        # Handle key presses for navigating the menu
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        # Enter key triggers the selected menu item
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # Start Game
                game_menu(stdscr)
            elif current_row == 1:  # Exit
                break
        stdscr.refresh()

# Function to handle the in-game menu.
# This menu includes options to view characters, suggest actions, view quests, or exit.
def game_menu(stdscr):
    current_row = 0
    # In-game menu options
    menu = ["View Characters", "Suggest Action", "Quests", "Exit"]
    
    # Infinite loop to keep the in-game menu active
    while 1:
        # Draw the in-game menu
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        # Handle key presses for navigating the menu
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        # Enter key triggers the selected menu item
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # View Characters
                character_menu(stdscr)
            elif current_row == 1:  # Suggest Action
                pass  # Implement suggestion logic here
            elif current_row == 2:  # View Quests
                quest_menu(stdscr)
            elif current_row == 3:  # Exit
                break
        stdscr.refresh()

# Function to display and interact with the character menu.
# This menu allows the player to view information on specific characters.
def character_menu(stdscr):
    current_row = 0
    # List of character names to be displayed
    char_names = social_engine.character_names
    
    # Infinite loop to keep the character menu active
    while 1:
        # Draw the character menu with a "Back" option at the end
        draw_menu(stdscr, current_row, char_names + ["Back"])
        key = stdscr.getch()

        # Handle key presses for navigating the menu
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(char_names):
            current_row += 1
        # Enter key triggers the selected menu item
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(char_names):  # Back
                break
            else:
                # Display selected character's information
                stdscr.clear()
                stdscr.addstr(0,0, social_engine.display_character_information(char_names[current_row]))
                stdscr.refresh()
                stdscr.getch()  # Wait for key press to continue
        stdscr.refresh()

def quest_menu(stdscr):
    current_row = 0
    menu = ["View Available Quests", "View Deployed Quests", "Advance Week", "Back"]

    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                stdscr.clear()
                quests = quest_keeper.get_quests('all')  # Adjusted to get available quests
                display_quests(stdscr, quests)
                selected_index = get_selection(stdscr, quests)  # Function to get user's choice
                if selected_index is not None:
                    selected_quest = quests[selected_index]
                    stdscr.clear()
                    quest_info = format_quest_info(quest_keeper.quests[selected_quest])
                    stdscr.addstr(0, 0, quest_info)
                    stdscr.getch()
            elif current_row == 1:
                stdscr.clear()
                quests = quest_keeper.get_quests('deployed')  # Adjusted to get deployed quests
                display_quests(stdscr, quests)
                selected_index = get_selection(stdscr, quests)  # Function to get user's choice
                if selected_index is not None:
                    selected_quest = quests[selected_index]
                    stdscr.clear()
                    quest_info = format_quest_info(quest_keeper.quests[selected_quest])
                    stdscr.addstr(0, 0, quest_info)
                    stdscr.getch()
            elif current_row == 2:
                stdscr.clear()
                quest_keeper.run_quest()
                stdscr.getch()
            elif current_row == 3:
                break
        stdscr.refresh()

def format_quest_info(quest_info):
    description = quest_info['description']
    requirements = ', '.join([f"{req['type']}: {req['value']} (Quantity: {req['quantity']})" for req in quest_info['requirements']])
    risks = ', '.join([f"{risk['type']}: {risk['value']} (Quantity: {risk['quantity']})" for risk in quest_info['risks']])
    return (f"Description: {description}\n"
            f"Requirements: {requirements}\n"
            f"Risks: {risks}\n"
            f"Minimum Party Size: {quest_info['minimum']}\n"
            f"Maximum Party Size: {quest_info['maximum']}")

def display_quests(stdscr, quests):
    stdscr.clear()
    for idx, quest in enumerate(quests):
        stdscr.addstr(idx, 0, f"{idx + 1}. {quest}")
    stdscr.addstr(len(quests) + 1, 0, "Select a quest by number or press 'q' to go back.")
    stdscr.refresh()

def get_selection(stdscr, quests):
    key = stdscr.getch()
    if key in [ord(str(i + 1)) for i in range(len(quests))]:
        return int(chr(key)) - 1
    elif key == ord('q'):
        return None
    return None


def main():
    curses.wrapper(main_menu)

# Ensure the main function is called when the script is run directly
if __name__ == "__main__":
    main()


#     # Create the Social engine
# social_engine = Social(characters)
# quest_keeper = QuestManager(social_engine)
# Everything below here is interface stuff

# # Main menu setup
# print("-------- Weclome to Tavern Week! --------")
# print("Influence the relationships between characters")
# print("in order to form parties to complete quests.")
# print("-----------------------------------------")
# print("(Type 'start' to begin the game, 'exit' to quit)")
# while True:
#         user_input = input("Enter a command: ")
        
#         if user_input == 'exit':
#             print("Exiting...")
#             exit(0)
#         elif user_input == 'start':
#             print("The game has begun!")
#             break
#         else:
#             print("Unknown command.")

# # Tavern main options
# print("You have entered the tavern...")
# char_names = ['BucketKnight', 'SheepGirl', 'StarboFantastica', 'VanessaConfessa', 'GrumblarTheDestructor', 'BarklerTrobbofield', 'WillabeeFreaky', 'DJWizard', 'TamberGauzeman', 'MossaWillows']
# while True:
#     print("\n")
#     print("What would you like to do?")
#     print("COMMAND LIST")
#     print("--------------------------")
#     print("char - View info on adventurers")
#     print("suggest - Make a suggestion")
#     print("quest - View available quests")
#     print("exit - Quit the game")
#     print("--------------------------")
#     user_input = input("Enter a command: ")
        
#     if user_input == 'exit':
#         print("Exiting...")
#         print("Come visit the tavern again soon!")
#         exit(0)
#     elif user_input == 'char':
#         print("\n")
#         # Loop allowing player to select character
#         while True:
#             print("Which adventurer?")
#             print("NAME LIST")
#             print("--------------------------")
#             print("BucketKnight")
#             print("SheepGirl")
#             print("StarboFantastica")
#             print("VanessaConfessa")
#             print("GrumblarTheDestructor")
#             print("BarklerTrobbofield")
#             print("WillabeeFreaky")
#             print("DJWizard")
#             print("TamberGauzeman")
#             print("MossaWillows")
#             print("exit - Return to previous menu")
#             print("--------------------------")
#             user_input = input("Enter a name or command: ")

#             if user_input == 'exit':
#                 break
#             elif user_input not in char_names:
#                 print("Unknown command.")
#                 continue

#             adv_name = user_input
#             # Loop to access character info
#             while True:
#                 print("\n")
#                 print("What would you like to know about " + adv_name + "?")
#                 print("COMMAND LIST")
#                 print("--------------------------")
#                 print("trait - Class and Personality traits")
#                 print("history - Social History")
#                 print("relation - Relationships with other characters")
#                 print("sck - Shared Cultural Knowledge (likes/dislikes)")
#                 print("exit - Return to previous menu")
#                 print("--------------------------")
#                 user_input = input("Enter a command: ")

#                 if user_input == 'exit':
#                     break
#                 elif user_input == 'trait':
#                     print(social_engine.get_traits(adv_name))
#                 elif user_input == 'history':
#                     print("gets social history, too tired to do this rn")
#                 elif user_input == 'relation':
#                     print("player enters character name and gets relationship, too tired to do this rn")
#                 elif user_input == 'sck':
#                     print(social_engine.get_sck_opinions(adv_name))
#                 else:
#                     print("Unknown command.")
#     elif user_input == 'suggest':
#         print("Here are available suggestions!")
#         # add loop allowing player to select suggestion
#     elif user_input == 'quest':
#         print("Here are available quests!")
#         while True:
#             print("Which adventurer?")
#             print("NAME LIST")
#             print("--------------------------")
#             print("BucketKnight")
#             print("SheepGirl")
#             print("StarboFantastica")
#             print("VanessaConfessa")
#             print("GrumblarTheDestructor")
#             print("BarklerTrobbofield")
#             print("WillabeeFreaky")
#             print("DJWizard")
#             print("TamberGauzeman")
#             print("MossaWillows")
#             print("exit - Return to previous menu")
#             print("--------------------------")
#             user_input = input("Enter a name or command: ")

#             if user_input == 'exit':
#                 break
#             elif user_input not in char_names:
#                 print("Unknown command.")
#                 continue
#         # add loop allowing player to select quest
#     else:
#         print("Unknown command.")