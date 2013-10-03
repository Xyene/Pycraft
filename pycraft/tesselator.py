#!/usr/bin/python
from pyglet.gl import *
from texture import TextureAtlas
from block import *

a = TextureAtlas(1, 32, 32)
        
def draw_face(block, x, y, z, face):
        c = a.coord
        b = a.bind_texture_region
        if face & TOP:
            if block:
                b(block.top)
            c(0.0, 1.0); glVertex3f(x-1.0, y+ 1.0,z-1.0)
            c(0.0, 0.0); glVertex3f(x-1.0,y+  1.0, z+ 1.0)
            c(1.0, 0.0); glVertex3f(x+ 1.0, y+ 1.0, z+ 1.0)
            c(1.0, 1.0); glVertex3f(x+ 1.0, y+ 1.0, z-1.0)
        if face & BOTTOM:
            if block:
                b(block.bottom)
            c(1.0, 1.0); glVertex3f(x-1.0, y-1.0, z-1.0)
            c(0.0, 1.0); glVertex3f(x+ 1.0, y-1.0, z-1.0)
            c(0.0, 0.0); glVertex3f(x+ 1.0, y-1.0,z+ 1.0)
            c(1.0, 0.0); glVertex3f(x-1.0,y-1.0, z+ 1.0)
        if face & NORTH:
            if block:
                b(block.north)
            c(1.0, 0.0); glVertex3f(x+ 1.0,y+  1.0,z-1.0)
            c(1.0, 1.0); glVertex3f(x+ 1.0, y-1.0, z-1.0)
            c(0.0, 1.0); glVertex3f(x-1.0,y-1.0, z-1.0)
            c(0.0, 0.0); glVertex3f(x-1.0, y+ 1.0,z-1.0)
        if face & SOUTH:
            if block:
                b(block.south)
            c(0.0, 0.0); glVertex3f(x+ 1.0,y+  1.0, z+ 1.0)
            c(1.0, 0.0); glVertex3f(x-1.0, y+ 1.0, z+ 1.0)
            c(1.0, 1.0); glVertex3f(x-1.0, y-1.0,  z+1.0)
            c(0.0, 1.0); glVertex3f(x+ 1.0,y-1.0, z+ 1.0)
        if face & EAST:
            if block:
                b(block.east)
            c(1.0, 0.0); glVertex3f(x+ 1.0, y+ 1.0, z+ 1.0)
            c(1.0, 1.0); glVertex3f(x+ 1.0,y-1.0, z+ 1.0)
            c(0.0, 1.0); glVertex3f(x+ 1.0, y-1.0, z-1.0)
            c(0.0, 0.0); glVertex3f(x+ 1.0,  y+1.0,z-1.0)
        if face & WEST:
            if block:
                b(block.west)
            c(0.0, 0.0); glVertex3f(x-1.0, y+ 1.0, z+ 1.0)
            c(1.0, 0.0); glVertex3f(x-1.0, y+ 1.0,z-1.0)
            c(1.0, 1.0); glVertex3f(x-1.0, y-1.0, z-1.0)
            c(0.0, 1.0); glVertex3f(x-1.0,y-1.0, z+ 1.0)