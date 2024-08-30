import sys
from social import Social
from quest import QuestManager
import pygame
import queue
import suggestions
from menus.Menu import Menu
from menus.QuestMenu import QuestMenu
from menus.MainMenu import MainMenu, MainGameMenu
from menus.CharacterMenu import CharacterMenu, CharacterDisplay

# Define Colors
TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)

social_engine = Social()
quest_keeper = QuestManager(social_engine)
suggestions.suggestionSetup() #Sets up the first group of suggestions from the starting social state

class Menu:
    def __init__(self, game):
        self.game = game
        self.character_selector = False


    def handle_input(self):
        pass

    def draw(self):
        pass

class MainMenu(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.game.menu_index == 0:  # Start Game
                self.game.state = "main_game_menu"
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 1:  # Exit
                pygame.quit()
                sys.exit()
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % 2
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % 2
    
    def draw(self):
        options = ["Start Game", "Exit"]
        welcome_text = "Welcome to Tavern Week"
        self.game.draw_text(welcome_text, (self.game.screen.get_width() // 2, 20), TEXT, center=True)
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(option, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)


class MainGameMenu(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.game.menu_index == 0:  # Characters
                self.game.state = "character_menu"
                self.game.menu_index = 0
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 1:  # Quests
                self.game.state = "quest_menu"
                self.game.menu_index = 0
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 2:  # Suggest Action
                self.game.state = "suggestion_menu"
                self.game.menu_index = 0
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 3:  # Exit
                pygame.quit()
                sys.exit()
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % 4
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % 4
    
    def draw(self):
        options = ["Characters", "Quests", "Suggest Action", "Exit"]
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(option, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)


class CharacterMenu(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.game.selected_character = self.game.characters[self.game.menu_index]
            self.game.state = "character_display"
            self.game.state_queue.put(self.game.state)
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % len(self.game.characters)
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % len(self.game.characters)
    
    def draw(self):
        for idx, character in enumerate(self.game.characters):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(character, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)

class QuestMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.add_character_selector = False
        self.remove_character_selector = False
        self.char_index = 0


#Available Quests, and the options to assign characters
    def handle_input(self):
        keys = pygame.key.get_pressed()

        ##These are for handling the sub menu selections
        if self.add_character_selector:
            if keys[pygame.K_RETURN]:
                self.game.selected_character = quest_keeper.available_members[self.char_index]
                print(quest_keeper.add_members(self.game.available_quests[0], self.game.selected_character))
                self.add_character_selector = False
                self.char_index = 0
            elif keys[pygame.K_UP]:
                self.game.char_index = (self.game.char_index - 1) % len(self.game.characters)
            elif keys[pygame.K_DOWN]:
                self.game.char_index = (self.game.char_index + 1) % len(self.game.characters)
        elif self.remove_character_selector: #Problem, currently the char select index isn't being properly reset
            if keys[pygame.K_RETURN]:
                print(self.char_index)
                self.game.selected_character = quest_keeper.unavailable_members[self.char_index]
                print(quest_keeper.remove_members(self.game.available_quests[0], self.game.selected_character))
                self.remove_character_selector = False
                self.char_index = 0
            elif keys[pygame.K_UP]:
                self.game.char_index = (self.game.char_index - 1) % len(self.game.available_quests[0].current_members)
            elif keys[pygame.K_DOWN]:
                self.game.char_index = (self.game.char_index + 1) % len(self.game.available_quests[0].current_members)
        ##Quest Menu Selection
        else:
            if keys[pygame.K_RETURN]:
                if self.game.menu_index == 0:  # Add Characters
                    #Draw Character Selector
                    self.add_character_selector = True
                    self.game.char_index = 0

                elif self.game.menu_index == 1 and len(quest_keeper.unavailable_members) != 0:  # Remove Characters
                    self.remove_character_selector = True
                    self.game.char_index = 0

                elif self.game.menu_index == 2: #Deploy Quest
                    pass
            elif keys[pygame.K_UP]:
                self.game.menu_index = (self.game.menu_index - 1) % 3
            elif keys[pygame.K_DOWN]:
                self.game.menu_index = (self.game.menu_index + 1) % 3

    def character_select(self): #SUBMENU
        for idx, character in enumerate(quest_keeper.available_members):
            color = (255, 0, 0) if idx == self.game.char_index else TEXT
            if idx >= 5:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + (idx-5) * 200, self.game.screen.get_height()- 125), color, center=False)
            else:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + idx * 200, self.game.screen.get_height()- 175), color, center=False)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
    
    def character_removal(self, quest):
        for idx, character in enumerate(quest.current_members):
            color = (255, 0, 0) if idx == self.game.char_index else TEXT
            if idx >= 5:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + (idx-5) * 200, self.game.screen.get_height()- 125), color, center=False)
            else:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + idx * 200, self.game.screen.get_height()- 175), color, center=False)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
    
    def format_requirements(self, requirements):
        formatted_requirements = []
        for requirement in requirements:
            if requirement['type'] == 'Class':
                formatted_string = f"Requires {requirement['quantity']} {requirement['value']}"
                if 'alt_value' in requirement:
                    formatted_string += f" or {requirement['alt_value']}"
            elif requirement['type'] == 'Trait':
                formatted_string = f"Requires {requirement['quantity']} {requirement['value']} Person"
            formatted_requirements.append(formatted_string)
        return formatted_requirements
    
    def format_risks(self,risks):
        """
        Formats a list of risk dictionaries into a list of readable strings.
        
        Parameters:
        - risks: A list of dictionaries representing risks.

        Returns:
        - A list of formatted risk strings.
        """
        formatted_risks = []

        for risk in risks:
            risk_type = risk.get('type')
            value = risk.get('value')
            quantity = risk.get('quantity', '1')
            
            if risk_type == 'SCK':
                opinion = risk.get('opinion')
                formatted_risks.append(f"Increased Risk if Someone's Opinion of {value} is {opinion})")
            elif risk_type == 'Class':
                formatted_risks.append(f"Increased Risk if Party Contains: {value}")
            elif risk_type == 'Trait':
                formatted_risks.append(f"Increased Risk if Party Contains: {value} Person")
            else:
                formatted_risks.append(f"Risk: {quantity} {value}")
        
        return formatted_risks

    def draw(self):
        # for idx, quest in enumerate(self.game.available_quests):
        #     color = (255, 0, 0) if idx == self.game.menu_index else TEXT
        #     self.game.draw_text(quest., (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)
        # self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
         # Define the rectangle
        border_radius = 20
        shadow_offset = 0
        ## Title Section
        title_rect_width = 800
        title_rect_height = 50
        title_rect_x = (self.game.screen.get_width() // 2) - title_rect_width // 2
        title_rect_y = 25
        quest = self.game.available_quests[0]
        quest_title = quest.get_title()
        # Draw the Title Box
        draw_rounded_rect_with_shadow(self.game.screen, (title_rect_x, title_rect_y, title_rect_width, title_rect_height), BORDER, border_radius, shadow_offset)
        # Draw Title Text
        self.game.draw_text(quest_title, (self.game.screen.get_width() // 2, title_rect_y + title_rect_height//2), TEXT, center=True)
        quest_description = quest.get_description()
        quest_requirements = self.format_requirements(quest.get_requirements())

        quest_risks = self.format_risks(quest.get_risks())
        quest_current_members = quest.get_current_members()
        quest_party_size = f"Party Size: {quest.get_minimum()} - {quest.get_maximum()}"
        # Draw the submenu for getting opinions
        # Smaller font for the opinion menu
        # smaller_font = pygame.font.Font(None, 20)
        # opinion_text = "Opinion of:"
        # self.game.draw_text(opinion_text, (20, placeholder[1]+30), TEXT, smaller_font)  # Adjust Y position as needed
        # ## Body
        body_rect_width = 1200
        body_rect_height = 400
        body_rect_x = (self.game.screen.get_width() // 2) - body_rect_width // 2
        body_rect_y = 90
        draw_rounded_rect_with_shadow(self.game.screen, (body_rect_x, body_rect_y, body_rect_width, body_rect_height), BORDER, border_radius, shadow_offset)
        self.game.draw_text(quest_description, (self.game.screen.get_width() // 2, body_rect_y + body_rect_height//10), TEXT, center=True)
        self.game.draw_text(quest_party_size, (self.game.screen.get_width() // 2, body_rect_y + body_rect_height//6), TEXT, center=True)

        start_height = (body_rect_y + body_rect_height//5)
        for item in quest_requirements:
            self.game.draw_text(item, (self.game.screen.get_width() // 4, start_height), TEXT, center=False)
            self.game.draw_bullet_point(self.game.screen, ((self.game.screen.get_width() // 4)-10, start_height+7))
            start_height += 24
        start_height = (body_rect_y + body_rect_height//5)
        for item in quest_risks:
            self.game.draw_text(item, (self.game.screen.get_width() // 2, start_height), TEXT, center=False)
            self.game.draw_bullet_point(self.game.screen, ((self.game.screen.get_width() // 2)-10, start_height+7))
            start_height += 24
        
        #Active Party Box - Will Contain Portraits eventually
        draw_rounded_rect_with_shadow(self.game.screen, (body_rect_x+12, body_rect_y+body_rect_height//2 - 39, body_rect_width-24, body_rect_height//1.75), BORDER, border_radius, shadow_offset)
        idx = 0
        member_height = (body_rect_y+body_rect_height//2 - 39) + (body_rect_height//1.75)//2
        for members in quest_current_members:
            self.game.draw_text(members, (self.game.screen.get_width() // 8 + idx * 200, member_height), TEXT, center=False)
            idx += 1
        #Options Menu
        options = ["Add to Party", "Remove from Party", "Deploy"]
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(option, ((self.game.screen.get_width() // 3) + idx * 200, self.game.screen.get_height()- 200 ), color, center=True)

        if self.add_character_selector:
            self.character_select()
        if self.remove_character_selector:
            self.character_removal(quest)

class DeployedDisplay(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.game.menu_index == 0:  # Available Quests
                self.game.state = "available_quest_menu"
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 1:  # Deployed Quest Menu
                self.game.state = "available_quest_menu"
                self.game.state_queue.put(self.game.state)
            
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % 2
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % 2
    
    def draw(self):
        # for idx, quest in enumerate(self.game.available_quests):
        #     color = (255, 0, 0) if idx == self.game.menu_index else TEXT
        #     self.game.draw_text(quest., (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)
        # self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
         # Define the rectangle
        rect_width = 800
        rect_height = 50
        rect_x = (self.game.screen.get_width() // 2) - rect_width // 2
        rect_y = 50
        border_radius = 20
        shadow_offset = 0

        # Draw the Title Box
        draw_rounded_rect_with_shadow(self.game.screen, (rect_x, rect_y, rect_width, rect_height), BORDER, border_radius, shadow_offset)

        # Draw a vertical line inside the rectangle, 1/4 of the way from the left
        # line_x = rect_x + rect_width // 4
        # pygame.draw.line(self.game.screen, BLACK, (line_x, rect_y), (line_x, rect_y + rect_height), 2)

class CharacterDisplay(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % len(self.game.characters)
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % len(self.game.characters)
        # elif keys[pygame.K_RETURN]:
        #     target_character = self.game.characters[self.game.menu_index]
        #     if target_character != self.game.selected_character:
        #         self.game.state = "opinion_display"
        #         self.game.state_queue.put(self.game.state)

    def draw(self):

        character_info = social_engine.display_character_information(self.game.selected_character)

        # Split the text into lines based on \n
        lines = character_info
        wrapped_lines = self.game.wrap_text(lines,self.game.screen.get_width() // 1.5)
        # Render each line on the screen
        placeholder = self.game.draw_multiline_text(wrapped_lines, (20, 50), TEXT)
        
        # Draw the submenu for getting opinions
        # Smaller font for the opinion menu
        smaller_font = pygame.font.Font(None, 20)
        opinion_text = "Opinion of:"
        self.game.draw_text(opinion_text, (20, placeholder[1]+30), TEXT, smaller_font)  # Adjust Y position as needed

        # List other characters to get opinion
        y_offset = placeholder[1] + 60  # Start a bit lower for character names
        for idx, character in enumerate(self.game.characters):
            if character != self.game.selected_character:  # Exclude the displayed character from the list
                color = (255, 0, 0) if idx == self.game.menu_index else TEXT
                if idx == self.game.menu_index:
                    opinion = social_engine.get_opinions(self.game.selected_character, character)
                    self.game.draw_text(str(opinion), (40, y_offset), color, smaller_font)
                else:
                    self.game.draw_text(character, (40, y_offset), color, smaller_font)  # Indent slightly
                y_offset += 30  # Move down for the next character

# Menu where the player can select suggestions
class SuggestionMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.menuDepth = 0 # 0=choosing charA, 1=choosing charB, 2=choosing suggestions
        self.charAIndex = 0 # suggestion performer index
        self.charBIndex = 0 # suggestion target index
        self.suggListLen = 5 # dedicated variable, as the full len func would take >50% of my screen width

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.menuDepth == 0: # charA list
            if keys[pygame.K_RETURN]:
                #self.game.selected_character = self.game.characters[self.game.menu_index]
                #self.game.state = "suggestion_display"
                #self.game.state_queue.put(self.game.state)
                self.char_index = 0
                self.charAIndex = self.game.menu_index
                self.game.menu_index = 0
                if self.charAIndex == 0:
                    self.char_index = 1
                    self.game.menu_index = 1
                    self.charBIndex = 1
                self.menuDepth += 1
                #print("selected char index " + str(self.charAIndex))
            elif keys[pygame.K_UP]:
                self.game.menu_index = (self.game.menu_index - 1) % len(self.game.characters)
                self.charAIndex = self.game.menu_index
            elif keys[pygame.K_DOWN]:
                self.game.menu_index = (self.game.menu_index + 1) % len(self.game.characters)
                self.charAIndex = self.game.menu_index
        elif self.menuDepth == 1: # charB list
            if keys[pygame.K_RETURN]:
                if self.charBIndex >= len(self.game.characters):
                    self.charBIndex = 0
                    self.menuDepth -= 1
                    self.game.menu_index = self.charAIndex
                else:
                    #self.game.selected_character = self.game.characters[self.game.menu_index]
                    #self.game.state = "suggestion_display"
                    #self.game.state_queue.put(self.game.state)
                    self.char_index = 0
                    self.menuDepth += 1
                    self.charBIndex = self.game.menu_index
                    self.game.menu_index = 0
                    self.suggListLen = len(suggestions.suggestionStorage[self.game.characters[self.charAIndex]][self.game.characters[self.charBIndex]])
            elif keys[pygame.K_UP]:
                self.game.menu_index = (self.game.menu_index - 1) % (len(self.game.characters) + 1)
                if self.game.menu_index == self.charAIndex:
                    self.game.menu_index = (self.game.menu_index - 1) % (len(self.game.characters) + 1) #skip index of pre-selected character
                self.charBIndex = self.game.menu_index
            elif keys[pygame.K_DOWN]:
                self.game.menu_index = (self.game.menu_index + 1) % (len(self.game.characters) + 1)
                if self.game.menu_index == self.charAIndex:
                    self.game.menu_index = (self.game.menu_index + 1) % (len(self.game.characters) + 1)
                self.charBIndex = self.game.menu_index
        elif self.menuDepth == 2: # suggestion list
            if keys[pygame.K_RETURN]:
                if self.game.menu_index >= self.suggListLen:
                    self.menuDepth -= 1
                    self.game.menu_index = self.charBIndex
                else:
                    #print("todo")
                    self.game.state = "suggestion_results"
                    self.game.state_queue.put(self.game.state)
                    self.game.menus["suggestion_results"].reset(suggestions.suggestionStorage[self.game.characters[self.charAIndex]][self.game.characters[self.charBIndex]][self.game.menu_index], self.charAIndex, self.charBIndex)
                    self.game.menus["suggestion_results"].performSuggestion()
            elif keys[pygame.K_UP]:
                self.game.menu_index = (self.game.menu_index - 1) % (self.suggListLen + 1)
                #self.charBIndex = self.game.menu_index
            elif keys[pygame.K_DOWN]:
                self.game.menu_index = (self.game.menu_index + 1) % (self.suggListLen + 1)
                #self.charBIndex = self.game.menu_index
    
    def draw(self):
        # charA list
        for idx, character in enumerate(self.game.characters):
            color = (255, 0, 0) if idx == self.charAIndex else TEXT
            self.game.draw_text(character, (self.game.screen.get_width() // 32, 50 + idx * 50), color, center=False)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
        # charB list
        if self.menuDepth >= 1:
            for idx, character in enumerate(self.game.characters):
                if idx == self.charAIndex:
                    continue #skip already existing character
                color = (255, 0, 0) if idx == self.charBIndex else TEXT
                self.game.draw_text(character, (self.game.screen.get_width() // 4, 50 + idx * 50), color, center=False)
            color = (255, 0, 0) if len(self.game.characters) == self.charBIndex else TEXT
            self.game.draw_text("Go back", (self.game.screen.get_width() // 4, 50 + len(self.game.characters) * 50), color, center=False)
        # suggestion list
        if self.menuDepth >= 2:
            for idx, suggestion in enumerate(suggestions.suggestionStorage[self.game.characters[self.charAIndex]][self.game.characters[self.charBIndex]]):
                color = (255, 0, 0) if idx == self.game.menu_index else TEXT
                self.game.draw_text(suggestion.name, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=False)
                #suggestion info display
                if idx == self.game.menu_index:
                    color = TEXT
                    self.game.draw_text("SUGGESTION INFO", (self.game.screen.get_width() * 3 // 4, 50), color, center=True)
                    self.game.draw_text(suggestion.name, (self.game.screen.get_width() * 3 // 4, 100), color, center=True)
                    self.game.draw_text(suggestion.intent, (self.game.screen.get_width() * 3 // 4, 150), color, center=True)
                    self.game.draw_text("Motives:", (self.game.screen.get_width() * 3 // 4, 200), color, center=True)
                    for idx2, motive in enumerate(suggestion.motives):
                        #self.game.draw_text(motive, (self.game.screen.get_width() * 3 // 4, 250 + idx2 * 50), color, center=False)
                        # wrapped lines code based off code that Lumina did. But so is every other part of this subclass, so...
                        wrapped_lines = self.game.wrap_text(motive,self.game.screen.get_width() // 5)
                        # Render each line on the screen (x pos = 3/4 minus half of text width (1/5) = 3/4-1/10 = 13/20)
                        placeholder = self.game.draw_multiline_text(wrapped_lines, (self.game.screen.get_width() * 13 // 20, 250 + idx2 * 75), TEXT)
            color = (255, 0, 0) if self.suggListLen == self.game.menu_index else TEXT
            self.game.draw_text("Go back", (self.game.screen.get_width() // 2, 50 + self.suggListLen * 50), color, center=False)

# Result screen for suggestions
class SuggestionResultsMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.state = "waiting"
        self.suggestion = None
        self.charA = None
        self.charB = None
        self.succeeded = False

    def reset(self, sugg=None,charAIndex=None,charBIndex=None):
        self.state = "waiting"
        self.suggestion = sugg
        if charAIndex!=None and charBIndex!=None and charAIndex!=charBIndex:
            self.charA = self.game.characters[charAIndex]
            self.charB = self.game.characters[charBIndex]
        else:
            self.charA,self.charB = None,None

    def performSuggestion(self):
        if self.suggestion != None:
            self.succeeded = suggestions.GetSuggestionResult(self.suggestion, self.charA, self.charB)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.state == "waiting":
                self.state = "show result"
            elif self.state == "show result":
                self.game.state = "main_game_menu"
                self.game.state_queue.put(self.game.state)
                self.reset()

    def draw(self):
        color = TEXT
        self.game.draw_text("SUGGESTION ATTEMPT", (self.game.screen.get_width() // 2, 50), color, center=True)
        self.game.draw_text(self.charA + " attempts to", (self.game.screen.get_width() // 2, 100), color, center=True)
        self.game.draw_text(self.suggestion.name, (self.game.screen.get_width() // 2, 125), color, center=True)
        # account for odd grammer by adjusting next line
        if self.suggestion.name in ["Be Kind","Be Rude","Brag"]:
            self.game.draw_text("to " + self.charB + "...", (self.game.screen.get_width() // 2, 150), color, center=True)
        elif self.suggestion.name in ["Bond Over Shared Interest","Argue Over Topic","Flirt","Split up","Break Up","Make Peace"]:
            self.game.draw_text("with " + self.charB + "...", (self.game.screen.get_width() // 2, 150), color, center=True)
        else: # No extra words needed
            self.game.draw_text(self.charB + "...", (self.game.screen.get_width() // 2, 150), color, center=True)
        
        if self.state == "waiting":
            self.game.draw_text("(Press enter to continue)", (self.game.screen.get_width() // 2, 200), color, center=True)
        else:
            if self.succeeded:
                self.game.draw_text("and they succeeded!", (self.game.screen.get_width() // 2, 200), color, center=True)
            else:
                self.game.draw_text("but they failed!", (self.game.screen.get_width() // 2, 200), color, center=True)
            self.game.draw_text("(Press enter to continue)", (self.game.screen.get_width() // 2, 250), color, center=True)



# class OpinionDisplay(Menu):
#     def draw(self):
#         target_character = self.game.characters[self.game.menu_index]
#         opinion = social_engine.get_opinions(self.game.selected_character, target_character)
#         if opinion:
#             string = f"{self.game.selected_character}'s opinion of {target_character}: {opinion}"
#         else:
#             string = f"{self.game.selected_character} has no opinion of {target_character}."
#         self.game.draw_text(string, (100, 240), TEXT)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.menu_index = 0
        self.social_engine = Social()
        self.quest_keeper = QuestManager(self.social_engine)
        self.state_queue = queue.LifoQueue()  # Stack-based queue to hold game states
        self.state = "main_menu"  # Initial state is the main menu
        self.state_queue.put(self.state)  # Push initial state onto the stack
        self.week_number = 0
        self.selected_character = None  # To hold the selected character name
        self.characters = self.social_engine.character_names
        self.quest_keeper.add_quests_weekly()
        self.available_quests = self.quest_keeper.possible_quests
        self.active_quests = self.quest_keeper.deployed_quests
        

        # Initialize menu instances
        self.menus = {
            "main_menu": MainMenu(self),
            "main_game_menu": MainGameMenu(self),
            "character_menu": CharacterMenu(self),
            "quest_menu": QuestMenu(self),
            "character_display": CharacterDisplay(self),
            "suggestion_menu": SuggestionMenu(self),
            "suggestion_results": SuggestionResultsMenu(self),
            #"deployed_display": DeployedDisplay(self),
            #"opinion_display": OpinionDisplay(self)
        }

    def handle_input(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            if not self.state_queue.empty():
                self.state_queue.get()  # Pop the most recent state
                if not self.state_queue.empty():
                    self.state = self.state_queue.queue[-1]  # Set the current state to the previous one
                self.menu_index = 0
        else:
            self.menus[self.state].handle_input()

    def update(self):
        # Update game state
        pass
    
    def wait_for_keypress(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False  # Exit the loop when any key is pressed

    def draw(self):
        self.screen.fill((0, 18, 90))  # Clear the screen
        self.menus[self.state].draw()

    def draw_text(self, text, position, color, font=None, center=False):
        """
        Draws text on the screen.

        Parameters:
        - text: The text to draw.
        - position: The (x, y) position where the text should be drawn.
        - color: The color of the text.
        - font: The font to use for the text. Defaults to self.font.
        - center: Whether to center the text at the position or not.
        """
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        if center:
            position = (position[0] - text_surface.get_width() // 2, position[1] - text_surface.get_height() // 2)
        self.screen.blit(text_surface, position)

    def draw_multiline_text(self, lines, position, color):
        x, y = position
        for line in lines:
            text_surface = self.font.render(line, True, color)
            self.screen.blit(text_surface, (x, y))
            y += text_surface.get_height()  # Move down for the next line
        return (x, y)
    
    def draw_bullet_point(self,screen,position):
        pygame.draw.circle(screen, TEXT, position,2, 0)


    def wrap_text(self, text, max_width):
        """
        Wraps text to fit within the specified width.

        Parameters:
        - text: The text to wrap.
        - max_width: The maximum width of the text area.

        Returns:
        - A list of lines, each line fitting within the max_width.
        """
        # Split the text into lines based on newlines
        words_line_split = text.split('\n')
        lines = []

        for line in words_line_split:
            # Split each line into words, breaking further on periods (.), so they can be treated separately
            words = line.split(' ')
            current_line = ""

            for word in words:
                # Test if adding the next word would exceed the max_width
                test_line = f"{current_line} {word}".strip()
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    # If the line would be too wide, store the current line and start a new one
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            # Add the last line for each split line
            if current_line:
                lines.append(current_line)
        return lines
    
    def draw_rounded_rect_with_shadow(self,screen, rect, color, border_radius, shadow_offset):
        x, y, width, height = rect

        # Draw shadow
        shadow_rect = (x-2, y-2,  width+4, height+4)
        pygame.draw.rect(screen, GRAY, shadow_rect,8, border_radius=border_radius+2)

        # Draw border rectangle
        pygame.draw.rect(screen, color, rect,4, border_radius=border_radius)

    def draw_results_window(self, screen, lines):
        screen_width, screen_height = screen.get_size()
        width = 800
        height = 200
        color = BORDER
        # Center the rect on the screen
        rect_x = (screen_width - width) // 2
        rect_y = (screen_height - height) // 2
        rect = (rect_x, rect_y, width, height)
        border_radius = 20
        text_color = TEXT
        # Draw shadow
        shadow_rect = (rect_x - 2, rect_y - 2, width + 4, height + 4)
        rect = (rect_x, rect_y, width, height)
        pygame.draw.rect(screen, GRAY, shadow_rect, 8, border_radius=border_radius + 2)

        # Draw border rectangle
        pygame.draw.rect(screen, color, rect, 0, border_radius=border_radius)

        # Center and draw each line of text
        font = pygame.font.Font(None, 24)  # Adjust font size as needed

        self.draw_text(str(lines), (rect_x+50,rect_y+76), TEXT)
        pygame.display.flip()
        self.wait_for_keypress()