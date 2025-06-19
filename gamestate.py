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
        self.colors_turn = 'w' if self.white_turn else 'b'
        self.checkmate = False
        self.stalemate = False

        self.move_log = []


    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "--"
        if move.promotion == True:
            valid_choices = {'N', 'B', 'R', 'Q'}
            choice = ""
            while True:
                user_input = input("Please input which piece you want to Promote to: (N) Knight (B) Bishop (R) Rook (Q) Queen:\n").upper()
                if user_input in valid_choices:
                    choice = user_input
                    break
            move.piece_moving = move.piece_moving[0] + choice
        self.board[move.end_row][move.end_column] = move.piece_moving
        self.move_log.append(move)
        self.white_turn = not self.white_turn
        self.colors_turn = 'w' if self.white_turn else 'b'

    def get_valid_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col][0] != self.colors_turn:
                    continue
                moves.extend(self.get_piece_moves(row, col))
               
        
        #for i in range(len(moves)):
        #   print(f"({moves[i].start_row, moves[i].start_column }) => ({moves[i].end_row, moves[i].end_column }) Promotion: {moves[i].promotion}")

        return moves

    def get_piece_moves(self, row, col):
        match self.board[row][col][1]:
                case 'P':
                    moves = self.get_valid_pawn_moves(row, col)
                case 'N':
                    moves = self.get_valid_knight_moves(row, col)
                case 'B':
                    moves = self.get_valid_bishop_moves(row, col)
                case 'R':
                    moves = self.get_valid_rook_moves(row, col)
                case 'Q':
                    moves = self.get_valid_queen_moves(row, col)
                case 'K':
                    moves = self.get_valid_king_moves(row, col)
        return moves

    def get_valid_pawn_moves(self, row, col):
        moves = []
        if self.colors_turn == 'w':
            move_amount = -1
            home_row = 6
            back_row = 0
            opponent_color = 'b'
            
        else:
            move_amount = 1
            home_row = 1
            back_row = 7
            opponent_color = 'w'
            
        promotion = False

        if self.board[row + move_amount][col] ==  "--":
            if row + move_amount == back_row:
                promotion = True
            moves.append(Move((row, col), (row + move_amount, col), self.board, promotion))

        if row == home_row and self.board[row + 2 * move_amount][col] ==  "--":
            moves.append(Move((row, col), (row + 2* move_amount, col), self.board, promotion))
        if col-1 >= -1:
            if self.board[row + move_amount][col-1][0] == opponent_color:
                if row + move_amount == back_row:
                    promotion = True
                moves.append(Move((row, col), (row + move_amount, col-1), self.board, promotion))
        if col+1 < 8:
            if self.board[row + move_amount][col+1][0] == opponent_color:
                if row + move_amount == back_row:
                    promotion = True
                moves.append(Move((row, col), (row + move_amount, col+1), self.board, promotion))
        
        return moves
            

    def get_valid_knight_moves(self, row, col):
        return []
    def get_valid_bishop_moves(self, row, col):
        return []
    def get_valid_rook_moves(self, row, col):
        return []
    def get_valid_queen_moves(self, row, col):
        return []
    def get_valid_king_moves(self, row, col):
        return []


class Move:
    def __init__(self, start_square, end_square, board, promotion = False):
        self.start_row, self.start_column = start_square
        self.end_row, self.end_column = end_square
        self.piece_moving = board[self.start_row][self.start_column]
        self.promotion = promotion
        self.unique_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column
        
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.unique_id == other.unique_id
        return False
        