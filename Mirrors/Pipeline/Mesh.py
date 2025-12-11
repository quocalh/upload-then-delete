# IMAGINE DRAWING OBJECT JUST BY COUPLE OF LINES
# MORE LIKE MODELS
import numpy as np
from typing import Union

from Pipeline.settings import *
from Pipeline.VBO import *
from Pipeline.VAO import *
from Pipeline.IBO import *
from Pipeline.Textures import *


class Mesh:
    MeshList = []
    def __init__(self, Layout: VBO_Layout, Vertices: Union[np.ndarray, np.float32]):
        self.Vertices = Vertices
        self.Layout = Layout
        # self.TextureList = TextureList
        self.Indices = None
        
        self.VAO = VAO(Layout)
        self.VAO.Bind()
        self.VBO = VBO(Vertices)
        
        self.VAO.AttribPointerSetup()
        
        """OPTIONAL: IBO CREATION"""
        self.IBO = None
        if self.Indices:
            self.IBO = IBO(self.Indices)

        self.Mat4_Pos = glm.mat4(1)
        self.Mat4_Rot = glm.mat4(1)
        self.Mat4_Scale = glm.mat4(1)

        self.MeshList.append(self)
    
        
    def Draw(self, Mode = GL_TRIANGLES):
        """
        SHADER HAS TO BE BINDED BEFORE EXECUTE THIS FUNCTION (Shader.Bind())
        """
        """ Set up Texture, (STILL NO CLUE HOW TO MANAGE THE NAME THOUGH)"""
        VerticesCounted = int(len(self.Vertices) // self.Layout.Stride)
        
        self.VAO.Bind()
        glDrawArrays(Mode, 0, VerticesCounted)
    
    def SetPosition(self, Position: glm.vec3):
        self.Mat4_Pos = glm.translate(glm.mat4(1), Position)

    def Delete(self):
        self.VBO.Delete()
        self.VAO.Delete()
        if self.IBO:
            self.IBO.Delete()
    
    @staticmethod
    def DrawAllMesh(Mode = GL_TRIANGLES):
        """ Remember to bind the desired SHADER before this fucntion \n 
            That's all, remember to Unbind the Shader after being used"""
        for mesh in Mesh.MeshList:
            mesh: Mesh = mesh
            mesh.Draw(Mode)




class MeshIBO:
    MeshList = []
    def __init__(self, Layout: VBO_Layout, Vertices: Union[np.ndarray, np.int32], Indices: np.array = None):
        self.Vertices = Vertices
        self.Layout = Layout
        # self.TextureList = TextureList
        # if Indices != None:
        self.Indices = Indices
        
        self.VAO = VAO(Layout)
        self.VAO.Bind()
        self.VBO = VBO(Vertices)
        self.IBO = IBO(self.Indices)
        self.VAO.AttribPointerSetup()


        self.Mat4_Pos = glm.mat4(1)
        self.Mat4_Rot = glm.mat4(1)
        self.Mat4_Scale = glm.mat4(1)

        self.MeshList.append(self)
    
        
    def Draw(self, Mode = GL_TRIANGLES):
        """
        SHADER HAS TO BE BINDED BEFORE EXECUTE THIS FUNCTION (Shader.Bind())
        """
        """ Set up Texture, (STILL NO CLUE HOW TO MANAGE THE NAME THOUGH)"""
        self.VAO.Bind()
        self.IBO.Bind()
        glDrawElements(Mode, len(self.Indices), GL_UNSIGNED_INT, 0)
    
    def SetPosition(self, Position: glm.vec3):
        self.Mat4_Pos = glm.translate(glm.mat4(1), Position)

    def Delete(self):
        self.VBO.Delete()
        self.VAO.Delete()
        self.IBO.Delete()
    
    @staticmethod
    def DrawAllMesh(Mode = GL_TRIANGLES):
        """ Remember to bind the desired SHADER before this fucntion \n 
            That's all, remember to Unbind the Shader after being used"""
        for mesh in MeshIBO.MeshList:
            mesh: Mesh = mesh
            mesh.Draw(Mode)


        
    
