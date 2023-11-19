# Day 14. Space Stoichiometry
# https://adventofcode.com/2019/day/14

import math
from collections import defaultdict

class Recipe:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.dependents = {}
    
    def add_dependent(self, name, quantity):
        self.dependents[name] = quantity

    def __repr__(self):
        s = f'{self.name} ({self.quantity}): [{self.dependents}]'
        return s
        
ORE = 'ORE'
FUEL = 'FUEL'

def read_input():
    with open("inputs/day14_input.txt") as f:
        lines = f.readlines()

    minerals = set()
    recipes = {}
    for l in lines:
        deps, min = l.split(' => ')

        q, n = min.split()
        r = Recipe(n, int(q))
        minerals.add(n)

        for d in deps.split(', '):
            p, m = d.split()
            r.add_dependent(m, int(p))

        recipes[n] = r

    return recipes, minerals

        
def part1():
    recipes, _ = read_input()
    inventory = defaultdict(int)
    ORE_START = 1_000_000_000_000
    inventory[ORE] = ORE_START
    required = {FUEL: 1}

    while required:
        # print(required)
        # loop through required and decompose into dependents
        # pop a random mineral off and convert to depedendents
        name, qty = required.popitem()
        if inventory[name] >= qty:
            inventory[name] -= qty
            continue
        else:
            qty -= inventory[name]
            inventory[name] = 0
        
        if name == ORE:
            continue
        
        recipe = recipes[name]
        copies = math.ceil(qty / recipe.quantity)
        # remainder if produced too much
        inventory[name] += (copies * recipe.quantity) - qty
        
        # produce
        for n, q in recipe.dependents.items():
            if n in required:
                required[n] += q * copies
            else:
                required[n] = q * copies

    print("Part 1:", ORE_START - inventory[ORE])




def part2():
    recipes, _ = read_input()
    inventory = defaultdict(int)
    ORE_START = 1_000_000_000_000
    inventory[ORE] = ORE_START
    fuel_count = 0

    while inventory[ORE] > 120_0000_000:
        print("\rRunning", inventory[ORE], fuel_count, end='')
        required = {FUEL: 1000}
        
        while required and inventory[ORE] >= 120_000_000:
            # loop through required and decompose into dependents
            # pop a random mineral off and convert to depedendents
            name, qty = required.popitem()
            if inventory[name] >= qty:
                inventory[name] -= qty
                continue
            else:
                qty -= inventory[name]
                inventory[name] = 0
            
            if name == ORE:
                continue
            
            recipe = recipes[name]
            copies = math.ceil(qty / recipe.quantity)
            # remainder if produced too much
            inventory[name] += (copies * recipe.quantity) - qty
            
            # produce
            for n, q in recipe.dependents.items():
                if n in required:
                    required[n] += q * copies
                else:
                    required[n] = q * copies

        if not required:
            fuel_count += 1000
            

    while inventory[ORE] > 0:
        print("\rRunning", inventory[ORE], fuel_count, end='')
        required = {FUEL: 1}
        
        while required and inventory[ORE] > 0:
            # loop through required and decompose into dependents
            # pop a random mineral off and convert to depedendents
            name, qty = required.popitem()
            if inventory[name] >= qty:
                inventory[name] -= qty
                continue
            else:
                qty -= inventory[name]
                inventory[name] = 0
            
            if name == ORE:
                continue
            
            recipe = recipes[name]
            copies = math.ceil(qty / recipe.quantity)
            # remainder if produced too much
            inventory[name] += (copies * recipe.quantity) - qty
            
            # produce
            for n, q in recipe.dependents.items():
                if n in required:
                    required[n] += q * copies
                else:
                    required[n] = q * copies

        if not required:
            fuel_count += 1

    print()
    print("Part 2:", fuel_count)

    
if __name__ == '__main__':
    part1()
    part2()