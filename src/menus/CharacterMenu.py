from menus.Menu import Menu
import pygame

TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)

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