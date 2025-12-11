#version 420 core

layout(location = 0) in vec3 iVertexPos;
layout(location = 1) in vec3 iNormal;

in mat4 Perspective;

out vec3 Normal;

void main()
{
    gl_Position = Perspective * vec4(iVertexPos, 1);
    Normal = iNormal;
}