import pygame as pg
from OpenGL.GL import *
import numpy as np
import os
import math; from math import tan
import glm
import time

from Pipeline.settings import *
from Pipeline.VAO import * 
from Pipeline.VBO import *
from Pipeline.IBO import *
from Pipeline.FBO import *
from Pipeline.Shaders import *
from Pipeline.Textures import *
from Pipeline.Specialist.Camera import *
from Pipeline.Specialist.Modelloading import *
from Pipeline.Mesh import * 


if __name__ == "__main__":

    """PYTHON & OPENGL SETUP"""
    pg.init()
    pg.event.set_grab(True)
    # glClearColor(0.1, 0.2, 0.3, 1)
    glClearColor(0.0, 0.0, 0.0, 1)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    """CAMERA CREATION"""
    Camera = Camera(glm.vec3(0, 0, -2))
    
    """RESOURCES"""
    current_path = os.getcwd()
    print(current_path)
    Vertices = ReadingOBJ(r"D:\vspython\OPENGL_AFTER_C\SubModule\Assets\Models\Monkey\Monkey.obj")
    Vertices = Vertices.Dictionary["Interleaved"]
    Vertices = np.array(Vertices, dtype = np.float32)
    ''' Currently, we have:  |   Positions_3    |      Texture_2    |         Normals_3          |'''
    layout = VBO_Layout(); layout.AddLayout(3); layout.AddLayout(2); layout.AddLayout(3)
    # layout = VBO_Layout(); layout.AddLayout(3); layout.AddLayout(3); layout.AddLayout(2)
    
    TablePosition = glm.vec3(0)
    MESH_Table = Mesh(layout, Vertices)


    # Vertices = ReadingOBJ(r"")

    """SHADER CREATION"""
    current_path = os.getcwd()

    shader = Shader(
        VertexShader = current_path + r"/Shaders/Phong/triangle.vert",
        FragmentShader = current_path + r"/Shaders/Phong/triangle.frag"
    )

    wall_texture = Texture(current_path + r"\Assets\Textures\brick_diff.png")
    table_Diffuse = Texture(current_path + r"\Assets\Models\Table\table_color.jpg")
    table_SpecularMap = Texture(current_path + r"\Assets\Models\Table\table_specular_map.jpg")

    """ Z - BUFFER CREATION (FOR FINAL POSTPROCESSING) OFF SCREEN RENDER ONLY """
    DepthBufferShader = Shader(
        VertexShader = current_path + r"\Shaders\Z_buffer\ShaderOffScreen\DepthBuffer.vert",
        FragmentShader = current_path + r"\Shaders\Z_buffer\ShaderOffScreen\DepthBuffer.frag" 
    )

    """ FBO CREATION (POST-PROCESSING)"""

    Z_buffer_fbo = FBO(); """ Extracting Z Buffer as a Texture """
    Z_buffer_fbo_screen = ScreenQuad(0, 0)
    Z_buffer_fbo_shader = Shader(
        VertexShader = current_path + r"\Shaders\Z_buffer\z_buffer_fbo.vert",
        FragmentShader = current_path + r"\Shaders\Z_buffer\z_buffer_fbo.frag"
    )

    fbo = FBO(); """ final postprocessing """
    fbo_screen = ScreenQuad(0, 0)
    fbo_shader = Shader(
        VertexShader = current_path + r"\Shaders\postprocessing\fbo.vert", 
        FragmentShader = current_path + r"\Shaders\postprocessing\fbo.frag"
    )

    PreviousTime = time.time()
    while running:
        dt = time.time() - PreviousTime
        PreviousTime = time.time()

        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        """ FIRST PASS (Z - BUFFER) (SHADER)"""
        glClearColor(1.0, 1.0, 1.0, 1)
        """ IF I TURN THIS OFF, I CANT READ glFragCoord.z 😭 (I DONT KNOW WHERE IS IS LOL)"""
        Z_buffer_fbo.Bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        DepthBufferShader.Bind()
        Camera.GetCamMatrix_LookingAround(dt, far = far, near = near); ''' the Camera'''
        Camera.SetUniformForCamMatrix(DepthBufferShader, "Perspective")

        DepthBufferShader.CreateTranslationMatrix("Mat4Pos", glm.vec3(TablePosition))

        DepthBufferShader.SetUniformFloat("Near", near)
        DepthBufferShader.SetUniformFloat("Far", far)

        MESH_Table.Draw(GL_TRIANGLES)
        DepthBufferShader.Unbind()




        """ PRIMARY PASS (2ND) (SHADER) """
        fbo.Bind()
        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        shader.Bind()
        Camera.GetCamMatrix_LookingAround(dt, far = far, near = near); ''' the Camera'''
        Camera.SetUniformForCamMatrix(shader, "Perspective")
        
        shader.SetUniformVec4("SunPos", glm.vec4(0, 1, 0, 1)); '''da Sun'''
        shader.SetUniformVec4("CamPos", glm.vec4(Camera.Position, 1))
        
        TablePosition.y += 0.1 * dt; """ GOMEN AMANAI """
        shader.CreateTranslationMatrix("Mat4Pos", glm.vec3(TablePosition))
        
        Texture.SetProvidedTextureUniform(shader, 
                                          {
                                              "wall"        : wall_texture,
                                              "TableDiffuse": table_Diffuse,
                                              "TableSpecmap": table_SpecularMap,
                                          })
        MESH_Table.Draw(GL_TRIANGLES)
        shader.Unbind()        

        """ FINAL PASS | FOURTH PASS (POST PROCESSING) (FBO) """
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        fbo_shader.Bind()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        
        fbo.SetProvidedTextureUnifrom("ScreenPixel", fbo_shader, 0)
        Z_buffer_fbo.SetProvidedTextureUnifrom("Z_BUFFER", fbo_shader, 1)
        fbo_shader.SetUniformFloat("WIDTH", WIDTH)
        fbo_shader.SetUniformFloat("HEIGHT", HEIGHT)

        fbo_screen.Draw()


        """ NEXT SCENES """
        pg.display.set_caption(f"{clock.get_fps() // 1}")
        pg.display.flip()
        clock.tick(1000)
        
    MESH_Table.Delete()
    

    