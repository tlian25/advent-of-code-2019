# Day 13. Care Package
# https://adventofcode.com/2019/day/13

from util.IntCode import IntCode

def read_input():
    with open("inputs/day13_input.txt") as f:
        lines = f.readlines()
    
    return [int(x) for x in lines[0].split(',')]
    
# output = (x, y, tile)
# tiles
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

TILES = {EMPTY: ' ', WALL: '|', BLOCK: '#', PADDLE: 'X', BALL: 'O'}


def parse_outputs(outputs):
    i = 0
    tiles = []
    ballposition = None
    paddleposition = None
    blockcount = 0
    while i < len(outputs):
        x = outputs[i]
        y = outputs[i+1]
        t = outputs[i+2]
        tiles.append((x, y, t))
        i += 3

        if t == BALL: ballposition = (x, y)
        elif t == PADDLE: paddleposition = (x, y)
        elif t == BLOCK: blockcount += 1

    return tiles, ballposition, paddleposition, blockcount



def print_tiles(tiles):
    minx, maxx, miny, maxy = 0, 0, 0, 0
    grid = {}
    score = 0
    for x, y, t in tiles:
        if x == -1 and y == 0: 
            score = t
            continue
        
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
        grid[(x,y)] = t
        
    s = f'Score: {score}\n'
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            s += TILES[grid[(x,y)]]
        s += '\n'

    print(s)
            
    
    

def part1():
    program = read_input()
    intcode = IntCode(program)
    intcode.run()
    outputs = intcode.get_outputs()
    tiles, _, _, count = parse_outputs(outputs)

    print("Part 1:", count)
    # print_tiles(tiles)
    


def part2():
    program = read_input()
    # Set memory address 0
    program[0] = 2

    joystick = 0
    ball = None
    paddle = None
    intcode = IntCode(program)
    count = 1 # to start
    while count > 0:
        intcode.run()
        outputs = intcode.get_outputs()
        tiles, ball, paddle, count = parse_outputs(outputs)
        print_tiles(tiles)

        # move joystick based on positions
        if paddle[0] > ball[0]: joystick = -1
        elif paddle[0] < ball[0]: joystick = 1
        else: joystick = 0

        intcode.add_inputs(joystick)
    
    print(tiles)




if __name__ == '__main__':
    part1()
    part2()