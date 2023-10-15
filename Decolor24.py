import os
from PIL import Image

def gray_scale(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    files = os.listdir(folder_path)

    for idx, file_name in enumerate(files):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            process_image(os.path.join(folder_path, file_name))

def process_image(input_path):
    original_image = Image.open(input_path)
    img_converted = original_image.convert("L")
    img_converted.save(input_path)

folder_path = input("Input folder path: ")
gray_scale(folder_path)
x = input("Input anything to exit: ")