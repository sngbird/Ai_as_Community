# game.py
from social import Social
from quest import QuestManager
import pygame
import sys
import queue

social_engine = Social()
quest_keeper = QuestManager(social_engine)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.menu_index = 0
        self.state_queue = queue.LifoQueue()  # Stack-based queue to hold game states
        self.state = "main_menu"  # Initial state is the main menu
        self.state_queue.put(self.state)  # Push initial state onto the stack

        self.selected_character = None  # To hold the selected character name

        # List of the names of characters for selection
        self.characters = social_engine.character_names

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not self.state_queue.empty():
                self.state_queue.get()  # Pop the most recent state
                if not self.state_queue.empty():
                    self.state = self.state_queue.queue[-1]  # Set the current state to the previous one
                self.menu_index = 0
        elif keys[pygame.K_UP]:
            if self.state in ["main_menu", "main_game_menu", "character_display"]:
                self.menu_index = (self.menu_index - 1) % self.get_menu_length()
            elif self.state == "quest_menu":
                self.menu_index = (self.menu_index - 1) % len(self.quests)
            elif self.state == "character_menu":
                self.menu_index = (self.menu_index - 1) % len(self.characters)
        elif keys[pygame.K_DOWN]:
            if self.state in ["main_menu", "main_game_menu", "character_display"]:
                self.menu_index = (self.menu_index + 1) % self.get_menu_length()
            elif self.state == "quest_menu":
                self.menu_index = (self.menu_index + 1) % len(self.quests)
            elif self.state == "character_menu":
                self.menu_index = (self.menu_index + 1) % len(self.characters)
        elif keys[pygame.K_RETURN]:
            if self.state == "main_menu":
                self.handle_main_menu()
            elif self.state == "main_game_menu":
                self.handle_main_game_menu()
            elif self.state == "quest_menu":
                self.handle_quest_menu()
            elif self.state == "character_menu":
                self.handle_character_menu()
            elif self.state == "character_display":
                self.handle_character_display_menu()

    def get_menu_length(self):
        if self.state == "main_menu":
            return 2  # Main menu has 2 options
        elif self.state == "main_game_menu":
            return 4  # Main game menu has 4 options
        elif self.state == "character_display":
            return len(self.characters)
        return 0

    def handle_main_menu(self):
        if self.menu_index == 0:  # Start Game
            self.state = "main_game_menu"
            self.state_queue.put(self.state)
        elif self.menu_index == 1:  # Exit
            pygame.quit()
            sys.exit()

    def handle_main_game_menu(self):
        if self.menu_index == 0:  # Characters
            self.state = "character_menu"
            self.state_queue.put(self.state)
        elif self.menu_index == 1:  # Quests
            self.state = "quest_menu"
            self.state_queue.put(self.state)
        elif self.menu_index == 2:  # Suggest Action
            pass  # Implement suggestion logic here
        elif self.menu_index == 3:  # Exit
            pygame.quit()
            sys.exit()

    def handle_character_menu(self):
        self.selected_character = self.characters[self.menu_index]  # Select character
        self.state = "character_display"  # Transition to character display state
        self.state_queue.put(self.state)

    def handle_quest_menu(self):
        # Logic for quest menu
        pass

    def update(self):
        # Update game state
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        if self.state == "main_menu":
            self.draw_main_menu()
        elif self.state == "main_game_menu":
            self.draw_main_game_menu()
        elif self.state == "quest_menu":
            self.draw_quest_menu()
        elif self.state == "character_menu":
            self.draw_character_menu()
        elif self.state == "character_display":
            self.draw_character_display()

    def draw_main_menu(self):
        options = ["Start Game", "Exit"]
        welcome_text = "Welcome to Tavern Week"
        self.draw_text(welcome_text, (self.screen.get_width() // 2, 20), (255, 255, 255), center=True)
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.menu_index else (255, 255, 255)
            self.draw_text(option, (self.screen.get_width() // 2, 50 + idx * 50), color, center=True)

    def draw_main_game_menu(self):
        options = ["Characters", "Quests", "Suggest Action", "Exit"]
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.menu_index else (255, 255, 255)
            self.draw_text(option, (self.screen.get_width() // 2, 50 + idx * 50), color, center=True)

    def draw_quest_menu(self):
        quests = quest_keeper.possible_quests
        for idx, quest in enumerate(quests):
            color = (255, 0, 0) if idx == self.menu_index else (255, 255, 255)
            self.draw_text(quest, (self.screen.get_width() // 2, 50 + idx * 50), color, center=True)
        
        self.draw_text("Press Enter to select", (self.screen.get_width() // 2, self.screen.get_height() - 50), (255, 255, 255), center=True)

    def draw_character_menu(self):
        for idx, character in enumerate(self.characters):
            color = (255, 0, 0) if idx == self.menu_index else (255, 255, 255)
            self.draw_text(character, (self.screen.get_width() // 2, 50 + idx * 50), color, center=True)

        self.draw_text("Press Enter to select", (self.screen.get_width() // 2, self.screen.get_height() - 50), (255, 255, 255), center=True)

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
    
    def draw_character_display(self):
        # Get the character information string which contains \n for newlines
        character_info = social_engine.display_character_information(self.selected_character)

        # Split the text into lines based on \n
        lines = character_info.split('\n')

        # Render each line on the screen
        placeholder = self.draw_multiline_text(lines, (20, 50), (255, 255, 255))

        # Draw the submenu for getting opinions
        # Smaller font for the opinion menu
        smaller_font = pygame.font.Font(None, 20)
        opinion_text = "Opinion of:"
        self.draw_text(opinion_text, (20, 240), (255, 255, 255), smaller_font)  # Adjust Y position as needed

        # List other characters to get opinion
        y_offset = 270  # Start a bit lower for character names
        for idx, character in enumerate(self.characters):
            if character != self.selected_character:  # Exclude the displayed character from the list
                color = (255, 0, 0) if idx == self.menu_index else (255, 255, 255)
                if idx == self.menu_index:
                    opinion = social_engine.get_opinions(self.selected_character, character)
                    self.draw_text(str(opinion), (40, y_offset), color, smaller_font)
                else:
                    self.draw_text(character, (40, y_offset), color, smaller_font)  # Indent slightly
                y_offset += 30  # Move down for the next character


    def handle_character_display_menu(self):
        target_character = self.characters[self.menu_index]
        
        if target_character != self.selected_character:
            # Retrieve the opinion from social_engine
            opinion = social_engine.get_opinions(self.selected_character, target_character)
            
            # Display debug information on the screen
            if opinion:
                # Format the string with the actual values
                string = f"{self.selected_character}'s opinion of {target_character}: {opinion}"
            else:
                # Inform the user if no opinion is available
                string = f"{self.selected_character} has no opinion of {target_character}."

            # Draw the formatted text on the screen
            self.draw_text(string, (100, 240), (255, 255, 255))
    
    def draw_multiline_text(self, lines, position, color):
        x, y = position
        for line in lines:
            text_surface = self.font.render(line, True, color)
            self.screen.blit(text_surface, (x, y))
            y += text_surface.get_height()  # Move down for the next line
        return (x,y)

    def wrap_text(self, text, max_width):
        """
        Wraps text to fit within the specified width.

        Parameters:
        - text: The text to wrap.
        - max_width: The maximum width for each line.

        Returns:
        - A list of strings, where each string is a line of wrapped text.
        """
        wrapped_lines = []
        font = self.font
        words = text.split(' ')
        current_line = ""

        for word in words:
            # Check if adding the next word exceeds the max width
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            wrapped_lines.append(current_line.strip())

        return wrapped_lines
