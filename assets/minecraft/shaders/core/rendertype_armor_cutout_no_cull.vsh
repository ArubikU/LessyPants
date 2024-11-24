#version 150

#define VSH

#moj_import <fog.glsl>
#moj_import <light.glsl>
#moj_import <emissive_utils.glsl>

#define INV_TEX_RES_SIX (1.0 / 64)
#define INV_TEX_RES_THREE (1.0 / 32)
#define IS_LEATHER_LAYER texelFetch(Sampler0, ivec2(0.0, 1.0), 0) == vec4(1.0) // If it's leather_layer_X.png texture

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV1, UV2;
uniform mat3 IViewRotMat;
in vec3 Normal;

uniform sampler2D Sampler0, Sampler2;
uniform mat4 ModelViewMat, ProjMat;
uniform int FogShape;
uniform vec3 Light0_Direction, Light1_Direction;
uniform vec4 ColorModulator;
uniform float GameTime;
uniform vec2 ScreenSize;

out float vertexDistance;
out vec4 vertexColor, tintColor, lightColor;
out vec2 texCoord0;
out vec4 normal;
flat out ivec2 RelativeCords;


#define COLOR_ARMOR(r,g,b) return true; case ((r<<16)+(g<<8)+b):

int colorId(vec3 c) {
    ivec3 v = ivec3(c*255);
    return (v.r<<16)+(v.g<<8)+v.b;
}
vec2 cords=vec2(0,0);

bool shouldApplyArmor(){
    int vertexColorId=colorId(Color.rgb);
    switch(vertexColorId){
        default:
        
        #moj_import<armorcords.glsl>
        
        return true;
    }
    return false;
}

void main() {
    vec3 pos = Position;

    // Common calculations
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    #moj_import <fog_reader.glsl>
    normal = ProjMat * ModelViewMat * vec4(Normal, 0.0);

    vec4 light = minecraft_mix_light(Light0_Direction, Light1_Direction, Normal, Color);
    lightColor = texelFetch(Sampler2, UV2 / 16, 0);
    texCoord0 = UV0;
    tintColor = Color;
    // Armor-specific logic
    RelativeCords = ivec2(0);
    if (IS_LEATHER_LAYER) {
        ivec2 atlasSize = textureSize(Sampler0, 0);
        vec2 armorAmount = vec2(atlasSize) * vec2(INV_TEX_RES_SIX, INV_TEX_RES_THREE);
        vec2 offset = 1.0 / armorAmount;

        texCoord0 *= offset;
        shouldApplyArmor();
        if (cords != vec2(0)) {
            tintColor = vec4(1);
        }
        RelativeCords = ivec2(floor(cords));
        texCoord0 += vec2(offset.x * cords.x, offset.y * cords.y);
    }
    // Final color calculations
    vertexColor = light  * ColorModulator;

}