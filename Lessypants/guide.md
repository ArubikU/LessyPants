# How to use
Starting we must edit the [armorcords](../assets/minecraft/shaders/include/armorcords.glsl)
here the format to setup you armors is 
```
COLOR_ARMOR(R, G, B) {
    cords =  vec2(XOFFSET, YOFFSET);
}
```
> The R G B are the values of the color to enable the armor and XOFFSET AND YOFFSET are the offsets to match the armor in the map


## Importing from Other systems

First whe need to add our current armor layers to the input [folder](./input/) later
if you have some custom that are not imported just need to add to the formats [folder](./formats/)
and that should add to the output layers

later need to replace the leather layers with the output layer