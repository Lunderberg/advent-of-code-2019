#!/usr/bin/env python3

import util

import numpy as np

def main():
    inputs = util.get_puzzle_input()
    width = 25
    height = 6

    num_layers = len(inputs)//(width*height)

    layers = []
    for i in range(num_layers):
        layers.append(inputs[i*width*height:(i+1)*width*height])

    checksum_layer = min(layers, key=lambda t:t.count('0'))
    print('Checksum =', checksum_layer.count('1')*checksum_layer.count('2'))

    layers = [np.array([int(c) for c in layer]) for layer in layers]

    running_image = np.zeros(shape=(width*height))
    running_image.fill(2)

    for layer in layers:
        running_image[running_image==2] = layer[running_image==2]

    running_image = running_image.reshape((height,width))

    for i in range(height):
        for j in range(width):
            char = '#' if running_image[i,j] else ' '
            print(char,end='')
        print()

if __name__ == '__main__':
    main()
