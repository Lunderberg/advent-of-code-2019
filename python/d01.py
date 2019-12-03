#!/usr/bin/env python3

import util

def fuel(x, tyranny=False):
    output = max(x//3 - 2, 0)
    if output and tyranny:
        return output + fuel(output, tyranny=True)
    else:
        return output

def main():
    inputs = [int(x) for x in util.get_puzzle_input().split()]
    total_fuel = sum(fuel(x) for x in inputs)
    print(total_fuel)
    total_fuel = sum(fuel(x,tyranny=True) for x in inputs)
    print(total_fuel)


if __name__=='__main__':
    main()
