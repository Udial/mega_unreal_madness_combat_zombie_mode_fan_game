import pygame
from Madness_Combat.src.core.game import Game


def main():
    pygame.init()

    try:
        game = Game()
        game.run()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()