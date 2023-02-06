import game_mechanics
import pygame
import random


JEWEL_HEIGHT = (1 / 13) - 0.01
JEWEL_WIDTH = (1 / 6) - 0.01
BORDER_RADIUS = 15

S = [242, 245, 66]
T = [66, 203, 245]
V = [66, 245, 75]
W = [120, 37, 37]
X = [209, 26, 255]
Y = [0, 92, 230]
Z = [255, 0, 0]

class Columns:
    def __init__(self):
        self.running = True
        self.f = None
        self.faller = None



    def main(self) -> None:
        """Main function that contains the game loop."""
        board = game_mechanics.SpawnBoard().create_board()
        self.f = self._create_faller(board)
        self.faller = game_mechanics.Faller(self.f[0], board, self.f[1], self.f[2], self.f[3])
        pygame.init()
        try:
            self._create_board((350, 700))
            clock = pygame.time.Clock()

            tick = 0
            while self.running:
                clock.tick(30)
                if self.faller.state == 'game over':
                    surface = pygame.display.get_surface()
                    width = surface.get_width()
                    height = surface.get_height()
                    surface.fill(pygame.Color(0, 0, 0))
                    pygame.font.init()
                    font = pygame.font.SysFont('Times New Roman', int(0.1 *(height + width) / 2), True)
                    text = font.render('GAME OVER', True, pygame.Color(39, 204, 2))
                    surface.blit(text, (0, 0))
                    pygame.display.flip()
                    self._handle_game_over()
                else:
                    self._event_handler()
                    if tick % 10 == 0:
                        if self.faller.state == 'set':
                            board_copy = self.faller.copy
                            self.f = self._create_faller(board_copy) 
                            self.faller = game_mechanics.Faller(self.f[0], board_copy, self.f[1], self.f[2], self.f[3])
                        self.faller.states()
                        self.redraw(self.faller.copy)
                    tick += 1
        except:
            pygame.quit()


    def _handle_game_over(self) -> None:
        """Close the game in the game over screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def _event_handler(self) -> None:
        """Handles all the events in the game."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._key_handler(event.key)


    def _key_handler(self,key) -> None:
        """Handle when the key is pressed down."""
        if key == pygame.K_SPACE:
            self.faller.rotate()
        elif key == pygame.K_RIGHT:
            self.faller.move_right()
        elif key == pygame.K_LEFT:
            self.faller.move_left()


    def redraw(self, board) -> None:
        """Changes the display surface periodically."""
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(0, 0, 0))
        self._draw_grid()
        self._draw_jewels(board)
        pygame.display.flip()


    def _create_faller(self, board: list) -> list:
        """Create a random faller with random jewels and column."""
        letters = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        jewel1 = random.choice(letters)
        jewel2 = random.choice(letters)
        jewel3 = random.choice(letters)
        col = random.randint(1, 6)
        while board[0][col - 1] != ' ':
            col = random.randint(1, 6)
        faller = [col, jewel1, jewel2, jewel3]
        return faller


    def _draw_grid(self) -> None:
        """Draw the grid lines for the game board."""
        surface = pygame.display.get_surface()
        height = surface.get_height()
        width = surface.get_width()
        x = 0
        y = 0
        for i in range(13):
            y += (height / 13)
            pygame.draw.line(surface, pygame.Color(255, 255, 255), (0, y), (width, y))
        for i in range(6):
            x += (width / 6)
            pygame.draw.line(surface, pygame.Color(255, 255, 255), (x, 0), (x, height))


    def _draw_jewels(self, board) -> None:
        """Draw individual jewels on the board."""
        surface = pygame.display.get_surface()
        height = surface.get_height()
        width = surface.get_width()
        y = 0.005
        for row in board:
            x = 0.005
            for col in row:
                rect_obj = pygame.Rect(x * width, y * height, JEWEL_WIDTH * width, JEWEL_HEIGHT * height)
                if '[' in col:
                    if 'S' in col:
                        pygame.draw.rect(surface, pygame.Color(S[0], S[1], S[2]), rect_obj, BORDER_RADIUS)
                    elif 'T' in col:
                        pygame.draw.rect(surface, pygame.Color(T[0], T[1], T[2]), rect_obj, BORDER_RADIUS)
                    elif 'V' in col:
                        pygame.draw.rect(surface, pygame.Color(V[0], V[1], V[2]), rect_obj, BORDER_RADIUS)
                    elif 'W' in col:
                        pygame.draw.rect(surface, pygame.Color(W[0], W[1], W[2]), rect_obj, BORDER_RADIUS)
                    elif 'X' in col:
                        pygame.draw.rect(surface, pygame.Color(X[0], X[1], X[2]), rect_obj, BORDER_RADIUS)
                    elif 'Y' in col:
                        pygame.draw.rect(surface, pygame.Color(Y[0], Y[1], Y[2]), rect_obj, BORDER_RADIUS)
                    elif 'Z' in col:
                        pygame.draw.rect(surface, pygame.Color(Z[0], Z[1], Z[2]), rect_obj, BORDER_RADIUS)
                
                elif '|' in col:
                    if 'S' in col:
                        pygame.draw.rect(surface, pygame.Color(S[0], S[1], S[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'T' in col:
                        pygame.draw.rect(surface, pygame.Color(T[0], T[1], T[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'V' in col:
                        pygame.draw.rect(surface, pygame.Color(V[0], V[1], V[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'W' in col:
                        pygame.draw.rect(surface, pygame.Color(W[0], W[1], W[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'X' in col:
                        pygame.draw.rect(surface, pygame.Color(X[0], X[1], X[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'Y' in col:
                        pygame.draw.rect(surface, pygame.Color(Y[0], Y[1], Y[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    elif 'Z' in col:
                        pygame.draw.rect(surface, pygame.Color(Z[0], Z[1], Z[2]), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj, BORDER_RADIUS)
                    
                elif (len(col) == 1) and (col != ' '):
                    if 'S' in col:
                        pygame.draw.rect(surface, pygame.Color(S[0], S[1], S[2]), rect_obj)
                    elif 'T' in col:
                        pygame.draw.rect(surface, pygame.Color(T[0], T[1], T[2]), rect_obj)
                    elif 'V' in col:
                        pygame.draw.rect(surface, pygame.Color(V[0], V[1], V[2]), rect_obj)
                    elif 'W' in col:
                        pygame.draw.rect(surface, pygame.Color(W[0], W[1], W[2]), rect_obj)
                    elif 'X' in col:
                        pygame.draw.rect(surface, pygame.Color(X[0], X[1], X[2]), rect_obj)
                    elif 'Y' in col:
                        pygame.draw.rect(surface, pygame.Color(Y[0], Y[1], Y[2]), rect_obj)
                    elif 'Z' in col:
                        pygame.draw.rect(surface, pygame.Color(Z[0], Z[1], Z[2]), rect_obj)
                
                elif '*' in col:
                    if 'S' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(S[0], S[1], S[2]), rect_obj, BORDER_RADIUS)
                    elif 'T' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(T[0], T[1], T[2]), rect_obj, BORDER_RADIUS)
                    elif 'V' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(V[0], V[1], V[2]), rect_obj, BORDER_RADIUS)
                    elif 'W' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(W[0], W[1], W[2]), rect_obj, BORDER_RADIUS)
                    elif 'X' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(X[0], X[1], X[2]), rect_obj, BORDER_RADIUS)
                    elif 'Y' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(Y[0], Y[1], Y[2]), rect_obj, BORDER_RADIUS)
                    elif 'Z' in col:
                        pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect_obj)
                        pygame.draw.rect(surface, pygame.Color(Z[0], Z[1], Z[2]), rect_obj, BORDER_RADIUS)
                
                elif col == ' ':
                    pygame.draw.rect(surface, pygame.Color(0, 0, 0), rect_obj)
                x += 1/6
            y += 1/13    


    def _create_board(self, size) -> None:
        """Create a resizable display for the game."""
        pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption('Columns.exe')


if __name__ == '__main__':
    Columns().main()