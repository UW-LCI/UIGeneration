import os
import random
import json
from PIL import Image

def load_random_format(formats_folder):
    format_files = [
        os.path.join(formats_folder, file)
        for file in os.listdir(formats_folder)
        if file.endswith(".json")
    ]
    if not format_files:
        raise ValueError(f"No format files found in {formats_folder}")
    selected_format = random.choice(format_files)
    with open(selected_format, 'r') as f:
        return json.load(f)

def combine_images(format_config, elements_folder, output_path):
    canvas_width, canvas_height = format_config["canvas_size"]
    canvas = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
    print(f"Canvas created with size: {canvas_width}x{canvas_height}")

    occupied_areas = []

    for layer in format_config["layers"]:
        folder = os.path.join(elements_folder, layer["folder"])

        images = load_images(folder)
        if not images:
            print(f"No images found in folder: {folder}, skipping layer.")
            continue
        if "repeat_range" in layer:
            min_repeat, max_repeat = layer["repeat_range"]
            repeat_count = random.randint(min_repeat, max_repeat)
        else:
            repeat_count = 1 

        for _ in range(repeat_count):
            placed = False
            attempts = 0
            max_attempts = 50

            while not placed and attempts < max_attempts:
                attempts += 1
                image = random.choice(images)
                if "resize" in layer:
                    image = image.resize(tuple(layer["resize"]), Image.Resampling.LANCZOS)
                if "random_position" in layer and layer["random_position"]:
                    max_x = canvas_width - image.width
                    max_y = canvas_height - image.height
                    x = random.randint(0, max_x) if max_x > 0 else 0
                    y = random.randint(0, max_y) if max_y > 0 else 0
                else:
                    x, y = layer["position"]

                bounding_box = (x, y, x + image.width, y + image.height)
                overlap = any(
                    x1 < bounding_box[2] and bounding_box[0] < x2 and
                    y1 < bounding_box[3] and bounding_box[1] < y2
                    for (x1, y1, x2, y2) in occupied_areas
                )

                if not overlap:
                    canvas.paste(image, (x, y), image if image.mode == "RGBA" else None)
                    occupied_areas.append(bounding_box)
                    placed = True
                # else:
                #     print(f"Overlap detected.")

            # if not placed:
            #     print(f"Failed to place image after {max_attempts} attempts, skipping.")

    canvas.save(output_path)
    print(f"Image saved to {output_path}")


def load_images(folder_path):
    if not os.path.exists(folder_path):
        return []

    all_files = os.listdir(folder_path)
    image_files = [
        os.path.join(folder_path, file)
        for file in all_files
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    images = []
    for file in image_files:
        try:
            img = Image.open(file)
            images.append(img)

        except Exception as e:
            print(f"Failed to load image {file}: {e}")

    return images

if __name__ == "__main__":
    formats_folder = "./formats"
    elements_folder = "./Elements"
    output_path = "./output/combined_image.png"

    format_config = load_random_format(formats_folder)
    combine_images(format_config, elements_folder, output_path)
