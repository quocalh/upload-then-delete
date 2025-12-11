from Pipeline.settings import *
from OpenGL.GL import *

import numpy as np

# class VBOLayout:
#     def __init__()

class VBO:
    def __init__(self, Vertices):
        self.Vertices = Vertices
        self.VBO = glGenBuffers(1)
        self.Bind()
        glBufferData(GL_ARRAY_BUFFER, self.Vertices.nbytes, self.Vertices, GL_STATIC_DRAW)

    def Bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

    def UnBind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def Delete(self):
        glDeleteBuffers(1, (self.VBO,))


        