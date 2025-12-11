#version 420 core

layout(location = 0) in vec3 in_VertexPos;
layout(location = 1) in vec3 in_Color;

uniform mat4 Perspective;       // Projection matrix
uniform mat4 View;              // View matrix (camera transformation)
uniform vec3 BillboardCenter;   // Center of the billboard
uniform mat4 Mat4Pos;
uniform mat4 Mat4Scale;

out vec3 Position3D;
out vec3 Color;


void main()
{
    Color = in_Color;
    
    // Calculate the right and up vectors from the view matrix
    vec3 Right = vec3(View[0][0], View[1][0], View[2][0]);
    vec3 Up = vec3(View[0][1], View[1][1], View[2][1]);
    
    // Compute the billboard position in world space
    vec3 BillboardPosition = BillboardCenter + Right * in_VertexPos.x + Up * in_VertexPos.y;
    
    // Transform the billboard position by the view matrix to get camera space
    vec4 ViewSpacePosition = vec4(BillboardPosition, 1.0);
    
    // Project the position to clip space
    gl_Position = Perspective * Mat4Pos * ViewSpacePosition;
    // gl_Position = Perspective * vec4(in_VertexPos, 1);
    Position3D = in_VertexPos;
}
