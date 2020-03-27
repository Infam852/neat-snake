import pygame as pg
import neat
import time
import os
import random
from settings import *


# init pygame
pg.font.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Snake")


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
        return self._board[pos[0]][pos[1]]

    def __setitem__(self, key, value):
        x, y = key
        self._board[x][y] = value

    def get_size(self):
        return self._cols, self._rows

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
        # print('----draw-----')
        for x, y in self.body:
            # print(x, y)
            pg.draw.rect(win, GREEN, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # print('-----------')

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
    snake.draw(win)
    target.draw(win)

    pg.display.flip()


def main():
    clock = pg.time.Clock()
    board = Board(WIN_HEIGHT // TILE_SIZE, WIN_WIDTH // TILE_SIZE)
    direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
    snake = Snake(direction, *STARTING_POS)
    target = spawn_target(snake, [-1, -1], board.get_size()[0], board.get_size()[1])

    score = 0
    # snake.extend_body([STARTING_POS[0], STARTING_POS[1]-1])
    # set random starting direction

    running = True
    while running:
        clock.tick(FPS)

        # -------events-------
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()
            # WSAD movement
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    direction = DIR_UP
                if event.key == pg.K_d:
                    direction = DIR_RIGHT
                if event.key == pg.K_s:
                    direction = DIR_DOWN
                if event.key == pg.K_a:
                    direction = DIR_LEFT

        # -------update-------
        snake.move(direction)

        # -------collision-------
        # head of snake with body
        if snake.collide(snake.body[0]):
            print('collision with body')
            running = False

        # snake with target
        if target.collide(snake.body[0]):
            snake.extend_body()
            target = spawn_target(snake, [target.x, target.y], board.get_size()[0], board.get_size()[1])
            score += 1

        # check whether the snake is out of the map or not
        if snake.body[0][0] < 0 or snake.body[0][0] > GRID_TILES_X-1 or snake.body[0][1] < 0 or snake.body[0][1] > GRID_TILES_Y-1:
            running = False
        # --------draw--------
        draw_window(screen, board, snake, target)
        caption_txt = "Score: {}".format(str(score))
        pg.display.set_caption(caption_txt)


if __name__ == "__main__":
    main()
