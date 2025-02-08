# Day 16. Flawed Frequency Transmission
# https://adventofcode.com/2019/day/16

from tqdm import tqdm

def read_input():
    with open("inputs/day16_input.txt") as f:
        lines = f.readlines()
    return [int(x) for x in lines[0]]

# list of numbers
# repeated phases
# new list is constructed with the same length as input list
# new list used as input for the next phase

BASE_PATTERN = [0, 1, 0, -1]

class Pattern:
    def __init__(self):
        self.base = BASE_PATTERN
        self.repeat = 1
        self.counter = 0

    def reset(self, r):
        self.repeat = r
        self.counter = 0
    
    def next(self) -> int:
        self.counter += 1
        idx = (self.counter // self.repeat) % 4
        return self.base[idx]


        

# skip first value exactly once

def step(input, pattern):
    next_input = []
    
    for n in range(len(input)):
        pattern.reset(n+1)
        s = 0
        for i in input:
            s += i * pattern.next()

        # Take last digit
        s = abs(s) % 10
        next_input.append(s)

    return next_input




def part1():
    input = read_input()
    pattern = Pattern()
    
    # for r in [1, 2, 3, 4, 5]:
    #     pattern.reset(r)
    #     for _ in range(8):
    #         n = pattern.next()
    #         print(n, ' ', end='')
    #     print()

    for p in tqdm(range(100)):
        input = step(input, pattern)
    
    # return first 8 digits
    print("Part 1:", ''.join([str(x) for x in input[:8]]))


def part2():
    input = read_input()
    offset = int(''.join([str(x) for x in input[:7]]))
    print("Offset:", offset)

    # Repeat 10000 times
    input *= 10_000
        
    pattern = Pattern()

    for p in tqdm(range(100)):
        input = step(input, pattern)

    # return first 8 digits
    print("Part 1:", ''.join([str(x) for x in input[offset:offset+8]]))
    
    

if __name__ == '__main__':
    # part1()
    part2()
