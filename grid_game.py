"""Module for representing a simple game"""

import sys
import datetime
import pygame
from grid import Occupation
from grid import Grid
import a_star

def read_map_from_file(file_name, grid):
    """Function for reading a map from a file and creating a matching grid"""

    file = None

    try:
        file = open(file_name, 'r')
    except IOError:
        print("Could not open file:", file_name)
        return grid

    for i in range(0, 15):
        line = file.readline()
        for j in range(0, 15):
            char = line[j * 2]

            if char == 'B':
                grid.set_occupation_pos(Occupation.BLOCKED, j, i)
            elif char == 'S':
                grid.set_occupation_pos(Occupation.START, j, i)
            elif char == 'G':
                grid.set_occupation_pos(Occupation.GOAL, j, i)

    return grid



# pylint: disable=no-member
# Because pylint does not seemingly work with pygame

DONE = False
pygame.init()
SCREEN = pygame.display.set_mode((632, 632))
CLOCK = pygame.time.Clock()

BLOCKS_IN_WIDTH = 15
BLOCKS_IN_HEIGHT = 15

GRID = Grid(BLOCKS_IN_WIDTH, BLOCKS_IN_HEIGHT, 40, 40)

if len(sys.argv) > 1:
    GRID = read_map_from_file(sys.argv[1], GRID)


while not DONE:
    SCREEN.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            GRID.update_occupation()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            GRID.set_occupation(Occupation.BLOCKED)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            GRID.set_occupation(Occupation.NONE)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if GRID.get_start() == (-1, -1) or GRID.get_goal() == (-1, -1):
                print("Missing a start or a goal")
                continue

            start = GRID.get_start()
            start = (start[0], (BLOCKS_IN_HEIGHT - 1) - start[1])
            goal = GRID.get_goal()
            goal = (goal[0], (BLOCKS_IN_HEIGHT - 1) - goal[1])
            path = a_star.a_star(GRID.to_tuple(), start, goal)
            GRID.clear_paths()

            if path is not None:
                if (path[0][0], (BLOCKS_IN_HEIGHT - 1) - path[0][1]) == GRID.get_start():
                    path = path[1:]
                if (path[-1][0], (BLOCKS_IN_HEIGHT - 1) - path[-1][1]) == GRID.get_goal():
                    path = path[:-1]

                for x_position, y_position in path:
                    y_position = (BLOCKS_IN_HEIGHT - 1) - y_position
                    GRID.set_occupation_pos(Occupation.PATH, x_position, y_position)
                    GRID.render(SCREEN)
                    pygame.display.flip()
                    CLOCK.tick(10)
            else:
                print("Impossible to create path")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            GRID.clear_paths()

    GRID.render(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)

#GRID.write_to_file((str(datetime.datetime.now()) + " map.txt").replace(" ", "_").replace("-", "_").replace(":", "_"))
