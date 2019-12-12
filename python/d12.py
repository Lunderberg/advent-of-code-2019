#!/usr/bin/env python3

import copy
import itertools
import math
import util

import numpy as np



def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


class System:
    def __init__(self):
        self.moons = []

    def add_moon(self, x,y,z):
        self.moons.append( dict(pos=np.array([x,y,z]),
                                vel=np.array([0,0,0])))

    def step(self):
        self.update_velocity()
        self.update_position()

    def update_velocity(self):
        for a,b in itertools.combinations(self.moons,2):
            offset = b['pos'] - a['pos']
            dv = np.sign(offset)
            a['vel'] = a['vel'] + dv
            b['vel'] = b['vel'] - dv

    def update_position(self):
        for moon in self.moons:
            moon['pos'] = moon['pos'] + moon['vel']

    def total_energy(self):
        output = 0
        for moon in self.moons:
            potential = np.abs(moon['pos']).sum()
            kinetic = np.abs(moon['vel']).sum()
            output += (potential*kinetic)

        return output


class System1D:
    def __init__(self, init_pos):
        self.pos = np.array(init_pos)
        self.vel = self.pos*0
        self.num_steps = 0

    def step(self):
        self.update_velocity()
        self.update_position()
        self.num_steps += 1

    def update_velocity(self):
        downwards   = (self.pos.reshape((-1,1)) < self.pos).sum(axis=0)
        upwards     = (self.pos.reshape((-1,1)) > self.pos).sum(axis=0)
        self.vel += (upwards-downwards)

    def update_position(self):
        self.pos += self.vel

    def state(self):
        return (*self.pos, *self.vel)


def steps_until_repeat(system):
    tortoise = copy.deepcopy(system)
    hare = copy.deepcopy(system)

    tortoise.step()
    hare.step()
    hare.step()
    while hare.state()!=tortoise.state():
        tortoise.step()
        hare.step()
        hare.step()

    tortoise = copy.deepcopy(system)
    while hare.state()!=tortoise.state():
        tortoise.step()
        hare.step()
    cycle_start = tortoise.num_steps

    hare = copy.deepcopy(tortoise)
    hare.step()
    while hare.state()!=tortoise.state():
        hare.step()
    first_repeat = hare.num_steps

    return first_repeat

def main():
    jup = System()

    # My set
    jup.add_moon(x=1, y=-4, z=3)
    jup.add_moon(x=-14, y=9, z=-4)
    jup.add_moon(x=-4, y=-6, z=7)
    jup.add_moon(x=6, y=-9, z=-11)

    for i in range(1000):
        jup.step()
    print('Energy =',jup.total_energy())

    x = System1D([1,-14,-4,6])
    y = System1D([-4,9,-6,-9])
    z = System1D([3,-4,7,-11])
    xr = steps_until_repeat(x)
    yr = steps_until_repeat(y)
    zr = steps_until_repeat(z)

    print('Until repeat = ',lcm(lcm(xr,yr),zr))


if __name__ == '__main__':
    main()
