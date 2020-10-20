"""Module for utelizing A* on a 2D grid"""

# Birk Brunell DVADS20h
# Estimerad tid 6h
# Faktisk tid 8h


import math
from grid import Occupation
from collections import defaultdict

def reconstruct_path(came_from, current):
    """Reconstructs the shortest path (there can be multiple paths of the same distance but the algorithm stops after finding 1)"""
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    print("Total Path: ", total_path)
    return total_path


def h_score(start, goal):
    """Calculates shortest possible theoretical path from given point (start) to the end (goal)"""
    # Manhattan distance
    #h_score = abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    # Euclidian distance
    h_score = math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)
    return h_score


def neighbors(current, grid):
    """Finds all four grid neighbors and checks if they are outside the grid or if they are BLOCKED"""
    # fixed grid size of 15
    grid_max = 14
    true_neighbors = []
    potential_neighbors = []

    # Finds all potential neighbors
    potential_neighbors.append(tuple([current[0] + 1, current[1]]))
    potential_neighbors.append(tuple([current[0], current[1] + 1]))
    potential_neighbors.append(tuple([current[0] - 1, current[1]]))
    potential_neighbors.append(tuple([current[0], current[1] - 1]))
    print(potential_neighbors)

    # Checks if they are allowed
    for potential_neighbor in potential_neighbors:
        if potential_neighbor[0] >= 0 and potential_neighbor[0] <= grid_max and potential_neighbor[1] >= 0 and potential_neighbor[1] <= grid_max:
            if grid[potential_neighbor[0]][potential_neighbor[1]] != Occupation.BLOCKED:
                true_neighbors.append(potential_neighbor)
    return true_neighbors


def a_star(grid, start, goal):
    """Function to calculate a path through a grid"""
    open_set = [start]
    came_from = {}
    
    g_score = defaultdict(lambda: math.inf)
    g_score[start] = 0    

    f_score = defaultdict(lambda: math.inf)
    f_score[start] = h_score(start, goal)
    
    # Runs as long as there exists unexplored paths
    while open_set:
        current = math.inf
        # Finds node with lowest f_score in open_set
        for node in open_set:
            f_score[node] = g_score[node] + h_score(node, goal)
            if f_score[node] < f_score[current]:
                current = node
    
        # Checks if goal has been reached
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        # Checks if new path to neighbors has lower g_score
        for neighbor in neighbors(current, grid):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h_score(neighbor, goal)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    # Open set is empty but goal was never reached
    return None