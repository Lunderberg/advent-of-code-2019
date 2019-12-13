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
    def __init__(self, memory, input_callback,
                 output_callback = None, num_output_args = None):
        self.memory = Memory(memory[:])
        self.ip = 0

        self.output_callback = output_callback
        if num_output_args is None:
            signature = inspect.signature(output_callback)
            self.num_output_args = len(signature.parameters)
        else:
            self.num_output_args = num_output_args

        self.input_callback = input_callback
        self.output_val = None
        self.output_callback_params = []
        self.done = False
        self.relative_base = 0

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
            raise ValueError('Unknown mode {} at ip={}, value='.format(
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
        x = self.input_callback()

        self.set_param(1, x)
        self.ip += 2

    def op_output(self):
        a = self.get_param(1)
        self.output_val = a

        if self.output_callback is not None:
            self.output_callback_params.append(a)
            if len(self.output_callback_params) == self.num_output_args:
                self.output_callback(*self.output_callback_params)
                self.output_callback_params.clear()

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
        while not self.done:
            self.iteration()



class Game:
    def __init__(self):
        self.tiles = defaultdict(int)
        self.score = 0

    def set_tile(self, x, y, val):
        if x==-1 and y==0:
            self.score = val
        else:
            self.tiles[(x,y)] = val

    def display(self):
        print(self.score)

        xmin = min(x for x,y in self.tiles)
        xmax = max(x for x,y in self.tiles)
        ymin = min(y for x,y in self.tiles)
        ymax = max(y for x,y in self.tiles)

        for y in range(ymax,ymin-1,-1):
            for x in range(xmin,xmax+1):
                val = self.tiles[(x,y)]
                if val==0:
                    c = ' '
                elif val==1:
                    c = '#'
                elif val==2:
                    c = 'x'
                elif val==3:
                    c = '-'
                elif val==4:
                    c = 'o'
                print(c,end='')
            print()

    def best_dir(self):
        paddle = [x for (x,y),val in self.tiles.items()
                  if val==3][0]
        ball = [x for (x,y),val in self.tiles.items()
                if val==4][0]

        if ball==paddle:
            return 0
        else:
            return math.copysign(1,ball - paddle)

def part_a():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]
    game = Game()
    interp = Interpreter(memory,
                         input_callback = game.best_dir,
                         output_callback = game.set_tile)
    interp.iterate_until_done()
    print('Num block:', sum(1 for tile in game.tiles.values() if tile==2))

def part_b():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]
    memory[0] = 2
    game = Game()
    interp = Interpreter(memory,
                         input_callback = game.best_dir,
                         output_callback = game.set_tile)
    interp.iterate_until_done()
    print('Winning score:', game.score)


def main():
    part_a()
    part_b()

if __name__ == '__main__':
    main()
