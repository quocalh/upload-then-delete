#version 420 core

in vec3 Color;
in vec3 Position3D;
in vec3 Normal;
in float MaxWaveHeight;
in vec3 OuputSlope;

uniform vec3 CameraPosition;

out vec4 f_color;

// const vec3 SunPosition = vec3(2, 6, 2);
uniform vec3 SunPosition;

float DiffuseLightning(vec3 Normal, vec3 SunPosition, vec3 Position)
{
    vec3 LightDir = normalize(Position - SunPosition);
    float diffuseValue = dot(Normal, -LightDir);
    diffuseValue = (diffuseValue + 1) * 0.5;
    return diffuseValue;
}

float SpecularLightning(vec3 Normal, vec3 SunPosition, vec3 Position, vec3 CameraPosition)
{
    vec3 LightDir = normalize(Position - SunPosition);
    vec3 EyeCast = normalize(Position - CameraPosition);
    vec3 Reflection = reflect(- LightDir, Normal);
    float SpecularValue = dot(Reflection, EyeCast);
    SpecularValue = max(pow(SpecularValue, 30), 0);
    return SpecularValue;
}

void main()
{   
    float Diffuse = DiffuseLightning(Normal, SunPosition, Position3D);
    float Specular = SpecularLightning(Normal, SunPosition, Position3D, CameraPosition);

    float FoamHeight = max(Position3D.y - MaxWaveHeight, 0);
    float FoamOpacity = max(0, pow(FoamHeight, 1.6) - OuputSlope.x * OuputSlope.z) / 10;

    // if (Diffuse > 0.5)
    // {
    //     Diffuse += 0.2;
    // }

    if (Position3D.y > 1)
    {
        Diffuse += pow(max(Position3D.y - 1, 0), 1.4)  * 0.2;
    }



    // float SlopeFactor = abs(OuputSlope.x) + abs(OuputSlope.z);
    // if (SlopeFactor > 0.5)
    // {
    //     Diffuse += 0.6 * pow(min(SlopeFactor - 0.5, 1), 1.4);
    //     // Specular -= 0.2;
    // }
    Diffuse -= 0.15;
    

    f_color = vec4(Color, 1);
    f_color = vec4(Color, 1) * Diffuse + vec4(vec3(Specular) / 2, 0) + vec4(0.3) * FoamOpacity;
    f_color.a = 1.0;



}