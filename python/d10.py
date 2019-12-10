#!/usr/bin/env python3

from collections import defaultdict
import util
import math
from math import gcd,atan2


def num_visible(asteroids, pos):
    directions = set()
    for asteroid in asteroids:
        if asteroid != pos:
            direction = (pos[0] - asteroid[0], pos[1] - asteroid[1])
            scale = gcd(direction[0], direction[1])
            direction = (direction[0]/scale, direction[1]/scale)
            directions.add(direction)

    return len(directions)

def order_destroyed(asteroids, pos):
    along_lines = defaultdict(list)

    for asteroid in asteroids:
        if asteroid != pos:
            direction = (pos[0] - asteroid[0], pos[1] - asteroid[1])
            scale = gcd(direction[0], direction[1])
            direction = (direction[0]/scale, direction[1]/scale)
            along_lines[direction].append(asteroid)

    for key,val in along_lines.items():
        val.sort(key = lambda ast:abs(ast[0]-pos[0]) + abs(ast[1]-pos[1]))

    clockwise = {(atan2(-key[0],key[1])+2*math.pi)%(2*math.pi)
                 :val for key,val in along_lines.items()}

    clockwise = [clockwise[key] for key in sorted(clockwise)]
    while any(clockwise):
        for direction in clockwise:
            if direction:
                yield direction[0]
                del direction[0]


def main():
    inputs = util.get_puzzle_input()
    field = [list(line) for line in inputs.split('\n')
             if line.strip()]
    asteroids = [(j,i) for i,line in enumerate(field)
                 for j,char in enumerate(line)
                 if char=='#']

    best = max(asteroids, key=lambda pos:num_visible(asteroids,pos))
    print(best)
    print(num_visible(asteroids,best))

    order = list(order_destroyed(asteroids, best))
    print(order[199])

if __name__ == '__main__':
    main()
