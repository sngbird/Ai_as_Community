import pygame
import sys
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tavern Week")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.handle_input()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(30)  # Maintain 60 FPS

if __name__ == "__main__":
    main()
