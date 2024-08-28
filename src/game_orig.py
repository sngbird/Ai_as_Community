import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.Rect(100, 100, 50, 50)  # Example player object (x, y, width, height)
        self.holdingClick = False #Used to determine if the player started/stopped clicking this specific frame (see check_mouse_click)
        self.characterList = []
        self.menus = []

        for i in range(3):
            button = Button(pygame.Rect(200, 150 + (i* 75), 50, 50),str(i),self.menus)
            button.setFunctionSubMenu(selectSuggestionSubMenuFunction([275, 150 + (i* 75)],self.menus))
            self.characterList.append(button)

    # update func, ran every frame.
    def update(self):
        # Update the game state (e.g., player movement, collision detection)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print(str(self.characterList) + str(self.menus))
            self.player.x -= 5
        if keys[pygame.K_RIGHT]:
            self.player.x += 5
        if keys[pygame.K_UP]:
            self.player.y -= 5
        if keys[pygame.K_DOWN]:
            self.player.y += 5
        self.check_mouse_click(self.characterList + [i for row in self.menus for i in row])

    # draw function, draws the scene every frame
    def draw(self):
        # Draw the game state (e.g., draw player, enemies, background)
        pygame.draw.rect(self.screen, (255, 255, 255), self.player)  # Draw player as white rectangle
        for item in self.characterList:
            pygame.draw.rect(self.screen, (200, 200, 200), item)
        for menu in self.menus:
            for clickable in menu:
                pygame.draw.rect(self.screen, (200, 200, 200), clickable)

    # Checks if the player clicked on one of the buttons inside the itemList array
    def check_mouse_click(self, itemList):
        if(pygame.mouse.get_pressed()[0] and self.holdingClick == False):
            print("clicked!")
            self.holdingClick = True
            boxesClicked = [box for box in itemList if box.rect.collidepoint(pygame.mouse.get_pos())]
            print("clicked on: " + str(boxesClicked))
            if(len(boxesClicked) > 0):
                #Should only have been able to click 1 box; we just take the first obj from list
                boxClicked = boxesClicked[0]
                boxClicked.function()
            print("CMC" + str(self.menus))
        elif(not pygame.mouse.get_pressed()[0] and self.holdingClick == True):
            print("stopped click!")
            self.holdingClick = False

    #def make_menu(self):

'''
MENU EXPLANATION
There is a 'main' menu called characterList. This List contains all the characters you can interact with in the scene.
By clicking those characters, you open up a submenu containing all the other characters they can interact with.
Clicking on of those opens another submenu with the suggestion buttons.
Clicking a suggestion button closes all submenus and performs the suggestion
'''

class Button:
    def __init__(self, rectangle, text, sceneMenus):
        self.rect = rectangle
        self.text = text
        self.sceneMenus = sceneMenus
        #function is set and performed later
        self.function = self.printInfo

    # Prints what button this is. Used as a default
    def printInfo(self):
        print("Button " + self.text + " clicked!")

    # sets the function to be the creation of a sub-menu
    def setFunctionSubMenu(self, getSubMenu):
        self.subMenuContents = getSubMenu #function that returns array of button objects
        self.function = self.makeSubMenu

    # Creates a sub-menu
    def makeSubMenu(self):
        #print("MSM " + str(self.sceneMenus))
        '''
        menuLayer = 0
        for menu in self.sceneMenus:
            print(self in menu)
            if self in menu:
                #Cut off all menus after the menu you're selecting from
                self.sceneMenus = self.sceneMenus[:menuLayer]
                break
            menuLayer += 1
        if menuLayer >= len(self.sceneMenus):
            self.sceneMenus = []
        '''
        #If this completes without being in any menu, then it's in the character list

        #print("MSM " + str(self.sceneMenus))
        #For now, make a new sub-layer with 3 more buttons, and apply it to the list of menus
        self.subMenuContents(self)
        #print("MSM " + str(self.sceneMenus))

    # Sets the function to be performing a suggestion.
    def setFunctionPerformSuggestion(self, suggestion):
        self.function = suggestion

    '''
    def PerformSuggestion(self):
        #clear out all other menus sans character
        self.sceneMenus = []
        #Then, perform the suggestion function
        self.function()
    '''

def selectTargetCharSubMenu():
    print('temp')

#Returns a function that creates a submenu with suggestion options
# location = (x,y) of first box
def selectSuggestionSubMenuFunction(location,menus):
    def SuggestionSubMenu(callingButton):
        menuLayer = 0
        for menu in menus:
            print(callingButton in menu)
            if callingButton in menu:
                #Cut off all menus after the menu you're selecting from
                #menus = menus[:menuLayer]
                while menuLayer + 1 < len(menus):
                    menus.pop()
                break
            menuLayer += 1
        if menuLayer >= len(menus):
            menus.clear()
        # The specific suggestions available depends on how it's coded.
        # For now, this produces a bunch of buttons that merely print to the console
        SuggestionList = []
        for i in range(3):
            button = Button(pygame.Rect(location[0], location[1] + (i* 75), 50, 50),str(i),menus)
            def sugg():
                print("Hello world! from button " + str(i))

            button.setFunctionPerformSuggestion(selectSuggestion(sugg,menus))
            SuggestionList.append(button)
        menus.append(SuggestionList)
        #print("SSM" + str(menus))

    return SuggestionSubMenu

# Returns a function that causes the game to perform a suggestion. Clears all menus when said function is executed
def selectSuggestion(suggestion, menus):
        def PerformSuggestion():
            print("test")
            #clear out all other menus sans character
            menus.clear()
            #Then, perform the suggestion function
            suggestion()
        
        return PerformSuggestion