#!/usr/bin/python
from pycraft import PycraftApplet
from pyglet.gl import *
import pyglet

INITIAL_WIN_HEIGHT = 480
INITIAL_WIN_WIDTH = 640
WIN_TITLE = "Pycraft"

if __name__=='__main__':
    print "Welcome to Pycraft. Your session will begin shortly."
    window = PycraftApplet(width=INITIAL_WIN_WIDTH, height=INITIAL_WIN_HEIGHT, caption=WIN_TITLE, resizable=True)
    pyglet.app.run()