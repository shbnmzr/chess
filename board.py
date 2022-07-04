import pygame
import pygame.image
import os
from game_logic import GameState
from move import Move
from Network import Network

pygame.init()


class Board:
    def __init__(self):
        self.path = './pieces/photos'
        self.WIDTH = 512
        self.HEIGHT = 512
        self.DIMENSIONS = 8
        self.SQUARE_SIZE = self.HEIGHT // self.DIMENSIONS
        self.IMAGES = dict()
        self.ready = False

    def load_images(self):
        for image in os.listdir(self.path):
            if image.endswith('.png'):
                name = image.replace('.png', '')
                self.IMAGES[name] = pygame.transform.scale(pygame.image.load(os.path.join(self.path, image)),
                                                      (self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_board(self):
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        window.fill(pygame.Color('white'))
        self.load_images()
        return window

    def update_board(self, window, network):
        game_state = GameState()
        selected_square = tuple()
        player_clicks = []
        clock = pygame.time.Clock()
        legal_moves = game_state.get_legal_moves()
        move_made = False

        running = True
        while running:
            try:
                game = network.send('get')
            except:
                running = False
                print('Could not get a game\n')
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    column = location[0] // self.SQUARE_SIZE
                    row = location[1] // self.SQUARE_SIZE
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
            self.draw_game_state(window, game_state)

    def draw_game_state(self, window, game_state):
        self.draw_squares(window)
        self.draw_pieces(window, game_state.board)

    def draw_squares(self, window):
        colors = [pygame.Color('white'), pygame.Color('grey')]
        for row in range(self.DIMENSIONS):
            for col in range(self.DIMENSIONS):
                color = colors[(row + col) % 2]
                pygame.draw.rect(window, color, pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                                            self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self, window, board):
        for row in range(self.DIMENSIONS):
            for col in range(self.DIMENSIONS):
                piece = board[row][col]
                if piece != '--':
                    window.blit(self.IMAGES[piece], pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                                           self.SQUARE_SIZE, self.SQUARE_SIZE))


def main():
    board = Board()
    window = board.draw_board()
    network = Network()
    board.update_board(window, network)


if __name__ == '__main__':
    main()
