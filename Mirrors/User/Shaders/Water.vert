# version 420 core

layout (location = 0) in vec3 in_VertexPos;
layout (location = 1) in vec3 in_Normal;
layout (location = 2) in vec3 in_Color;

uniform mat4 Perspective;
uniform float fTime;

out vec3 Normal;
out vec3 Position3D;
out vec3 Color;
out float MaxWaveHeight;
out vec3 OuputSlope;

const float e = 2.718281828459045;
// const int WaveNum = 72;
const int WaveNum = 72/4;
// const int WaveNum = 1;

// Hardcoded wave directions
// const vec2[72] WaveDir = vec2[72](
//     normalize(vec2(0.87, -0.49)),
//     normalize(vec2(-0.23, 0.97)),
//     normalize(vec2(0.42, 0.91)),
//     normalize(vec2(-0.99, -0.11)),
//     normalize(vec2(0.68, -0.74)),
//     normalize(vec2(-0.34, 0.94)),
//     normalize(vec2(0.56, 0.83)),
//     normalize(vec2(-0.76, -0.64)),
//     normalize(vec2(0.21, -0.98)),
//     normalize(vec2(0.95, 0.31)),
//     normalize(vec2(-0.68, 0.73)),
//     normalize(vec2(-0.42, -0.91)),
//     normalize(vec2(0.99, 0.08)),
//     normalize(vec2(-0.78, 0.62)),
//     normalize(vec2(0.59, -0.81)),
//     normalize(vec2(-0.19, -0.98)),
//     normalize(vec2(0.83, 0.56)),
//     normalize(vec2(-0.54, -0.84)),
//     normalize(vec2(0.30, 0.95)),
//     normalize(vec2(-0.93, -0.36)),
//     normalize(vec2(0.70, -0.71)),
//     normalize(vec2(-0.89, 0.45)),
//     normalize(vec2(0.60, 0.80)),
//     normalize(vec2(-0.25, 0.97)),
//     normalize(vec2(0.75, -0.66)),
//     normalize(vec2(-0.61, 0.79)),
//     normalize(vec2(0.89, -0.44)),
//     normalize(vec2(-0.29, 0.96)),
//     normalize(vec2(0.48, -0.87)),
//     normalize(vec2(-0.97, -0.23)),
//     normalize(vec2(0.35, 0.93)),
//     normalize(vec2(-0.83, -0.55)),
//     normalize(vec2(0.76, 0.65)),
//     normalize(vec2(-0.47, -0.88)),
//     normalize(vec2(0.11, -0.99)),
//     normalize(vec2(-0.68, 0.73)),

//     // New Directions
//     normalize(vec2(0.84, -0.54)),
//     normalize(vec2(-0.50, 0.86)),
//     normalize(vec2(0.57, 0.82)),
//     normalize(vec2(-0.91, -0.29)),
//     normalize(vec2(0.63, -0.77)),
//     normalize(vec2(-0.41, 0.91)),
//     normalize(vec2(0.62, 0.77)),
//     normalize(vec2(-0.80, -0.60)),
//     normalize(vec2(0.16, -0.99)),
//     normalize(vec2(0.97, 0.24)),
//     normalize(vec2(-0.72, 0.69)),
//     normalize(vec2(-0.38, -0.93)),
//     normalize(vec2(0.95, 0.33)),
//     normalize(vec2(-0.81, 0.57)),
//     normalize(vec2(0.51, -0.86)),
//     normalize(vec2(-0.26, -0.97)),
//     normalize(vec2(0.76, 0.64)),
//     normalize(vec2(-0.58, -0.81)),
//     normalize(vec2(0.24, 0.97)),
//     normalize(vec2(-0.89, -0.45)),
//     normalize(vec2(0.72, -0.70)),
//     normalize(vec2(-0.84, 0.54)),
//     normalize(vec2(0.59, 0.81)),
//     normalize(vec2(-0.31, 0.95)),
//     normalize(vec2(0.80, -0.60)),
//     normalize(vec2(-0.65, 0.76)),
//     normalize(vec2(0.83, -0.56)),
//     normalize(vec2(-0.28, 0.96)),
//     normalize(vec2(0.54, -0.85)),
//     normalize(vec2(-0.93, -0.33)),
//     normalize(vec2(0.37, 0.93)),
//     normalize(vec2(-0.79, -0.62)),
//     normalize(vec2(0.71, 0.71)),
//     normalize(vec2(-0.48, -0.88)),
//     normalize(vec2(0.12, -0.99)),
//     normalize(vec2(-0.65, 0.75))
// );

// Hardcoded wave directions
const vec2[72] WaveDir = vec2[72](
    normalize(vec2(0.5, 0.5)), // baseline
    normalize(vec2(0.6, 0.4)),
    normalize(vec2(0.4, 0.6)),
    normalize(vec2(0.7, 0.3)),
    normalize(vec2(0.3, 0.7)),
    normalize(vec2(0.8, 0.2)),
    normalize(vec2(0.2, 0.8)),
    normalize(vec2(0.9, 0.1)),
    normalize(vec2(0.1, 0.9)),
    normalize(vec2(1.0, 0.0)),
    normalize(vec2(0.0, 1.0)),
    normalize(vec2(0.7, 0.7)),
    normalize(vec2(0.5, 0.9)),
    normalize(vec2(0.9, 0.5)),
    normalize(vec2(0.6, 0.8)),
    normalize(vec2(0.8, 0.6)),
    normalize(vec2(0.4, 0.9)),
    normalize(vec2(0.9, 0.4)),
    normalize(vec2(0.3, 0.8)),
    normalize(vec2(0.8, 0.3)),
    normalize(vec2(0.5, 0.5)),
    normalize(vec2(0.4, 0.4)),
    normalize(vec2(0.6, 0.6)),
    normalize(vec2(0.3, 0.3)),
    normalize(vec2(0.7, 0.7)),
    normalize(vec2(0.2, 0.2)),
    normalize(vec2(0.8, 0.8)),
    normalize(vec2(0.1, 0.1)),
    normalize(vec2(0.9, 0.9)),
    normalize(vec2(0.0, 0.0)),
    normalize(vec2(0.7, 0.8)),
    normalize(vec2(0.8, 0.7)),
    normalize(vec2(0.6, 0.9)),
    normalize(vec2(0.9, 0.6)),
    normalize(vec2(0.5, 0.7)),
    normalize(vec2(0.7, 0.5)),
    normalize(vec2(0.4, 0.8)),
    normalize(vec2(0.8, 0.4)),
    normalize(vec2(0.6, 0.5)),
    normalize(vec2(0.5, 0.6)),
    normalize(vec2(0.3, 0.7)),
    normalize(vec2(0.7, 0.3)),
    normalize(vec2(0.4, 0.6)),
    normalize(vec2(0.55, 0.55)),
    normalize(vec2(0.75, 0.25)),
    normalize(vec2(0.25, 0.75)),
    normalize(vec2(0.85, 0.15)),
    normalize(vec2(0.15, 0.85)),
    normalize(vec2(0.95, 0.05)),
    normalize(vec2(0.05, 0.95)),
    normalize(vec2(0.65, 0.35)),
    normalize(vec2(0.35, 0.65)),
    normalize(vec2(0.45, 0.55)),
    normalize(vec2(0.55, 0.45)),
    normalize(vec2(0.35, 0.45)),
    normalize(vec2(0.45, 0.35)),
    normalize(vec2(0.25, 0.55)),
    normalize(vec2(0.55, 0.25)),
    normalize(vec2(0.45, 0.75)),
    normalize(vec2(0.75, 0.45)),
    normalize(vec2(0.35, 0.55)),
    normalize(vec2(0.55, 0.35)),
    normalize(vec2(0.65, 0.45)),
    normalize(vec2(0.45, 0.65)),
    normalize(vec2(0.75, 0.55)),
    normalize(vec2(0.55, 0.75)),
    normalize(vec2(0.85, 0.45)),
    normalize(vec2(0.45, 0.85)),
    normalize(vec2(0.25, 0.45)),
    normalize(vec2(0.10, 0.90)), 
    normalize(vec2(0.90, 0.10)), 
    normalize(vec2(-0.7, 0.70))
    // normalize(vec2(0.70, -0.7))  
);



/*
                         __               
   ____ ____  __________/ /_____  ___  _____
  / __ `/ _ \/ ___/ ___/ __/ __ \/ _ \/ ___/
 / /_/ /  __/ /  (__  ) /_/ / / /  __/ /    
 \__, /\___/_/  /____/\__/_/ /_/\___/_/     
/____/                                      
*/

vec3 GetGerstnerWaveAmplitude(float fTime, float steep, float freq, float speed, vec2 DirectionXZ)
{
    // vec3 WavePos = in_VertexPos;
    vec3 WavePos = vec3(0);
    float DirDotXZ = dot(DirectionXZ, vec2(in_VertexPos.x, in_VertexPos.z));
    WavePos.x += in_VertexPos.x + steep * cos(freq * DirDotXZ + speed * fTime);
    WavePos.z += in_VertexPos.z + steep * cos(freq * DirDotXZ + speed * fTime);
    WavePos.y += steep * sin(freq * DirDotXZ + speed * fTime);

    in_VertexPos;
    return WavePos;
}

vec3 GerstnerWave(float fTime)
{

    // float height = 1;
    // // float freq = 0.07;
    // float freq = 0.1;
    // float speed = 4.5;
    // vec3 Pos = vec3(0);
    // vec3 GerstnerNormal = vec3(0); // currently yes (not as good as GPU Gems), blud thought he had the upper hand 💀
    // vec2 Direction;
    // float DirDotXZ;

    // float FreqMult = 1.205;
    // float HeighMult = 0.70;
    // float SpeedMult = 1.08;

    vec3 VertexPos = in_VertexPos;

    float height = 1.4;
    float freq = 0.054;
    float speed = 1.8;
    vec3 Pos = vec3(0);
    vec3 GerstnerNormal = vec3(0); // currently yes (not as good as GPU Gems), blud thought he had the upper hand 💀
    vec2 Direction;
    float DirDotXZ;

    float FreqMult = 1.30;
    float HeighMult = 0.80;
    float SpeedMult = 1.1;

    Direction = WaveDir[0];
    
    DirDotXZ = dot(Direction, vec2(VertexPos.x, VertexPos.z));


    GerstnerNormal.x += height * freq * Direction.x * -1 * sin(freq * DirDotXZ + speed * fTime + 5);
    GerstnerNormal.z += height * freq * Direction.y * -1 * sin(freq * DirDotXZ + speed * fTime + 5);
    DirDotXZ = dot(Direction, vec2(VertexPos.x + GerstnerNormal.x, VertexPos.z + GerstnerNormal.z));

    VertexPos.x += Direction.x;
    VertexPos.z += Direction.y;
    
    Pos.x += height * cos(freq * DirDotXZ + speed * fTime + 5);
    Pos.z += height * cos(freq * DirDotXZ + speed * fTime + 5);
    Pos.y += height * sin(freq * DirDotXZ + speed * fTime);

    freq *= FreqMult;
    height *= HeighMult;
    speed *= SpeedMult;



    for (int i = 1; i < WaveNum; i++)
    {   
        Direction = WaveDir[i];

        DirDotXZ = dot(Direction, vec2(VertexPos.x, VertexPos.z));
        GerstnerNormal.x += height * freq * Direction.x * -1 * sin(freq * DirDotXZ + speed * fTime);
        GerstnerNormal.z += height * freq * Direction.y * -1 * sin(freq * DirDotXZ + speed * fTime);

        DirDotXZ = dot(Direction, vec2(VertexPos.x + GerstnerNormal.x, VertexPos.z + GerstnerNormal.z));

        // VertexPos.x += Direction.x / i;
        // VertexPos.z += Direction.y / i;
        // VertexPos.y =


        Pos.x += height * cos(freq * DirDotXZ + speed * fTime);
        Pos.z += height * cos(freq * DirDotXZ + speed * fTime);
        Pos.y += height * sin(freq * DirDotXZ + speed * fTime);
        // domain warping if only i have normals || based on it deteriorate value 

        freq *= FreqMult;
        height *= HeighMult;
        speed *= SpeedMult;
    }
    // VertexPos.y *= Pos.y;

    vec3 Tangent = normalize(vec3(1, GerstnerNormal.x, 0));
    vec3 Bitangent = normalize(vec3(0, GerstnerNormal.z, 1));

    OuputSlope = GerstnerNormal;
    MaxWaveHeight = height;

    vec3 WaveNormal = normalize(cross(Bitangent, Tangent));
    mat3 NormalMap = mat3(Tangent, WaveNormal, Bitangent);
    Normal = NormalMap * in_Normal;
    
    // VertexPos.x += 10;

    return Pos + VertexPos;
}

/*
   _____(_)___  ___  _____
  / ___/ / __ \/ _ \/ ___/
 (__  ) / / / /  __(__  ) 
/____/_/_/ /_/\___/____/  
*/

float GetWaveMagnitude_Dir(float fTime, float height, float freq, float speed, vec2 DirectionXZ, vec3 PrevSlopeDerv) {
    float DirDotXZ = dot(DirectionXZ, vec2(in_VertexPos.x, in_VertexPos.z));
    // return height * sin(freq * DirDotXZ + speed * fTime);
    return exp(height * sin(freq * DirDotXZ + speed * fTime)) - 1; // i doubt it asf
}

vec3 GetWaveMagnitude_Dir_Slope(float fTime, float height, float freq, float speed, vec2 DirectionXZ, vec3 PrevSlope) {
    float DirDotXZ = dot(DirectionXZ, vec2(in_VertexPos.x, in_VertexPos.z));
    float SlopeX = height * cos(freq * DirDotXZ + speed * fTime) * DirectionXZ.x * freq;
    float SlopeZ = height * cos(freq * DirDotXZ + speed * fTime) * DirectionXZ.y * freq;

    SlopeX = pow(e, height * sin(freq * DirDotXZ + speed * fTime)) * SlopeX;
    SlopeZ = pow(e, height * sin(freq * DirDotXZ + speed * fTime)) * SlopeZ;

    return vec3(SlopeX, 0, SlopeZ);
}

float waves_partial_derv() {
    float Magnitude = 0.0;
    vec3 Slope = vec3(0.0);

    float height = 1.05; 
    MaxWaveHeight = height;
    float freq = 0.07;
    float speed = 4.0;
    vec3 PrevSlopeDerv;

    for (int i = 0; i < WaveNum; i++) {
        vec2 Direction = WaveDir[i];
        Magnitude += GetWaveMagnitude_Dir(fTime, height, freq, speed, Direction, PrevSlopeDerv);
        PrevSlopeDerv = GetWaveMagnitude_Dir_Slope(fTime, height, freq, speed, Direction, PrevSlopeDerv);
        Slope += PrevSlopeDerv;

        height *= 0.76;
        freq *= 1.145;
    }

    vec3 Tangent = normalize(vec3(1.0, Slope.x, 0.0));
    vec3 Bitangent = normalize(vec3(0.0, Slope.z, 1.0));
    vec3 WaveNormal = normalize(cross(Bitangent, Tangent));
    Slope = vec3(Slope.x, 0, Slope.z);
    mat3 NormalMap = mat3(Tangent, WaveNormal, Bitangent);

    Normal = NormalMap * in_Normal;

    return Magnitude;
}

void main() {
    vec3 Position = in_VertexPos + vec3(0.0, waves_partial_derv(), 0.0);
    // EXPERIMENT EXCLUSIVELY (GERSTNER WAVES)
    // Position = GetGerstnerWaveAmplitude(fTime, 0.5, 1, 1, normalize(vec2(1)));
    Position = GerstnerWave(fTime);
    // Position.y *= (Position.y - in_VertexPos.y);

    gl_Position = Perspective * vec4(Position, 1.0);
    Position3D = Position;
    Color = in_Color;
}

