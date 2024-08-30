import sys
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
            elif self.game.menu_index == 3:  # Advance Time
                if len(self.game.quest_keeper.deployed_quests) > 0:
                    score = self.game.quest_keeper.advance_time()
                    self.game.advance_time(score)
            elif self.game.menu_index == 4:  # Exit
                pygame.quit()
                sys.exit()
        elif keys[pygame.K_UP]:
            self.game.menu_index = (self.game.menu_index - 1) % 5
        elif keys[pygame.K_DOWN]:
            self.game.menu_index = (self.game.menu_index + 1) % 5
    
    def draw(self):
        banner = f"Welcome to Tavern Week"
        week_counter = f"Current Week: {self.game.week_number}"
        score_counter = f"Total Quest Score: {self.game.score}"
        self.game.draw_text(banner, (self.game.screen.get_width() // 2, 50), TEXT, center=True)
        self.game.draw_text(week_counter, (self.game.screen.get_width() // 2, 80), TEXT, center=True)
        self.game.draw_text(score_counter, (self.game.screen.get_width() // 2, 110), TEXT, center=True)

        border_radius = 20
        shadow_offset = 0
        ## Title Section
        rect_width = 200
        rect_height = 300
        rect_x = (self.game.screen.get_width() // 2) - rect_width // 2
        rect_y = self.game.screen.get_height()//2 -150
        self.game.draw_rounded_rect_with_shadow(self.game.screen,(rect_x,rect_y, rect_width, rect_height), BORDER, border_radius, 0)
        options = ["Characters", "Quests", "Suggest Action", "Advance Time" ,"Exit"]
        for idx, option in enumerate(options):
            color = (255, 0, 0) if idx == self.game.menu_index else TEXT
            self.game.draw_text(option, (self.game.screen.get_width() // 2, self.game.screen.get_height()//2 -100 + idx * 50), color, center=True)
