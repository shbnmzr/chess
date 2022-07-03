from move import Move


class GameState:
    def __init__(self):
        # 8 by 8 2-D list representing the board
        self.board = [
            ['black_rook', 'black_knight', 'black_bishop', 'black_queen',
             'black_king', 'black_bishop', 'black_knight', 'black_rook'],
            ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn',
             'black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn',
             'white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
            ['white_rook', 'white_knight', 'white_bishop', 'white_queen',
             'white_king', 'white_bishop', 'white_knight', 'white_rook'],
        ]
        self.white_turn = True
        self.move_funtions = {
            'pawn': self.get_pawn_moves, 'rook': self.get_rook_moves, 'knight': self.get_knight_moves,
            'bishop': self.get_bishop_moves, 'queen': self.get_queen_moves, 'king': self.get_king_moves
        }

    def make_move(self, move):
        self.board[move.start[0]][move.start[1]] = '--'
        self.board[move.end[0]][move.end[1]] = move.piece_moved
        self.white_turn = not self.white_turn

    def get_legal_moves(self):
        return self.get_possible_moves()

    def get_possible_moves(self):
        moves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != '--':
                    turn, piece = self.board[row][col].split('_')
                    if (turn == 'white' and self.white_turn) or (turn == 'black' and not self.white_turn):
                        self.move_funtions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        if self.white_turn:
            if self.board[row - 1][col] == '--':
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == '--':
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = 'b' if self.white_turn else 'w'
        for direction in directions:
            for i in range(1, 8):
                end = row + direction[0] * i, col + direction[1] * i
                if 0 <= end[0] < 8 and 0 <= end[1] < 8:
                    end_piece = self.board[end[0]][end[1]]
                    if end_piece == '--':
                        moves.append(Move((row, col), end, self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), end, self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        own = 'w' if self.white_turn else 'b'
        for move in knight_moves:
            end = row + move[0], col + move[1]
            if 0 <= end[0] < 8 and 0 <= end[1] < 8:
                piece = self.board[end[0]][end[1]]
                if piece[0] != own:
                    moves.append(Move((row, col), end, self.board))

    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = 'b' if self.white_turn else 'w'
        for direction in directions:
            for i in range(1, 8):
                end = row + direction[0] * i, col + direction[1] * i
                if 0 <= end[0] < 8 and 0 <= end[1] < 8:
                    end_piece = self.board[end[0]][end[1]]
                    if end_piece == '--':
                        moves.append(Move((row, col), end, self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), end, self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, 1))
        own = 'w' if self.white_turn else 'b'
        for move in king_moves:
            end = row + move[0], col + move[1]
            if 0 <= end[0] < 8 and 0 <= end[1] < 8:
                piece = self.board[end[0]][end[1]]
                if piece[0] != own:
                    moves.append(Move((row, col), end, self.board))
