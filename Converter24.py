from PIL import Image
import os

# Function to convert images to .jpg format
def convert_images_to_jpg(folder_path):
    for filename in os.listdir(folder_path):
        # Check if the file is an image (you can add more extensions if needed)
        if filename.lower().endswith(('.png', '.gif', '.bmp', '.jpeg', '.jpg')):
            try:
                # Open the image file
                with Image.open(os.path.join(folder_path, filename)) as img:
                    # Convert and save the image as .jpg
                    img.convert("RGB").save(os.path.join(folder_path, os.path.splitext(filename)[0] + ".jpg"))
                    print(f"Converted {filename} to .jpg")
                    # Optionally, you can remove the original image file
                    # os.remove(os.path.join(folder_path, filename))
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Specify the path to the folder containing the images
folder_path = "C:/Users/USER/Desktop/backup/640Data/Faulty/Raw/New folder"

# Call the function to convert images to .jpg
convert_images_to_jpg(folder_path)
