# Day 5. Sunny with a Chance of Asteroids
# https://adventofcode.com/2019/day/5

from util.IntCode import IntCode


def read_input():
    with open("inputs/day05_input.txt") as f:
        lines = f.readlines()
    
    program = [int(x) for x in lines[0].split(',')]
    return program




def part1():
    program = read_input()
    inputs = [1]
    
    intcode = IntCode(program)

    outputs = intcode.run(inputs)
    print("Solution 1:", outputs)
    
    
def part2():
    program = read_input()
    inputs = [5]
    
    intcode = IntCode(program)
    # intcode.log_enabled = True

    outputs = intcode.run(inputs)
    print("Solution 2:", outputs)



if __name__ == '__main__':
    part1()
    part2()