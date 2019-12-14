#!/usr/bin/env python3

from collections import defaultdict
import math

import util

def parse_input():
    inputs = [line.strip()
              for line in util.get_puzzle_input().split('\n')
              if line.strip()]

    outputs = {}
    for line in inputs:
        reaction = {}

        reactants,product = line.split('=>')
        num_product,product = product.strip().split()
        num_product = int(num_product)

        reaction['product'] = product
        reaction['num_product'] = num_product
        reaction['reactants'] = []
        reaction['line'] = line.strip()
        for reactant in reactants.split(','):
            num_reactant,reactant = reactant.strip().split()
            num_reactant = int(num_reactant)
            reaction['reactants'].append( dict(num = num_reactant,
                                               reactant =reactant) )

        outputs[product] = reaction

    return outputs

def calc_ore_needed(reactions, fuel):
    have = defaultdict(int)
    have['FUEL'] = fuel

    while True:
        # Continue until the only items are ORE and negative amounts
        # Negative values indicate additional side products made in
        # excess.
        can_decompose = [(item,amount) for item,amount in have.items()
                         if item!='ORE' and amount>0]
        if not can_decompose:
            break

        to_decompose,amount = can_decompose[0]
        reaction = reactions[to_decompose]

        # Working backwards, need to run the reaction backwards enough
        # times that none of the product remains
        num_reactions = int(math.ceil(amount/reaction['num_product']))

        for reactant in reaction['reactants']:
            have[reactant['reactant']] += reactant['num']*num_reactions

        # Can't just get rid of the value, since it is possible that a
        # different decomposition will also result in the product that
        # we just got rid of.
        have[to_decompose] -= reaction['num_product']*num_reactions

    return have['ORE']


def binary_search(func, target, min_range, max_range):
    if max_range-1 == min_range:
        return (min_range, func(min_range), max_range, func(max_range))

    split = (min_range + max_range)//2
    split_val = func(split)
    if split_val < target:
        return binary_search(func, target, split, max_range)
    else:
        return binary_search(func, target, min_range, split)


def main():
    reactions = parse_input()
    ore_needed = lambda fuel:calc_ore_needed(reactions,fuel)

    print('Ore for 1 fuel:', ore_needed(fuel=1))
    print('Fuel from 10^12 ore:',
          binary_search(ore_needed, int(1e12), 0, int(1e12))[0])



if __name__ == '__main__':
    main()
