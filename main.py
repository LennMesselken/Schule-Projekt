import pygame
from gamestate import Gamestate, Move


WIDTH, HEIGHT = 896, 896 #screen dimension
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS #size of single square
WHITE = (255, 255, 255)  #color for white squares
BROWN = (160, 82, 45) #color for black squares
BLACK = (80, 80, 80) #color for black squares
MAX_FPS = 60

#window config
pygame.init()
images = {} #images for piece sprites


def load_images(): #fills images dictionary with correct files
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (64, 128))

load_images()

def main():
    

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Chess")

    #global varialbes config
    gamestate = Gamestate() #gamestate Object
    gamestate.get_valid_moves()
    square_selected = () #keeps track of last player click (single tuple)
    player_clicks = [] #keeps track of players clicks (up to two tuples)
    move_made = False
    
    # Game loop
    running = True

    while running:
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #window quitting
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN: # player clicks
                location = pygame.mouse.get_pos() # get mouse position (x, y) on click
                column = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                if square_selected == (row, column): #player clicks on same square 
                    square_selected = () # Deselects square
                    player_clicks = []

                else: #player clicks on new square
                    if len(player_clicks) == 0: #first piece has to be of turn player
                         #which colors turn
                        if gamestate.board[row][column][0] == gamestate.colors_turn: #player clicks on own piece
                            square_selected = (row, column)
                            player_clicks.append(square_selected)
                    else:
                        square_selected = (row, column)
                        player_clicks.append(square_selected)

                if len(player_clicks) == 2: #player has clicked on two different squares
                    move = Move(player_clicks[0], player_clicks[1], gamestate.board)
                    valid_moves = gamestate.get_valid_moves()
                    #for i in range(len(valid_moves)):
                    #    print(f"valid  ({valid_moves[i].start_row, valid_moves[i].start_column }) => ({valid_moves[i].end_row, valid_moves[i].end_column }) Promotion: {valid_moves[i].promotion}")

                    #print(f"actual ({move.start_row, move.start_column }) => ({move.end_row, move.end_column }) Promotion: {move.promotion}")
                    for i in range(len(valid_moves)):
                        #print(move, valid_moves[i])
                        if move == valid_moves[i]: #move is valid
                            gamestate.make_move(valid_moves[i])
                            #gamestate.make_move(move)
                            move_made = True
                            square_selected = () #clean up
                            player_clicks = [] #clean up
                
                    if not move_made: #if move was not valid last clicked square is only player click
                        player_clicks = [square_selected]

                    if move_made: #resets
                        move_made = False
                        

        draw_gamestate(screen, gamestate, square_selected)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def draw_gamestate(screen, gamestate, square_selected):
    draw_board(screen) #draws the Board
    highlight_squares(screen, gamestate, square_selected) #highlights relevant squares
    draw_pieces(screen, gamestate) #draws the pieces



def draw_board(screen):
    colors = [WHITE, BLACK]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlight_squares(screen, gamestate, square_selected):
    if len(gamestate.move_log) != 0:
        last_move = gamestate.move_log[-1]
        start_row, start_column = last_move.start_row, last_move.start_column
        end_row, end_column = last_move.end_row, last_move.end_column
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        #s.set_alpha(100)
        s.fill(pygame.Color((255, 255, 0)))
        screen.blit(s, (start_column * SQUARE_SIZE, start_row * SQUARE_SIZE))
        screen.blit(s, (end_column * SQUARE_SIZE, end_row * SQUARE_SIZE))

    if square_selected != ():
        row, column = square_selected
        
        if gamestate.board[row][column][0] == gamestate.colors_turn: #player clicks on own piece
            
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            #s.set_alpha(100) #color should be transparent so color underneath can be seen
            s.fill(pygame.Color((0,255,0)))
            screen.blit(s, (column* SQUARE_SIZE, row * SQUARE_SIZE))
            s.fill(pygame.Color((0,0,255)))
            moves = []
            moves = gamestate.get_piece_moves(row, column)
            for i in range(len(moves)):
                screen.blit(s, (moves[i].end_column * SQUARE_SIZE, moves[i].end_row * SQUARE_SIZE))
    


def draw_pieces(screen, gamestate):
    for row in range(ROWS):
        for col in range(COLS):
            piece = gamestate.board[row][col]
            if piece != '--':
                screen.blit(images[piece], (col*112+24,row*112-20))

if __name__ == "__main__":
    main()