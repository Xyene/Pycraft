#!/usr/bin/python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
from pyglet.window import key, mouse

class Camera:
    def __init__(self, aspectRatio, x, y, z, pitch, yaw, roll, zNear, zFar):
        self.aspectRatio = aspectRatio
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.zNear = zNear
        self.zFar = zFar
        self._x = -1
        self._y = -1

    def move_to(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def rotate_to(self, pitch, yaw, roll):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def apply_perspective(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(80, self.aspectRatio, self.zNear, self.zFar)
        glPopAttrib()

    def translate(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(GL_MODELVIEW)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glRotatef(self.roll, 0, 0, 1)
        glTranslatef(-self.x, -self.y, -self.z)
        glPopAttrib()

    def move(self, dx, dy, dz):
        self.z += dx * cos(radians(self.yaw - 90)) + dz * cos(radians(self.yaw));
        self.x -= dx * sin(radians(self.yaw - 90)) + dz * sin(radians(self.yaw));
        self.y += dy * sin(radians(self.pitch - 90)) + dz * sin(radians(self.pitch));

    def mouse_move(self, dx, dy):
        #if self._x != -1 and self._y != -1:
        MAX_LOOK_UP = 90
        MAX_LOOK_DOWN = -90
        #dx = -((self._x - x) * 0.8)
        #dy = (self._y - y) * 0.8
        if self.yaw + dx >= 360:
            self.yaw = self.yaw + dx - 360
        elif self.yaw + dx < 0:
            self.yaw = 360 - self.yaw + dx
        else:
            self.yaw += dx

        if self.pitch - dy >= MAX_LOOK_DOWN and self.pitch - dy <= MAX_LOOK_UP:
            self.pitch += -dy
        elif self.pitch - dy < MAX_LOOK_DOWN:
            self.pitch = MAX_LOOK_DOWN
        elif self.pitch - dy > MAX_LOOK_UP:
            self.pitch = MAX_LOOK_UP
        #self._x, self._y = x, y
        '''cx = glutGet(GLUT_WINDOW_WIDTH) / 2 + glutGet(GLUT_WINDOW_X) # Get center x of window
        cy = glutGet(GLUT_WINDOW_HEIGHT) / 2 + glutGet(GLUT_WINDOW_Y) # Get center y of screen'''
        '''GLUT_WINDOW_HEIGHT does not return the height of the client area, so we must
           compensate by checking if delta y is > 40 (more than the window's header).'''        
        '''if abs(cx - x) < 10 and abs(cy - y) < 40:
            self._x, self._y = x, y
        else:
            self._x, self._y = cx, cy
            glutWarpPointer(cx, cy)'''

    def keyboard(self, delta, speedX, speedY, speedZ, symbol):
        keyUp = symbol == key.W
        keyDown = symbol == key.S
        keyLeft = symbol == key.A
        keyRight = symbol == key.D
        flyUp = symbol == key.SPACE 
        flyDown = symbol == key.LSHIFT 

        if keyUp and keyRight and not keyLeft and not keyDown:
            self.move(speedX * delta * 0.003, 0, -speedZ * delta * 0.003)

        if keyUp and keyLeft and not keyRight and not keyDown:
            self.move(-speedX * delta * 0.003, 0, -speedZ * delta * 0.003)
        
        if keyUp and not keyLeft and not keyRight and not keyDown:
            self.move(0, 0, -speedZ * delta * 0.003)

        if keyDown and keyLeft and not keyRight and not keyUp:
            self.move(-speedX * delta * 0.003, 0, speedZ * delta * 0.003)

        if keyDown and keyRight and not keyLeft and not keyUp:
            self.move(speedX * delta * 0.003, 0, speedZ * delta * 0.003)

        if keyDown and not keyUp and not keyLeft and not keyRight:
            self.move(0, 0, speedZ * delta * 0.003)

        if keyLeft and not keyRight and not keyUp and not keyDown:
            self.move(-speedX * delta * 0.003, 0, 0)

        if keyRight and not keyLeft and not keyUp and not keyDown:
            self.move(speedX * delta * 0.003, 0, 0)

        if flyUp and not flyDown:
            self.y += speedY * delta * 0.003

        if flyDown and not flyUp:
            self.y -= speedY * delta * 0.003

    def direction(self):
        m = cos(radians(self.pitch))

        dy = -sin(radians(self.pitch))
        dx = cos(radians(self.yaw - 90)) * m
        dz = sin(radians(self.yaw - 90)) * m
        return (dx, dy, dz)
