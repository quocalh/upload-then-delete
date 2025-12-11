#version 420 core


in vec3 TexCoord;

out vec4 f_color;

// layout (binding = 0) uniform samplerCube skybox;

void main()
{
    // f_color = texture(skybox, TexCoord);
    f_color = vec4(0.32, 1.0, 0.0, 1.0);
}
