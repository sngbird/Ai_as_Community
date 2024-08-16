import pygame
from game import Game
from social import Social

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    screen = pygame.display.set_mode((800, 600))  # Set window size (width, height)
    pygame.display.set_caption("My Pygame Project")

    # Create a clock object to manage frame rate
    clock = pygame.time.Clock()

    # Initialize game and social (rules) logic
    game = Game(screen)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        game.update()

        # Draw everything
        screen.fill((0, 0, 0))  # Fill screen with black
        game.draw()
        pygame.display.flip()

        # Cap the frame rate to 60 FPS
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
