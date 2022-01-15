import pygame
import os

# Loading up all of the sprite images to use for display
chessboard = pygame.transform.scale(pygame.image.load((os.path.join("Sprites","Chess_board.jpg"))), (626,626))
chesspylogo = pygame.transform.scale(pygame.image.load(os.path.join("Sprites","ChesspyLogo1.png")), (160,120))
madeby = pygame.transform.scale(pygame.image.load(os.path.join("Sprites","madeby.png")), (260, 38))
woodboard = pygame.transform.scale(pygame.image.load((os.path.join("Sprites","woodboard.jpg"))), (626,626))

black_bishop = pygame.image.load(os.path.join("Sprites", "blackBishop.png"))
black_king = pygame.image.load(os.path.join("Sprites", "blackKing.png"))
black_knight = pygame.image.load(os.path.join("Sprites", "blackKnight.png"))
black_pawn = pygame.image.load(os.path.join("Sprites", "blackPawn.png"))
black_rook = pygame.image.load(os.path.join("Sprites", "blackRook.png"))
black_queen = pygame.image.load(os.path.join("Sprites", "blackQueen.png"))

white_bishop = pygame.image.load(os.path.join("Sprites", "whiteBishop.png"))
white_king = pygame.image.load(os.path.join("Sprites", "whiteKing.png"))
white_knight = pygame.image.load(os.path.join("Sprites", "whiteKnight.png"))
white_pawn = pygame.image.load(os.path.join("Sprites", "whitePawn.png"))
white_rook = pygame.image.load(os.path.join("Sprites", "whiteRook.png"))
white_queen = pygame.image.load(os.path.join("Sprites", "whiteQueen.png"))

black = [black_bishop, black_king, black_knight, black_pawn, black_queen, black_rook]
white = [white_bishop, white_king, white_knight, white_pawn, white_queen, white_rook]

# for scaling the pieces and the board
BlackPieces = []
for piece in black:
    BlackPieces.append(pygame.transform.scale(piece, (64,64)))
WhitePieces = []
for piece in white:
    WhitePieces.append(pygame.transform.scale(piece, (64,64)))


class ChessPieces:
    # index used to reference each piece later on
    index = -1
    game_field = (60, 60, 505, 505)
    start_x_pos = game_field[0]
    start_y_pos = game_field[1]

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.all_possible_movements_list = []
        # self.pawn is true when a pawn is chosen subsequently the same for self.king if a king is chosen
        self.pawn = False
        # self.selected_piece is true when a piece is selected other than that all others that are not should be false
        self.selected_piece = False
        self.king = False

    def get_color(self):
        return self.color

    def get_selected(self):
        return self.selected_piece

    def possible_moves(self, board):
        self.all_possible_movements_list = self.move_valid(board)

    def move_pos(self, pos):
        self.row = pos[0]
        self.column = pos[1]

    def border(self, win, board):
        if self.color == "White":
            img = WhitePieces[self.index]
        else:
            img = BlackPieces[self.index]

        if self.selected_piece:
            moves = self.move_valid(board)

            # Positions of red dots to display moves
            for movement in moves:
                x_pos = 33 + self.start_x_pos + (movement[0] * self.game_field[2] / 8)
                y_pos = 33 + self.start_x_pos + (movement[1] * self.game_field[3] / 8)
                pygame.draw.circle(win, (255,0,0),(x_pos, y_pos), 10)

        # to find coordinates of 1st column and row in chessboard
        x_pos = self.start_x_pos + (self.column * self.game_field[2] / 8)
        y_pos = self.start_x_pos + (self.row * self.game_field[3] / 8)

        # Blue border to outline which piece is selected
        if self.selected_piece:
            pygame.draw.rect(win, (0,0,255), (x_pos, y_pos,65,65), 2)

        win.blit(img, (x_pos, y_pos))


class Bishop(ChessPieces):
    index = 0
    
    # move_valid and all other move valids later on are all logical operations to tell the movement set of a piece, which is then put into a list
    def move_valid(self, board):
        rows = self.row
        columns = self.column

        move_list = []

        # Top Right Move
        dial = columns + 1
        diar = columns - 1
        for x in range(rows - 1, -1, -1):
            if dial < 8:
                j = board[x][dial]
                if j == 0:
                    move_list.append((dial, x))
                elif j.color != self.color:
                    move_list.append((dial, x))
                    break
                else:
                    dial = 9

            dial += 1

        for x in range(rows - 1, -1, -1):
            if diar > -1:
                j = board[x][diar]
                if j == 0:
                    move_list.append((diar, x))
                elif j.color != self.color:
                    move_list.append((diar, x))
                    break
                else:
                    diar = -1

            diar -= 1

        # Top Left Movement
        dial = columns + 1
        diar = columns - 1
        for x in range(rows + 1, 8):
            if dial < 8:
                j = board[x][dial]
                if j == 0:
                    move_list.append((dial, x))
                elif j.color != self.color:
                    move_list.append((dial, x))
                    break
                else:
                    dial = 9
            dial += 1

        for x in range(rows + 1, 8):
            if diar > -1:
                j = board[x][diar]
                if j == 0:
                    move_list.append((diar, x))
                elif j.color != self.color:
                    move_list.append((diar, x))
                    break
                else:
                    diar = -1

            diar -= 1


        return move_list


# instill methods into pawn class as pawns have extra features such as being able to turn to a queen and first moves
class Pawn(ChessPieces):
    index = 3

    def __init__(self, rows, columns, color):
        super().__init__(rows, columns, color)
        self.first_movement = True
        self.pawn = True
        self.turn_to_queen = False


    def move_valid(self, board):
        currrow = self.row
        currcol = self.column

        move_list = []
        try:
            if self.color == "Black":
                if self.first_movement:
                    if currrow < 6:
                        j = board[currrow + 2][currcol]
                        if j == 0:
                            move_list.append((currcol, currrow + 2))

                if currrow < 7:
                    j = board[currrow + 1][currcol]
                    if j == 0:
                        move_list.append((currcol, currrow + 1))

                # Diagonal attacks
                # Right attack
                if currcol < 7:
                    j = board[currrow + 1][currcol + 1]
                    if j != 0:
                        if j.color != self.color:
                            move_list.append((currcol + 1, currrow + 1))

                # Left attack
                if currcol > 0:
                    j = board[currrow + 1][currcol - 1]
                    if j != 0:
                        if j.color != self.color:
                            move_list.append((currcol - 1, currrow + 1))

            else:
                if self.first_movement:
                    if currrow > 0:
                        j = board[currrow - 2][currcol]
                        if j == 0:
                            move_list.append((currcol, currrow - 2))

                if currrow > 0:
                    j = board[currrow - 1][currcol]
                    if j == 0:
                        move_list.append((currcol, currrow - 1))

                # Diagonal attacks
                # Right attack
                if currcol < 7:
                    j = board[currrow - 1][currcol + 1]
                    if j != 0:
                        if j.color != self.color:
                            move_list.append((currcol + 1, currrow - 1))

                # Left attack
                if currcol > 0:
                    j = board[currrow - 1][currcol - 1]
                    if j != 0:
                        if j.color != self.color:
                            move_list.append((currcol - 1, currrow - 1))
        except IndexError:
            pass

        return move_list


class King(ChessPieces):
    index = 1

    def __init__(self, rows, columns, color):
        super().__init__(rows, columns, color)
        self.king = True

    def move_valid(self, board):
        currrow = self.row
        currcol = self.column

        move_list = []

        if currrow > 0:
            # Top Left Movement
            if currcol > 0:
                j = board[currrow - 1][currcol - 1]
                if j == 0:
                    move_list.append((currcol - 1, currrow - 1))
                elif j.color != self.color:
                    move_list.append((currcol - 1, currrow - 1))

            # Top Middle Movement
            j = board[currrow - 1][currcol]
            if j == 0:
                move_list.append((currcol, currrow - 1))
            elif j.color != self.color:
                move_list.append((currcol, currrow - 1))

            # Top Right
            if currcol < 7:
                j = board[currrow - 1][currcol + 1]
                if j == 0:
                    move_list.append((currcol + 1, currrow - 1))
                elif j.color != self.color:
                    move_list.append((currcol + 1, currrow - 1))

        if currrow < 7:
            # Bottom Left
            if currcol > 0:
                j = board[currrow + 1][currcol - 1]
                if j == 0:
                    move_list.append((currcol - 1, currrow + 1))
                elif j.color != self.color:
                    move_list.append((currcol - 1, currrow + 1))

            # Bottom Middle
            j = board[currrow + 1][currcol]
            if j == 0:
                move_list.append((currcol, currrow + 1))
            elif j.color != self.color:
                move_list.append((currcol, currrow + 1))

            # Bottom Right
            if currcol < 7:
                j = board[currrow + 1][currcol + 1]
                if j == 0:
                    move_list.append((currcol + 1, currrow + 1))
                elif j.color != self.color:
                    move_list.append((currcol + 1, currrow + 1))

        # Middle Left
        if currcol > 0:
            j = board[currrow][currcol - 1]
            if j == 0:
                move_list.append((currcol - 1, currrow))
            elif j.color != self.color:
                move_list.append((currcol - 1, currrow))

        # Middle Right
        if currcol < 7:
            j = board[currrow][currcol + 1]
            if j == 0:
                move_list.append((currcol + 1, currrow))
            elif j.color != self.color:
                move_list.append((currcol + 1, currrow))


        return move_list


class Queen(ChessPieces):
    index = 4

    def move_valid(self, board):
        currrow = self.row
        currcol = self.column

        move = []

        # Top Right Move
        dial = currcol + 1
        diar = currcol - 1
        for i in range(currrow - 1, -1, -1):
            if dial < 8:
                j = board[i][dial]
                if j == 0:
                    move.append((dial, i))
                elif j.color != self.color:
                    move.append((dial, i))
                    break
                else:
                    dial = 9

            dial += 1

        for i in range(currrow - 1, -1, -1):
            if diar > -1:
                j = board[i][diar]
                if j == 0:
                    move.append((diar, i))
                elif j.color != self.color:
                    move.append((diar, i))
                    break
                else:
                    diar = -1

            diar -= 1

        # Top Left Move
        dial = currcol + 1
        diar = currcol - 1
        for i in range(currrow + 1, 8):
            if dial < 8:
                j = board[i][dial]
                if j == 0:
                    move.append((dial, i))
                elif j.color != self.color:
                    move.append((dial, i))
                    break
                else:
                    dial = 9
            dial += 1
        for i in range(currrow + 1, 8):
            if diar > -1:
                j = board[i][diar]
                if j == 0:
                    move.append((diar, i))
                elif j.color != self.color:
                    move.append((diar, i))
                    break
                else:
                    diar = -1

            diar -= 1

        # Up Movement
        for x in range(currrow - 1, -1, -1):
            j = board[x][currcol]
            if j == 0:
                move.append((currcol, x))
            elif j.color != self.color:
                move.append((currcol, x))
                break
            else:
                break

        # Down Movement
        for x in range(currrow + 1, 8, 1):
            j = board[x][currcol]
            if j == 0:
                move.append((currcol, x))
            elif j.color != self.color:
                move.append((currcol, x))
                break
            else:
                break

        # Left Movement
        for x in range(currcol - 1, -1, -1):
            j = board[currrow][x]
            if j == 0:
                move.append((x, currrow))
            elif j.color != self.color:
                move.append((x, currrow))
                break
            else:
                break

        # Right Movement
        for x in range(currcol + 1, 8, 1):
            j = board[currrow][x]
            if j == 0:
                move.append((x, currrow))
            elif j.color != self.color:
                move.append((x, currrow))
                break
            else:
                break

        return move


class Rook(ChessPieces):
    index = 5

    def move_valid(self, board):
        currrow = self.row
        currcol = self.column

        move_list = []

        # Up
        for x in range(currrow - 1, -1, -1):
            j = board[x][currcol]
            if j == 0:
                move_list.append((currcol,x))
            elif j.color != self.color:
                move_list.append((currcol,x))
                break
            else:
                break

        # Down
        for x in range(currrow + 1, 8, 1):
            j = board[x][currcol]
            if j == 0:
                move_list.append((currcol,x))
            elif j.color != self.color:
                move_list.append((currcol,x))
                break
            else:
                break

        # Left
        for x in range(currcol - 1, -1, -1):
            j = board[currrow][x]
            if j == 0:
                move_list.append((x,currrow))
            elif j.color != self.color:
                move_list.append((x,currrow))
                break
            else:
                break

        # Right
        for x in range(currcol + 1, 8, 1):
            j = board[currrow][x]
            if j == 0:
                move_list.append((x,currrow))
            elif j.color != self.color:
                move_list.append((x,currrow))
                break
            else:
                break

        return move_list


class Knight(ChessPieces):
    index = 2

    def move_valid(self, board):
        currrow = self.row
        currcol = self.column

        move_list = []

        # Down Left
        if currrow < 6 and currcol > 0:
            j = board[currrow + 2][currcol - 1]
            if j == 0:
                move_list.append((currcol - 1, currrow + 2))
            elif j.color != self.color:
                move_list.append((currcol - 1, currrow + 2))

        # Up left
        if currrow > 1 and currcol > 0:
            j = board[currrow - 2][currcol - 1]
            if j == 0:
                move_list.append((currcol - 1, currrow - 2))
            elif j.color != self.color:
                move_list.append((currcol - 1, currrow - 2))

        # Down right
        if currrow < 6 and currcol < 7:
            j = board[currrow + 2][currcol + 1]
            if j == 0:
                move_list.append((currcol + 1, currrow + 2))
            elif j.color != self.color:
                move_list.append((currcol + 1, currrow + 2))

        # Up right
        if currrow > 1 and currcol < 7:
            j = board[currrow - 2][currcol + 1]
            if j == 0:
                move_list.append((currcol + 1, currrow - 2))
            elif j.color != self.color:
                move_list.append((currcol + 1, currrow - 2))

        if currrow > 0 and currcol > 1:
            j = board[currrow - 1][currcol - 2]
            if j == 0:
                move_list.append((currcol - 2, currrow - 1))
            elif j.color != self.color:
                move_list.append((currcol - 2, currrow - 1))

        if currrow > 0 and currcol < 6:
            j = board[currrow - 1][currcol + 2]
            if j == 0:
                move_list.append((currcol + 2, currrow - 1))
            elif j.color != self.color:
                move_list.append((currcol + 2, currrow - 1))

        if currrow < 7 and currcol > 1:
            j = board[currrow + 1][currcol - 2]
            if j == 0:
                move_list.append((currcol - 2, currrow + 1))
            elif j.color != self.color:
                move_list.append((currcol - 2, currrow + 1))

        if currrow < 7 and currcol < 6:
            j = board[currrow + 1][currcol + 2]
            if j == 0:
                move_list.append((currcol + 2, currrow + 1))
            elif j.color != self.color:
                move_list.append((currcol + 2, currrow + 1))

        return move_list

