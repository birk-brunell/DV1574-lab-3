"""Module for renderable grids"""

from enum import Enum
import pygame

class Occupation(Enum):
    """Enum class for representing different states of squares in a grid"""
    NONE = 1
    GOAL = 2
    START = 3
    BLOCKED = 4
    PATH = 5


class Grid:
    """Class representing a grid in a game"""

    class Square:
        """Class representing a square in a grid"""
        # pylint: disable=too-many-instance-attributes

        def __init__(self, width=8, height=8, x_pos=0, y_pos=0):
            self.__inner_width = width
            self.__inner_height = height
            self.__border_size = 2
            self.__top = y_pos
            self.__left = x_pos
            self.__border_rect = pygame.Rect(self.__left, self.__top,
                                             self.__inner_width + self.__border_size,
                                             self.__inner_height + self.__border_size)
            self.__inner_rect = pygame.Rect(self.__left + self.__border_size,
                                            self.__top + self.__border_size,
                                            self.__inner_width, self.__inner_height)
            self.__occupied = Occupation.NONE
            self.__red = 255
            self.__green = 255
            self.__blue = 255

        def render(self, screen):
            """Function to render the square"""
            pygame.draw.rect(screen, (0, 0, 0), self.__border_rect)
            pygame.draw.rect(screen, (self.__red, self.__green, self.__blue), self.__inner_rect)

        def set_colour(self, red, green, blue):
            """Function to set the colour of the square"""
            self.__red = red
            self.__green = green
            self.__blue = blue

        def set_occupation(self, value):
            """Function to set the occupation status of the square"""
            self.__occupied = value
            if self.__occupied == Occupation.NONE:
                self.__red, self.__green, self.__blue = 255, 255, 255
            elif self.__occupied == Occupation.GOAL:
                self.__red, self.__green, self.__blue = 0, 0, 255
            elif self.__occupied == Occupation.START:
                self.__red, self.__green, self.__blue = 0, 255, 0
            elif self.__occupied == Occupation.BLOCKED:
                self.__red, self.__green, self.__blue = 255, 0, 0
            elif self.__occupied == Occupation.PATH:
                self.__red, self.__green, self.__blue = 255, 255, 0

        def get_occupation(self):
            """Function to get the occupation type of the square"""
            return self.__occupied

        def check_intersection(self, x_pos, y_pos):
            """Function to see if a point intersects the square"""
            right_edge = self.__left + self.__inner_width + self.__border_size
            if self.__left <= x_pos <= right_edge:
                bottom_edge = self.__top + self.__inner_height + self.__border_size
                if self.__top <= y_pos <= bottom_edge:
                    return True
            return False

        def toggle_occupation(self):
            """Function to handle the square getting clicked on"""
            if self.__occupied == Occupation.NONE:
                self.set_occupation(Occupation.GOAL)
            elif self.__occupied == Occupation.GOAL:
                self.set_occupation(Occupation.START)
            elif self.__occupied == Occupation.START:
                self.set_occupation(Occupation.BLOCKED)
            else:
                self.set_occupation(Occupation.NONE)

        def get_coordinates(self):
            """Function to return the coordinates as in which square in the grid it is"""
            return (int(self.__left / (self.__inner_width + self.__border_size)),
                    int(self.__top / (self.__inner_height + self.__border_size)))


    def __init__(self, grid_width=10, grid_height=10, square_width=8, square_height=8):
        self.__width = grid_width
        self.__height = grid_height
        self.__goal = (-1, -1)
        self.__start = (-1, -1)
        self.__squares = []
        self.__square_border_size = 2
        for x_pos in range(self.__width):
            self.__squares.append([])
            for y_pos in range(self.__height):
                self.__squares[x_pos].append(Grid.Square(square_width, square_height,
                                                         x_pos*(square_width + self.__square_border_size),
                                                         y_pos*(square_height + self.__square_border_size)
                                                        ))

    def render(self, screen):
        """Function to render the grid"""
        for x_pos in range(self.__width):
            for y_pos in range(self.__height):
                self.__squares[x_pos][y_pos].render(screen)

    def __reset_start(self, new_x, new_y):
        if self.__start[0] >= 0 and self.__squares[self.__start[0]][self.__start[1]].get_occupation() == Occupation.START:
            self.__squares[self.__start[0]][self.__start[1]].set_occupation(Occupation.NONE)
        self.__start = (new_x, new_y)

    def __reset_goal(self, new_x, new_y):
        if self.__goal[0] >= 0 and self.__squares[self.__goal[0]][self.__goal[1]].get_occupation() == Occupation.GOAL:
            self.__squares[self.__goal[0]][self.__goal[1]].set_occupation(Occupation.NONE)
        self.__goal = (new_x, new_y)

    def set_occupation(self, value):
        """Function to set the occupation type of a square in the grid based on mouse pos"""
        for column in self.__squares:
            for square in column:
                if square.check_intersection(*(pygame.mouse.get_pos())):
                    if value == Occupation.START:
                        self.__reset_start(*square.get_coordinates())
                    elif value == Occupation.GOAL:
                        self.__reset_goal(*square.get_coordinates())

                    if square.get_occupation() == Occupation.START:
                        self.__reset_start(-1, -1)
                    elif square.get_occupation() == Occupation.GOAL:
                        self.__reset_goal(-1, -1)

                    square.set_occupation(value)

                    return

    def set_occupation_pos(self, value, x_pos, y_pos):
        """Function to set the occupation type of a square in the grid"""
        if value == Occupation.START:
            self.__reset_start(x_pos, y_pos)
        elif value == Occupation.GOAL:
            self.__reset_goal(x_pos, y_pos)

        if self.__squares[x_pos][y_pos].get_occupation() == Occupation.START:
            self.__reset_start(-1, -1)
        elif self.__squares[x_pos][y_pos].get_occupation() == Occupation.GOAL:
            self.__reset_goal(-1, -1)

        self.__squares[x_pos][y_pos].set_occupation(value)

    def update_occupation(self):
        """Function to update squares"""
        for column in self.__squares:
            for square in column:
                if square.check_intersection(*(pygame.mouse.get_pos())):
                    if square.get_occupation() == Occupation.START:
                        self.__start = (-1, -1)
                    elif square.get_occupation() == Occupation.GOAL:
                        self.__goal = (-1, -1)

                    square.toggle_occupation()

                    if square.get_occupation() == Occupation.START:
                        self.__reset_start(*square.get_coordinates())
                    elif square.get_occupation() == Occupation.GOAL:
                        self.__reset_goal(*square.get_coordinates())

                    return

    def to_tuple(self):
        """Function to generate a tuple version of the map, reversed to match standard"""
        return tuple(tuple(square.get_occupation() for square in reversed(column))
                     for column in self.__squares)

    def clear_paths(self):
        """Function to turn any path squares currently in the grid to none squares"""
        for column in self.__squares:
            for square in column:
                if square.get_occupation() == Occupation.PATH:
                    square.set_occupation(Occupation.NONE)

    def get_start(self):
        """Function to return the start pos"""
        return self.__start

    def get_goal(self):
        """Function to return the goal pos"""
        return self.__goal

    def write_to_file(self, file_name):
        """Function to write the current map to a file"""

        file = open(file_name, "w")
        grid_map = ""

        for y in range(0, self.__height):
            for x in range(0, self.__width):
                to_write = "N "

                if self.__squares[x][y].get_occupation() == Occupation.START:
                    to_write = "S "
                elif self.__squares[x][y].get_occupation() == Occupation.GOAL:
                    to_write = "G "
                elif self.__squares[x][y].get_occupation() == Occupation.BLOCKED:
                    to_write = "B "

                grid_map += to_write

            grid_map = grid_map[:-1] + "\n"

        file.write(grid_map[:-1])