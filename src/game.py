import sys
from social import Social
from quest import QuestManager
import pygame
import queue
from menus.Menu import Menu
from menus.QuestMenu import QuestMenu
from menus.MainMenu import MainMenu, MainGameMenu
from menus.CharacterMenu import CharacterMenu, CharacterDisplay

# Define Colors
TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)




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