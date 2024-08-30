from menus.Menu import Menu
import pygame
import suggestions

TEXT = (255, 255, 255)


# Menu where the player can select suggestions
class SuggestionMenu(Menu):
    def __init__(self, game):
        self.game = game
        self.menuDepth = 0 # 0=choosing charA, 1=choosing charB, 2=choosing suggestions
        self.charAIndex = 0 # suggestion performer index
        self.charBIndex = 0 # suggestion target index
        self.suggListLen = 5 # dedicated variable, as the full len func takes up >50% of my screen width

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
                    self.menuDepth = 0
                    self.charAIndex = 0
                    self.charBIndex = 0
                    self.game.menu_index = 0

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