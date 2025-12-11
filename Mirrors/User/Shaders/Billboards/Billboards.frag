#version 420 core

in vec3 Color;
in vec3 BillboardCenter;
in vec3 Position3D;

out vec4 f_color;

uniform mat4 Perspective;
uniform vec3 SunPosition;

void main()
{
    // change billboard world space's center into screen space (this only 4 learnign, use 3d Pos instaead in real practice)
    // vec4 Billboard4DSpace = Perspective * vec4(BillboardCenter, 1);
    // vec3 BillboardClipSpace = Billboard4DSpace.xyz / Billboard4DSpace.w;
    // vec3 BillboardScreenSpace = 0.5 * BillboardClipSpace.xyz + vec3(1);
    
    // if statelment and smooth step based on how close they are to the 
    vec3 Distance = BillboardCenter - Position3D;
    if (length(Distance) > 10)
    {
        discard;
    }
    // float value = smoothstep(0, 5, length(Distance) / 5);
    float value = (10 - length(Distance)) / 1.55 / 1.55;



    f_color = vec4(vec3(Color), value);
}