#!/usr/bin/env python3

import collections
import util

def is_password_part1(x):
    digits = list(str(x))

    has_double = len(set(digits)) < len(digits)
    increasing = all(int(a)<=int(b) for (a,b) in zip(digits[:-1],digits[1:]))
    return has_double and increasing

def is_password_part2(x):
    digits = list(str(x))

    digit_counts = collections.Counter(digits)
    has_double = any(b==2 for (a,b) in digit_counts.items())

    increasing = all(int(a)<=int(b) for (a,b) in zip(digits[:-1],digits[1:]))
    return has_double and increasing

def main():
    min_val = 402328
    max_val = 864247

    print(sum(1 for i in range(min_val,max_val+1) if is_password_part1(i)))
    print(sum(1 for i in range(min_val,max_val+1) if is_password_part2(i)))

if __name__ == '__main__':
    main()
