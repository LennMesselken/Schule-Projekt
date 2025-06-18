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

                if square_selected == (column, row): #player clicks on same square 
                    square_selected = () # Deselects square
                    player_clicks = []

                else: #player clicks on new square
                    square_selected = (column, row)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2: #player has clicked on two different squares
                    move = Move(player_clicks[0], player_clicks[1], gamestate.board)
                    valid_moves = gamestate.get_valid_moves()
                    if True:
                    #for i in range(len(valid_moves)):
                        #if move == valid_moves[i]: #move is valid
                        if True:
                            #gamestate.make_move(valid_moves[i])
                            gamestate.make_move(move)
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
    if square_selected != ():
        row, column = square_selected
        colors_turn = 'w' if gamestate.white_turn else 'b' #which colors turn
        if gamestate.board[column][row][0] == colors_turn: #player clicks on own piece
            
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100) #color should be transparent so color underneath can be seen
            s.fill(pygame.Color((0,255,0)))
            screen.blit(s, (row* SQUARE_SIZE, column * SQUARE_SIZE))


def draw_pieces(screen, gamestate):
    for row in range(ROWS):
        for col in range(COLS):
            piece = gamestate.board[row][col]
            if piece != '--':
                screen.blit(images[piece], (col*112+24,row*112-20))

if __name__ == "__main__":
    main()