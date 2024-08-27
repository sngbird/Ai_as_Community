import curses
import rule_engine  # Assuming these are defined elsewhere
from social import Social
from suggestions import suggestion
from quest import QuestManager
from utils import load_characters_from_xml

# Create instances of Social and QuestManager classes.
# The Social engine manages character relationships and opinions,
# while the QuestManager handles quests and interactions with the Social engine.
social_engine = Social()
quest_keeper = QuestManager(social_engine)

def draw_menu(stdscr, selected_row_idx, menu_items):
    """
    Draws the menu with selectable options.

    Parameters:
    - stdscr: The curses screen object.
    - selected_row_idx: Index of the currently selected menu item.
    - menu_items: List of strings representing menu options.
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Loop through each menu item and display it on the screen
    for idx, row in enumerate(menu_items):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu_items) // 2 + idx
        
        # Highlight the selected menu item
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def main_menu(stdscr):
    """
    Displays the main menu and handles navigation.
    The way this menu is laid out is pretty much how I'll handle all of them
    Parameters:
    - stdscr: The curses screen object.
    """
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    current_row = 0
    menu = ["Start Game", "Exit"]

    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # Start Game
                game_menu(stdscr)
            elif current_row == 1:  # Exit
                break

        stdscr.refresh()

def game_menu(stdscr):
    """
    Displays the in-game menu and handles navigation.

    Parameters:
    - stdscr: The curses screen object.
    """
    current_row = 0
    menu = ["View Characters", "Suggest Action", "Quests", "Exit"]
    
    while True:
        draw_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:  # View Characters
                character_menu(stdscr)
            elif current_row == 1:  # Suggest Action
                pass  # Implement suggestion logic here
            #
            #
            #
            elif current_row == 2:  # View Quests
                quest_menu(stdscr)
            elif current_row == 3:  # Exit
                break

        stdscr.refresh()

#Functionality to be added to char_menu - Check Opinions
def character_menu(stdscr):
    """
    Displays the character menu and allows viewing character information.

    Parameters:
    - stdscr: The curses screen object.
    """
    current_row = 0
    char_names = social_engine.character_names
    
    while True:
        # Include "Back" option in the menu
        draw_menu(stdscr, current_row, char_names + ["Back"])
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(char_names):
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(char_names):  # Back
                break
            else:
                # Display selected character's information
                stdscr.clear()
                selected_name = char_names[current_row]
                stdscr.addstr(0, 0, social_engine.display_character_information(selected_name))
                stdscr.refresh()
                stdscr.getch()  # Wait for key press to continue

        stdscr.refresh()

def quest_menu(stdscr):
    """
    Displays the quest menu, allowing the user to select a quest and perform actions on it.
    
    Parameters:
    - stdscr: The curses screen object.
    """
    quests = quest_keeper.get_quests_description('all')  # Adjusted to get available quests
    
    while True:
        stdscr.clear()
        
        # Display available quests
        display_quests(stdscr, quests)
        selected_index = get_selection(stdscr, quests)  # Function to get user's choice
        
        if selected_index is not None:
            selected_quest = quests[selected_index]
            quest_name = selected_quest[0]
            quest_info = format_quest_info(quest_keeper.quests[quest_name])
            
            current_action_row = 0  # Reset the current row for the action menu
            while True:
                stdscr.clear()
                
                # Display quest info at the top
                stdscr.addstr(0, 0, quest_info)
                
                # Calculate the starting row for the action menu
                action_menu_start_row = quest_info.count('\n') + 1
                
                # Display the action menu options
                action_menu = ["Add Character to Party", "Remove Character from Party", "Deploy Quest", "Back"]
                for idx, option in enumerate(action_menu):
                    x = 0
                    y = action_menu_start_row + idx
                    if idx == current_action_row:
                        stdscr.attron(curses.color_pair(1))
                        stdscr.addstr(y, x, option)
                        stdscr.attroff(curses.color_pair(1))
                    else:
                        stdscr.addstr(y, x, option)
                
                stdscr.refresh()
                
                # Handle key presses for the action menu
                key = stdscr.getch()
                if key == curses.KEY_UP and current_action_row > 0:
                    current_action_row -= 1
                elif key == curses.KEY_DOWN and current_action_row < len(action_menu) - 1:
                    current_action_row += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if current_action_row == 0:  # Add Character to Party
                        # Debug message
                        stdscr.addstr(action_menu_start_row + len(action_menu), 0, "Debug: Add Character to Party selected.")
                        stdscr.refresh()
                        stdscr.getch()  # Wait for key press to continue

                        # Implement logic to add a character to the party
                        pass
                    elif current_action_row == 1:  # Remove Character from Party
                        pass  # Implement logic to remove a character from the party
                    elif current_action_row == 2:  # Deploy Quest
                        pass  # Implement logic to deploy the quest
                    elif current_action_row == 3:  # Back
                        break  # Exit the action menu and go back to quest selection

        if selected_index is None:
            break  # Exit the quest menu if 'q' is pressed in the quest selection
        stdscr.refresh()



# def action_menu(stdscr, quest):
#     """
#     Displays a menu for actions related to the selected quest.

#     Parameters:
#     - stdscr: The curses screen object.
#     - quest: The current quest object.
#     """
#     current_row = 0
#     menu = ["Add Character to Party", "Remove Character from Party", "Deploy Quest", "Back"]

#     while True:
#         draw_menu(stdscr, current_row, menu)
#         key = stdscr.getch()

#         if key == curses.KEY_UP and current_row > 0:
#             current_row -= 1
#         elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
#             current_row += 1
#         elif key == curses.KEY_ENTER or key in [10, 13]:
#             if current_row == 0:  # Add Character to Party
#                 stdscr.clear()
#                 available_characters = social_engine.character_names
#                 display_characters(stdscr, available_characters)
#                 selected_index = get_selection(stdscr, available_characters)
#                 if selected_index is not None:
#                     selected_character = available_characters[selected_index]
#                     quest.add_character(selected_character)  # Implement add_character in Quest
#                     stdscr.addstr(0, 0, f"Added {selected_character} to party.")
#                     stdscr.refresh()
#                     stdscr.getch()  # Wait for key press to continue

#             elif current_row == 1:  # Remove Character from Party
#                 stdscr.clear()
#                 current_party = quest.get_current_party()  # Implement get_current_party in Quest
#                 display_characters(stdscr, current_party)
#                 selected_index = get_selection(stdscr, current_party)
#                 if selected_index is not None:
#                     selected_character = current_party[selected_index]
#                     quest.remove_character(selected_character)  # Implement remove_character in Quest
#                     stdscr.addstr(0, 0, f"Removed {selected_character} from party.")
#                     stdscr.refresh()
#                     stdscr.getch()  # Wait for key press to continue

#             elif current_row == 2:  # Deploy Quest
#                 stdscr.clear()
#                 quest.deploy()  # Implement deploy in Quest
#                 stdscr.addstr(0, 0, "Quest deployed.")
#                 stdscr.refresh()
#                 stdscr.getch()  # Wait for key press to continue

#             elif current_row == 3:  # Back
#                 break

#         stdscr.refresh()

def display_characters(stdscr, characters):
    """
    Displays a list of characters for user selection.

    Parameters:
    - stdscr: The curses screen object.
    - characters: List of character names.
    """
    stdscr.clear()
    for idx, character in enumerate(characters):
        stdscr.addstr(idx, 0, f"{idx + 1}. {character}")
    stdscr.addstr(len(characters) + 1, 0, "Select a character by number or press 'q' to go back.")
    stdscr.refresh()

def get_selection(stdscr, options):
    """
    Gets the user's selection from a list of options.

    Parameters:
    - stdscr: The curses screen object.
    - options: List of options to choose from.

    Returns:
    - The index of the selected option, or None if cancelled.
    """
    key = stdscr.getch()
    if key in [ord(str(i + 1)) for i in range(len(options))]:
        return int(chr(key)) - 1
    elif key == ord('q'):
        return None
    return None

def format_quest_info(quest):
    # Extract quest attributes
    title = quest.get_title()
    description = quest.get_description()
    requirements = ', '.join([f"{req['type']}: {req['value']} (Quantity: {req['quantity']})" for req in quest.get_requirements()])
    risks = ', '.join([f"{risk['type']}: {risk['value']} (Quantity: {risk['quantity']})" for risk in quest.get_risks()])
    
    # Get current party members and format them
    current_party = quest.get_current_members()  # Use the correct method to get current party members

    # Format the current party members as a string
    current_party_str = ', '.join(current_party) if current_party else 'No members in party'

    # Menu options for actions related to the quest
    
    return (f"Quest Name: {title}\n"
            f"Description: {description}\n"
            f"Requirements: {requirements}\n"
            f"Risks: {risks}\n"
            f"Minimum Party Size: {quest.get_minimum()}\n"
            f"Maximum Party Size: {quest.get_maximum()}\n"
            f"Current Party: {current_party_str}\n"
            )

def display_quests(stdscr, quests):
    """
    Displays a list of quests for user selection.

    Parameters:
    - stdscr: The curses screen object.
    - quests: List of quest tuples (name, description).
    """
    stdscr.clear()
    for idx, quest in enumerate(quests):
        stdscr.addstr(idx, 0, f"{idx + 1}. {quest[0]}")
    stdscr.addstr(len(quests) + 1, 0, "Select a quest by number or press 'q' to go back.")
    stdscr.refresh()

if __name__ == "__main__":
    # Start the curses application
    curses.wrapper(main_menu)
