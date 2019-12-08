#!/usr/bin/env python3

import itertools
import util
import threading
import queue

class Interpreter:
    def __init__(self, memory):
        self.memory = memory[:]
        self.ip = 0
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.done = False
        self.thread = None

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
        x = self.input_queue.get()
        xi = self.memory[self.ip+1]
        self.memory[xi] = x
        self.ip += 2

    def op_output(self):
        a = self.get_param(1)
        self.output_queue.put(a)
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
        while not self.done:
            self.iteration()

    def start_thread(self):
        self.thread = threading.Thread(target=self.iterate_until_done,
                                       daemon=True)
        self.thread.start()



def test_sequence(memory, seq):
    interpreters = [Interpreter(memory) for phase_setting in seq]

    for interp_a,interp_b in zip(interpreters,interpreters[1:]):
        interp_a.output_queue = interp_b.input_queue
    interpreters[-1].output_queue = interpreters[0].input_queue

    for interp,phase_setting in zip(interpreters,seq):
        interp.input_queue.put(phase_setting)

    interpreters[0].input_queue.put(0)

    for interp in interpreters:
        interp.start_thread()

    for interp in interpreters:
        interp.thread.join()

    return interpreters[-1].output_queue.get()


def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input('d07').split(',')]

    best = max(itertools.permutations(list(range(5))),
               key=lambda seq:test_sequence(memory,seq))
    print(best, test_sequence(memory, best))

    best = max(itertools.permutations(list(range(5,10))),
               key=lambda seq:test_sequence(memory,seq))
    print(best, test_sequence(memory, best))

if __name__ == '__main__':
    main()
