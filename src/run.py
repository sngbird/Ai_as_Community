import pygame
import sys
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Tavern Week")
    clock = pygame.time.Clock()

    game = Game(screen)
    frame_count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        frame_count += 1
        if frame_count % 5 == 0: game.handle_input()
        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

if __name__ == "__main__":
    main()
