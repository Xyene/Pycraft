#!/usr/bin/python
'''Here, each face is defined as a bit.
    When we want to set a block's visibility, we can use
    the or (|) operator to add them together. Essentially,
    00001 |
    00010
    -----
    00011
    
    To check if a visibility flag shows a specific face, we use the
    and (&) operator. That is:
    flag & TOP
    If the result of the & operation != 0, then that flag exists.
'''
TOP    = 0b000001
BOTTOM = 0b000010
NORTH  = 0b000100
EAST   = 01001000
SOUTH  = 0b010000
WEST   = 0b100000
ALL = TOP | BOTTOM | NORTH | EAST | SOUTH | WEST

TEX_GRASS_TOP  = (32, 32, 16, 16)
TEX_GRASS_SIDE = (0, 0, 16, 16)
TEX_DIRT       = (32, 0, 16, 16)
TEX_STONE      = (0, 32, 16, 16)

class Block:
    def __init__(self, top, bottom, north, east, south, west):
        self.top = top
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.bottom = bottom
        
DIRT = Block(TEX_DIRT, TEX_DIRT, TEX_DIRT, TEX_DIRT, TEX_DIRT, TEX_DIRT)
GRASS = Block(TEX_GRASS_TOP, TEX_DIRT, TEX_GRASS_SIDE, TEX_GRASS_SIDE, TEX_GRASS_SIDE, TEX_GRASS_SIDE)
STONE = Block(TEX_STONE, TEX_STONE, TEX_STONE, TEX_STONE, TEX_STONE, TEX_STONE)
