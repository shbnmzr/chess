import pygame
import pygame.image
import os
from game import GameState
from move import Move

pygame.init()

WIDTH = 512
HEIGHT = 512
DIMENSIONS = 8

SQUARE_SIZE = HEIGHT // DIMENSIONS

IMAGES = dict()


def load_images():
    path = './pieces/photos/'
    for image in os.listdir(path):
        if image.endswith('.png'):
            name = image.replace('.png', '')
            IMAGES[name] = pygame.transform.scale(pygame.image.load(os.path.join(path, image)),
                                                  (SQUARE_SIZE, SQUARE_SIZE))


def update_board():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    window.fill(pygame.Color('white'))
    game_state = GameState()
    load_images()
    selected_square = tuple()
    player_clicks = []
    legal_moves = game_state.get_legal_moves()
    move_made = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                column = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if selected_square == (row, column):
                    selected_square = tuple()
                    player_clicks = []
                else:
                    selected_square = (row, column)
                    player_clicks.append(selected_square)

                if len(player_clicks) == 2:
                    move = Move(player_clicks[0], player_clicks[1], game_state.board)
                    if move in legal_moves:
                        move_made = True
                        game_state.make_move(move)
                        selected_square = tuple()
                        player_clicks = []
                    else:
                        player_clicks = [selected_square]

            if move_made:
                legal_moves = game_state.get_legal_moves()
                move_made = False

        clock.tick()
        pygame.display.flip()
        draw_game_state(window, game_state)


def draw_game_state(window, game_state):
    draw_squares(window)
    draw_pieces(window, game_state.board)


def draw_squares(window):
    colors = [pygame.Color('white'), pygame.Color('grey')]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(window, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                        SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(window, board):
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            piece = board[row][col]
            if piece != '--':
                window.blit(IMAGES[piece], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                                       SQUARE_SIZE, SQUARE_SIZE))


def main():
    load_images()
    update_board()


if __name__ == '__main__':
    main()
