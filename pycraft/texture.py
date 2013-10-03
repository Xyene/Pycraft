#!/usr/bin/python
from pyglet import image
from pyglet.gl import *

def load_texture(file):
    raw = image.load(file)
    width, height = raw.width, raw.height
    texture = image.load(file).get_data('RGBA', width * 4) # 4bpp, RGBA format

    buffer = [0] # Buffer to hold the returned texture id
    glGenTextures(1, (GLuint * len(buffer))(*buffer))

    glBindTexture(GL_TEXTURE_2D, buffer[0])
    
    #Load textures with no filtering. Filtering generally makes the texture blur.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture)
    
    return buffer[0]

class TextureAtlas:
    def __init__(self, id, width, height):
        self.id = id
        self.width = float(width)
        self.height = float(height)
        self.bound = False

    def bind_texture_region(self, region):
        self.x, self.y, self.b_width, self.b_height = region
        self.bound = True

    def coord(self, u, v):
        if self.bound:
            glTexCoord2f(((self.x / self.width) - (self.b_width / self.width)) * u, ((self.y / self.height) - (self.b_height / self.height)) * v)