#!/usr/bin/env python3

import util

def parse_wire(wire):
    wire = wire.split(',')

    loc_x,loc_y = 0,0
    dist = 0

    path = {}

    for step in wire:
        direction = step[0]
        distance = int(step[1:])
        if direction=='R':
            d_x,d_y = 1,0
        elif direction=='U':
            d_x,d_y = 0,1
        elif direction=='L':
            d_x,d_y = -1,0
        elif direction=='D':
            d_x,d_y = 0,-1

        for i in range(1,distance+1):
            loc_x += d_x
            loc_y += d_y
            dist += 1

            path[(loc_x, loc_y)] =  dist

    return path

def manhattan_dist(p):
    return abs(p[0]) + abs(p[1])

def main():
    wire_a,wire_b,*rest = util.get_puzzle_input().split('\n')

    path_a = parse_wire(wire_a)
    path_b = parse_wire(wire_b)

    intersections = set(path_a) & set(path_b)

    manhattan = lambda p: abs(p[0]) + abs(p[1])
    distance = lambda p: path_a[p] + path_b[p]

    closest = min(intersections, key = manhattan)
    print(closest, manhattan(closest))

    closest = min(intersections, key = distance)
    print(closest, distance(closest))



if __name__ == '__main__':
    main()
