import pygame
from game import Game
from assets import CELL_SIZE, window_size, GREEN, BLACK, DARKGREY

pygame.init()

window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Checkers Game')


def display_winner_screen(winner_name):
    x = window_size[0]
    y = window_size[1]
    font = pygame.font.SysFont('arial', 80, bold=True)
    if winner_name == 'Grey':
        text = font.render('GREY WINS', True, GREEN, BLACK)
    else:
        text = font.render('WHITE WINS', True, GREEN, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (x // 2, y // 2)
    while True:
        window.fill(BLACK)
        window.blit(text, text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

# converts pixel values to grid coordinates
def get_grid_coordinates(pos):
    return pos[1]//CELL_SIZE, pos[0]//CELL_SIZE

def main():
    game_running = True
    game = Game(window)
    while game_running:
        if game.winner() is not None:
            if game.winner() == DARKGREY:
                display_winner_screen('Grey')
                print('Winner is: Grey')
            else:
                display_winner_screen('White')
                print('Winner is: White')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                coordinates = get_grid_coordinates(position)
                game.select(coordinates[0], coordinates[1])
        game.update()

    pygame.quit()

main()
