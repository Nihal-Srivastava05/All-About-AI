from ursina import *
# from TicTacToeAgent import *
from TicTacToeWithAlphaBeta import *

if __name__ == '__main__':
    app = Ursina()

camera.orthographic = True
camera.fov = 4
camera.position = (1, 1)
Text.default_resolution *= 2

player = Entity(name='o', color=color.azure)
cursor = Tooltip(player.name, color=player.color, origin=(0,0), scale=4, enabled=True)
cursor.background.color = color.clear
mouse.visible = False

board = [[None for x in range(3)] for y in range(3)]

def get_position(loc):
    x, y = loc[0], loc[1]
    new_y = x
    new_x = 2 - y
    return (int(new_x), int(new_y))

def get_board_position(loc):
    x, y = loc[0], loc[1]
    new_x = y
    new_y = 2 - x
    return (int(new_x), int(new_y))

for y in range(3):
    for x in range(3):
        b = Button(parent=scene, position=(x,y))
        board[x][y] = b

        def on_click(b=b):
            b.text = 'o'
            b.color = color.azure
            b.collision = False

            loc = b.position
            pos = get_position(loc)
            ai_board[pos[0]][pos[1]] = 'o'

            ai_move = findBestMove(ai_board=ai_board)
            board_pos = get_board_position(ai_move)

            if(isMovesLeft(ai_board)):
                ai_b = Button(parent=scene, position=board_pos, text='x', color=color.orange)
                board[board_pos[0]][board_pos[1]] = ai_b
                ai_board[ai_move[0]][ai_move[1]] = 'x'

            check_for_victory()

        b.on_click = on_click


def check_for_victory():

    counter = 0
    for x in range(3):
        for y in range(3):
            if board[x][y].text == None:
                counter += 1
                break

    if(counter == 0):
        print('Draw')
        destroy(cursor)
        mouse.visible = True
        Panel(z=1, scale=10, model='quad')
        t = Text(f'Draw...', scale=3, origin=(0,0), background=True)
        t.create_background(padding=(.5,.25), radius=Text.size/2)
        t.background.color = color.yellow.tint(-.2)

    won_x = (
    (board[0][0].text == 'x' and board[1][0].text == 'x' and board[2][0].text == 'x') or # across the bottom
    (board[0][1].text == 'x' and board[1][1].text == 'x' and board[2][1].text == 'x') or # across the middle
    (board[0][2].text == 'x' and board[1][2].text == 'x' and board[2][2].text == 'x') or # across the top
    (board[0][0].text == 'x' and board[0][1].text == 'x' and board[0][2].text == 'x') or # down the left side
    (board[1][0].text == 'x' and board[1][1].text == 'x' and board[1][2].text == 'x') or # down the middle
    (board[2][0].text == 'x' and board[2][1].text == 'x' and board[2][2].text == 'x') or # down the right side
    (board[0][0].text == 'x' and board[1][1].text == 'x' and board[2][2].text == 'x') or # diagonal /
    (board[0][2].text == 'x' and board[1][1].text == 'x' and board[2][0].text == 'x'))   # diagonal \

    won_o = (
    (board[0][0].text == 'o' and board[1][0].text == 'o' and board[2][0].text == 'o') or # across the bottom
    (board[0][1].text == 'o' and board[1][1].text == 'o' and board[2][1].text == 'o') or # across the middle
    (board[0][2].text == 'o' and board[1][2].text == 'o' and board[2][2].text == 'o') or # across the top
    (board[0][0].text == 'o' and board[0][1].text == 'o' and board[0][2].text == 'o') or # down the left side
    (board[1][0].text == 'o' and board[1][1].text == 'o' and board[1][2].text == 'o') or # down the middle
    (board[2][0].text == 'o' and board[2][1].text == 'o' and board[2][2].text == 'o') or # down the right side
    (board[0][0].text == 'o' and board[1][1].text == 'o' and board[2][2].text == 'o') or # diagonal /
    (board[0][2].text == 'o' and board[1][1].text == 'o' and board[2][0].text == 'o'))  

    if won_x:
        print('winner is Computer')
        destroy(cursor)
        mouse.visible = True
        Panel(z=1, scale=10, model='quad')
        t = Text(f'player x won!', scale=3, origin=(0,0), background=True)
        t.create_background(padding=(.5,.25), radius=Text.size/2)
        t.background.color = color.orange.tint(-.2)
    
    if won_o:
        print('You beat the computer')
        destroy(cursor)
        mouse.visible = True
        Panel(z=1, scale=10, model='quad')
        t = Text(f'player o won!', scale=3, origin=(0,0), background=True)
        t.create_background(padding=(.5,.25), radius=Text.size/2)
        t.background.color = color.azure.tint(-.2)

if __name__ == '__main__':
    app.run()