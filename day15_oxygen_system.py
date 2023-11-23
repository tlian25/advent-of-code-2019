# Day 15. Oxygen System
# https://adventofcode.com/2019/day/15

import sys
from random import randint
from util.IntCode import IntCode
from collections import deque, defaultdict

def read_input():
    with open("inputs/day15_input.txt") as f:
        lines = f.readlines()
    return [int(x) for x in lines[0].split(',')]


# Loop forever
# accept movement command via input
# Send movement command to repair droid
# Wait for repair droid to finish movement operation
# Report on status of repair droid

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIR = {NORTH: (-1, 0), SOUTH: (1, 0), WEST: (0, -1), EAST: (0, 1)}

# Grid
DROID = 'X'
WALL = u"\u2588"
SPACE = '.'
OXYGEN = 'O'


# Status codes
BLOCKED = 0
STEP = 1
FOUND = 2


def print_grid(grid):
    minr, maxr, minc, maxc = 100000000, 0, 10000000, 0

    for r, c in grid:
        minr = min(minr, r)
        maxr = max(maxr, r)
        minc = min(minc, c)
        maxc = max(maxc, c)
    
    s = []
    for r in range(minr, maxr+1):
        for c in range(minc, maxc+1):
            if (r,c) not in grid:
                s.append(' ')
            elif (r,c) == (0,0):
                s.append(DROID)
            elif grid[(r,c)] == WALL:
                s.append(WALL)
            elif grid[(r,c)] == OXYGEN:
                s.append(OXYGEN)
            else:
                s.append(SPACE)
        s.append('\n')
    print(''.join(s))
                

def opposite_direction(dir):
    if dir == NORTH: return SOUTH
    if dir == SOUTH: return NORTH
    if dir == EAST: return WEST
    if dir == WEST: return EAST

def turn_right(dir):
    if dir == NORTH: return EAST 
    if dir == EAST: return SOUTH 
    if dir == SOUTH: return WEST 
    if dir == WEST: return NORTH 

def turn_left(dir):
    if dir == NORTH: return WEST 
    if dir == WEST: return SOUTH 
    if dir == SOUTH: return EAST 
    if dir == EAST: return NORTH 


def build_grid():
    program = read_input()
    intcode = IntCode(program)
    grid = {(0, 0): SPACE}
    seen = defaultdict(int)


    r = 0
    c = 0
    d = 1

    while True:
        print('\r', r, c, end='')
        seen[(r,c)] += 1
        if seen[(r,c)] > 5:
            break
        
        dr, dc = DIR[d]
        nr = r+dr
        nc = c+dc

        # move in direction
        intcode.add_inputs(d)
        intcode.run()
        res = intcode.pop_output()

        if res == BLOCKED:
            # position stays the same
            # record wall in direction
            grid[(nr, nc)] = WALL
            d = turn_right(d)
        else:
            if res == FOUND:
                grid[(nr, nc)] = FOUND
            else:
                grid[(nr, nc)] = SPACE
                
            r = nr
            c = nc
            d = turn_left(d)

    print()
    return grid


def shortest_path(grid):
    q = deque([(0, 0, 0)])
    seen = set()
    
    while q:
        r, c, steps = q.popleft()
        print('\r', r, c, end='')
        if (r,c) in grid and grid[(r,c)] == FOUND:
            return r, c, steps

        seen.add((r,c))
        for _, (dr, dc) in DIR.items():
            nr = r + dr
            nc = c + dc
            if (nr, nc) in grid and grid[(nr, nc)] != WALL:
                if (nr, nc) not in seen:
                    q.append((nr, nc, steps+1))
    return -1


def flood_fill(grid, r, c):
    q = deque([(r, c, 0)])
    maxt = 0
    while q:
        r, c, t = q.popleft()
        maxt = max(maxt, t)
        print('\r', r, c, end='')
        
        grid[(r,c)] = OXYGEN
        
        for _, (dr, dc) in DIR.items():
            nr = r + dr
            nc = c + dc
            if (nr, nc) in grid and grid[(nr, nc)] not in (WALL, OXYGEN):
                q.append((nr, nc, t+1))
    print()
    return maxt




def part1and2():
    
    grid = build_grid()
    print_grid(grid)
    
    ro, co, steps = shortest_path(grid)
    print()
    print("Part 1:", steps)

    maxt = flood_fill(grid, ro, co)
    print_grid(grid)
    print()
    
    print("Part 2:", maxt)
    

    
    
    
    
    
    

if __name__ == '__main__':
    part1and2()