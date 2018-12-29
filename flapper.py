from microbit import *
import random

# Suggestions for improvements:
## - Make the explosion animation prettier (maybe make it so the explosion
##   starts at the player position, instead of the middle of the screen)
## - Create a score counter that increases as you stay alive,
##   then display this as your score when you die
## - Better obstacle generation (right now it's just random positions,
##   but you could make it so it looks like you're flying through a cave)
## - Add a main menu
##   - Let the player choose a difficulty, which changes the value of `turn_ms`

# Constants
## These are specific values we want to give a name to.
## They should not be changed while the game is running!

## These are LED values, from 0 to 9.
## Make sure they are at least 1 and different from each other!
obstacle_brightness = 5
player_brightness = 9

## How many milliseconds one game turn should last.
turn_ms = 500

# State
## These are data that our game keeps track of and changes.
## We call it "state" since it's the current state of the game.

board = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

player_pos = 2

# Functions
## These functions are used by the game loop to change the game state.
## Most functions take and return a `board`, to make it easier to read
## our code, but when we need to change our state directly we use `global`
## followed by the variable name. We can then change the state from within
## a function.

def draw_screen(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            display.set_pixel(x, y, board[y][x])

def add_obstacle(board):
    x = random.randint(0, len(board)-1)
    new_line = [0, 0, 0, 0, 0]
    new_line[x] = obstacle_brightness
    new_board = [new_line]
    new_board += board[:-1]
    return new_board

def add_player(board, prev_pos):
    if player_pos == prev_pos: # The player did not move
        board[-1][player_pos] = player_brightness
        return board
    else:
        # Make sure that the prev_pos is not an obstacle before clearing it
        if board[-1][prev_pos] == player_brightness:
            board[-1][prev_pos] = 0
        board[-1][player_pos] = player_brightness
        return board

def update_player():
    global player_pos
    prev_pos = player_pos
    if button_a.was_pressed() and player_pos > 0:
        player_pos -= 1
    elif button_b.was_pressed() and player_pos < 4:
        player_pos += 1
    return prev_pos

def check_collision():
    has_collided = board[-1][player_pos] == obstacle_brightness
    return has_collided

def reset_board():
    global board
    board = [[0 for i in range(5)] for j in range(5)]

# Images

## Explosion animation when we die!

explode1 = Image("00000:"
                 "00000:"
                 "00900:"
                 "00000:"
                 "00000")
explode2 = Image("00000:"
                 "00700:"
                 "07970:"
                 "00700:"
                 "00000")
explode3 = Image("00700:"
                 "07970:"
                 "79797:"
                 "07970:"
                 "00700")
explode4 = Image("57775:"
                 "77777:"
                 "77577:"
                 "77777:"
                 "57775")
explode5 = Image("35555:"
                 "55555:"
                 "55355:"
                 "55555:"
                 "35553")
explode6 = Image("33333:"
                 "33333:"
                 "33133:"
                 "33333:"
                 "33333")
explode7 = Image("00100:"
                 "01110:"
                 "11011:"
                 "01110:"
                 "00100")

explosion = [explode1, explode2, explode3, explode4, explode5, explode6, explode7]

# Game loop
## Everything we need has now been defined, so we create a game loop that runs
## forever and edits the game state defined above, giving us a working game!

while True:
    prev_pos = update_player()
    board = add_obstacle(board)
    has_collided = check_collision()
    if has_collided: # The player has died!
        display.show(explosion, delay=50)
        display.clear()
        reset_board()
        sleep(2000)
        continue
    board = add_player(board, prev_pos)
    draw_screen(board)
    sleep(turn_ms)
