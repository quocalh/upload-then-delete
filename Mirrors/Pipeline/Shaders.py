from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm
from enum import Enum

class ENUM_UNIFORM_ERROR(Enum):
    INVALID_UNIFORM_OR_UNIFORM_NOT_FOUND = "[NAH SHADER FUCKED UP] It indicates that you misstype a name but most of the case: FIX YOUR SHADER MAN @@"
class ShaderLoadout:
    def __init__(self, Vertex = None, Fragment = None):
        self.VertexShader = Vertex
        self.FragmentShader = Fragment

class Shader:
    def __init__(self, VertexShader, FragmentShader):
        with open(VertexShader, "r") as file:
            VertexSource = file.readlines()
        with open(FragmentShader, "r") as file:
            FragmentSource = file.readlines()
        self.FragmentSource = FragmentSource
        self.VertexSource = VertexSource
        self.CreateShader()

    def CreateShader(self):
        self.Shader = compileProgram(
            compileShader(self.VertexSource  , GL_VERTEX_SHADER),
            compileShader(self.FragmentSource, GL_FRAGMENT_SHADER),
        )
        return self.Shader
    
    def Bind(self):
        glUseProgram(self.Shader)
    
    def Unbind(self):
        glUseProgram(0)
    
    def SetUniformi(self, name, value: int):
        self.Bind()
        glUniform1i(glGetUniformLocation(self.Shader, name), value)
        
    def SetUniformMat4(self, name, mat4):
        mat4 = np.array(mat4.to_list(), dtype=np.float32)
        self.Bind()
        glUniformMatrix4fv(glGetUniformLocation(self.Shader, name), 1, False, mat4)

    def SetUniformVec4(self, name, vec4):
        vec4 = np.array(vec4.to_list(), dtype=np.float32)
        glUniform4f(glGetUniformLocation(self.Shader, name), vec4[0], vec4[1], vec4[2], vec4[3])
    
    def SetUniformVec3(self, name, vec3):
        vec3 = np.array(vec3.to_list(), dtype=np.float32)
        glUniform3f(glGetUniformLocation(self.Shader, name), vec3[0], vec3[1], vec3[2])
    
    def SetUniformVec2(self, name, vec2):
        vec2 = np.array(vec2.to_list(), dtype=np.float32)
        glUniform2f(glGetUniformLocation(self.Shader, name), vec2[0], vec2[1])

    def SetUniformFloat(self, name, float_value: float):
        glUniform1f(glGetUniformLocation(self.Shader, name), float_value)

    def CreateTranslationMatrix(self, name, Position: glm.vec3):
        PositionMatrix = glm.translate(glm.mat4(1), Position)
        self.SetUniformMat4(name, PositionMatrix) 
        return PositionMatrix

    def CreateRotationMatrix(self, name, RotationMatrix):
        self.SetUniformMat4(name, RotationMatrix)
        return RotationMatrix
    
    def SetProvidedUniform():
        """
        This going to set multiple of textures base on a input Hashmap\n
        Only support mat4, vec3, vec4, int, float (im sowy)\n
        For example:
        urShader.SetProvideUniform({
                                    "lights": np.int32,
                                    "Proportion": float,
                                    "Direction": glm.vec3, 
                                  })
        """
        pass


        