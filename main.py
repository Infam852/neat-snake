import pygame as pg
import neat
import time
import os
import random
from settings import *


class Board:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self.tile_size = TILE_SIZE
        self._board = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, win):
        for row in range(self._rows):
            pg.draw.line(win, LIGHT_GRAY, (0, row * TILE_SIZE), (WIN_WIDTH, row * TILE_SIZE))
        for col in range(self._cols):
            pg.draw.line(win, LIGHT_GRAY, (col * TILE_SIZE, 0), (col * TILE_SIZE, WIN_HEIGHT))

    def __getitem__(self, pos):
        """ Returns pixel coordinates of the position x, y on the board """
        # print(pos)
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= GRID_TILES_X or pos[1] >= GRID_TILES_Y:
            state = WALL
        else:
            state = self._board[pos[0]][pos[1]]
        return state

    def __setitem__(self, key, value):
        x, y = key
        self._board[x][y] = value

    def get_size(self):
        return self._cols, self._rows

    def update_state(self, snake, target):
        """ Create map that marks position of the snake and target """
        self._board = self.get_clear_board()
        try:
            for x, y in snake.body:
                self[x, y] = SNAKE
        except IndexError:
            pass

        self[target.x, target.y] = TARGET
        # print(self)

    def get_clear_board(self):
        return [[0 for _ in range(self._cols)] for _ in range(self._rows)]

    def print_board(self):
        for y in range(len(self._board)):
            for x in range(len(self._board[0])):
                print(self[[x, y]], end="")
            print()
        print('---')


class Snake:
    def __init__(self, direction, x, y):
        self.x = x
        self.y = y
        self.body = [[x, y]]    # head will be body[0]
        self.direction = direction
        self.last_position = []
        self.head = self.body[0]

    def draw(self, win):
        k = 0
        for x, y in self.body:
            if k == 0:
                pg.draw.rect(win, GREEN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pg.draw.rect(win, DARK_GREEN, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            k += 1

    def move(self, dir):
        # check if new direction is not opposite to actual direction
        if self.direction == -dir:
            dir = self.direction
        else:
            self.direction = dir

        new_head = list(self.body[0])       # initialize new list
        # move head
        if dir == DIR_UP:
            new_head[1] -= 1
        elif dir == DIR_DOWN:
            new_head[1] += 1
        elif dir == DIR_RIGHT:
            new_head[0] += 1
        elif dir == DIR_LEFT:
            new_head[0] -= 1

        # keep track of position in the previous frame
        self.last_position = list(self.body[-1])

        # move the rest of the body
        for k in range(len(self)-1, 0, -1):
            # print("MOVE: ", self.body[k], self.body[k-1])
            self.body[k] = self.body[k-1]

        self.body[0] = new_head

    def extend_body(self):
        self.body.append(self.last_position)

    def collide(self, other, head_exlude=1):
        """ Check collision with the snake, you can set to not to check collision with the head """

        for xb, yb in self.body[head_exlude:]:
            if xb == other[0] and yb == other[1]:
                return True
        return False

    def __len__(self):
        return len(self.body)


class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pg.draw.rect(win, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def collide(self, other):
        if other[0] == self.x and other[1] == self.y:
            return True


def spawn_target(snake, target, max_x, max_y):
    """ Spawn target on an empty field """
    # max_x, max_y = board.get_size()
    is_empty = False
    x, y = -1, -1
    while not is_empty:
        is_empty = True
        x = random.randint(0, max_x - 1)
        y = random.randint(0, max_y - 1)

        if target[0] == x and target[1] == y:
            continue

        for xb, yb in snake.body:
            if xb == x and yb == y:
                is_empty = False

        if is_empty:
            break

    return Target(x, y)


def get_coordinates(pos):
    """ Returns pixel coordinates """
    return pos[0] * TILE_SIZE, pos[1] * TILE_SIZE


def draw_window(win, board, snake, target):
    """ Draw all objects onto windows surface """
    win.fill(BLACK)
    board.draw(win)
    # for snake in snakes:
    snake.draw(win)
    target.draw(win)

    pg.display.flip()






