import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.Font(pygame.font.get_default_font(), 36)

# Load images
pause_icon = pygame.image.load('pause_icon.png')
pause_icon = pygame.transform.scale(pause_icon, (30, 30))
exit_icon = pygame.image.load('exit_icon.png')
exit_icon = pygame.transform.scale(exit_icon, (30, 30))

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Retro Tetris')

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]


class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_x = int(cols / 2 - len(self.current_piece[0]) / 2)
        self.piece_y = 0
        self.game_over = False

    def new_piece(self):
        return random.choice(SHAPES)

    def rotate_piece(self):
        self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]

    def valid_move(self, piece, offset):
        off_x, off_y = offset
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    if x + off_x < 0 or x + off_x >= self.cols or y + off_y >= self.rows:
                        return False
                    if self.board[y + off_y][x + off_x]:
                        return False
        return True

    def add_piece_to_board(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece_y][x + self.piece_x] = cell
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_x = int(self.cols / 2 - len(self.current_piece[0]) / 2)
        self.piece_y = 0
        if not self.valid_move(self.current_piece, (self.piece_x, self.piece_y)):
            self.game_over = True

    def clear_lines(self):
        lines = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines:
            del self.board[i]
            self.board.insert(0, [0 for _ in range(self.cols)])
        return len(lines)

    def drop_piece(self):
        if not self.valid_move(self.current_piece, (self.piece_x, self.piece_y + 1)):
            self.add_piece_to_board()
            return True
        self.piece_y += 1
        return False

    def move_piece(self, dx):
        if self.valid_move(self.current_piece, (self.piece_x + dx, self.piece_y)):
            self.piece_x += dx

    def hard_drop(self):
        while not self.drop_piece():
            pass


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Retro Tetris', FONT, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_play = pygame.Rect(50, 100, 200, 50)
        button_settings = pygame.Rect(50, 200, 200, 50)
        button_quit = pygame.Rect(50, 300, 200, 50)

        pygame.draw.rect(screen, BLUE, button_play)
        pygame.draw.rect(screen, GREEN, button_settings)
        pygame.draw.rect(screen, RED, button_quit)

        draw_text('Play', FONT, WHITE, screen, 60, 110)
        draw_text('Settings', FONT, WHITE, screen, 60, 210)
        draw_text('Quit', FONT, WHITE, screen, 60, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_play.collidepoint((mx, my)):
            if click:
                game()
        if button_settings.collidepoint((mx, my)):
            if click:
                settings()
        if button_quit.collidepoint((mx, my)):
            if click:
                quit_confirmation()

        pygame.display.update()


def settings():
    while True:
        screen.fill(BLACK)
        draw_text('Settings', FONT, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_easy = pygame.Rect(50, 100, 200, 50)
        button_medium = pygame.Rect(50, 200, 200, 50)
        button_hard = pygame.Rect(50, 300, 200, 50)
        button_back = pygame.Rect(50, 400, 200, 50)

        pygame.draw.rect(screen, BLUE, button_easy)
        pygame.draw.rect(screen, GREEN, button_medium)
        pygame.draw.rect(screen, RED, button_hard)
        pygame.draw.rect(screen, GRAY, button_back)

        draw_text('Easy', FONT, WHITE, screen, 60, 110)
        draw_text('Medium', FONT, WHITE, screen, 60, 210)
        draw_text('Hard', FONT, WHITE, screen, 60, 310)
        draw_text('Back', FONT, WHITE, screen, 60, 410)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_easy.collidepoint((mx, my)):
            if click:
                print('Set difficulty to Easy')
        if button_medium.collidepoint((mx, my)):
            if click:
                print('Set difficulty to Medium')
        if button_hard.collidepoint((mx, my)):
            if click:
                print('Set difficulty to Hard')
        if button_back.collidepoint((mx, my)):
            if click:
                return

        pygame.display.update()


def quit_confirmation():
    while True:
        screen.fill(BLACK)
        draw_text('Are you sure you want to quit?', FONT, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_yes = pygame.Rect(50, 100, 200, 50)
        button_no = pygame.Rect(50, 200, 200, 50)

        pygame.draw.rect(screen, RED, button_yes)
        pygame.draw.rect(screen, GREEN, button_no)

        draw_text('Yes', FONT, WHITE, screen, 60, 110)
        draw_text('No', FONT, WHITE, screen, 60, 210)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_yes.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_no.collidepoint((mx, my)):
            if click:
                return

        pygame.display.update()


def game():
    tetris = Tetris(20, 10)
    clock = pygame.time.Clock()
    speed = 500  # Lower value means faster game
    move_down = pygame.USEREVENT + 1
    pygame.time.set_timer(move_down, speed)

    while True:
        screen.fill(BLACK)

        mx, my = pygame.mouse.get_pos()
        button_pause = pygame.Rect(SCREEN_WIDTH - 90, 10, 30, 30)
        button_exit = pygame.Rect(SCREEN_WIDTH - 50, 10, 30, 30)

        screen.blit(pause_icon, (SCREEN_WIDTH - 90, 10))
        screen.blit(exit_icon, (SCREEN_WIDTH - 50, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1)
                if event.key == pygame.K_RIGHT:
                    tetris.move_piece(1)
                if event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                if event.key == pygame.K_UP:
                    tetris.rotate_piece()
                if event.key == pygame.K_SPACE:
                    tetris.hard_drop()
            if event.type == move_down:
                if tetris.drop_piece():
                    tetris.clear_lines()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_pause.collidepoint((mx, my)):
                        # Pause functionality
                        pass
                    if button_exit.collidepoint((mx, my)):
                        return

        # Draw board and piece
        for y, row in enumerate(tetris.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for y, row in enumerate(tetris.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, (
                        (tetris.piece_x + x) * BLOCK_SIZE, (tetris.piece_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main_menu()
