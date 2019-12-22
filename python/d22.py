#!/usr/bin/env python3

import util


def increment(deck, n):
    num_cards = len(deck)
    indexed = list(enumerate(deck))
    indexed.sort(key = lambda ic : (ic[0]*n)%num_cards)
    return [c for (i,c) in indexed]


def stack(deck):
    return list(reversed(deck))


def cut(deck, n):
    return deck[n:] + deck[:n]


def part_a_by_array():
    lines = [line.strip()
             for line in util.get_puzzle_input().split('\n')
             if line.strip()]

    num_cards = 10007
    deck = list(range(num_cards))
    for line in lines:
        if line=='deal into new stack':
            deck = stack(deck)
        elif line.startswith('deal with increment'):
            n = int(line.split()[-1])
            deck = increment(deck, n)
        elif line.startswith('cut'):
            n = int(line.split()[-1])
            deck = cut(deck, n)
        else:
            raise ValueError('Unknown shuffle type: "{}"'.format(line))

    print(deck.index(2019))


def parse_input():
    """
    Returns a list of tuples, each one representing a shuffle.
    Each tuple (a,b) gives the location of a card after shuffling,
    y = (a*x + b) % deck_size.

    This uses the correct % operator, which returns a value on [0,deck_size),
    not the broken % operator, which returns a value on (-deck_size,deck_size).
    When I make my C++ version, it will need to be
    y = (((a*x + b) % deck_size) + deck_size) % deck_size
    """

    lines = [line.strip()
             for line in util.get_puzzle_input().split('\n')
             if line.strip()]
    output = []
    for line in lines:
        if line=='deal into new stack':
            output.append( (-1,-1) )
        elif line.startswith('deal with increment'):
            n = int(line.split()[-1])
            output.append( (n,0) )
        elif line.startswith('cut'):
            n = int(line.split()[-1])
            output.append( (1,-n) )
        else:
            raise ValueError('Unknown shuffle type: "{}"'.format(line))
    return output

def merge_commands(commands, deck_size):
    mul = 1
    add = 0
    for com_mul,com_add in commands:
        mul *= com_mul
        add *= com_mul
        add += com_add

        mul %= deck_size
        add %= deck_size

    return mul,add


def repeat_command(command, deck_size, num_repeats):
    mul,add = command

    cum_mul = 1
    cum_add = 0
    as_binary = bin(num_repeats)[2:]
    for i,digit in enumerate(reversed(as_binary)):
        #If bit is non-zero, add it in
        if digit=='1':
            cum_mul *= mul
            cum_add *= mul
            cum_add += add
            cum_mul %= deck_size
            cum_add %= deck_size


        # Square the operator
        # y = m*(m*x + b) + b
        # y = (m*m)*x + m*b + b
        add = (mul+1)*add
        add %= deck_size
        mul = mul*mul
        mul %= deck_size

    return cum_mul, cum_add


def part_a_by_group():
    commands = parse_input()

    num_cards = 10007
    card_pos = 2019

    commands = [merge_commands(commands, num_cards)]

    for mul,add in commands:
        card_pos *= mul
        card_pos += add


# From https://stackoverflow.com/a/54534390/2689797
def modular_multiplicative_inverse(a, m):
    """
    Returns x such that a*x = 1 (mod m)
    """
    lastremainder, remainder = abs(a), abs(m)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y

    g,x,y = lastremainder, lastx * (-1 if a < 0 else 1), lasty * (-1 if m < 0 else 1)
    if g != 1:
        raise ValueError('modinv for {} does not exist'.format(a))
    return x % m


def inverse_command(command, deck_size):
    # y = m*x + b
    # y - b = m*x
    # x = inv(m)*(y-b)
    # x = inv(m)*y - inv(m)*b
    mul,add = command
    invmod = modular_multiplicative_inverse(mul, deck_size)
    return (invmod, -invmod * add)

def part_b():
    deck_size = 119315717514047
    num_repeats = 101741582076661
    final_pos = 2020

    commands = parse_input()
    command = merge_commands(commands, deck_size)
    command = repeat_command(command, deck_size, num_repeats)
    command = inverse_command(command, deck_size)

    output = (final_pos*command[0] + command[1]) % deck_size
    print(output)


def main():
    part_a_by_array()
    part_a_by_group()
    part_b()


if __name__ == '__main__':
    main()
