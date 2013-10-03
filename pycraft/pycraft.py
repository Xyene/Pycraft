#!/usr/bin/python
from tesselator import *
from camera import Camera
from block import *
from texture import *
from world import World
from o_chunk_provider import OverworldChunkProvider
from world_renderer import WorldRenderer

try:
    from pyglet import image
    from pyglet.gl import *
    from pyglet.window import key, mouse
    import pyglet
except:
    print "Pyglet not installed correctly, or at all."

from camera import Camera
import sys
from math import *
import time
import random

class PycraftApplet(pyglet.window.Window):             
    def load_textures(self):
        print 'Loading textures...'      
        # Simply loading the texture binds it to the current OpenGL context
        PycraftApplet.ATLAS_ID = load_texture('assets/terrain.png')

    def update(self, dt):
        for symbol in self.keys:
            if self.keys[symbol]:
                x, y, z = self.cam.x, self.cam.y, self.cam.z
                self.cam.keyboard(128, self.speed, self.speed, self.speed, symbol)
                dx, dy, dz = self.cam.x, self.cam.y, self.cam.z

                bdx, bdy, bdz = int(dx / 2), int(dy / 2), int(dz / 2)
                bx, by, bz = int(x / 2), int(y / 2), int(z / 2)
                
                _x, _y, _z = dx, dy, dz

                height = 2
                
                for i in xrange(-height, height):
                    if self.world.get_block((bdx, bdy - height, bdz)):
                        _y = y
                        break
                if self.world.get_block((x, _y, bdz + 1)):
                    _z = z
             
                self.cam.x, self.cam.y, self.cam.z = _x, _y, _z
                chunk = (bdx / 8, bdz / 8)
                if chunk not in self.queued:
                    self.world.generate_chunk(chunk, async=True)
                    self.queued.append(chunk)
                        

    def __init__(self, *args, **kwargs):
        super(PycraftApplet, self).__init__(*args, **kwargs)
        self.queued = []
        self.world = World("overworld", OverworldChunkProvider(random.randint(1, 20))) # That seed.
        self.speed = 2
        self.world_renderer = WorldRenderer(self.world)
        self.keys = {}
        self.label = pyglet.text.Label('', font_name='Consolas', font_size = 13, x = 10, y = self.height - 20, color = (0, 0, 0, 255))
        # Resize is called on window start anyways, so we can start with 0 values.
        self.cam = Camera(0, 0, 60, 0, 0, 0, 0, 0, 0)

        self.exclusive = False
        TPS = 40 # Update 40 times a second
        pyglet.clock.schedule_interval(self.update, 1.0 / TPS)

        glEnable(GL_TEXTURE_2D)

        glClearColor(0.78, 0.86, 1.0, 1)
        glClearDepth(1.0)

        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_POLYGON_OFFSET_FILL) # Stops z-buffer fighting

        # Comment if PyCraft lags
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.78, 0.86, 1.0, 1))
        glHint(GL_FOG_HINT, GL_NICEST)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # Specify how close fog should start to the camera
        glFogf(GL_FOG_START, 100.0)
        glFogf(GL_FOG_END, 200.0)
        self.cam.apply_perspective()
        glMatrixMode(GL_MODELVIEW)
        self.load_textures()

    def set_exclusive_mouse(self, exclusive):
        super(PycraftApplet, self).set_exclusive_mouse(exclusive) # Pass to parent
        self.exclusive = exclusive # Toggle flag
 
    def selected_block(self):
        '''Write-only code to determine which block the player is looking at.
            If this stops working, abandon all hope.
            And cry.'''
        c = self.cam
        (dx, dy, dz) = c.direction()

        # Multiply the direction vector by 0..64 and check if a block exists there
        for m in xrange(64):
            # pos is always in world units; / 2 to get array index
            (x, y, z) = int(dx * m + c.x), int(dy * m + c.y), int(dz * m + c.z)
            chunk_pos = (x / 8 / 2, z / 8 / 2) # / by 8 to get chunk, and / 2 to get it in world coords
            '''if self.world.get_block((pos[0] / 2 & ~1, pos[1] / 2 & ~1, pos[2] / 2 & ~1)):
                print "yes."
                return (pos[0] & ~1, pos[1] & ~1, pos[2] & ~1)'''
            
            if chunk_pos in self.world.chunks: # Chunk is generated and exists
                ch_x = x / 2 % 8 # the block chosen in a chunk is the block % 8, as each chunk is 8x8
                ch_z = z / 2 % 8

                if (ch_x, y / 2, ch_z) in self.world.chunks[chunk_pos].data: # Check if our chunk does exist
                    return (ch_x * 2 + chunk_pos[0] * 8 * 2, y & ~1, ch_z * 2 + chunk_pos[1] * 8 * 2)
        return None # Player is not looking at a block, or is too far from a block

    def on_mouse_press(self, x, y, button, modifiers):
        if self.exclusive:
            block = self.selected_block()
            if block:
                chunk = (int(block[0] / 8 / 2), int(block[2] / 8 / 2))
                self.world.chunks[chunk].data.pop((block[0] / 2 % 8, block[1] / 2, block[2] / 2 % 8), None) # Remove the block from the world
                self.world_renderer.mark_chunk_dirty(chunk)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.exclusive: # Only handle camera movement if mouse is grabbed
            self.cam.mouse_move(dx, dy)

    def on_key_press(self, symbol, modifiers):
        if self.exclusive: # Only handle keyboard input if mouse is grabbed
            if symbol == key.ESCAPE:
                sys.exit() # Quit game
            if symbol == key.E:
                self.set_exclusive_mouse(False) # Escape mouse
            elif symbol == key.F:
                self.set_fullscreen(not self.fullscreen)
            elif symbol == key.NUM_ADD:
                self.speed += 3
            elif symbol == key.NUM_SUBTRACT:
                self.speed -= 3
            else:
                self.keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.keys[symbol] = False

    def on_resize(self, width, height):
        height = max(height, 1) # Prevent / by 0
        self.label.y = height - 20
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # A field of view of 45
        gluPerspective(45.0, width / float(height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.cam.translate()
        self.world_renderer.draw_chunks((int(self.cam.x / 8 / 2), int(self.cam.z / 8 / 2)), 3)

        # Draw focused block frame
        block = self.selected_block()
        if block:      
            glPolygonOffset(1, 1)
            # Disable textures; we don't want our focus to be textured!
            glDisable(GL_TEXTURE_2D)
            glPushAttrib(GL_CURRENT_BIT)
            # Black cursor colour
            glColor3f(0, 0, 0)
            # Will have a thickness of 2
            glLineWidth(2)
            # Start drawing in wireframe mode
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            '''Draw with a quad. The current polygon mode will only draw the edges, so if we
                were to use triangles, then there would be an edge cutting through the the 
                selected block's faces.'''
            glBegin(GL_QUADS)
            # Trick tesselator into drawing without texture by passing null block
            draw_face(None, block[0], block[1], block[2], ALL)
            glEnd()
            # Exit wireframe; start filling
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()
            glEnable(GL_TEXTURE_2D)

        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity(); 

        x, y, z = self.cam.x, self.cam.y, self.cam.z
        self.label.text = '%d FPS\n@ (x=%.2f, y=%.2f, z=%.2f, cx=%s, cy=%s)\n%s chunks loaded.' % (pyglet.clock.get_fps(), x, y, z, int(self.cam.x / 8 / 2), int(self.cam.z / 8 / 2), len(self.world.chunks))
        self.label.draw()
        
        glPushAttrib(GL_CURRENT_BIT | GL_LINE_BIT)
        glColor3f(0, 0, 0)
        glLineWidth(3)
        glBegin(GL_LINES)
        CROSSHAIR_SIZE = 15
        glVertex2f(width / 2 - CROSSHAIR_SIZE, height / 2)
        glVertex2f(width / 2 + CROSSHAIR_SIZE, height / 2)
        glVertex2f(width / 2, height / 2 - CROSSHAIR_SIZE)
        glVertex2f(width / 2, height / 2 + CROSSHAIR_SIZE)
        glEnd()
        glPopAttrib()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)

