class Gamestate:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        
        self.white_turn = True
        self.checkmate = False
        self.stalemate = False


    def make_move(self, move):
        self.board[move.start_column][move.start_row] = "--"
        self.board[move.end_column][move.end_row] = move.piece_moving

    def get_valid_moves(self):
        pass



class Move:
    def __init__(self, start_square, end_square, board):
        self.start_row, self.start_column = start_square
        self.end_row, self.end_column = end_square
        self.piece_moving = board[self.start_column][self.start_row]
        
        