# Day 12. The N-Body Problem
# https://adventofcode.com/2019/day/12

import math
from collections import defaultdict, deque
from itertools import combinations


class Moon:
    def __init__(self, name, x ,y ,z):
        self.name = name
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]
    
    def update_position(self):
        for i in range(3):
            self.position[i] += self.velocity[i]

    def potential_energy(self):
        return sum([abs(p) for p in self.position])
    
    def kinetic_energy(self):
        return sum([abs(v) for v in self.velocity])
    
    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()
    
    def __repr__(self):
        return f"Moon: {self.name} - {self.position} - {self.velocity}"
    
    def get_position(self):
        return tuple(self.position)



def read_input():
    with open("inputs/day12_input.txt") as f:
        lines = f.readlines()
    
    moons = []
    for i, l in enumerate(lines):
        l = l.replace('<', '').replace('>', '').split(', ')

        x = int(l[0].replace('x=', ''))
        y = int(l[1].replace('y=', ''))
        z = int(l[2].replace('z=', ''))

        moons.append(Moon(i, x, y, z))

    return moons



def apply_gravity(moon1, moon2):
    for i in range(3):
        c1 = moon1.position[i]
        c2 = moon2.position[i]

        if c2 == c1: continue 
        if c2 < c1: moon1, moon2 = moon2, moon1

        moon1.velocity[i] += 1
        moon2.velocity[i] -= 1




def step(moons):
    # first update velocities
    for m1, m2 in combinations(moons, 2):
        apply_gravity(m1, m2)
    
    # update positions
    for m in moons:
        m.update_position()


def calculate_total_energy(moons):
    total_energy = 0
    for m in moons:
        total_energy += m.total_energy()
    return total_energy


def part1():
    
    moons = read_input()

    for _ in range(1000):
        step(moons)
    
    total_energy = calculate_total_energy(moons)
    
    print("Part 1:", total_energy)





# Keep state on each dimension separately instead
class System:
    def __init__(self, moons):
        self.steps = 0
        self.x = [m.position[0] for m in moons]
        self.y = [m.position[1] for m in moons]
        self.z = [m.position[2] for m in moons]
        self.dx = [m.velocity[0] for m in moons]
        self.dy = [m.velocity[1] for m in moons]
        self.dz = [m.velocity[2] for m in moons]
        
    
    def update_velocity(self):
        for i, j in combinations([0, 1, 2, 3], 2):
            if self.x[i] < self.x[j]: 
                self.dx[i] += 1
                self.dx[j] -= 1
            elif self.x[i] > self.x[j]:
                self.dx[i] -= 1
                self.dx[j] += 1
            
            if self.y[i] < self.y[j]: 
                self.dy[i] += 1
                self.dy[j] -= 1
            elif self.y[i] > self.y[j]:
                self.dy[i] -= 1
                self.dy[j] += 1
            
            if self.z[i] < self.z[j]: 
                self.dz[i] += 1
                self.dz[j] -= 1
            elif self.z[i] > self.z[j]:
                self.dz[i] -= 1
                self.dz[j] += 1


    def update_position(self):
        for i in range(4):
            self.x[i] += self.dx[i]
            self.y[i] += self.dy[i]
            self.z[i] += self.dz[i]
    
    
    def step(self):
        self.update_velocity()
        self.update_position()
        self.steps += 1
        
    


def part2():

    
    moons = read_input()
    system = System(moons)
    starts = [tuple(system.x+system.dx), tuple(system.y+system.dy), tuple(system.z+system.dz)]
    print("Start", starts)
    cycles = [None for _ in range(3)]
    found = 0
    while found < 3:
        system.step()

        if not cycles[0] and tuple(system.x+system.dx) == starts[0]:
                cycles[0] = system.steps
                print("Found X")
                found += 1

        if not cycles[1] and tuple(system.y+system.dy)== starts[1]:
                cycles[1] = system.steps
                print("Found Y")
                found += 1

        if not cycles[2] and tuple(system.z+system.dz) == starts[2]:
                cycles[2] = system.steps
                print("Found Z")
                found += 1
        
    
    print("Cycles:", cycles)
    s = math.lcm(*cycles)
    print()
    print("Part 2:", s)

if __name__ == '__main__':
    part1()
    part2()