#!/usr/bin/python
import multiprocessing
from functools import partial
from o_chunk_provider import OverworldChunkProvider
import time

def _provide_chunk_async_proxy(provider, loc):
    chunk = provider.provide_chunk(loc[0], loc[1])
    time.sleep(0.5)
    return chunk

class World(object):
    def __init__(self, name, chunk_provider, chunks = {}):
        self.name = name
        self.chunks = chunks
        self.chunk_provider = chunk_provider
        self.pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        self.generation_queue = []
    
    def get_block(self, location):
        x, y, z = location
        chunk = (int(x / 8), int(z / 8))
        if chunk not in self.chunks:
            return None
        return self.chunks[chunk].data.get((x % 8, y, z % 8), None)
    
    def set_block(self, location, block):
        x, y, z = location
        chunk = (x / 8, z / 8)
        if chunk not in self.chunks:
            return
        if block:
            self.chunks[chunk].data[location] = block
        else:
            self.chunks[chunk].data.pop(location, None)
   
    def set_chunk(self, location, chunk):
        if chunk:
            self.chunks[location] = chunk
        else:
            self.chunks.pop(location, None)
        
    def get_chunk(self, location):
        return self.chunks[location] if location in self.chunks else None

    def generate_chunk(self, location, async=True):
        if location not in self.generation_queue:
            if async:
                def call(x):
                    self.chunks[location] = x
                    self.generation_queue.remove(location)
                self.generation_queue.append(location)
                self.pool.apply_async(_provide_chunk_async_proxy, [self.chunk_provider, location], callback=call)
            else:
                self.chunks[location] = self.chunk_provider.provide_chunk(location[0], location[1])