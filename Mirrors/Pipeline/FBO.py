from OpenGL.GL import *
import numpy as np

from Pipeline.settings import *
from Pipeline.VBO import *
from Pipeline.VAO import *
from Pipeline.Shaders import *

class FBO:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width, self.height = width, height

        self.FBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

        self.FBO_TextureID = glGenTextures(1); """ Color Buffer """

        glBindTexture(GL_TEXTURE_2D, self.FBO_TextureID)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, 
            GL_RGB, GL_UNSIGNED_BYTE, None
        )
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.FBO_TextureID, 0)
        """
        ColorBuffer(self.FBO) has 32 bits
        In this case, we would use 24 bits for depth buffer
                 the last 8 bits is used for stencil buffer
        """
        self.DepthStencilBuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.DepthStencilBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.width, self.height)



        glBindRenderbuffer(GL_RENDERBUFFER, 0) ; """ AVOID MINOR BUGS IN THE FUTURE PERHAPS? """

        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, 
                                  GL_RENDERBUFFER, self.DepthStencilBuffer)
        
        fboStatus = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if fboStatus != GL_FRAMEBUFFER_COMPLETE:
            print(f"framebuffer: {fboStatus} ")
        self.Unbind()

    def SetProvidedTextureUnifrom(self, name, shader: Shader, Unit: int):
        glActiveTexture(GL_TEXTURE0 + Unit)
        glBindTexture(GL_TEXTURE_2D, self.FBO_TextureID)
        shader.SetUniformi(name, Unit)
    
    def Bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
    
    def Unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def Bind_FBOTexture(self):
        """ THERE IS NO GL_ACTIVE_TEXTURE FUNCTION IN HERE """
        glBindTexture(GL_TEXTURE_2D, self.FBO_TextureID)

    def Unbind_FBOTexture(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def BindRenderBuffer(self):
        glBindRenderbuffer(GL_RENDERBUFFER, self.DepthStencilBuffer)
    
    def UnbindRenderBuffer(self):
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

    def Delete(self):
        glDeleteTextures(1, (self.FBO_TextureID,))
        glDeleteRenderbuffers(1, (self.DepthStencilBuffer,))
        glDeleteFramebuffers(1, (self.FBO,))




class ScreenQuad: 
    """ GOT TO BE CHANGED SOON TO FIT THE DEMAND """
    def __init__(self, x = 0, y = 0, w = 1, h = 1):
        self.Vertices = np.array([
            x - w, y + h, 0, 1,
            x - w, y - h, 0, 0,
            x + w, y - h, 1, 0,
            
            x - w, y + h, 0, 1,
            x + w, y - h, 1, 0,
            x + w, y + h, 1, 1,
        ], dtype=np.float32)

        ''' |    Positions_2    |        Texture_2      |'''
        self.layout: VBO_Layout = VBO_Layout()
        self.layout.AddLayout(2); self.layout.AddLayout(2); 
        self.VerticesCounted = int(len(self.Vertices) // self.layout.Stride)

        self.VAO = VAO(self.layout)
        self.VAO.Bind();
        self.VBO = VBO(self.Vertices)

        self.VBO.Bind()
        self.VAO.AttribPointerSetup()

    def Draw(self, DrawMode = GL_TRIANGLES):
        self.VAO.Bind()
        glDrawArrays(DrawMode, 0, self.VerticesCounted)

    def Delete(self):
        self.VBO.Delete()
        self.VAO.Delete()

