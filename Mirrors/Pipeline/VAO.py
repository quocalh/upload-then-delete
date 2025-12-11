from Pipeline.settings import *
from OpenGL.GL import *

import ctypes
import numpy as np
from enum import Enum, auto




class VBO_Layout:
    def __init__(self):
        self.AttribLayout = []
        self.Stride = 0

    def AddLayout(self, Tray: int):
        self.AttribLayout.append(Tray)
        self.Stride += Tray

class VAO:
    def __init__(self, Layout: VBO_Layout):
        self.Layout: VBO_Layout = Layout
        self.VAO = glGenVertexArrays(1)
        self.Bind()

    def Bind(self):
        glBindVertexArray(self.VAO)
    
    def UnBind(self):
        glBindVertexArray(0)
    
    def Delete(self):
        glDeleteVertexArrays(1, (self.VAO,))

    def AttribPointerSetup(self):
        # self.Bind() # TODO: i doubted this interfere the process so i turned it off

        startPointer = 0
        byteSize = 4
        for index, tray in enumerate(self.Layout.AttribLayout):
            glEnableVertexAttribArray(index)                            # 4 is the np.float 32 size            # 4 is the np.float 32 size             
            glVertexAttribPointer(index, tray, GL_FLOAT, GL_FALSE, 
                                  self.Layout.Stride * byteSize, ctypes.c_void_p(startPointer * byteSize))
            startPointer += tray



    