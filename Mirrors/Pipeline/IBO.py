from OpenGL.GL import *
from typing import Union
import numpy as np

class IBO:
    def __init__(self, indices):
        self.Indices = indices
        self.IBO = glGenBuffers(1)
        self.IndicesCounted = len(self.Indices)
        self.Bind()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.Unbind()
    
    def Bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.IBO)
    
    def Unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def Delete(self):
        glDeleteBuffers(1, (self.IBO, ))
        