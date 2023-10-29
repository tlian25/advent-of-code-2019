# Day 7. Amplification Circuit
# https://adventofcode.com/2019/day/7

from util.IntCode import IntCode
from itertools import permutations
from collections import deque


def read_input():
    with open("inputs/day07_input.txt") as f:
        lines = f.readlines()
    
    program = [int(x) for x in lines[0].split(',')]
    return program

    
def part1():
    program = read_input()
    
    mxoutput = 0
    for comb in permutations(range(5), 5):
        comb = deque(comb)
        
        inp = 0
        while comb:
            pg = program.copy()
            intcode = IntCode(pg)
            intcode.add_inputs(comb.popleft(), inp)
            intcode.run()
            inp = intcode.outputs[0]
            
        mxoutput = max(mxoutput, inp)
    
    print("Solution 1:", mxoutput)
        

def part2():
    program = read_input()
    
    intcodes = []
    for _ in range(5):
        pg = program.copy()
        intcodes.append(IntCode(pg))

    
    mxoutput = 0
    for comb in permutations(range(5, 10), 5):
        
        # Set up intcodes for first input
        intcodes = []
        for i in range(5):
            pg = program.copy()
            intcode = IntCode(pg)
            intcode.add_inputs(comb[i])
            intcodes.append(intcode)
        
        idx = 0
        inp = 0
        ended = set()
        while len(ended) < 5:
            if idx in ended:
                idx = (idx + 1) % 5
                continue
            
            intcode = intcodes[idx]
            intcode.add_inputs(inp)
            # If run ended, then we can skip in later runs
            if intcode.run(): ended.add(idx)
            
            # get output and set as next input
            inp = intcode.get_outputs().popleft()
            idx = (idx + 1) % 5

        mxoutput = max(mxoutput, inp)
        
    print("Solution 2:", mxoutput)
 

if __name__ == '__main__':
    part1()
    part2()