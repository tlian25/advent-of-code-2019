# Day 10. Monitoring Station
# https://adventofcode.com/2019/day/10D

from collections import defaultdict

def read_input():
    grid = []
    with open('inputs/day10_input.txt') as f:
        lines = f.readlines()
        for l in lines:
            grid.append(list(l.replace('\n', '')))
        
    return grid


ASTEROID = '#'
SPACE = '.'

INF = float('inf')

def calc_slope(r1, c1, r2, c2):
    if (c2-c1) == 0: return INF
    return -1 * (r2-r1) / (c2-c1)

def calc_dist(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def get_asteroids(grid):
    asteroids = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == ASTEROID:
                asteroids.append((r, c))
                
    return asteroids


def buildSeen(r, c, asteroids):
    right = defaultdict(list)
    left = defaultdict(list)
    above = defaultdict(list)
    below = defaultdict(list)
    
    for r1, c1 in asteroids:
        slope = calc_slope(r, c, r1, c1)
        if (r == r1 and c == c1):
            continue
        elif (c == c1 and r > r1):
            above[slope].append((r1, c1))
        elif (c == c1 and r < r1):
            below[slope].append((r1, c1))
        elif (c1 > c):
            right[slope].append((r1, c1))
        elif (c1 < c):
            left[slope].append((r1, c1))
        else:
            raise ValueError(f"Unknown case - {r} - {c} - {r1} - {c1}")


    return right, left, above, below
    





def part1():
    grid = read_input()
    asteroids = get_asteroids(grid)

    mxcount = 0
    mxr, mxc = 0, 0
    for r, c in asteroids:
        right, left, above, below = buildSeen(r, c, asteroids)

        count = len(right.keys()) + len(left.keys()) + len(above.keys()) + len(below.keys())
        if count > mxcount:
            # print(r, c, count)
            mxcount = count
            mxr = r
            mxc = c
            
    return mxcount, mxr, mxc

    



def part2():
    grid = read_input()
    asteroids = get_asteroids(grid)
    _, r, c = part1()
    right, left, above, below = buildSeen(r, c, asteroids)

    rightkeys = sorted(right.keys(), reverse=True)
    leftkeys = sorted(left.keys(), reverse=True)
    
    # Sort by distance from 
    for d in (right, left, above, below):
        for k, v in d.items():
            v.sort(key=lambda x: calc_dist(x[0], x[1], r, c) * -1)
            
            
            
    order = []
    while len(order) < 200:
        # 12 oclock
        if above[INF]:
            v = above[INF].pop()
            # print(INF, v)
            order.append(v)
        
        
        # right
        for k in rightkeys:
            if right[k]:
                v = right[k].pop()
                # print(k, v)
                order.append(v)

        # 6 oclock
        if below[INF]:
            v = below[INF].pop()
            # print(INF, v)
            order.append(v)
            
        # left
        for k in leftkeys:
            if left[k]:
                v = left[k].pop()
                # print(k, v)
                order.append(v)
            
        
    y, x = order[199]
    # print(order)
    # print(order[199])
    return x * 100 + y 
        
    

    

                
    




if __name__ == '__main__':
    count, _, _ = part1()
    print("Part 1", count)
    res = part2()
    print("Part 2", res)