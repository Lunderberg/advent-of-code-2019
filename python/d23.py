#!/usr/bin/env python3

from collections import deque
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
    def __init__(self, memory, input_iter,
                 output_callback = None, num_output_args = None):
        self.memory = Memory(memory[:])
        self.ip = 0

        self.output_callback = output_callback
        if num_output_args is None:
            signature = inspect.signature(output_callback)
            self.num_output_args = len(signature.parameters)
        else:
            self.num_output_args = num_output_args

        self.input_iter = input_iter
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
        x = next(self.input_iter)

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


    def iterate_until_done(self, max_iterations=None):
        iter_num = 0
        while not self.done:
            self.iteration()
            iter_num += 1
            if max_iterations is not None and iter_num>max_iterations:
                break



class Network:
    def __init__(self, memory):
        num_computers = 50
        self.interpreters = [Interpreter(memory,
                                         input_iter = self.input_iter(i),
                                         output_callback = self.send_message)
                             for i in range(num_computers)]
        self.message_queues = [deque() for i in range(num_computers)]
        self.failed_input_requests = [0 for i in range(num_computers)]

        self.nat_val = None
        self.prev_y_value = None
        self.output_val = None

    def input_iter(self, i):
        yield i

        while True:
            if self.message_queues[i]:
                x,y = self.message_queues[i].popleft()
                yield x
                yield y
                self.failed_input_requests[i] = 0
            else:
                yield -1
                self.failed_input_requests[i] += 1
                self.nat_test()

    def send_message(self, addr, x, y):
        if addr==255:
            if self.nat_val is None:
                print('First y NAT val stored:', y)
            self.nat_val = (x,y)
        else:
            self.message_queues[addr].append( (x,y) )

    def nat_test(self):
        no_messages_waiting = not any(self.message_queues)
        many_read_attempts = all(r>50 for r in self.failed_input_requests)
        if no_messages_waiting and many_read_attempts:
            if self.prev_y_value == self.nat_val[1]:
                self.output_val = self.prev_y_value
            self.message_queues[0].append(self.nat_val)
            self.prev_y_value = self.nat_val[1]


    def run(self, ops_per = 1000):
        while self.output_val is None:
            for interp in self.interpreters:
                interp.iterate_until_done(ops_per)

        return self.output_val
        

def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]

    network = Network(memory)
    import sys
    print('First repeated y NAT val:',network.run(int(sys.argv[-1])))

if __name__ == '__main__':
    main()
