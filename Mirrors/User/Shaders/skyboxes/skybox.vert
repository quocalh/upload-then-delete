#version 420 core

layout (location = 0) in vec3 in_VertexPos;

out vec3 TexCoord;

uniform mat4 Perspective;

void main()
{
    vec4 pos = Perspective * vec4((in_VertexPos, 1));
    gl_Position = pos;
    TexCoord = vec3(in_VertexPos.x, in_VertexPos.y, in_VertexPos.z);
}
