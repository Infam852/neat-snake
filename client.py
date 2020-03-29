import pygame as pg
import os
import random
from settings import *
from main import *


# init pygame
pg.font.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Snake")


def main():
    clock = pg.time.Clock()
    board = Board(WIN_HEIGHT // TILE_SIZE, WIN_WIDTH // TILE_SIZE)
    direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
    snake = Snake(direction, *STARTING_POS)
    target = spawn_target(snake, [-1, -1], board.get_size()[0], board.get_size()[1])

    score = 0
    # snake.extend_body([STARTING_POS[0], STARTING_POS[1]-1])
    # set random starting direction
    last_distance = 100
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
                board.update_state(snake, target)
                board.print_board()
                a = (target.x - snake.body[0][0]) ** 2
                b = (target.y - snake.body[0][1]) ** 2
                distance = (a + b) ** 0.5
                head = snake.body[0]
                left = head[0] - 1, head[1]
                right = head[0] + 1, head[1]
                up = head[0], head[1] - 1
                down = head[0], head[1] + 1
                print((target.x, target.y), board[left], board[right], board[up], board[down])
                print(distance)
                if distance < last_distance:
                    print('closer')
                last_distance = distance
        # -------collision-------
        # head of snake with body
        if snake.collide(snake.body[0]):
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