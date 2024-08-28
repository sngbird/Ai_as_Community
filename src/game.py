from social import Social
from quest import QuestManager
import pygame
import sys
import queue

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
        self.game.draw_text(welcome_text, (self.game.screen.get_width() // 2, 20), (255, 255, 255), center=True)
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else (255, 255, 255)
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
            color = (255, 0, 0) if idx == self.game.menu_index else (255, 255, 255)
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
            color = (255, 0, 0) if idx == self.game.menu_index else (255, 255, 255)
            self.game.draw_text(character, (self.game.screen.get_width() // 2, 50 + idx * 50), color, center=True)
        self.game.draw_text("Press Enter to select", (self.game.screen.get_width() // 2, self.game.screen.get_height() - 50), (255, 255, 255), center=True)

class QuestMenu(Menu):
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Logic for selecting quests
            pass
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % len(quest_keeper.possible_quests)
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % len(quest_keeper.possible_quests)

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
        lines = character_info.split('\n')

        # Render each line on the screen
        placeholder = self.game.draw_multiline_text(lines, (20, 50), (255, 255, 255))
        
        # Draw the submenu for getting opinions
        # Smaller font for the opinion menu
        smaller_font = pygame.font.Font(None, 20)
        opinion_text = "Opinion of:"
        self.game.draw_text(opinion_text, (20, placeholder[1]+30), (255, 255, 255), smaller_font)  # Adjust Y position as needed

        # List other characters to get opinion
        y_offset = placeholder[1] + 60  # Start a bit lower for character names
        for idx, character in enumerate(self.game.characters):
            if character != self.game.selected_character:  # Exclude the displayed character from the list
                color = (255, 0, 0) if idx == self.game.menu_index else (255, 255, 255)
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
#         self.game.draw_text(string, (100, 240), (255, 255, 255))

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.menu_index = 0
        self.state_queue = queue.LifoQueue()  # Stack-based queue to hold game states
        self.state = "main_menu"  # Initial state is the main menu
        self.state_queue.put(self.state)  # Push initial state onto the stack

        self.selected_character = None  # To hold the selected character name
        self.characters = social_engine.character_names

        # Initialize menu instances
        self.menus = {
            "main_menu": MainMenu(self),
            "main_game_menu": MainGameMenu(self),
            "character_menu": CharacterMenu(self),
            "quest_menu": QuestMenu(self),
            "character_display": CharacterDisplay(self),
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
        self.screen.fill((0, 0, 0))  # Clear the screen
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

    def wrap_text(self, text, max_width):
        """
        Wraps text to fit within the specified width.

        Parameters:
        - text: The text to wrap.
        - max_width: The maximum width of the text area.

        Returns:
        - A list of lines, each line fitting within the max_width.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
