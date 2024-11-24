#version 150

#define FSH

#moj_import <light.glsl>
#moj_import <fog.glsl>
#moj_import <emissive_utils.glsl>

uniform sampler2D Sampler0;
uniform float GameTime;
uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform vec3 Light0_Direction;
uniform vec3 Light1_Direction;
uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;
uniform mat3 IViewRotMat;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in vec4 normal;
in vec4 lightColor;
in vec4 tintColor;
in vec2 uv;
in float fogAlpha;
flat in float transparency;
flat in int isGui;
flat in ivec2 RelativeCords;

out vec4 fragColor;

void main() {
    gl_FragDepth = gl_FragCoord.z;
    float vDistance = vertexDistance;
    vec2 texSize = textureSize(Sampler0, 0);
    vec4 color = texture(Sampler0, texCoord0);

    if (color.a < 0.1) discard;
    color *= vertexColor * lightColor;

    color *= ColorModulator;

    fragColor = linear_fog(color, vDistance, FogStart, FogEnd, FogColor);
    
    fragColor *= * tintColor;
}