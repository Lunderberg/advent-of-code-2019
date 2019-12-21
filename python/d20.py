#!/usr/bin/env python3

from collections import defaultdict
import heapq
import string

import util

class Maze:
    def __init__(self):
        self.spaces = set()
        self.telelabels = {}
        self.teleports = {}

    @classmethod
    def parse_maze(cls, text):
        telechars = {}
        spaces = set()

        lines = [line for line in text.split('\n') if line.strip()]
        for y,line in enumerate(lines):
            for x,c in enumerate(line):
                pos = (x,y)
                if c=='.':
                    spaces.add(pos)
                elif c in string.ascii_uppercase:
                    telechars[pos] = c

        telelabels = defaultdict(list)
        for (x,y),c in telechars.items():
            # Labels only go right or down
            for dx,dy in [(1,0), (0,1)]:
                next_pos = (x+dx, y+dy)
                if next_pos in telechars:
                    label = c + telechars[next_pos]
                    possible_spaces = [(x-dx,y-dy), (x+2*dx, y+2*dy)]
                    for space in possible_spaces:
                        if space in spaces:
                            telelabels[label].append(space)

        xmin = min(x for (x,y) in spaces)
        xmax = max(x for (x,y) in spaces)
        ymin = min(y for (x,y) in spaces)
        ymax = max(y for (x,y) in spaces)
        center = ( (xmin+xmax)/2, (ymin+ymax)/2 )

        teleports = {}
        for label,telespaces in telelabels.items():
            if len(telespaces)==2:
                inner,outer = sorted(
                    telespaces,
                    key=lambda p:max(abs(p[0]-center[0]), abs(p[1]-center[1]))
                )

                teleports[inner] = (outer, +1)
                teleports[outer] = (inner, -1)

        output = cls()
        output.spaces = spaces
        output.telelabels = dict(telelabels)
        output.teleports = teleports
        return output


    def initial_state(self):
        return (self.telelabels['AA'][0],0)

    def target(self):
        return (self.telelabels['ZZ'][0],0)


    def get_next_states(self, state):
        (x,y),level = state

        directions = [(0,1), (0,-1), (1,0), (-1,0)]

        output = []

        for dx,dy in directions:
            new_loc = (x+dx, y+dy)
            if new_loc in self.spaces:
                output.append( (new_loc,level) )

        if (x,y) in self.teleports:
            new_pos, dlevel = self.teleports[(x,y)]
            if level+dlevel >= 0:
                output.append( (new_pos, level+dlevel) )

        return output

    def fastest_solution(self):
        init = self.initial_state()
        target = self.target()
        distances = {init: 0}
        # paths = {init: []}
        to_visit = [ (0,init) ]

        heapq.heapify(to_visit)

        while to_visit:
            distance,state = heapq.heappop(to_visit)
            for new_state in self.get_next_states(state):
                # if new_state not in paths:
                #     new_path = paths[state][:] + [state]
                #     paths[new_state] = new_path
                #     heapq.heappush(to_visit, (len(new_path), new_state))

                #     if new_state == target:
                #         return new_path

                if new_state == target:
                    return distance+1

                if new_state not in distances:
                    distances[new_state] = distance+1
                    heapq.heappush(to_visit, (distance+1, new_state) )

        return '???'


def main():
    inputs = util.get_puzzle_input()

    maze = Maze.parse_maze(inputs)
    dist = maze.fastest_solution()
    print(dist)

    # sol = maze.fastest_solution()
    # print(len(sol))


if __name__ == '__main__':
    main()
