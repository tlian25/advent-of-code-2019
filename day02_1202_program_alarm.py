# Day 2. 1202 Program Alaram
# https://adventofcode.com/2019/day/2

from util.IntCode import IntCode


def read_input():
    with open("inputs/day02_input.txt") as f:
        lines = f.readlines()
    
    program = [int(x) for x in lines[0].split(',')]
    return program




def part1():
    program = read_input()
    # replace idx 1 with 12
    # replace idx 2 with 2
    program[1] = 12
    program[2] = 2
    
    intcode = IntCode(program)

    intcode.run()
    
    print("Solution 1:", intcode.get(0))


def part2():
    program = read_input()
    TARGET = 19690720

    for noun in range(100):
        for verb in range(100):
            pg = program.copy()
            pg[1] = noun
            pg[2] = verb
            intcode = IntCode(pg)
            try:
                intcode.run()
                if intcode.get(0) == TARGET:
                    print("Solution 2:", noun, verb, 100 * noun + verb)
                    return
            except Exception as e:
                print(e)

            
if __name__ == '__main__':
    part1()
    part2()
    

    
        