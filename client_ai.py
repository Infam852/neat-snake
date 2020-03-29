import pygame as pg
import os
import random
from settings import *
from main import *
import operator


# init pygame
pg.font.init()
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Snake")


def eval_genomes(genomes, config):
    clock = pg.time.Clock()
    board = Board(WIN_HEIGHT // TILE_SIZE, WIN_WIDTH // TILE_SIZE)
    direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])

    snakes = []
    targets = []
    nets = []
    ge = []
    boards = []
    last_distances = []
    lifetimes = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)

        snake = Snake(direction, *STARTING_POS)
        snakes.append(snake)

        g.fitness = 0
        ge.append(g)

        board = Board(WIN_HEIGHT // TILE_SIZE, WIN_WIDTH // TILE_SIZE)
        boards.append(board)
        targets.append(spawn_target(snake, [-1, -1], board.get_size()[0], board.get_size()[1]))
        last_distances.append(LARGE_DIST)

        lifetimes.append(200)

    score = 0

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

        # update board state

        # -------update-------
        for k, snake in enumerate(snakes):
            # inputs: snake adjacent fields (empty or not and distance to the target - fields have to be simple types)
            head = snake.body[0]
            left = head[0] - 1, head[1]
            right = head[0] + 1, head[1]
            up = head[0], head[1] - 1
            down = head[0], head[1] + 1
            # print((targets[k].x, targets[k].y), left, right, up, down)
            a = (targets[k].x - snake.body[0][0])**2
            b = (targets[k].y - snake.body[0][1])**2
            distance = (a + b)**0.5
            output = nets[k].activate((distance, boards[k][left], boards[k][right], boards[k][up], boards[k][down]))
            # output = nets[k].activate((boards[k][left], boards[k][right], boards[k][up], boards[k][down]))
            index, value = max(enumerate(output), key=operator.itemgetter(1))
            if index == 0:
                direction = DIR_LEFT
            elif index == 1:
                direction = DIR_DOWN
            elif index == 2:
                direction = DIR_RIGHT
            elif index == 3:
                direction = DIR_UP

            snake.move(direction)
            # closer to target - get better score (not always true)
            if distance < last_distances[k]:
                ge[k].fitness += 0.3
                # print('closer')
                # lifetimes[k] += 1
            # else:
            #     ge[k].fitness -= 0.5

            last_distances[k] = distance

        for k, board in enumerate(boards):
            board.update_state(snakes[k], targets[k])

        # -------collision-------
        # head of snake with body
        for snake in snakes:
            idx = snakes.index(snake)
            if snake.collide(snake.body[0]):
                pop_snake(snake, snakes, nets, boards, ge, lifetimes)

            # snake with target
            elif targets[idx].collide(snake.body[0]):
                snake.extend_body()
                target = spawn_target(snake, [targets[idx].x, targets[idx].y], board.get_size()[0], board.get_size()[1])
                targets[idx] = target
                score += 1
                ge[idx].fitness += 100
                lifetimes[idx] += 100

        # check whether the snake is out of the map or not
            elif snake.body[0][0] < 0 or snake.body[0][0] > GRID_TILES_X-1 or snake.body[0][1] < 0 or snake.body[0][1] > GRID_TILES_Y-1:
                pop_snake(snake, snakes, nets, boards, ge, lifetimes)

        for k, snake in enumerate(snakes):
            # print(lifetimes)
            lifetimes[snakes.index(snake)] -= 1
            if lifetimes[snakes.index(snake)] <= 0:
                print("------------- lifetime ends -----------")
                ge[snakes.index(snake)].fitness -= 300
                pop_snake(snake, snakes, nets, boards, ge, lifetimes)

        # --------draw--------
        if not len(snakes):
            break

        draw_window(screen, boards[0], snakes[0], targets[0])
        # caption_txt = "Score: {}".format(str(score))
        # pg.display.set_caption(caption_txt)


def eval_genomes2(genomes, config):
    clock = pg.time.Clock()
    direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        snake = Snake(direction, *STARTING_POS)
        g.fitness = 0
        board = Board(WIN_HEIGHT // TILE_SIZE, WIN_WIDTH // TILE_SIZE)
        target = spawn_target(snake, [-1, -1], board.get_size()[0], board.get_size()[1])
        last_distance = LARGE_DIST
        lifetime = 200


    # set random starting direction

        while True:
            clock.tick(FPS)

            # -------events-------
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            # decide where to go
            # head = snake.body[0]
            # left = head[0] - 1, head[1]
            # right = head[0] + 1, head[1]
            # up = head[0], head[1] - 1
            # down = head[0], head[1] + 1
            head = snake.body[0]
            x = head[0]
            y = head[1]
            left_wall = euclidean_distance(x, 0, y, y)
            up_wall = euclidean_distance(x, x, y, 0)
            right_wall = euclidean_distance(x, GRID_TILES_X - 1, y, y)
            down_wall = euclidean_distance(x, x, y, GRID_TILES_Y - 1)
            on_line = int(target_on_line(x, y, target.x , target.y))

            # print((targets[k].x, targets[k].y), left, right, up, down)
            a = (target.x - snake.body[0][0]) ** 2
            b = (target.y - snake.body[0][1]) ** 2
            distance = (a + b) ** 0.5
            # output = net.activate((distance, board[left], board[right], board[up], board[down]))
            output = net.activate((distance, left_wall, up_wall, right_wall, down_wall, on_line))

            index, value = max(enumerate(output), key=operator.itemgetter(1))
            if index == 0:
                direction = DIR_LEFT
            elif index == 1:
                direction = DIR_DOWN
            elif index == 2:
                direction = DIR_RIGHT
            elif index == 3:
                direction = DIR_UP

            snake.move(direction)

            if distance < last_distance:
                g.fitness += 0.1

            last_distance = distance

            board.update_state(snake, target)

            if snake.collide(snake.body[0]):
                g.fitness -= 20
                break

            # snake with target
            elif target.collide(snake.body[0]):
                snake.extend_body()
                target = spawn_target(snake, [target.x, target.y], board.get_size()[0], board.get_size()[1])
                g.fitness += 70
                lifetime += 100

            # check whether the snake is out of the map or not
            elif snake.body[0][0] < 0 or snake.body[0][0] > GRID_TILES_X - 1 or snake.body[0][1] < 0 or snake.body[0][
                1] > GRID_TILES_Y - 1:
                g.fitness -= 20
                break
            if target_on_line(snake.head[0], snake.head[1], target.x, target.y):
                g.fitness += 5

            lifetime -= 1
            if lifetime <= 0:
                print("------------- lifetime ends -----------")
                g.fitness -= 100
                break

            draw_window(screen, board, snake, target)

        # caption_txt = "Score: {}".format(str(score))
        # pg.display.set_caption(caption_txt)


def distance_to_walls(x, y):
    left_wall = euclidean_distance(x, 0, y, y)
    up_wall = euclidean_distance(x, x, y, 0)
    right_wall = euclidean_distance(x, GRID_TILES_X-1, y, y)
    down_wall = euclidean_distance(x, x, y, GRID_TILES_Y-1)


def target_on_line(x, y, xt, yt):
    if x == xt or y == yt:
        return True
    return False

def euclidean_distance(x1, x2, y1, y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def pop_snake(snake, snakes, nets, boards, ge, lifetimes):
    idx = snakes.index(snake)
    ge[idx].fitness -= 50
    snakes.pop(idx)
    boards.pop(idx)
    nets.pop(idx)
    ge.pop(idx)
    lifetimes.pop(idx)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    # population is top-level object for NEAT run
    p = neat.Population(config)

    # add reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run for 50 generations, it will run until at least one genome achieves
    # the fitness_threshold or 50 generations is pass
    winner = p.run(eval_genomes, 100)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    run(config_path)