# Day 11: Space Police
# https://adventofcode.com/2019/day/11

from util.IntCode import IntCode
from collections import defaultdict, deque

def read_input():
    with open("inputs/day11_input.txt") as f:
        lines = f.readlines()
    
    program = [int(x) for x in lines[0].split(',')]
    return program

# Robot needs to be able to move around the grid of square panels
# detect color of current panel
# paint its current panel black or white
# 
# all current panels are black

# Intcode Program
# output [color - b/w, direction - degrees right]
# always move forward one panel

# Robot starts facing up


BLACK = 0
WHITE = 1
TOP = 0
RIGHT = 1
BOT = 2
LEFT = 3
DIRS = {TOP: (1, 0), RIGHT: (0, 1), BOT: (-1, 0), LEFT: (0, -1)}

def turn(facing:int, turndirection:int) -> int:
    if turndirection == 0: # turn left
        return (facing - 1) % 4
    else: # turn right
        return (facing + 1) % 4
        
        
def move(facing:int, position:tuple) -> tuple:
    r, c = position
    dr, dc = DIRS[facing]
    return r+dr, c+dc
    
    
    
def part1():
    program = read_input()
    
    position = (0, 0)
    facing = TOP
    panel = defaultdict(int)
    
    # Start on black
    intcode = IntCode(program, [0])

    while intcode.is_ended() != True:
        intcode.run()
        outputs = intcode.get_outputs()
        if not outputs: break
        
        color = outputs.popleft()
        turndirection = outputs.popleft()
        
        # paint current panel
        panel[position] = color
        
        # turn and move
        facing = turn(facing, turndirection)
        position = move(facing, position)
        
        # get next panel color and put as input
        color = panel[position]
        intcode.add_inputs(color)
        
    print("Part 1:", len(panel))



def print_panel(panel:dict):
    # get boundaries first
    minrow = 0
    mincol = 0
    maxrow = 0
    maxcol = 0
    
    for r, c in panel:
        minrow = min(minrow, r)
        mincol = min(mincol, c)
        maxrow = max(maxrow, r)
        maxcol = max(maxcol, c)
        
    s = [] # list of chars, join later to string
    # Need to reverse rows to print right side up
    for r in range(maxrow, minrow-1, -1):
        for c in range(mincol, maxcol+1):
            if panel[(r, c)] == BLACK:
                s.append(u"\u2588") # solid block
            else:
                s.append(' ')
        s.append('\n')
    print(''.join(s))
    
    

    
def part2():
    program = read_input()
    
    position = (0, 0)
    facing = TOP
    panel = defaultdict(int)
    
    # Start on white
    intcode = IntCode(program, [1])

    while intcode.is_ended() != True:
        intcode.run()
        outputs = intcode.get_outputs()
        if not outputs: break
        
        color = outputs.popleft()
        turndirection = outputs.popleft()
        
        # paint current panel
        panel[position] = color
        
        # turn and move
        facing = turn(facing, turndirection)
        position = move(facing, position)
        
        # get next panel color and put as input
        color = panel[position]
        intcode.add_inputs(color)
        

    # Need to actually print the full panel now
    print("Part 2:")
    print_panel(panel)





if __name__ == '__main__':
    part1()
    part2()