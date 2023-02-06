import sys
from copy import deepcopy

class SpawnBoard:
    def __init__(self):
        self.board = []


    def create_board(self):
        """Create empty game board with 13 rows and 6 columns."""
        for r in range(13):
            lst = []
            for c in range(6):
                lst.append(' ')
            self.board.append(lst)
        return self.board


class Matching:
    def __init__(self, board):
        self.board = board


    def horizontal(self) -> bool:
        '''checks horizontal matching'''
        index = []
        count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] != ' ') and (j <= len(self.board[0]) - 3):
                    if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2]:
                        index.append([i, j])
                        count = 1
                        while j + count < len(self.board[0])-1:
                            try:
                                while self.board[i][j + count] == self.board[i][j]:
                                    index.append([i, j + count])
                                    count +=1
                            except:
                                pass
        for a in index:

            x = self.board[a[0]][a[1]]
            if '*' not in self.board[a[0]][a[1]]:
                self.board[a[0]][a[1]] = ('*' + x + '*')
                count +=1
        if len(index) > 1:
            index.clear()
            return True
        else:
            index.clear()
            return False


    def vertical(self) -> bool:
        '''checks vertical matching'''
        index = []
        count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (self.board[i][j] != ' ') and (i <= len(self.board) - 3):
                    if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j]:
                        index.append([i, j])
                        count = 1
                        while i + count < len(self.board) - 1:
                            try:
                                while self.board[i + count][j] == self.board[i][j]:
                                    index.append([i + count, j])
                                    count +=1
                            except:
                                pass
        for a in index:
            x = self.board[a[0]][a[1]]
            if '*' not in self.board[a[0]][a[1]]:
                self.board[a[0]][a[1]] = ('*' + x + '*')
                count +=1
        if len(index) > 1:
            index.clear()
            return True
        else:
            index.clear()
            return False


def shift_down(board) -> list:
    """Check if there is a hole below to move all the content below."""
    while check_below(board) == False:
        for r in range(len(board)-1):
            for c in range(len(board[0])):
                if (board[r][c] != ' ') and (board[r + 1][c] == ' '):
                    val = board[r][c]
                    board[r][c] = ' '
                    board[r + 1][c] = val
    return board


def check_below(board: list) -> bool:
    """Check if there is an empty space below every element."""
    result = True
    for r in range(len(board) - 1):
        for c in range(len(board[0])):
            if (board[r][c] != ' ') and (board[r + 1][c] == ' '):
                result = False
    return result


class Jewel:
    def __init__(self, letter, col, row):
        """Each jewel in the faller has its own characteristics."""
        self.letter = letter
        self.col = col
        self.row = row


class Faller:
    def __init__(self, col: str, board: list, one: str, two: str, three: str):
        self.board = board
        self.col = int(col)
        self.one = one
        self.two = two
        self.three = three
        self.row = 0
        self.copy = []
        self.bottom = Jewel(self.three, self.col -1,-1)
        self.middle = Jewel(self.two, self.col -1,-1)
        self.top = Jewel(self.one, self.col -1,-1)
        self.jewels = [self.top, self.middle, self.bottom]
        self.state = 'falling'


    def copygrid(self) -> None:
        """Make a copy of the game board."""
        copy = deepcopy(self.board)
        return copy


    def match(self) -> None:
        """Check for every possible match and returns boolean."""
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if '*' in self.board[i][j]:
                    self.board[i][j] = ' '
        self.board = shift_down(self.board)
        board1 = Matching(self.board)
        if board1.horizontal() or board1.vertical():
            self.state = 'match'
            self.board = board1.board
            board1 = None
        else:
            self.state = 'set'


    def states(self) -> None:
        """Call the function according to the state of the faller."""
        if self.state == 'falling':
            self.fall()
        if self.state == 'land':
            self.land()
        elif self.state == 'freeze':
            self.freeze()
        elif self.state == 'match':
            self.match()


    def move_right(self) -> None:
        """Check if right 3 rows are empty next to the faller and move it right."""
        if self.state != 'set':
            try:
                r = self.jewels[2].row
                c = self.jewels[2].col
                v = int(c) + 1
                if self.copy[r][v] == ' ':
                    for a in self.jewels:
                        if a.row != -1:
                            self.copy[a.row][(a.col+1)] = self.copy[a.row][(a.col)]
                            self.copy[a.row][(a.col)] = ' '
                            a.col +=1
                    self.col += 1
            except:
                pass
            else:
                if self.check_below_faller() == True:
                    if self.state == 'land' or self.state == 'freeze':
                        self.state = 'falling'
                        self.fall()
                elif self.check_below_faller() == False:
                    if self.state == 'falling':
                        self.state = 'land'
                        self.land()
                        self.row +=1



    def land(self) -> None:
        """Land the faller and add '|' to the jewels on both sides."""
        for i in self.jewels:
            if i.row >= 0:
                self.copy[i.row][(i.col)] = ('|' + str(i.letter) + '|')
        self.state = 'freeze'


    def move_left(self) -> None:
        """Check if left side to the faller is empty and move it left."""
        if self.state != 'set':
            try:
                r = self.jewels[2].row
                c = self.jewels[2].col
                v = int(c) + -1
                if self.copy[r][v] == ' ':
                    for a in self.jewels:
                        if a.row != -1 and a.col-1 >=0:
                            self.copy[a.row][(a.col-1)] = self.copy[a.row][(a.col)]
                            self.copy[a.row][(a.col)] = ' '
                            a.col = a.col- 1


            except:
                pass
            else:
                if self.jewels[2].col >= 0:
                    self.col = self.jewels[2].col + 1
                    if self.check_below_faller() == True:
                        if self.state == 'land' or self.state == 'freeze':
                            self.state = 'falling'
                            self.fall()
                    elif self.check_below_faller() == False:
                        if self.state == 'falling':
                            self.state = 'land'
                            self.land()
                            self.row +=1


    def freeze(self) -> None:
        """Implement the freeze motion of each faller."""
        count = 0
        for i in self.jewels:
            if i.row >= 0:
                count += 1
                self.copy[i.row][(i.col)] = self.copy[i.row][(i.col)].strip('|')
        if count < 3:
            self.state = 'game over'
        else:
            self.state = 'set'
            self.board = self.copy


    def game_over(self) -> None:
        """
        Check if the game is over by checking if the frozen faller is outside 
        the board and if there is a combination of jewels that match.
        """
        unused_jewels = []
        if self.match():
            for i in reversed(self.jewels):
                if i.row == -1:
                    unused_jewels.append(i.letter)
                    i.row = 0
            for j in unused_jewels:
                self.board[0][self.col] = j
                self.board = shift_down(self.board)
        else:
            print('GAME OVER')
            sys.exit()


    def check_below_faller(self) -> bool:
        """Check if there is a hole under the faller."""
        r = self.jewels[2].row
        c = self.jewels[2].col
        v = int(r) + 1
        try:
            if self.copy[v][c] == ' ':
                return True
            else:
                return False
        except:
            return False


    def rotate(self) -> None:
        """Rotate the faller by placing bottom jewel at the top."""
        three = self.jewels[2].letter
        two = self.jewels[1].letter
        one = self.jewels[0].letter
        self.jewels[0].letter = three
        self.jewels[1].letter = one
        self.jewels[2].letter = two

        for a in self.jewels:
            if self.state == 'falling':
                if a.row != -1:
                    self.copy[a.row][a.col] = ('[' + str(a.letter) + ']')
            elif self.state == 'freeze' or 'land':
                if a.row != -1:
                    self.copy[a.row][a.col] = ('|' + str(a.letter) + '|')
    

    def fall(self) -> None:
        """Makes the faller fall further."""
        copy = self.copygrid()
        if ((self.row == 12) and (self.board[self.row][self.col - 1] == ' ')) or ((self.row < 12) and (self.board[self.row + 1][self.col - 1] != ' ')):
            copy[self.row][self.col - 1] = ('[' + str(self.jewels[2].letter) + ']')
            self.bottom = Jewel(str(self.jewels[2].letter), self.col - 1, self.row)

            if (self.row - 1) >= 0:
                copy[self.row - 1][self.col - 1] = ('[' + str(self.jewels[1].letter) + ']')
                self.middle = Jewel(str(self.jewels[1].letter), self.col - 1, self.row - 1)
            if (self.row - 2) >= 0:
                copy[self.row - 2][self.col - 1] = ('[' + str(self.jewels[0].letter) + ']')
                self.top = Jewel(str(self.jewels[0].letter), self.col - 1, self.row - 2)
            self.state = 'land'
            self.copy = copy
            self.jewels = [self.top, self.middle, self.bottom]

        elif (self.board[self.row][self.col - 1] == ' ') and (self.row < len(copy) - 1):
            copy[self.row][self.col - 1] = ('[' + str(self.jewels[2].letter) + ']')
            self.bottom = Jewel(str(self.jewels[2].letter), self.col - 1, self.row)

            if (self.row - 1) >= 0:
                copy[self.row - 1][self.col - 1] = ('[' + str(self.jewels[1].letter) + ']')
                self.middle = Jewel(str(self.jewels[1].letter),self.col - 1, self.row - 1)
            if (self.row - 2) >= 0:
                copy[self.row - 2][self.col - 1] = ('[' + str(self.jewels[0].letter) + ']')
                self.top = Jewel(str(self.jewels[0].letter), self.col - 1, self.row - 2)
            self.copy = copy
            self.row += 1
            self.jewels = [self.top, self.middle, self.bottom]
            self.state = 'falling'
