# Day 9. Sensor Boost
# https://adventofcode.com/2019/day/9

from util.IntCode import IntCode
from itertools import permutations
from collections import deque


def read_input():
    with open("inputs/day09_input.txt") as f:
        lines = f.readlines()
    
    program = [int(x) for x in lines[0].split(',')]
    return program

# Support relative mode
# relative base - starts at 0
# itself + current relative base
# relative base offset
# 9 - adjusts relative base by value of its only parameter


def part1():
    program = read_input()
    
    intCode = IntCode(program, [1])
    # intCode.log_enabled = True
    intCode.run()
    
    print(intCode.get_outputs())
    
    
def part2():
    program = read_input()
    
    intCode = IntCode(program, [2])
    # intCode.log_enabled = True
    intCode.run()
    
    print(intCode.get_outputs())
    
    
    
if __name__ == '__main__':
    part1()
    part2()