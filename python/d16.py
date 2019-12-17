#!/usr/bin/env python3

import functools
import itertools

import numpy as np

import util

def get_pattern(length, repeats):
    x = np.arange(length)
    # Offset pattern earlier by 1
    x += 1
    # Repat value
    x //= repeats
    # Convert to [0,1,2,3]
    x %= 4
    # Converts [0,1,2,3] => [0,1,0,-1]
    x = (x & 1) * (1 - (x & 2))
    return x

def fft_iter(vals):
    output = []
    vals = np.array(vals)
    length = len(vals)
    for i in range(length):
        pattern = get_pattern(length, repeats=i+1)
        new_val = abs((pattern*vals).sum()) % 10
        output.append(new_val)
    return output


def fft_iter_second_half(vals):
    vals = np.array(vals)
    vals = vals[::-1].cumsum()[::-1]
    vals = np.abs(vals)%10
    return vals




def part_a():
    # 17 minutes
    inputs = util.get_puzzle_input()
    vals = [int(c) for c in inputs if c.strip()]
    length = len(vals)
    vals_a = vals[:]

    for i in range(100):
        vals = fft_iter(vals)

    first_8 = ''.join(map(str,vals[:8]))
    print(first_8)

def part_b():
    inputs = util.get_puzzle_input()

    message_input = int(inputs[:7])
    vals = [int(c) for c in inputs if c.strip()]
    vals = vals*10000

    for i in range(100):
        vals = fft_iter_second_half(vals)

    output = ''.join(map(str,vals))
    print(output[message_input:message_input+8])



def main():
    part_a()
    part_b()

if __name__ == '__main__':
    main()
