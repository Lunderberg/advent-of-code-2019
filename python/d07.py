#!/usr/bin/env python3

import itertools
import util

class Interpreter:
    def __init__(self, memory, input_val = None, output_callback = None):
        self.memory = memory[:]
        self.ip = 0
        self.output_callback = output_callback
        self.input_val = input_val
        self.output_val = None
        self.done = False
        self.paused = False

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
        elif opcode == 99:
            pass
        else:
            raise ValueError('Unknown opcode: {}'.format(opcode))

        self.done = (opcode == 99)

    def get_param(self,i):
        mode = self.memory[self.ip]
        mode = mode // (10**(i+1))
        mode = mode % 10

        val = self.memory[self.ip+i]
        if not mode:
            val = self.memory[val]

        return val

    def op_add(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = a+b
        xi = self.memory[self.ip+3]
        self.memory[xi] = x
        self.ip += 4

    def op_mul(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = a*b
        xi = self.memory[self.ip+3]
        self.memory[xi] = x
        self.ip += 4

    def op_input(self):
        if self.input_val is None:
            self.paused = True
            return
        else:
            x = self.input_val
            self.input_val = None

        xi = self.memory[self.ip+1]
        self.memory[xi] = x
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
        xi = self.memory[self.ip+3]
        self.memory[xi] = x
        self.ip += 4

    def op_eq(self):
        a = self.get_param(1)
        b = self.get_param(2)

        x = int(a==b)
        xi = self.memory[self.ip+3]
        self.memory[xi] = x
        self.ip += 4


    def iterate_until_done(self):
        while not self.done and not self.paused:
            self.iteration()



def test_sequence(memory, seq):
    interpreters = [Interpreter(memory, input_val = phase_setting)
                   for phase_setting in seq]

    for interp in interpreters:
        interp.iterate_until_done()

    value = 0
    for interp in itertools.cycle(interpreters):
        interp.input_val = value
        interp.iterate_until_done()
        value = interp.output_val

        if all(interp.done for interp in interpreters):
            break

    return value


def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]

    best = max(itertools.permutations(list(range(5))),
               key=lambda seq:test_sequence(memory,seq))
    print(best, test_sequence(memory, best))

    best = max(itertools.permutations(list(range(5,10))),
               key=lambda seq:test_sequence(memory,seq))
    print(best, test_sequence(memory, best))

if __name__ == '__main__':
    main()
