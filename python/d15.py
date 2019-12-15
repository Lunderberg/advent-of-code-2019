#!/usr/bin/env python3

from collections import defaultdict
import inspect
import math
import time

import util

class Memory(list):
    """
    Implements a self-expanding memory of integers.
    """
    def __getitem__(self,key):
        if key < 0:
            raise IndexError('Negative memory pos {} not allowed.'.format(key))
        elif key >= len(self):
            return 0
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError('Negative memory pos {} not allowed.'.format(key))

        extension_needed = (key+1) - len(self)
        if extension_needed > 0:
            self.extend([0]*extension_needed)

        super().__setitem__(key, value)


class Interpreter:
    def __init__(self, memory, input_val = None, output_callback = None):
        self.memory = Memory(memory[:])
        self.ip = 0
        self.output_callback = output_callback
        self.input_val = input_val
        self.output_val = None
        self.done = False
        self.paused = False
        self.relative_base = 0

    @property
    def input_val(self):
        return self._input_val

    @input_val.setter
    def input_val(self,val):
        self._input_val = val
        self.paused = False

    def iteration(self):
        opcode = self.memory[self.ip] % 100
        if opcode == 1:
            self.op_add()
        elif opcode == 2:
            self.op_mul()
        elif opcode == 3:
            self.op_input()
        elif opcode == 4:
            self.op_output()
        elif opcode == 5:
            self.op_jump_if_true()
        elif opcode == 6:
            self.op_jump_if_false()
        elif opcode == 7:
            self.op_lt()
        elif opcode == 8:
            self.op_eq()
        elif opcode == 9:
            self.op_adjust_relative_base()
        elif opcode == 99:
            pass
        else:
            raise ValueError('Unknown opcode: {}'.format(opcode))

        self.done = (opcode == 99)

    def get_mode(self,i):
        mode = self.memory[self.ip]
        mode = mode // (10**(i+1))
        mode = mode % 10

        return mode

    def get_param(self,i):
        mode = self.get_mode(i)

        val = self.memory[self.ip+i]
        if mode==0:
            val = self.memory[val]
        elif mode==1:
            val = val
        elif mode==2:
            val = self.memory[val + self.relative_base]
        else:
            raise ValueError('Unknown mode {} at ip={}, value={}'.format(
                mode, self.ip, self.memory[self.ip]
            ))

        return val

    def set_param(self, i, val):
        mode = self.get_mode(i)

        addr = self.memory[self.ip + i]
        if mode==0:
            self.memory[addr] = val
        elif mode==1:
            raise ValueError('Cannot use mode==1 (immediate mode) for output params')
        elif mode==2:
            self.memory[addr + self.relative_base] = val


    def op_add(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = a+b
        self.set_param(3, x)
        self.ip += 4

    def op_mul(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = a*b
        self.set_param(3, x)
        self.ip += 4

    def op_input(self):
        if self.input_val is None:
            self.paused = True
            return
        else:
            x = self.input_val
            self.input_val = None

        self.set_param(1, x)
        self.ip += 2

    def op_output(self):
        a = self.get_param(1)
        self.output_val = a

        if self.output_callback is not None:
            self.output_callback(a)

        self.ip += 2


    def op_jump_if_true(self):
        a = self.get_param(1)
        b = self.get_param(2)

        if a:
            self.ip = b
        else:
            self.ip += 3

    def op_jump_if_false(self):
        a = self.get_param(1)
        b = self.get_param(2)

        if not a:
            self.ip = b
        else:
            self.ip += 3

    def op_lt(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = int(a<b)
        self.set_param(3, x)
        self.ip += 4

    def op_eq(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = int(a==b)
        self.set_param(3, x)
        self.ip += 4


    def op_adjust_relative_base(self):
        a = self.get_param(1)
        self.relative_base += a
        self.ip += 2


    def iterate_until_done(self):
        while not self.done and not self.paused:
            self.iteration()



directions = {1: (0,1),
              2: (0,-1),
              3: (-1,0),
              4: (1,0)}
reverse_dir = {1: 2,
               2: 1,
               3: 4,
               4: 3}

def add_dir(pos, direction):
    if direction in directions:
        direction = directions[direction]

    x,y = pos
    dx,dy = direction
    return (x+dx, y+dy)

class RepairBot:
    def __init__(self, memory):
        self.loc = (0,0)
        self.tiles = {(0,0): 1}
        self.path_from_start = {(0,0): []}

        self.interp = Interpreter(memory)


    def move(self, command):
        self.interp.input_val = command
        self.interp.iterate_until_done()

        old_loc = self.loc
        x,y = self.loc
        dx,dy = directions[command]
        attempted_loc = (x+dx, y+dy)

        result = self.interp.output_val
        if result == 0:
            self.tiles[attempted_loc] = 2
            return

        self.loc = attempted_loc

        if result == 1:
            self.tiles[attempted_loc] = 1
        elif result == 2:
            self.tiles[attempted_loc] = 3
        else:
            raise ValueError('Unknown result code: {}'.format(result))

        if self.loc not in self.path_from_start:
            self.path_from_start[self.loc] = self.path_from_start[old_loc] + [command]


    def next_explore(self):
        for pos,tile in self.tiles.items():
            if tile != 2:
                for command in directions:
                    new_loc = add_dir(pos,command)
                    if new_loc not in self.tiles:
                        return pos, command

        return None


    def explore(self):
        to_explore = self.next_explore()
        if to_explore is None:
            return False


        loc, next_command = to_explore
        self.goto(loc)
        self.move(next_command)
        return True


    def fully_explore(self, display_every=None, stop_func = None):
        i = 0
        while self.explore():
            i += 1
            if display_every is not None and i%display_every == 0:
                self.display()

            if stop_func is not None and stop_func(self):
                break


    def path_to(self, loc):
        # Backtrack towards the origin along the fastest route, then
        # go forwards toward the target location.  Won't be the
        # fastest route in case of loops, but is fast enough.
        target_path = self.path_from_start[loc]
        current_path = self.path_from_start[self.loc]

        shared_path = 0
        for i,(a,b) in enumerate(zip(target_path,current_path)):
            if a!=b:
                shared_path_len = i
                break
        else:
            shared_path_len = min(len(target_path), len(current_path))

        to_backtrack = [reverse_dir[d] for d in
                        reversed(current_path[shared_path_len:])]
        to_advance = target_path[shared_path_len:]
        return to_backtrack + to_advance


    def goto(self, loc):
        for command in self.path_to(loc):
            self.move(command)


    def display(self):
        xmin = min(x for x,y in self.tiles)
        xmax = max(x for x,y in self.tiles)
        ymin = min(y for x,y in self.tiles)
        ymax = max(y for x,y in self.tiles)

        for y in range(ymax,ymin-1,-1):
            for x in range(xmin,xmax+1):

                if (x,y) == self.loc:
                    c = 'D'
                elif (x,y) not in self.tiles:
                    c = ' '
                else:
                    val = self.tiles[(x,y)]
                    if val==1:
                        c = '.'
                    elif val==2:
                        c = '#'
                    elif val==3:
                        c = '*'
                print(c,end='')
            print()


def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]

    # Explore until the oxygen system is found
    bot = RepairBot(memory)
    found_oxygen = lambda bot:any(t==3 for t in bot.tiles.values())
    bot.fully_explore(stop_func = found_oxygen)

    goal = [pos for pos,t in bot.tiles.items() if t==3][0]
    print(len(bot.path_from_start[goal]))

    # Start the bot exploring again, but starting at the oxygen system.
    bot.goto(goal)
    bot.tiles = {goal: 3}
    bot.path_from_start = {goal: []}
    bot.fully_explore()

    print(max(len(path) for path in bot.path_from_start.values()))
    bot.display()


if __name__ == '__main__':
    main()
