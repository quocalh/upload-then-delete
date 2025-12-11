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

from vertices import *
from SkyBoxMeshData import *
pg.event.set_grab(True)


WIREFRAME_TOGGLE = False

# Camera Creation
UserCamera = Camera(glm.vec3(0, 0, -2))
UserCamera.OriginVelocity = 80

# shader
WaterShader = Shader(
    VertexShader = r"User\Shaders\Water.vert",
    FragmentShader = r"User\Shaders\Water.frag" 
)
BillboardShader = Shader(
    VertexShader = r"User\Shaders\Billboards\Billboards.vert",
    FragmentShader = r"User\Shaders\Billboards\Billboards.frag"
)
SkyboxShader = Shader(
    VertexShader = r"User\Shaders\skyboxes\skybox.vert",
    FragmentShader = r"User\Shaders\skyboxes\skybox.frag"
)

Skybox_Vertices = np.array([
    -1.0, -1.0,  1.0,
    -1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0,  1.0,  1.0,
     1.0, -1.0,  1.0,
    -1.0, -1.0,  1.0,
], dtype = np.float32)

Skybox_layout = VBO_Layout(); Skybox_layout.AddLayout(3)
Skybox_Mesh = Mesh(Skybox_layout, Skybox_Vertices)

# WaterVertices = CreateVertices(1000, 1000, 1, (0.7, 0.8, 1))
# WaterVertices_IBO = IBO(WaterVertices.Indices)
# layout = VBO_Layout(); layout.AddLayout(3); layout.AddLayout(3); layout.AddLayout(3)
# Triangle = Mesh(layout, WaterVertices.Vertices)

# The SUN
Sun_layout = VBO_Layout(); Sun_layout.AddLayout(3); Sun_layout.AddLayout(3)
abitray = 2
Sun_Vertices = np.array([
 -5 * abitray, -5 * abitray, 0.0 * abitray, 1, 1, 1,
 5 * abitray, -5 * abitray, 0.0 * abitray, 1, 1, 1,
 -5 * abitray, 5 * abitray, 0.0 * abitray, 1, 1, 1,
 5 * abitray, 5 * abitray, 0.0 * abitray, 1, 1, 1,
 ], dtype = np.float32)
Sun_Position = glm.vec3(-6 * 5, 15 * 3, 500)
Sun_Mesh = Mesh(Sun_layout, Sun_Vertices)

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable( GL_BLEND )


Wavetime = 0

PreviousTime = time.time()
while running:
    dt = time.time() - PreviousTime
    PreviousTime = time.time()

    Wavetime += dt

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


    BillboardShader.Bind()
    Sun_Mesh.VAO.Bind()
    UserCamera.SetUniformForCamMatrix(BillboardShader, "Perspective")
    BillboardShader.CreateTranslationMatrix("Mat4Pos", Sun_Position)
    BillboardShader.SetUniformMat4("View", UserCamera.view)
    BillboardShader.SetUniformVec3("BillboardCenter", glm.vec3(0))
    Sun_Mesh.Draw(GL_TRIANGLE_STRIP)
    BillboardShader.Unbind()

    # glDepthFunc(GL_LEQUAL)
    SkyboxShader.Bind()
    UserCamera.SetUniformForCamMatrix(SkyboxShader, "Perspective")
    # SkyboxShader.SetUniformi("skybox", 0)
    # glActiveTexture(GL_TEXTURE0)
    # glBindTexture(GL_TEXTURE_CUBE_MAP, SkyBox_CubemapTexture.CubeMapTexture)
    # SkyBox_CubemapTexture.Bind()
    Skybox_Mesh.Draw(GL_TRIANGLES)

    SkyboxShader.Unbind()
    # glDepthFunc(GL_LESS)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    pg.display.flip()
    pg.display.set_caption(f'{clock.get_fps() // 1}')
    clock.tick(100000)
    