import glm
from pygame.locals import*
import pygame as pg
from math import asin, radians, degrees

from Pipeline.settings import *
from Pipeline.Shaders import *


class Camera:
    def __init__(self, Position, Orientation: glm.vec3 = glm.vec3(0, 0, 1), 
                 Sensitivity = 70, width = WIDTH, height = HEIGHT): 
        '''THIS CAN BE CHANGE THROUGHOUT TWEAKS AND INNOVAITON'''
        self.Orientation = Orientation
        self.Up = glm.vec3(0, 1, 0)
        self.Right = glm.normalize(glm.cross(self.Up, self.Orientation))
        
        self.width = width
        self.height = height

        self.Position = Position
        self.aspect = width / height
        self.Sensitivity = Sensitivity
        self.CamMatrix = glm.mat4(1)
        self.Velocity = 3
        self.OriginVelocity = 3

        self.FirstClick = True

    def SetUniformForCamMatrix(self, shader: Shader, name: str):
        shader.SetUniformMat4(name, self.CamMatrix)

    
    def GetCamMatrix_LookingAround(self, dt, near = near, far = far, fovy = FOV / 2):
        """ not really sure how glm, cone perspective work so i copy people codes 😋"""
        self.Perspective = glm.perspective(fovy, self.aspect, near, far)
        self.KeyInput(dt)
        self.MouseInput(dt)

        self.view = glm.mat4(1.0)
        self.projection = glm.mat4(1.0)
        self.projection = glm.perspective(fovy, self.width / self.height, near, far)
        self.view = glm.lookAt(self.Position, self.Position + self.Orientation, self.Up)
        self.CamMatrix = self.projection * self.view
        return self.CamMatrix

    def GetCamMatrix(self, near = near, far = far, fovy = FOV / 2):
        """ not really sure how glm, cone perspective work so i copy people codes 😋"""
        self.Perspective = glm.perspective(fovy, self.aspect, near, far)

        self.view = glm.mat4(1.0)
        self.projection = glm.mat4(1.0)
        self.projection = glm.perspective(fovy, self.width / self.height, near, far)
        self.view = glm.lookAt(self.Position, self.Position + self.Orientation, self.Up)
        self.CamMatrix = self.projection * self.view
        return self.CamMatrix

    def MouseInput(self, dt):
        mouse = pg.mouse.get_pressed()
        if mouse[0]:
            pg.mouse.set_pos((WIDTH / 2, HEIGHT / 2))
            pg.mouse.set_visible(False)
            Impulse = glm.vec2(pg.mouse.get_rel())
            RotateX = Impulse.x * dt * self.Sensitivity
            RotateY = Impulse.y * dt * self.Sensitivity

            # if radians(-85) > - RotateY + asin(self.Orientation.y) and - RotateY < 0:

            if not self.FirstClick:

                The_X_Bar = glm.normalize(glm.cross(self.Orientation, self.Up)); ''' ------------  '''
                self.Orientation = glm.rotate(self.Orientation, glm.radians(-RotateY), The_X_Bar)
                self.Orientation = glm.rotate(self.Orientation, glm.radians(-RotateX), self.Up)

                self.Right = glm.normalize(glm.cross(self.Up, self.Orientation))
                self.FirstClick = False
            else:
                self.FirstClick = False
                
        else:
            self.FirstClick = True
            pg.mouse.set_visible(True)
        
    
    def KeyInput(self, dt):
        keys = pg.key.get_pressed()
        self.Velocity = self.OriginVelocity
        if keys[K_LSHIFT]:
            self.Velocity *= 2
        if keys[K_w]:
            self.Position += self.Orientation * self.Velocity * dt
        if keys[K_s]:
            self.Position -= self.Orientation * self.Velocity * dt
        if keys[K_d]:
            self.Position -= self.Right * self.Velocity * dt
        if keys[K_a]:
            self.Position += self.Right * self.Velocity * dt
        if keys[K_SPACE]:
            self.Position += self.Up * self.Velocity * dt
        if keys[K_LCTRL]:
            self.Position -= self.Up * self.Velocity * dt

        