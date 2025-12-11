from pygame.locals import *
import pygame as pg
from OpenGL.GL import *

from Pipeline.settings import *
from Pipeline.Shaders import *

class Texture:
    TextureUnit = 0
    def __init__(self, Path):
        self.Path = Path

        self.TextureID = glGenTextures(1)
        Texture.TextureUnit += 1
        
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
        
        self.SetWrapMode(GL_REPEAT, GL_REPEAT)
        self.SetFilterMode(GL_NEAREST, GL_LINEAR)
        self.LoadImage()
        glBindTexture(GL_TEXTURE_2D, 0)

    def Bind(self, Unit):
        glActiveTexture(GL_TEXTURE0 + Unit)
        glBindTexture(GL_TEXTURE_2D, self.TextureID)
    
    def Unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def Delete(self):
        glDeleteTextures(1, (self.TextureID,))
    
    @staticmethod
    def SetWrapMode(Wrap_s, Wrap_t):
        '''
        imagine it like skew in photoshop or (the wrapper wrapping around the gift boxes), it chooses approriate mode for certain distortion
        '''
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, Wrap_s)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, Wrap_t)
    
    @staticmethod
    def SetFilterMode(MinFilter, MagFilter):
        '''
        These function MinMagFileter helps textures to scale up, scale down to the valid proportion
        we chose the approriate mode to make it looks as good as possible
        '''
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, MinFilter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, MagFilter)
    
    def LoadImage(self):
        image = pg.image.load(self.Path).convert_alpha()
        width, height = image.get_rect().width, image.get_rect().height
        image_data = pg.image.tostring(image, "RGBA") 
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    
    def TextureUniformBind(self, shader: Shader, Unit: int, Name: str):
        """
        Exec it before render objects
        """
        self.Bind(Unit)
        shader.SetUniformi(Name, Unit)
        

    @staticmethod
    def SetProvidedTextureUniform(shader: Shader, TexHashmap: dict[str]):
        """
        only exec it when the shader is Binded
        """
        for index, Tex_key in enumerate(TexHashmap):
            Tex_bucket: Texture = TexHashmap[Tex_key]
            Tex_bucket.TextureUniformBind(shader, index, Tex_key)
            # print(index, Tex_key, Tex_bucket.Path)

    @staticmethod
    def SetProvidedNamelessTextureUniform(shader: Shader, ListOfTextures: list):
        """
        only exec when the shader is binded
        """
        for index, texture in enumerate(ListOfTextures):
            texture_name = "texture" + str(index)
            texture: Texture = texture
            texture.TextureUniformBind(shader, index, texture_name)
            
            

class CubeMapTextureCombineTexture:
    def __init__(self, path):
        self.path = path
        self.CombinedImage = pg.image.load(self.path).convert_alpha()
        self.SkyBoxFaces = []
        
        # Define face order for cubemap
        Order_Based_Index = (
            (2, 1), # right
            (0, 1), # left
            (1, 0), # top
            (1, 2), # bottom
            (1, 1), # front
            (3, 1), # back
        )
        
        SubWidth = self.width // 4
        SubHeight = self.height // 3

        for x, y in Order_Based_Index:
            left = x * SubWidth
            top = y * SubHeight
            size = (SubWidth, SubHeight)
            SubSurface = self.CombinedImage.subsurface(pg.Rect(left, top, *size)).convert()
            self.SkyBoxFaces.append(SubSurface)

        self.CubeMapTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.CubeMapTexture)
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        for i in range(len(self.SkyBoxFaces)):
            self.LoadImageBuffer(self.SkyBoxFaces[i], GL_TEXTURE_CUBE_MAP_POSITIVE_X + i)

        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    def LoadImageBuffer(self, ImageSurface: pg.Surface, target):
        image_data = pg.image.tostring(ImageSurface, "RGBA", True)
        glTexImage2D(target, 0, GL_RGBA, self.subwidth, self.subheight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    @property
    def width(self):
        return self.CombinedImage.get_rect().width

    @property
    def height(self):
        return self.CombinedImage.get_rect().height

    @property
    def subwidth(self):
        return self.width // 4

    @property
    def subheight(self):
        return self.height // 3

    def Bind(self):
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.CubeMapTexture)
