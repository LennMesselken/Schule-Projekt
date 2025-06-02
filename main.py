import pygame
from gamestate import Gamestate


WIDTH, HEIGHT = 896, 896
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
BROWN = (160, 82, 45)

#window config
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")

images = {}
gamestate = Gamestate()

def load_images():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP',
              'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'assets/{piece}.png'), (64, 128))

def draw_board():
    colors = [WHITE, BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = gamestate.board[row][col]
            if piece != '--':
                screen.blit(images[piece], (col*112+24,row*112-20))


# Game loop
running = True
while running:
    
    #init_game()
    load_images()
    draw_board()
    draw_pieces()
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False