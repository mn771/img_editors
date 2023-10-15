import os
from PIL import Image

def crop_resize(folder_path, save_path, TOP, LEFT, SIDE, NEW_SIDE):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    files = os.listdir(folder_path)

    for idx, file_name in enumerate(files):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            process_image(os.path.join(folder_path, file_name), save_path, TOP, LEFT, SIDE, NEW_SIDE)

def process_image(input_path, save_path, TOP, LEFT, SIDE, NEW_SIDE):
    original_image = Image.open(input_path)
    img_converted = original_image.crop((LEFT, TOP, LEFT+SIDE, TOP+SIDE)).resize((NEW_SIDE, NEW_SIDE))
    img_converted.save(os.path.join(save_path, input_path[-8:]))

def main():
    folder_path = input("Input folder path: ")
    save_path = input("Input save folder path: ")
    LEFT = int(input("Input X coordinate of TOP corner: "))
    TOP = int(input("Input Y coordinate of TOP corner: "))
    SIDE = int(input("Input the size of the square crop region: "))
    NEW_SIDE = int(input("Input the size of the new square image: "))
    crop_resize(folder_path, save_path, TOP, LEFT, SIDE, NEW_SIDE)
    x = input("Input anything to exit: ")

main()