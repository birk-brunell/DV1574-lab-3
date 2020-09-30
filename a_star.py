"""Module for utelizing A* on a 2D grid"""

import math
from grid import Occupation
from collections import defaultdict

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.Keys:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def h(start):

	return


def lowest_F_in_open_set(start):
	
	return


def neighbor(current):

	return

def a_star(grid, start, goal):
	"""Function to calculate a path through a grid"""
	# The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
	open_set = [start]

	# For node n, came_from[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

	# For node n, g_score[n] is the cost of the cheapest path from start to n currently known.
    g_score = defaultdict(lambda: math.inf)
    g_score[start] = 0      

	# For node n, f_score[n] = g_score[n] + h(n). f_score[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = defaultdict(lambda: math.inf)
    f_score[start] = h(start)

    while open_set
        # This operation can occur in O(1) time if open_set is a min-heap or a priority queue
        current = lowest_F_in_open_set():
        if current = goal
            return reconstruct_path(came_from, current)

        open_set.Remove(current)
        for neighbor(current)
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_g_score is the distance from start to the neighbor through current
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor)
                if neighbor not in open_set
                    open_set.add(neighbor)

    # Open set is empty but goal was never reached
    return None


def main():

	return


main()