#!/usr/bin/python
from tesselator import *
from block import *
from texture import *
from world import World

from pyglet import image
from pyglet.gl import *
from pyglet.window import key, mouse
import pyglet

class WorldRenderer(object):
    def __init__(self, world):
        self.cdisplays = {}
        self.world = world
        self.queued = []

    def draw_chunk(self, location):
        if location not in self.cdisplays:
            if location not in self.world.chunks:
                if location not in self.queued:
                    self.world.generate_chunk(location)
                    self.queued.append(location)
                return # Will be gen'd async                
               
        display = 0
        try:
            display = self.cdisplays[location]
        except KeyError:   
            world = self.world
            self.cdisplays[location] = display = glGenLists(1)
            glNewList(self.cdisplays[location], GL_COMPILE)

            data = world.chunks[location].data
            
            glBegin(GL_QUADS)

            cx, cz = location
            cx *= 8
            cz *= 8
            for pos, block in data.iteritems():
                (rx, ry, rz) = pos
                x = rx + cx
                z = rz + cz

                '''Cull all none-visible faces.
                    Excludes those behind blocks or outside projection;
                    Checks if face has air next to it, and only renders if so.
                    BlockFace is a bitwise enum, to store the visible faces of a block
                    as an integer.'''
                face = 0

                if not world.get_block((x, ry + 1, z)):
                    face |= TOP
                if not world.get_block((x, ry - 1, z)):
                    face |= BOTTOM

                if not world.get_block((x + 1, ry, z)):
                    face |= EAST
                if not world.get_block((x - 1, ry, z)):
                    face |= WEST

                if not world.get_block((x, ry, z - 1)):
                    face |= NORTH
                if not world.get_block((x, ry, z + 1)):
                    face |= SOUTH

                if face: # The face is only 0 is no face is exposed
                    draw_face(block, x * 2, ry * 2, z * 2, face)

            glEnd()
            glEndList()                                                     
        glCallList(display)
        
    def mark_chunk_dirty(self, location):
        if location in self.cdisplays:
            # Free the list memory
            glDeleteLists(self.cdisplays[location], 0)
            # Remove list id from displays; will cause recompilation next render loop
            self.cdisplays.pop(location, None)

    def get_displayable_chunks(self, origin, view_distance):
        chunks = []
        # Load all chunks in a square around the origin
        for x in xrange(-view_distance, view_distance + 1):
            for z in xrange(-view_distance, view_distance + 1):
                chunks.append((origin[0] + x, origin[1] + z))
        return chunks

    def draw_chunks(self, origin, view_distance):
        glBindTexture(GL_TEXTURE_2D, 0)
        # Draw chunks we already know are visible
        for displayable in self.cdisplays:
            self.draw_chunk(displayable)

        chunks = self.get_displayable_chunks(origin, view_distance)
        for chunk in chunks:
            if chunk not in self.cdisplays:
                self.draw_chunk(chunk)