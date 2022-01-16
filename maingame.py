import pygame
import os
import MoveableUnitsandSprites as p
import chessboard as bo
import time

# position of board disregarding background == (start x, start y, end x, end y)
game_field = (60, 60, 505, 505)


def game_window(king, color, turn):
    # puts all the board sprites along with the logo and madeby and the other pieces
    win.blit(p.chessboard, (0, 0))
    win.blit(p.chesspylogo, (230, -25))
    win.blit(p.madeby, (350, 580))
    b.draw(win, b.get_board())
    pygame.display.update()
    # used to display other sprites
    if king == 1:
        win.blit(check, (200, 565))
    if color == "White":
        win.blit(whiteturn, (60, 20))
    else:
        win.blit(blackturn, (60, 20))
    text = font.render(f"Turn : {turn}", True, white)
    win.blit(text, (490, 30))
    pygame.display.update()


# determine mouse position and which tile it is on
def select(pos):
    x = pos[0]
    y = pos[1]
    if game_field[0] < x < game_field[0] + game_field[2]:
        if game_field[1] < x < game_field[1] + game_field[3]:
            recX = x - game_field[0]
            recY = y - game_field[0]
            # int used to round the float value to an integer so it is accurate in which tile is being pressed
            u = int(recX / (game_field[2] / 8))
            i = int(recY / (game_field[3] / 8))
            return u, i


def main():
    global b
    color = "White"
    turn = 1

    # Chessboard object being made
    b = bo.Chessboard(8, 8)
    clock = pygame.time.Clock()
    king = -1
    condition = 1
    while True:

        # used to define the tickrate which determines the fps
        clock.tick(60)
        game_window(king, color, turn)

        for k in pygame.event.get():

            if k.type == pygame.QUIT:
                quit()
                pygame.quit()
                break

            if k.type == pygame.MOUSEMOTION:
                pass

            if k.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                if click[0]:
                    pes = pygame.mouse.get_pos()
                    try:
                        i, j = select(pes)
                        b.selectinboard(i, j)
                        g, d = i, j
                    except TypeError:
                        continue
                    except IndexError:
                        continue

            if k.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                # If click[2] is right click in pygame documentation
                if click[2]:
                    pos = pygame.mouse.get_pos()
                    try:
                        i, j = select(pos)
                        if i != g or j != d:
                            # moves the pieces
                            turn, color, king, condition = b.do_move_chesspiece((d, g), (j, i), turn, color, win)
                        else:
                            pass
                    except ValueError:
                        continue
                    except TypeError:
                        continue
                    except IndexError:
                        continue
                    except UnboundLocalError:
                        continue
                        
        if condition == 0:
            # the end of the game once the king is checkmated
            endgame = font.render("Checkmate", True, white)
            win.blit(pygame.transform.scale(endgame, (500, 300)), (60, 200))
            pygame.display.update()
            # delay
            time.sleep(5)
            quit()
            break


# dimensions of the window
width = 626
height = 626

# loading up some sprites
check = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "check.png")), (90, 60))
blackturn = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "blacks-turn.png")), (200, 38))
whiteturn = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "whites-turn.png")), (200, 38))
logo = pygame.transform.scale2x(pygame.image.load(os.path.join("Sprites", "ChesspyLogo1.png")))
pygame.display.set_icon(logo)
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("ChessPy")
white = (255, 255, 255)

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 16)

# starting screen for the program
while True:
    win.blit(p.woodboard, (0, 0))
    win.blit(pygame.transform.scale(p.chesspylogo, (650, 490)), (0, 0))
    text = font.render("click anywhere on the screen to continue", True, white)
    win.blit(text, (150, 350))
    pygame.display.update()
    start = pygame.event.poll()
    if start.type == pygame.MOUSEBUTTONDOWN:
        main()
        break
    elif start.type == pygame.QUIT:
        quit()
        pygame.quit()
        break
    else:
        continue



