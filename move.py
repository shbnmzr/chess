
class Move:
    ranks_to_rows = {
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
    }
    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}
    files_to_cols = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    def __init__(self, start, end, current_board_state):
        self.start = start
        self.end = end
        self.current_board_state = current_board_state
        self.piece_moved = self.current_board_state[self.start[0]][self.start[1]]
        self.piece_captured = self.current_board_state[self.end[0]][self.end[1]]
        self.move_id = self.start[0] * 1000 + self.start[1] * 100 + self.end[0] * 10 + self.end[1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_notation(self):
        return self.get_rank_file(self.start[0], self.start[1]) + self.get_rank_file(self.end[0], self.end[1])

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
