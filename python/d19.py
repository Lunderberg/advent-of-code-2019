#!/usr/bin/env python3

from collections import defaultdict
import functools
import inspect
import itertools
import math
import sys
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


memory = [int(x.strip()) for x in
          util.get_puzzle_input().split(',')]

@functools.lru_cache(maxsize=None)
def is_tractor(x,y):
    interp = Interpreter(memory)
    interp.input_val = x
    interp.iterate_until_done()
    interp.input_val = y
    interp.iterate_until_done()
    return bool(interp.output_val)

@functools.lru_cache(maxsize=None)
def tractor_xrange(y):
    if y < 10:
        xmin = next(x for x in itertools.count() if is_tractor(x,y))
        xmax = next(x for x in itertools.count(xmin) if not is_tractor(x,y))
        return (xmin, xmax-1)

    for y_test in range(10,y):
        tractor_xrange(y_test)

    prev_xmin,prev_xmax = tractor_xrange(y-1)
    xmin = next(x for x in itertools.count(prev_xmin) if is_tractor(x,y))
    xmax = next(x for x in itertools.count(max(xmin,prev_xmax)) if not is_tractor(x,y))
    return (xmin, xmax-1)



def is_tractor_cheat(x,y):
    if y < 10:
        return is_tractor(x,y)
    else:
        xmin,xmax = tractor_xrange(y)
        return xmin <= x <= xmax


def is_grid_start(size, x,y):
    return all(is_tractor_cheat(x+dx, y+dy)
               for dx in range(size)
               for dy in range(size))


def find_grid(size, max_xy=2000):
    output = []
    for xy in itertools.count(1):
        if xy % 100 == 0:
            print('xy sum: ', xy)
        for x in range(0,xy):
            y = xy - x
            if is_grid_start(size, x, y):
                return (x,y)


def draw(xmin, xmax, ymin, ymax, xp, yp):
    for y in range(ymin,ymax+1):
        for x in range(xmin,xmax+1):
            if (x,y) == (xp,yp):
                c = 'O'
            elif is_tractor_cheat(x,y):
                c = '#'
            else:
                c = '.'
            print(c,end='')
        print()


def main():
    num_active = 0
    for x in range(50):
        for y in range(50):
            num_active += is_tractor(x,y)

    print('50x50 active:', num_active)

    size = 100
    print('Size: {}\tfirst: {}'.format(size, find_grid(size)))



if __name__ == '__main__':
    main()
