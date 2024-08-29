from social import Social
from quest import QuestManager
import pygame
import sys
import queue

# Define Colors
TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)

social_engine = Social()
quest_keeper = QuestManager(social_engine)

class Menu:
    def __init__(self, game):
        self.game = game


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
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 1:  # Quests
                self.game.state = "quest_menu"
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 2:  # Suggest Action
                pass  # Implement suggestion logic here
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
#Main Quest Menu, Available Quests, and Deployed Quests
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if self.game.menu_index == 0:  # Available Quests
                self.game.state = "available_quest_menu"
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 1:  # Deployed Quest Menu
                self.game.state = "deployed_display"
                self.game.state_queue.put(self.game.state)
            elif self.game.menu_index == 3:  # exit
                pass  # Implement suggestion logic here
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % 3
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % 3
    
    def draw(self):
        options = ["Available Quests", "Deployed Quests", "Back"]
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(option, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)

class AvailableMenu(Menu):
#Available Quests, and the options to assign characters
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
        ## Body
        body_rect_width = 1200
        body_rect_height = 400
        body_rect_x = (self.game.screen.get_width() // 2) - body_rect_width // 2
        body_rect_y = 125
        draw_rounded_rect_with_shadow(self.game.screen, (body_rect_x, body_rect_y, body_rect_width, body_rect_height), BORDER, border_radius, shadow_offset)
        self.game.draw_text(quest_description, (self.game.screen.get_width() // 2, body_rect_y + body_rect_height//8), TEXT, center=True)
        self.game.draw_bullet_point(self.game.screen, (50,50))

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
        self.state_queue = queue.LifoQueue()  # Stack-based queue to hold game states
        self.state = "main_menu"  # Initial state is the main menu
        self.state_queue.put(self.state)  # Push initial state onto the stack
        self.week_number = 0
        self.selected_character = None  # To hold the selected character name
        self.characters = social_engine.character_names
        quest_keeper.add_quests_weekly()
        self.available_quests = quest_keeper.possible_quests
        self.active_quests = quest_keeper.deployed_quests

        # Initialize menu instances
        self.menus = {
            "main_menu": MainMenu(self),
            "main_game_menu": MainGameMenu(self),
            "character_menu": CharacterMenu(self),
            "quest_menu": QuestMenu(self),
            "character_display": CharacterDisplay(self),
            "available_quest_menu": AvailableMenu(self),
            "deployed_display": DeployedDisplay(self),
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

def draw_rounded_rect_with_shadow(screen, rect, color, border_radius, shadow_offset):
    x, y, width, height = rect

    # Draw shadow
    shadow_rect = (x-2, y-2,  width+4, height+4)
    pygame.draw.rect(screen, GRAY, shadow_rect,8, border_radius=border_radius+2)

    # Draw border rectangle
    pygame.draw.rect(screen, color, rect,4, border_radius=border_radius)

