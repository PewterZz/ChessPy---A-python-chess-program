from MoveableUnitsandSprites import Bishop
from MoveableUnitsandSprites import King
from MoveableUnitsandSprites import Queen
from MoveableUnitsandSprites import Pawn
from MoveableUnitsandSprites import Knight
from MoveableUnitsandSprites import Rook
from MoveableUnitsandSprites import ChessPieces as x


class Chessboard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

        self.board = [[0 for _ in range(8)]for x in range(8)]


        # Positions of each piece on the board for black
        self.board[0][0] = Rook(0,0, "Black")
        self.board[0][1] = Knight(0,1, "Black")
        self.board[0][2] = Bishop(0,2, "Black")
        self.board[0][3] = Queen(0,3, "Black")
        self.board[0][4] = King(0,4, "Black")
        self.board[0][5] = Bishop(0,5, "Black")
        self.board[0][6] = Knight(0,6, "Black")
        self.board[0][7] = Rook(0,7, "Black")

        for _ in range(8):
            self.board[1][_] = Pawn(1, _, "Black")

        # for white
        self.board[7][0] = Rook(7, 0, "White")
        self.board[7][1] = Knight(7, 1, "White")
        self.board[7][2] = Bishop(7, 2, "White")
        self.board[7][3] = Queen(7, 3, "White")
        self.board[7][4] = King(7, 4, "White")
        self.board[7][5] = Bishop(7, 5, "White")
        self.board[7][6] = Knight(7, 6, "White")
        self.board[7][7] = Rook(7, 7, "White")

        for _ in range(8):
            self.board[6][_] = Pawn(6 , _, "White")

    def get_board(self):
        return self.board

    def draw(self, win, board):
        for _ in range(self.rows):
            for i in range(self.columns):
                if self.board[_][i] != 0:
                    self.board[_][i].border(win, board )

    # for determining the border select and selecting only one at a time
    def selectinboard(self, columns, rows):
        for _ in range(self.rows):
            for i in range(self.columns):
                if self.board[_][i] != 0:
                    # turns all positions in board as unselected
                    self.board[_][i].selected_piece = False
        if self.board[rows][columns] != 0:
            # turns singular piece in column and rows as selected
            self.board[rows][columns].selected_piece = True

    def updater(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].possible_moves(self.board)


    def reset(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].selected_piece = False

    def return_king_pos(self):
        Dboard = self.board[:]
        king_pos = []
        for x in range(self.rows):
            for _ in range(self.columns):
                try:
                    if Dboard[x][_].king:
                        king_pos.append((_,x))
                except:
                    continue
        return king_pos


    def do_move_chesspiece(self, org, end, turn, color, win):
        self.updater()
        condition = 1
        cBoard = self.board[:]
        try:
            king = 0
            if turn % 2 != 0 and color == x.get_color(self.board[org[0]][org[1]]):
                if (end[1],end[0]) in self.board[org[0]][org[1]].all_possible_movements_list and (org[0], org[1]) != (end[0], end[1]):
                    print('White Moved')
                    if cBoard[org[0]][org[1]].pawn:
                        cBoard[org[0]][org[1]].first_movement = False

                    if (end[1],end[0]) in self.board[org[0]][org[1]].all_possible_movements_list:
                        trueend = end
                        cBoard[org[0]][org[1]].move_pos((end[0], end[1]))
                        cBoard[end[0]][end[1]] = cBoard[org[0]][org[1]]
                        cBoard[org[0]][org[1]] = 0
                        self.updater()
                        king_pos = self.return_king_pos()
                        try:
                            if king_pos[0] in self.board[trueend[0]][trueend[1]].all_possible_movements_list or king_pos[1] in self.board[trueend[0]][trueend[1]].all_possible_movements_list:
                                king = 1
                            else:
                                king = 0
                        except:
                            condition = 0
                        if len(king_pos) < 2:
                            condition = 0
                        self.board = cBoard


                    else:
                        self.reset()

                    self.updater()

                    turn += 1
                    color = "Black"
                    return turn, color, king, condition

            elif turn % 2 == 0 and color == x.get_color(self.board[org[0]][org[1]]):
                if (end[1],end[0]) in self.board[org[0]][org[1]].all_possible_movements_list and (org[0], org[1]) != (end[0], end[1]):
                    print('Black Moved')
                    if cBoard[org[0]][org[1]].pawn:
                        cBoard[org[0]][org[1]].first_movement = False

                    if (end[1],end[0]) in self.board[org[0]][org[1]].all_possible_movements_list:
                        trueend = end
                        cBoard[org[0]][org[1]].move_pos((end[0], end[1]))
                        cBoard[end[0]][end[1]] = cBoard[org[0]][org[1]]
                        cBoard[org[0]][org[1]] = 0
                        self.updater()
                        king_pos = self.return_king_pos()
                        try:
                            if king_pos[0] in self.board[trueend[0]][trueend[1]].all_possible_movements_list or king_pos[1] in self.board[trueend[0]][trueend[1]].all_possible_movements_list:
                                king = 1
                            else:
                                king = 0
                        except:
                            condition = 0
                        if len(king_pos) < 2:
                            condition = 0
                        self.board = cBoard

                    else:
                        self.reset()

                    self.updater()

                    turn += 1
                    color = "White"
                    return turn, color, king, condition

            else:
                pass
            return turn, color, king, condition

        except AttributeError:
            pass
        except TypeError:
            pass
