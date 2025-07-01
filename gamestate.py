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

        self.white_castle_king_side = True
        self.white_castle_queen_side = True
        self.black_castle_king_side = True
        self.black_castle_queen_side = True

        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)


        self.in_check = False
        self.pins = []
        self.checks = []


    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "--"
        if move.piece_moving[0] == 'w':
            if move.piece_moving[1] == 'K':
                self.white_castle_king_side = False
                self.white_castle_queen_side = False
            elif move.piece_moving[1] == 'R':
                if move.start_column == 0:
                    self.white_castle_queen_side = False
                elif move.start_column == 7:
                    self.white_castle_king_side = False
        if move.piece_moving[0] == 'b':
            if move.piece_moving[1] == 'K':
                self.black_castle_king_side = False
                self.black_castle_queen_side = False
            elif move.piece_moving[1] == 'R':
                if move.start_column == 0:
                    self.black_castle_queen_side = False
                elif move.start_column == 7:
                    self.black_castle_king_side = False


        if move.promotion == True:
            valid_choices = {'N', 'B', 'R', 'Q'}
            choice = ""
            while True:
                user_input = input("Please input which piece you want to Promote to: (N) Knight (B) Bishop (R) Rook (Q) Queen:\n").upper()
                if user_input in valid_choices:
                    choice = user_input
                    break
            move.piece_moving = move.piece_moving[0] + choice

        if move.en_passant == True:
            self.board[move.start_row][move.end_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moving

        if move.castle:
            if move.end_column == 6:
                if self.colors_turn == 'w':
                    self.make_move(Move((7,7), (7,5), self.board))
                    self.white_king_location = (7,6)
                else:
                    self.make_move(Move((0,7), (0,5), self.board))
                    self.black_king_location = (0,6)
            elif move.end_column == 2:
                if self.colors_turn == 'w':
                    self.make_move(Move((7,0), (7,3), self.board))
                    self.white_king_location = (7,2)
                else: 
                    self.make_move(Move((0,0), (0,3), self.board))
                    self.black_king_location = (0,2)
        else:
            if move.piece_moving[1] == 'K':
                if move.piece_moving[0] == 'w':
                    self.white_king_location = (move.end_row, move.end_column)
                else:
                    self.black_king_location = (move.end_row, move.end_column)

            self.move_log.append(move)
            self.white_turn = not self.white_turn
            self.colors_turn = 'w' if self.white_turn else 'b'

    def get_valid_moves(self):
        moves = []
        #print(f"Before: {self.in_check} {len(self.pins)} {len(self.checks)}")
        self.in_check, self.pins, self.checks = self.check_checks_and_pins()
        #print(f"{self.white_king_location[0]} {self.white_king_location[1]} {self.black_king_location[0]} {self.black_king_location[1]}")
        #print(f"After: {self.in_check} {len(self.pins)} {len(self.checks)}")

        if self.colors_turn == 'w':
            king_row, king_column = self.white_king_location[0], self.white_king_location[1]
        else:
            king_row, king_column = self.black_king_location[0], self.black_king_location[1]

        if self.in_check:
            if len(self.checks) == 1: #Only 1 Check that can be blocked
                moves = self.get_all_moves()
                check = self.checks[0]
                check_row, check_column = check[0], check[1]
                piece_checking = self.board[check_row][check_column]
                valid_squares = []
                if piece_checking[1] == 'K':
                    valid_squares = [(check_row, check_column)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_column + check[3] * i)  # 2 & 3 = check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_column:
                            break
                for i in range(len(moves) - 1, -1, -1):  # Gets rid of move not blocking, checking, or moving king
                    if moves[i].piece_moving[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_column) in valid_squares:
                            moves.remove(moves[i])   

            else: #king twice in check and has to move
                moves = self.get_valid_king_moves(king_row, king_column)               

        else: #not in check
            moves = self.get_all_moves()

        if len(moves) == 0: #Checkmate or Stalemate
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        
               
        
        return moves

    def get_all_moves(self):
        moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col][0] != self.colors_turn:
                    continue
                moves.extend(self.get_piece_moves(row, col))
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
        piece_pinned = False
        pin_direction = ()
        for i in range (len(self.pins) -1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
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

        #normal moves
        if self.board[row + move_amount][col] ==  "--":
            if not piece_pinned or pin_direction == (move_amount, 0):
                if row + move_amount == back_row:
                    promotion = True
                moves.append(Move((row, col), (row + move_amount, col), self.board, promotion))

        #option of 2 square move as first move
        if row == home_row and self.board[row + 2 * move_amount][col] ==  "--":
            moves.append(Move((row, col), (row + 2* move_amount, col), self.board, promotion))

        #capturing
        if col-1 >= -1:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col-1][0] == opponent_color:
                    if row + move_amount == back_row:
                        promotion = True
                    moves.append(Move((row, col), (row + move_amount, col-1), self.board, promotion))
        if col+1 < 8:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[row + move_amount][col+1][0] == opponent_color:
                    if row + move_amount == back_row:
                        promotion = True
                    moves.append(Move((row, col), (row + move_amount, col+1), self.board, promotion))

        #en passant
        if len(self.move_log) > 0:
            if self.move_log[-1].piece_moving[1] == 'P' and self.move_log[-1].start_row == (7 - home_row) and (self.move_log[-1].end_row == 3 or self.move_log[-1].end_row == 4) and (row == self.move_log[-1].end_row)and (col - self.move_log[-1].start_column == 1 or col - self.move_log[-1].start_column == -1):
                if self.move_log[-1].end_column < col:
                    col_move_direction = -1
                else:
                    col_move_direction = 1
                if not piece_pinned or pin_direction == (move_amount, col_move_direction):
                    moves.append(Move((row, col), (row + move_amount, self.move_log[-1].start_column), self.board, promotion, True))
        
        return moves
            

    def get_valid_knight_moves(self, row, col):
        opponent = 'b' if self.white_turn else 'w'

        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        moves = []
        for d in directions:
            end_row = row + d[0]
            end_column = col + d[1] 
            if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board): # piece remains on board
                end_square = self.board[end_row][end_column]
                if end_square[0] == opponent:
                    moves.append(Move((row, col),(end_row, end_column), self.board))
                elif end_square == "--": 
                    moves.append(Move((row, col),(end_row, end_column), self.board))
        return moves
    
    def get_valid_bishop_moves(self, row, col):
        opponent = 'b' if self.white_turn else 'w'

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = [(-1,-1),(1,-1),(-1,1),(1,1)]

        moves = []
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_column = col + d[1] * i
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board): # piece remains on board
                    if not piece_pinned or pin_direction == (-d[0], -d[1]):
                        end_square = self.board[end_row][end_column]
                        if end_square == "--":
                            moves.append(Move((row, col),(end_row, end_column), self.board))
                        elif end_square[0] == opponent:
                            moves.append(Move((row, col),(end_row, end_column), self.board)) 
                            break
                        else:
                            break
                else:
                    break
        return moves

    def get_valid_rook_moves(self, row, col):
        opponent = 'b' if self.white_turn else 'w'

        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':  # Can't remove queen from pin on rook moves (only bishop moves)
                    self.pins.remove(self.pins[i])
                break

        directions = [(0,-1),(0, 1),(-1,0),(1,0)]
        moves = []
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_column = col + d[1] * i
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board): # piece remains on board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_square = self.board[end_row][end_column]
                        if end_square == "--":
                            moves.append(Move((row, col),(end_row, end_column), self.board))
                        elif end_square[0] == opponent:
                            moves.append(Move((row, col),(end_row, end_column), self.board)) 
                            break
                        else:
                            break
                else:
                    break
        return moves
    def get_valid_queen_moves(self, row, col):
        moves = self.get_valid_bishop_moves(row, col)
        moves.extend(self.get_valid_rook_moves(row, col))
        return moves
    
    def get_valid_king_moves(self, row, col):
        #print(f"king loc before {self.white_king_location[0]} {self.white_king_location[1]} {self.black_king_location[0]} {self.black_king_location[1]}")
        ally = 'w' if self.white_turn else 'b'
        opponent = 'b' if self.white_turn else 'w'
        directions = [(0,-1),(0, 1),(-1,0),(1,0),(-1,-1),(1,-1),(-1,1),(1,1)]
        moves = []
        for d in directions:
                end_row = row + d[0] 
                end_column = col + d[1] 
                if 0 <= end_row < len(self.board) and 0 <= end_column < len(self.board): # piece remains on board
                    end_square = self.board[end_row][end_column]
                    if end_square[0] != ally:
                        if ally == 'w':
                            self.white_king_location = (end_row, end_column)
                        else:
                            self.black_king_location = (end_row, end_column)
                        in_check, pins, checks = self.check_checks_and_pins()
                        if not in_check:
                            moves.append(Move((row, col),(end_row, end_column), self.board)) 
                        if ally == 'w':
                            self.white_king_location = (row, col)
                        else:
                            self.black_king_location = (row, col)

                    
        if self.in_check == False:
            if self.white_castle_king_side and self.colors_turn == 'w':
                if self.board[7][7] == 'wR':
                    if self.board[7][5] == '--' and not self.square_attacked(7, 5) and self.board[7][6] == '--' and not self.square_attacked(7,6):
                        moves.append(Move((row, col), (7, 6), self.board, castle=True))

            if self.white_castle_queen_side and self.colors_turn == 'w':
                if self.board[7][0] == 'wR':
                    if self.board[7][1] == '--' and not self.square_attacked(7, 1) and self.board[7][2] == '--' and not self.square_attacked(7, 2) and self.board[7][3] == '--' and not self.square_attacked(7, 3):
                        moves.append(Move((row, col), (7, 2), self.board, castle=True))

            if self.black_castle_king_side and self.colors_turn == 'b':
                if self.board[0][7] == 'bR':
                    if self.board[0][5] == '--' and not self.square_attacked(0, 5) and self.board[0][6] == '--' and not self.square_attacked(0, 6):
                        moves.append(Move((row, col), (0, 6), self.board, castle=True))

            if self.black_castle_queen_side and self.colors_turn == 'b':
                if self.board[0][0] == 'bR':
                    if self.board[0][1] == '--' and not self.square_attacked(0, 1) and self.board[0][2] == '--' and not self.square_attacked(0, 2) and self.board[0][3] == '--' and not self.square_attacked(0, 3):
                        moves.append(Move((row, col), (0, 2), self.board, castle=True))
        #print(f"king loc after {self.white_king_location[0]} {self.white_king_location[1]} {self.black_king_location[0]} {self.black_king_location[1]}")
        return moves
    

    def square_attacked(self, row, col):
        ally = 'w' if self.white_turn else 'b'
        opponent = 'b' if self.white_turn else 'w'
        directions = [(-1,-1),(1,-1),(-1,1),(1,1),(0,-1),(0, 1),(-1,0),(1,0)]
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1,8):
                end_row = row + d[0] * i
                end_column = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0] == ally:
                        break
                    elif end_piece[0] == opponent:
                        piece_type = end_piece[1]
                        if (0 <= j < 4 and piece_type == 'B') or (4 <= j <= 7 and piece_type == 'R') or (i == 1 and piece_type == 'P' and ((opponent == 'w' and j == 1 or j == 3) or (opponent == 'b' and j == 0 or j == 2)) or (piece_type == 'Q') or (i == 1 and piece_type == 'K')):
                            return True
                        else:
                            break

                else:
                    break
        knight_directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for d in knight_directions:
            end_row = row + d[0]
            end_column = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    return True
        return False
    
    def check_checks_and_pins(self):
        pins = []
        checks = []
        in_check = False

        if self.colors_turn == 'w':
            opponent = 'b'
            ally = 'w'
            start_row, start_column = self.white_king_location[0], self.white_king_location[1]

        else:
            opponent = 'w'
            ally = 'b'
            start_row, start_column = self.black_king_location[0], self.black_king_location[1]

        #print(f"Inside Start Location {start_row} {start_column} Ally {ally} Opponent {opponent}")
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            #print(f"123 {d}")
            possible_pin = ()
            for i in range(1,8):
                #print("test")
                end_row = start_row + d[0] * i
                end_column = start_column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_column < 8:
                    end_piece = self.board[end_row][end_column]
                    if end_piece[0] == ally and end_piece[1] != 'K':
                        if possible_pin == (): # no piece blocking
                           possible_pin = (end_row, end_column, d[0], d[1])
                        else: # piece blocking
                           #print("break 1")
                           break 

                    elif end_piece[0] == opponent:
                        piece_type = end_piece[1]
                        #print(f"Inside: {piece_type}")
                        if (0 <= j <= 3 and piece_type == 'R') or (4 <= j <= 7 and piece_type == 'B') or (i == 1 and piece_type == 'P' and ((opponent == 'w' and 6 <= j <= 7) or (opponent == 'b' and 4 <= j <= 5))) or (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            #print(f"Inside: {j}")
                            if possible_pin == (): #no piece blocking
                                in_check = True
                                checks.append((end_row, end_column, d[0], d[1]))
                                #print("break 2")
                                break
                            else: #piece blocking
                                pins.append(possible_pin)
                                #print("break 3")
                                break

                        else:
                            #print("break 4")
                            break
                else:
                    #print("break 5")
                    break

        knight_directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for d in knight_directions:
            end_row = start_row + d[0]
            end_column = start_column + d[1]
            if 0 <= end_row < 8 and 0 <= end_column < 8:
                end_piece = self.board[end_row][end_column]
                if end_piece[0] == opponent and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_column, d[0], d[1]))
        #print(f"Inside Return {in_check} {pins} {checks}")
        return in_check, pins, checks  


        


        


class Move:
    def __init__(self, start_square, end_square, board, promotion = False, en_passant = False, castle = False):
        self.start_row, self.start_column = start_square
        self.end_row, self.end_column = end_square
        self.piece_moving = board[self.start_row][self.start_column]
        self.promotion = promotion
        self.unique_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column
        self.en_passant = en_passant
        self.castle = castle

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.unique_id == other.unique_id
        return False
        