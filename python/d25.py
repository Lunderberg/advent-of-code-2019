#!/usr/bin/env python3

from collections import deque
import inspect
import itertools
import math
import sys
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
    def __init__(self, memory, input_val = None, output_callback = None):
        self.memory = Memory(memory[:])
        self.ip = 0
        self.output_callback = output_callback
        self.input_val = input_val
        self.output_val = None
        self.done = False
        self.paused = False
        self.relative_base = 0

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
            raise ValueError('Unknown mode {} at ip={}, value={}'.format(
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
        if self.input_val is None:
            self.paused = True
            return
        else:
            x = self.input_val
            self.input_val = None

        self.set_param(1, x)
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


    def iterate_until_done(self):
        while not self.done and not self.paused:
            self.iteration()





def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s,r)
                                         for r in range(len(s)+1))



class TextGame:
    def __init__(self,memory):
        self.lines = []
        self.current_line = ''

        self.current_room = None
        self.known_rooms = {}

        self.interp = Interpreter(memory, output_callback=self.output_callback)
        self.interp.iterate_until_done()
        self.on_enter_room(None)

        self.inventory = set()

    def output_callback(self, c):
        if c < 128:
            c = chr(c)
            print(c, end='')

            if c=='\n':
                self.lines.append(self.current_line)
                self.current_line = ''
            else:
                self.current_line += c
        else:
            raise ValueError('Non-ASCII value: {}'.format(c))

    def send_command(self, command):
        print('Command =',command)
        for c in command+'\n':
            self.interp.input_val = ord(c)
            self.interp.iterate_until_done()

        if command in ['north', 'south', 'east', 'west']:
            self.on_enter_room(command)

        if command.split()[0] == 'take':
            item = command.split(maxsplit=1)[1]
            self.inventory.add(item)

        if command.split()[0] == 'drop':
            item = command.split(maxsplit=1)[1]
            self.inventory.remove(item)

    def current_room_description(self):
        idx_loc = [i for i,line in enumerate(self.lines)
                   if line.startswith('==')][-1]
        try:
            idx_loc_end = next(i for i,line in enumerate(self.lines)
                               if i>idx_loc and line=='Command?')
        except StopIteration:
            return

        lines = self.lines[idx_loc:idx_loc_end]

        name = lines[0][3:-3]

        doors = []
        if 'Doors here lead:' in lines:
            idx_doors_start = lines.index('Doors here lead:')
            for line in lines[idx_doors_start+1:]:
                if not line:
                    break
                doors.append(line[2:])


        items = []
        if 'Items here:' in lines:
            idx_items_start = lines.index('Items here:')
            for line in lines[idx_items_start+1:]:
                if not line:
                    break
                items.append(line[2:])

        return dict(name=name, doors=doors, items=items)


    def on_enter_room(self, direction):
        prev_room = self.current_room

        desc = self.current_room_description()
        if desc is None:
            self.current_room = None
            return

        self.current_room = desc['name']


        if self.current_room in self.known_rooms:
            known = self.known_rooms[self.current_room]
        else:
            known = {}
            self.known_rooms[self.current_room] = known


        if prev_room is not None and direction is not None:
            prev_known = self.known_rooms[prev_room]
            prev_known['doors'][direction] = desc['name']


        if 'name' not in known:
            known['name'] = desc['name']

        if 'doors' not in known:
            known['doors'] = {d:None for d in desc['doors']}

        # Overwrite in case of revisiting rooms
        known['items'] = desc['items']



    def path_to(self, target):
        # BFS to find a door that leads somewhere unknown.  Could
        # speed this up by assuming that north/south and east/west are
        # opposites, but simpler not to assume.

        # target=None finds an unexplored room
        to_visit = deque()
        to_visit.append(self.current_room)
        paths = {self.current_room: []}

        while to_visit:
            name = to_visit.popleft()
            room = self.known_rooms[name]
            path = paths[name]
            for direction,other_room in room['doors'].items():
                new_path = path+[direction]
                if other_room == target:
                    return new_path
                else:
                    if other_room not in paths:
                        paths[other_room] = new_path
                        to_visit.append(other_room)

        return None

    def go_to(self, target):
        path = self.path_to(target)
        if path is None:
            raise ValueError('No path to {}'.format(target))

        for command in path:
            self.send_command(command)

    def explore_all(self, collect_items=True):
        while True:
            try:
                self.go_to(None)
            except ValueError:
                break

            if collect_items:
                self.collect_items()


    def collect_items(self):
        forbidden_items = ['photons',
                           'escape pod',
                           'infinite loop',
                           'giant electromagnet',
                           'molten lava',
        ]

        items = self.known_rooms[self.current_room]['items']
        for item in items:
            if item not in forbidden_items:
                self.send_command('take {}'.format(item))


    def state(self):
        output = []
        for name,room in sorted(self.known_rooms.items()):
            output.append('-----------')
            output.append('Name: {}'.format(name))
            for direction,other_room in sorted(room['doors'].items()):
                output.append('{}: {}'.format(direction, other_room))

        return '\n'.join(output)


    def security_checkpoint(self):
        self.go_to('Security Checkpoint')

        direction = next(door for door,name in
                         self.known_rooms['Security Checkpoint']['doors'].items()
                         if name=='Security Checkpoint')

        too_light = []
        too_heavy = []

        all_items = sorted(self.inventory)

        for itemset in powerset(all_items):
            itemset = set(itemset)
            if (any(itemset.issuperset(prev) for prev in too_heavy) or
                any(itemset.issubset(prev) for prev in too_light)):
                continue

            for item in list(self.inventory):
                self.send_command('drop {}'.format(item))
            for item in itemset:
                self.send_command('take {}'.format(item))

            self.send_command(direction)
            if self.current_room != 'Security Checkpoint':
                break

            reject_line = next(line for line in reversed(self.lines)
                               if 'Droids on this ship' in line)
            if 'lighter' in reject_line:
                too_heavy.append(set(itemset))
            elif 'heavier' in reject_line:
                too_light.append(set(itemset))

        else:
            print('Could not find the correct combination')



def main():
    memory = [int(x.strip()) for x in
              util.get_puzzle_input().split(',')]
    game = TextGame(memory)

    game.explore_all()
    game.security_checkpoint()


if __name__ == '__main__':
    main()
