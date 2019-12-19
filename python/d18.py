#!/usr/bin/env python3

import copy
import heapq
import string

import util

directions = [(0,1), (0,-1), (1,0), (-1,0)]

class Maze:
    def __init__(self):
        self.locs = []
        self.spaces = set()
        self.keys = {}
        self.doors = {}
        self.total_steps = 0
        self.distance_cache = None

    @classmethod
    def parse_input(cls, text):
        output = cls()

        lines = [line.strip() for line in text.split('\n') if line.strip()]

        for y,line in enumerate(lines):
            for x,c in enumerate(line):
                if c=='#':
                    continue

                pos = (x,y)
                output.spaces.add(pos)
                if c=='@':
                    output.locs.append(pos)
                elif c in string.ascii_uppercase:
                    output.doors[pos] = c
                elif c in string.ascii_lowercase:
                    output.keys[pos] = c.upper()

        return output

    def draw(self):
        xmin = min(x for x,y in self.spaces)
        xmax = max(x for x,y in self.spaces)
        ymin = min(y for x,y in self.spaces)
        ymax = max(y for x,y in self.spaces)

        for y in range(0,ymax+2):
            for x in range(0,xmax+2):
                pos = (x,y)
                if pos in self.locs:
                    c = '@'
                elif pos in self.doors:
                    c = self.doors[pos]
                elif pos in self.keys:
                    c = self.keys[pos].lower()
                elif pos in self.spaces:
                    c = '.'
                else:
                    c = '#'
                print(c,end='')
            print()

    def initial_states(self):
        keys_held = ()
        output = []
        for bot_num in range(len(self.locs)):
            output.append( (keys_held, tuple(self.locs), bot_num) )
        return output

    def get_next_states(self, state):
        keys_held, locs, active_bot = state

        output = []

        x,y = locs[active_bot]
        for dx,dy in directions:
            new_loc = (x+dx, y+dy)
            door = self.doors.get(new_loc,None)
            if new_loc in self.spaces and (door is None or door in keys_held):
                if new_loc in self.keys and self.keys[new_loc] not in keys_held:
                    new_keys = tuple(sorted(set(keys_held + (self.keys[new_loc],))))
                    next_active_bot_options = range(len(self.locs))
                else:
                    new_keys = keys_held
                    next_active_bot_options = [active_bot]

                all_new_locs = (*locs[:active_bot], new_loc, *locs[active_bot+1:])
                for next_active_bot in next_active_bot_options:
                    output.append( (new_keys,all_new_locs,next_active_bot) )

        return output

    def fastest_solution(self):
        distances = {}
        to_visit = []
        for initial_state in self.initial_states():
            distances[initial_state] = 0
            to_visit.append( (0,initial_state) )

        heapq.heapify(to_visit)

        best_num_keys = 0

        while to_visit:
            distance,state = heapq.heappop(to_visit)
            for new_state in self.get_next_states(state):
                num_keys = len(new_state[0])
                if num_keys == len(self.keys):
                    return distance+1
                if num_keys > best_num_keys:
                    print('Found {} keys in {} steps'.format(num_keys,distance+1))
                    best_num_keys = num_keys

                if new_state not in distances:
                    distances[new_state] = distance+1
                    heapq.heappush(to_visit, (distance+1, new_state) )

        return '???'

    def adjust_start(self):
        x,y = self.locs[0]
        self.locs = [
            (x+1, y+1),
            (x-1, y+1),
            (x+1, y-1),
            (x-1, y-1),
        ]
        self.spaces.remove( (x,y) )
        self.spaces.remove( (x-1, y) )
        self.spaces.remove( (x+1, y) )
        self.spaces.remove( (x, y-1) )
        self.spaces.remove( (x, y+1) )



def main():
    inputs = util.get_puzzle_input()
    maze = Maze.parse_input(inputs)
    print('Part a:', maze.fastest_solution())

    maze.adjust_start()
    #maze.draw()
    print('Part b:', maze.fastest_solution())

if __name__ == '__main__':
    main()
