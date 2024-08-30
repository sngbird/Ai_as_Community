from menus.Menu import Menu
import pygame

TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)

class QuestMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.add_character_selector = False
        self.remove_character_selector = False
        self.char_index = 0
        self.draw_results = False
        self.add_result = "None"


#Available Quests, and the options to assign characters
    def handle_input(self):
        keys = pygame.key.get_pressed()

        ##These are for handling the sub menu selections
        #def draw_results_window(self, screen, rect, color, border_radius, shadow_offset, lines, text_color):

        if self.add_character_selector:
            if keys[pygame.K_RETURN]:
                self.game.selected_character = self.game.quest_keeper.available_members[self.char_index]
                self.add_result = self.game.quest_keeper.add_members(self.game.available_quests[0], self.game.selected_character)
                if self.add_result != "None":
                    self.draw_results = True
                    
                self.add_character_selector = False
                self.char_index = 0
            elif keys[pygame.K_UP]:
                self.char_index = (self.char_index - 1) % len(self.game.quest_keeper.available_members)
            elif keys[pygame.K_DOWN]:
                self.char_index = (self.char_index + 1) % len(self.game.quest_keeper.available_members)
        elif self.remove_character_selector: #Problem, currently the char select index isn't being properly reset
            if keys[pygame.K_RETURN]:
                print(self.char_index)
                self.game.selected_character = self.game.quest_keeper.unavailable_members[self.char_index]
                print(self.game.quest_keeper.remove_members(self.game.available_quests[0], self.game.selected_character))
                self.remove_character_selector = False
                self.char_index = 0
            elif keys[pygame.K_UP]:
                self.char_index = (self.char_index - 1) % len(self.game.available_quests[0].current_members)
            elif keys[pygame.K_DOWN]:
                self.char_index = (self.char_index + 1) % len(self.game.available_quests[0].current_members)
        ##Quest Menu Selection
        else:
            if keys[pygame.K_RETURN]:
                if self.game.menu_index == 0:  # Add Characters
                    #Draw Character Selector
                    self.add_character_selector = True
                    self.game.char_index = 0

                elif self.game.menu_index == 1 and len(self.game.quest_keeper.unavailable_members) != 0:  # Remove Characters
                    self.remove_character_selector = True
                    self.game.char_index = 0

                elif self.game.menu_index == 2: #Deploy Quest
                    self.game.quest_keeper.deploy_quest(self.game.quest_keeper.possible_quests[0])
                    self.game.quest_keeper.run_quest(self.game.quest_keeper.deployed_quests[0])
            elif keys[pygame.K_UP]:
                self.game.menu_index = (self.game.menu_index - 1) % 3
            elif keys[pygame.K_DOWN]:
                self.game.menu_index = (self.game.menu_index + 1) % 3

    def character_select(self): #SUBMENU
        for idx, character in enumerate(self.game.quest_keeper.available_members):
            color = (255, 0, 0) if idx == self.char_index else TEXT
            if idx >= 5:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + (idx-5) * 200, self.game.screen.get_height()- 125), color, center=False)
            else:
                self.game.draw_text(character, (self.game.screen.get_width() // 10 + idx * 200, self.game.screen.get_height()- 175), color, center=False)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), TEXT, center=True)
    
    def character_removal(self, quest):
        for idx, character in enumerate(quest.current_members):
            color = (255, 0, 0) if idx == self.char_index else TEXT
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
        self.game.draw_rounded_rect_with_shadow(self.game.screen, (title_rect_x, title_rect_y, title_rect_width, title_rect_height), BORDER, border_radius, shadow_offset)
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
        self.game.draw_rounded_rect_with_shadow(self.game.screen, (body_rect_x, body_rect_y, body_rect_width, body_rect_height), BORDER, border_radius, shadow_offset)
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
        self.game.draw_rounded_rect_with_shadow(self.game.screen, (body_rect_x+12, body_rect_y+body_rect_height//2 - 39, body_rect_width-24, body_rect_height//1.75), BORDER, border_radius, shadow_offset)
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

        if self.draw_results:
            self.game.draw_results_window(self.game.screen,self.add_result)
            self.game.wait_for_keypress()
            self.draw_results = False
            self.add_result = "None"

