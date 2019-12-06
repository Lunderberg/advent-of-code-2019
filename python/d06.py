#!/usr/bin/env python3

import util

def get_edges():
    inputs = util.get_puzzle_input().split('\n')

    edges = []
    for i in inputs:
        if i:
            i = i.split(')')
            edges.append( (i[0],i[1]) )
    return set(edges)

def part_a():
    edges = get_edges()

    distance = {'COM': 0}
    while edges:
        found = set()
        for a,b in edges:
            if a in distance:
                distance[b] = distance[a]+1
                found.add( (a,b) )
        edges = edges - found

    print('Total direct+indirect orbits:', sum(distance.values()))


def part_b():
    edges = get_edges()

    parent = {}
    for a,b in edges:
        parent[b] = a

    def path_to_com(start):
        path = [start]
        while path[-1]!='COM':
            path.append(parent[path[-1]])
        return path

    you_path = set(path_to_com('YOU'))
    san_path = set(path_to_com('SAN'))

    transfer_path = (you_path | san_path) - (you_path & san_path)
    # If transfer path is just 'YOU' and 'SAN', already there.
    # Otherwise, each additional step is one transfer
    print('Number of transfers:',len(transfer_path)-2)

def main():
    part_a()
    part_b()

if __name__ == '__main__':
    main()
