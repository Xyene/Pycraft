#!/usr/bin/python
from chunk import Chunk
from noise import perlin
from block import *

class OverworldChunkProvider(object):
    def __init__(self, seed):
        '''For this simplex noise generator, the period is essentially the seed.
            However, the larger the period, the more memory is consumed.'''
        self.noise = perlin.SimplexNoise(period = seed)

    
    def noise_gen(self, scale, magnitude, x, z):
        return self.noise.noise2(x / scale, z / scale) * magnitude + 15 # Ensure a sea level of 15
    
    def provide_chunk(self, cx, cz):
        '''We store the world as a dictionary.
            In an average world, most of the blocks existing would be air.
            By using a dictionary over a 3D array, we gain the advantage of not
            having to iterate over empty blocks, saving processing time.'''
        data = {}

        # We're given chunk coords; convert to normal coords
        cx *= 8
        cz *= 8

        # Each chunk has a width and height of 8
        for x in xrange(8):
            for z in xrange(8):
                height0 = self.noise_gen(500.0, 8, x + cx, z + cz) # Spread out, tall hills
                height1 = self.noise_gen(64.0, 4, x + cx, z + cz) # Hills packed together but small

                # Chain two generators together, ensuring at least a height of 2
                height = int(max(height0, height1, 2))

                for y in xrange(height - 2): # We will pad the top blocks with grass & dirt
                    data[(x, y, z)] = STONE
                # Add two layers of dirt, and a final layer of grass
                data[(x, height, z)] = GRASS
                data[(x, height - 1, z)] = DIRT
                data[(x, height - 2, z)] = DIRT
        return Chunk(data) # Construct a new Chunk object from our block data