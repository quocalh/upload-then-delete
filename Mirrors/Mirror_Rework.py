import pygame as pg
from OpenGL.GL import *
import numpy as np
import os
import math; from math import tan
import glm
import time
import imgui

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


from MirrorMesh import *
pg.event.set_grab(True)
WIREFRAME_TOGGLE = False




# Camera Creation
UserCamera = Camera(glm.vec3(0, 0, -2))
UserCamera.OriginVelocity = 8

# shader
Shader_FBO_Mirror = Shader(VertexShader = r"D:\vspython\OPENGL_AFTER_C\Mirrors\Shaders\MirrorFBO.vert",
                    FragmentShader = r"D:\vspython\OPENGL_AFTER_C\Mirrors\Shaders\MirrorFBO.frag")

Shader_Mirror = Shader(VertexShader = r"User\Shaders\Ordinary\shader.vert",
                       FragmentShader = r"User\Shaders\Ordinary\shader.frag")
# FBO
FBO_Mirror = FBO()

# MIRROR MESH
Mirror_Layout = VBO_Layout(); Mirror_Layout.AddLayout(3); Mirror_Layout.AddLayout(3)
MirrorVertices
MirrorIBO = IBO(MirrorIndices)
MirrorMesh = Mesh(Mirror_Layout, MirrorVertices)

# TABLE
TableTextures: dict[str, Texture] = {
    "color" : Texture(r"Assets\Models\Table\table_color.jpg"),
    "occ"   : Texture(r"Assets\Models\Table\table_occlusion_map.jpg"),
    "spec"  : Texture(r"Assets\Models\Table\table_specular_map.jpg")
}
TableVertices = ReadingOBJ(r"Assets/Models/Table/table.obj").GetVBO_data()
TableLayout = VBO_Layout(); TableLayout.AddLayout(3); TableLayout.AddLayout(2); TableLayout.AddLayout(3)

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)


Wavetime = 0

PreviousTime = time.time()
while running:
    dt = time.time() - PreviousTime
    PreviousTime = time.time()

    Wavetime += dt

    # Mirror reflections (DONE IT LATER)
    Texture.SetProvidedTextureUniform()
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_q:
                WIREFRAME_TOGGLE = not WIREFRAME_TOGGLE
    UserCamera.GetCamMatrix_LookingAround(dt)
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.8, 0.9, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    if WIREFRAME_TOGGLE:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    Shader_Mirror.Bind()
    UserCamera.SetUniformForCamMatrix(Shader_Mirror, "Perspective")

    MirrorMesh.VAO.Bind()
    MirrorIBO.Bind()
    glDrawElements(GL_TRIANGLES, MirrorIBO.IndicesCounted, GL_UNSIGNED_INT, None)
    
    Shader_Mirror.Unbind()    



    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    pg.display.flip()
    pg.display.set_caption(f'{clock.get_fps() // 1}')
    clock.tick(100000)
    