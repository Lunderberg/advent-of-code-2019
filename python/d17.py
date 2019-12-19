#!/usr/bin/env python3

from collections import defaultdict
import inspect
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






directions = [(0,1), (0,-1), (1,0), (-1,0)]

class Scaffolds:
    def __init__(self, memory):
        self.memory = memory
        self.cam_x = 0
        self.cam_y = 0
        self.tiles = {}


        interp = Interpreter(memory, output_callback=self.camera)
        interp.iterate_until_done()

        self.xmax = max(x for x,y in self.tiles)
        self.ymax = max(y for x,y in self.tiles)

    def camera(self, c):
        c = chr(c)
        if c in ('#', '<', '>', '^', 'v'):
            self.tiles[(self.cam_x, self.cam_y)] = c
            self.cam_x += 1
        elif c=='.':
            self.cam_x += 1
        elif c=='\n':
            self.cam_x = 0
            self.cam_y += 1

    def intersections(self):
        output = []
        for point in self.tiles:
            x,y = point
            if all( (x+dx,y+dy) in self.tiles for (dx,dy) in directions):
                output.append(point)

        return output

    def draw(self):
        intersections = self.intersections()

        xmin = min(x for x,y in self.tiles)
        xmax = max(x for x,y in self.tiles)
        ymin = min(y for x,y in self.tiles)
        ymax = max(y for x,y in self.tiles)

        for y in range(0,ymax+1,1):
            for x in range(0,xmax+1):

                pos = (x,y)
                if pos in intersections:
                    c = 'O'
                elif (x,y) in self.tiles:
                    c = self.tiles[pos]
                else:
                    c = '.'
                print(c,end='')
            print()

    def give_directions(self,
                        main='A,B,C,A,B,C',
                        a='',
                        b='',
                        c='',
                        feed=False):
        memory = self.memory[:]
        memory[0] = 2

        def callback(c):
            if c<256:
                print(chr(c), end='')
            else:
                print(c)


        interp = Interpreter(memory, output_callback=callback)

        feed = 'y' if feed else 'n'
        commands = '\n'.join([main,a,b,c,feed,''])

        for c in commands:
            interp.input_val = ord(c)
            interp.iterate_until_done()









def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]


    s = Scaffolds(memory)
    print(sum(x*y for (x,y) in s.intersections()))

    s.give_directions(
        main='A,C,C,B,C,B,C,B,A,A',
        a = 'L,6,R,8,L,4,R,8,L,12',
        b = 'L,12,L,6,L,4,L,4',
        c = 'L,12,R,10,L,4',
        feed = False,
    )


if __name__ == '__main__':
    main()
