#!/usr/bin/env python3

from collections import defaultdict
import itertools
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
    def __init__(self, memory, input_callback, output_callback = None):
        self.memory = Memory(memory[:])
        self.ip = 0
        self.output_callback = output_callback
        self.input_callback = input_callback
        self.output_val = None
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
        while not self.done:
            self.iteration()


class Robot:
    def __init__(self):
        #self.colors = {}
        self.colors = {(0,0):1}
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 1
        self.state = 'paint'

    def turn_left(self):
        if self.dx==0 and self.dy==1:
            self.dx=-1
            self.dy=0
        elif self.dx==-1 and self.dy==0:
            self.dx=0
            self.dy=-1
        elif self.dx==0 and self.dy==-1:
            self.dx=1
            self.dy=0
        elif self.dx==1 and self.dy==0:
            self.dx=0
            self.dy=1
        else:
            raise 'Bad!'

    def turn_right(self):
        if self.dx==0 and self.dy==1:
            self.dx=1
            self.dy=0
        elif self.dx==1 and self.dy==0:
            self.dx=0
            self.dy=-1
        elif self.dx==0 and self.dy==-1:
            self.dx=-1
            self.dy=0
        elif self.dx==-1 and self.dy==0:
            self.dx=0
            self.dy=1
        else:
            raise 'Bad!'

    def move_forward(self):
        self.x += self.dx
        self.y += self.dy

    def paint(self, color):
        self.colors[(self.x,self.y)] = color

    def command(self, val):
        if self.state=='paint':
            self.paint(val)
            self.state = 'move'

        elif self.state == 'move':
            if val==0:
                self.turn_left()
            elif val==1:
                self.turn_right()
            else:
                raise 'Bad!!'

            self.move_forward()
            self.state = 'paint'

    def camera(self, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        if (x,y) in self.colors:
            return self.colors[(x,y)]
        else:
            return 0

    def display(self):
        xmin = min(x for x,y in self.colors)
        xmax = max(x for x,y in self.colors)
        ymin = min(y for x,y in self.colors)
        ymax = max(y for x,y in self.colors)

        for y in range(ymax,ymin-1,-1):
            for x in range(xmin,xmax+1):
                if self.camera(x,y):
                    print('#',end='')
                else:
                    print(' ',end='')
            print()



def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]

    robot = Robot()
    def output_callback(val):
        robot.command(val)

    def input_callback():
        return robot.camera()


    interp = Interpreter(memory,
                         input_callback = input_callback,
                         output_callback = output_callback)
    interp.iterate_until_done()
    print(len(robot.colors))
    robot.display()

if __name__ == '__main__':
    main()
