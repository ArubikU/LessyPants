# LessFancyPants but moreeee lessy

[fancypants](https://github.com/Ancientkingg/fancyPants) is kinda really inefficent and unoptimized yes
[lessfancypants](https://github.com/Godlander/lessfancypants) is very more optimized but still lower fps than vanilla
(compared with 1k entities)

lessy fancy pants is a bit "easy" not like lessfancypants but very more optimized , equals vanilla

## usage:

i suggest personally use the [Importer](./Lessypants/importer.py) to setup all your armors

the first step is build you armor in formats folder in format <name>.json <name>_layer_1.png <name>_layer_2.png

with that you execute the importer to generate output layer files and the armorcords.glsl file that you will need to replace in
[armorcords.glsl](./assets//minecraft//shaders//include//armorcords.glsl)

to equipe you use the same methods as normally changuing the color to the selected

`/item replace entity @s armor.chest with minecraft:leather_chestplate[dyed_color=1]`

*colors beyond total number of armor textures will default to use the first texture, but with tint color applied*

when the glowing effect is applied, the first custom armor texture is what glowing outline will show

### "Manually implementation"Steps to Manually Stack Armor Textures

1. **Prepare Your Textures**
   - Ensure all your armor textures are 64x32 pixels in size.
   - Name your files consistently, e.g., `armor_name_layer_1.png` for the base layer and `armor_name_layer_2.png` for the overlay layer.

2. **Choose Unique Colors**
   - Assign a unique RGB color to each armor set.
   - Create a small colored pixel (1x1) in the top-left corner of each texture to represent this color.

3. **Stack Textures**
   - Open an image editing software (e.g., GIMP, Photoshop).
   - Create a new image with width 64 pixels and height `32 * number_of_armor_sets` pixels.
   - Paste each armor texture vertically and horizontal, one below the other, in order of their assigned colors.

4. **Save Output Images**
   - Save two separate images: one for layer 1 (base) and one for layer 2 (overlay).
   - Name them `output_layer_1.png` and `output_layer_2.png`.

5. **Create GLSL File**
   - Create a new text file named `armorcords.glsl`.
   - For each armor set, add an entry in the following format:

     ```glsl
     COLOR_ARMOR(r, g, b) {
         cords = vec2(x, y);
     }
     ```

   - Replace `r`, `g`, `b` with the RGB values of your chosen color.
   - Replace `y` with the vertical position of the armor texture in the stacked image (0 for the first, 1 for the second, etc.).
   - Replace `x` with the horizontal position of the armor texture in the stacked image (0 for the first, 1 for the second, etc.).

   > X and Y are offset like x * 64 , and y * 32 starting from 0 0 the top left corner

## performance:

texture reading is a fairly expensive operation in shaders

original fancypants does all the calculation in the fragment shader for some reason, which means everything is calculated for every single pixel of armor on the screen and lessfancypant fix that issue but i come with a very high improve to rendering things
that i merely understand but it work and is more efficient

it also uses a `switch` loop that select depending on the color and path you setup

> the compiler will usually optimize loops if they run a predictable number of times, but since this loop's run time is dependent on the result of the texture read, that will not be possible

that issue is fixed by lessypants behind the case that all the cordinates are generated so that issue is corrected to more performance.
