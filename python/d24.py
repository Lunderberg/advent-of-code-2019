#!/usr/bin/env python3

from collections import defaultdict

import util

class Bugs:
    def __init__(self, bugs):
        self.height = len(bugs)
        self.width = len(bugs[0])
        self.bugs = bugs


    @classmethod
    def parse_input(cls, text):
        is_bug = {'.': False, '#': True}

        bugs = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                line_bugs = [is_bug[c] for c in line]
                bugs.append(line_bugs)

        return cls(bugs)


    def draw(self):
        for line in self.bugs:
            for has_bug in line:
                if has_bug:
                    c = '#'
                else:
                    c = '.'
                print(c, end='')
            print()


    def is_bug(self, x, y):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.bugs[y][x]
        else:
            return False


    def num_neighbors(self, x, y):
        return (self.is_bug(x-1, y) +
                self.is_bug(x+1, y) +
                self.is_bug(x, y-1) +
                self.is_bug(x, y+1))


    def step(self):
        new_bugs = []
        for y,line in enumerate(self.bugs):
            new_bug_line = []
            for x,is_bug in enumerate(line):
                neighbors = self.num_neighbors(x,y)
                is_new_bug = ((is_bug and (neighbors==1)) or
                              (not is_bug and (neighbors in [1,2])))
                new_bug_line.append(is_new_bug)

            new_bugs.append(new_bug_line)

        self.bugs = new_bugs

    def score(self):
        total = 0
        cum_mul = 1
        for line in self.bugs:
            for is_bug in line:
                if is_bug:
                    total += cum_mul
                cum_mul *= 2
        return total


class BugsRecursive:
    def __init__(self, bugs):
        self.bugs = bugs


    @classmethod
    def parse_input(cls, text):
        bugs = set()

        is_bug = {'.': False, '#': True}

        for y,line in enumerate(text.split('\n')):
            line = line.strip()
            if line:
                for x,c in enumerate(line):
                    if c=='#':
                        bugs.add( (x,y,0) )

        return cls(bugs)


    def draw(self):
        min_level = min(level for x,y,level in self.bugs)
        max_level = max(level for x,y,level in self.bugs)

        for level in range(min_level, max_level+1):
            print('Level = {}'.format(level))
            for y in range(5):
                for x in range(5):
                    if (x,y) == (2,2):
                        c = '?'
                    elif (x,y,level) in self.bugs:
                        c = '#'
                    else:
                        c = '.'
                    print(c, end='')
                print()


    def draw_neighbors(self):
        neighbors = self.all_neighbors()
        min_level = min(level for x,y,level in neighbors)
        max_level = max(level for x,y,level in neighbors)

        for level in range(min_level, max_level+1):
            print('Level = {}'.format(level))
            for y in range(5):
                for x in range(5):
                    if (x,y) == (2,2):
                        c = '?'
                    else:
                        c = str(neighbors[(x,y,level)])
                    print(c, end='')
                print()


    def all_neighbors(self):
        neighbors = defaultdict(int)

        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for x,y,level in self.bugs:
            for dx,dy in directions:
                nx = x+dx
                ny = y+dy
                if (nx,ny)==(2,2):
                    if dx==1:
                        for inner_y in range(5):
                            neighbors[ (0,inner_y,level+1) ] += 1
                    elif dx==-1:
                        for inner_y in range(5):
                            neighbors[ (4,inner_y,level+1) ] += 1
                    elif dy==1:
                        for inner_x in range(5):
                            neighbors[ (inner_x, 0, level+1) ] += 1
                    elif dy==-1:
                        for inner_x in range(5):
                            neighbors[ (inner_x, 4, level+1) ] += 1

                else:
                    if nx < 0:
                        neighbors[ (1,2,level-1) ] += 1
                    elif nx >= 5:
                        neighbors[ (3,2,level-1) ] += 1
                    elif ny < 0:
                        neighbors[ (2,1,level-1) ] += 1
                    elif ny >= 5:
                        neighbors[ (2,3,level-1) ] += 1
                    else:
                        neighbors[ (nx,ny,level) ] += 1

        return neighbors

    def step(self):
        new_bugs = set()
        for loc,num_neighbors in self.all_neighbors().items():
            if (num_neighbors==1 or
                (num_neighbors==2 and loc not in self.bugs)):
                new_bugs.add(loc)

        self.bugs = new_bugs


def part_a(text):
    state = Bugs.parse_input(text)

    scores = set()

    while True:
        new_score = state.score()
        if new_score in scores:
            break
        scores.add(new_score)
        state.step()

    print(new_score)


def part_b(text):
    state = BugsRecursive.parse_input(text)
    for i in range(200):
        state.step()
    print(len(state.bugs))


def main():
    text = util.get_puzzle_input()
    part_a(text)
    part_b(text)


if __name__ == '__main__':
    main()
