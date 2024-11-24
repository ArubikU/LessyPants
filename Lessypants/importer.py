import glob
import json
import math
import os
from collections import OrderedDict

from PIL import Image

layer1Crops = {}
layer2Crops = {}

def process_image(image_path, layer=0):
    img = Image.open(image_path)
    color_dict = {}
    
    for y in range(0, img.height, 32):
        for x in range(0, img.width, 64):
            crop = img.crop((x, y, x + 64, y + 32))
            
            r, g, b, a = crop.getpixel((0, 0))
            if a == 0:
                continue
            if r == 0 and g==0 and b==0:
                continue
            color_key = (r, g, b)
            if color_key not in color_dict:
                color_dict[color_key] = (r, g, b)
            if layer == 0:
                layer1Crops[color_key] = crop
            else:
                layer2Crops[color_key] = crop
    
    return color_dict

def read_json_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return (data['r'], data['g'], data['b'])

def process_input_layer(layer_pattern, input_dir, layer=0):
    layer_dict = {}
    for image_path in glob.glob(layer_pattern, root_dir=input_dir):
        layer_dict.update(process_image(os.path.join(input_dir, image_path), layer))
    return layer_dict

def process_formats_layer(formats_dir, layer=0):
    layer_dict = {}
    for armor_name in os.listdir(formats_dir):
        if str(armor_name).endswith(".png"):
            continue
        armor_name = str(armor_name).replace(".json","")
        json_path = os.path.join(formats_dir, f"{armor_name}.json")
        layer_path = os.path.join(formats_dir, f"{armor_name}_layer_{layer+1}.png")
        if os.path.exists(json_path) and os.path.exists(layer_path):
            color_key = read_json_data(json_path)
            layer_dict[color_key] = color_key
            crop = Image.open(layer_path)
            if layer == 0:
                layer1Crops[color_key] = crop
            else:
                layer2Crops[color_key] = crop
    return layer_dict

def create_layout(num_images):
    if num_images == 0:
        return []
    cols = max(1, math.ceil(math.sqrt(num_images)))
    rows = math.ceil(num_images / cols)
    layout = []
    for i in range(num_images):
        row = i // cols
        col = i % cols
        layout.append((col, row))
    return layout

def create_output_image(colors, layout, image_size=(64, 32), layer=0):
    if not layout:
        print("Warning: No colors found. Creating a blank image.")
        return Image.new('RGBA', image_size, (0, 0, 0, 0))  # Return a transparent image if layout is empty
    cols = max(pos[0] for pos in layout) + 1
    rows = max(pos[1] for pos in layout) + 1
    output_image = Image.new('RGBA', (cols * image_size[0], rows * image_size[1]), (0, 0, 0, 0))
    
    for (r, g, b), pos in zip(colors, layout):
        if layer == 0 and (r,g,b) in layer1Crops:
            output_image.paste(layer1Crops[(r,g,b)], (pos[0] * image_size[0], pos[1] * image_size[1]))
        elif layer == 1 and (r,g,b) in layer2Crops:
            output_image.paste(layer2Crops[(r,g,b)], (pos[0] * image_size[0], pos[1] * image_size[1]))
    
    return output_image

def generate_glsl(sorted_dict, layout):
    glsl_content = ""
    for (r, g, b), pos in zip(sorted_dict.keys(), layout):
        x, y = pos
        glsl_content += f"COLOR_ARMOR({r}, {g}, {b}) {{\n"
        glsl_content += f"    cords = vec2({x}, {y});\n"
        glsl_content += "}\n"
    return glsl_content

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(script_dir, "input")
formats_dir = os.path.join(script_dir, "formats")

# Process all layer 1 and layer 2 images from input folder
layer1_input = process_input_layer(os.path.join("*_layer_1.png"), input_dir, 0)
layer2_input = process_input_layer(os.path.join("*_layer_2.png"), input_dir, 1)

# Process all layer 1 and layer 2 images from formats folder
layer1_formats = process_formats_layer(formats_dir, 0)
layer2_formats = process_formats_layer(formats_dir, 1)


# Combine layers from both sources
layer1 = {**layer1_input, **layer1_formats}
layer2 = {**layer2_input, **layer2_formats}

# Create the sorted dictionary
sorted_dict = OrderedDict()

# First, add colors present in both layers
for color in sorted(set(layer1.keys()) & set(layer2.keys())):
    sorted_dict[color] = {"layer1": layer1[color], "layer2": layer2[color]}

# Then, add colors present only in layer1
for color in sorted(set(layer1.keys()) - set(layer2.keys())):
    sorted_dict[color] = {"layer1": layer1[color], "layer2": None}

# Finally, add colors present only in layer2
for color in sorted(set(layer2.keys()) - set(layer1.keys())):
    sorted_dict[color] = {"layer1": None, "layer2": layer2[color]}

# Create layout
layout = create_layout(len(sorted_dict))

if not layout:
    print("No colors found in the input images. Creating blank output files.")
    blank_image = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    blank_image.save(os.path.join(script_dir, "output_layer_1.png"))
    blank_image.save(os.path.join(script_dir, "output_layer_2.png"))
    with open(os.path.join(script_dir, "armorcords.glsl"), "w") as glsl_file:
        glsl_file.write("// No colors found\n")
else:
    # Create output images
    output_layer1 = create_output_image([color['layer1'] if color['layer1'] else (0, 0, 0) for color in sorted_dict.values()], layout, layer=0)
    output_layer2 = create_output_image([color['layer2'] if color['layer2'] else (0, 0, 0) for color in sorted_dict.values()], layout, layer=1)

    # Save output images
    output_layer1.save(os.path.join(script_dir, "output_layer_1.png"))
    output_layer2.save(os.path.join(script_dir, "output_layer_2.png"))

    # Generate GLSL content
    glsl_content = generate_glsl(sorted_dict, layout)

    # Save GLSL file
    with open(os.path.join(script_dir, "armorcords.glsl"), "w") as glsl_file:
        glsl_file.write(glsl_content)

print("Output images and GLSL file have been generated.")

# Print some debug information
print(f"Number of unique colors: {len(sorted_dict)}")
print(f"Layout: {layout}")
print(f"Input directory: {input_dir}")
print(f"Files in input directory: {os.listdir(input_dir)}")
print(f"Formats directory: {formats_dir}")
print(f"Armor sets in formats directory: {os.listdir(formats_dir)}")
print(f"Layer 1 colors: {list(layer1.keys())}")
print(f"Layer 2 colors: {list(layer2.keys())}")