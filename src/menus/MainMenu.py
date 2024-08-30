from menus.Menu import Menu
import pygame

TEXT = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (136, 136, 136)
BORDER = (77,17,150)

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
