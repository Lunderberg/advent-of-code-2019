#!/usr/bin/env python3

import util

class Interpreter:
    def __init__(self, memory):
        self.memory = memory
        self.ip = 0

    def iteration(self):
        opcode = self.memory[self.ip]
        if opcode == 99:
            return True

        ai = self.memory[self.ip+1]
        a = self.memory[ai]
        bi = self.memory[self.ip+2]
        b = self.memory[bi]

        if opcode == 1:
            x = a+b
        elif opcode == 2:
            x = a*b
        else:
            raise ValueError('Unknown opcode: {}'.format(opcode))

        xi = self.memory[self.ip+3]
        self.memory[xi] = x
        self.ip += 4

        return False

    def iterate_until_done(self):
        done = False
        while not done:
            done = self.iteration()



def apply_func(a, b, memory):
    memory = memory[:]
    memory[1] = a
    memory[2] = b

    interp = Interpreter(memory)
    interp.iterate_until_done()

    return interp.memory[0]


def main():
    memory = [int(x.strip()) for x in
               util.get_puzzle_input().split(',')]

    print(apply_func(12, 2, memory))

    for a in range(100):
        for b in range(100):
            output = apply_func(a, b, memory)
            if output == 19690720:
                print(a,b)

if __name__ == '__main__':
    main()
