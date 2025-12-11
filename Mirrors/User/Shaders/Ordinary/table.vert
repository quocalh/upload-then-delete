#version 420 core

layout(location = 0) in vec3 iVertexPos;
layout(location = 1) in vec2 iTexCoord;
layout(location = 2) in vec3 iNormal;

uniform mat4 Perspective;

out vec3 Normal;
out vec2 TexCoord;

void main()
{
    gl_Position = Perspective * vec4(iVertexPos, 1);
    Normal = iNormal;
    TexCoord = iTexCoord;
}