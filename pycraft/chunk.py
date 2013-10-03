#!/usr/bin/python
class Chunk(object):
    def __init__(self, blocks = {}):
        self.data = blocks
    
    def set_block(self, location, block):
        self.data[location] = block

    def get_block(self, location):
        return self.data[location]
   
    def rm_block(self, location):
        return self.data.pop(location, None)