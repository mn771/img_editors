from PIL import Image
import os

def mirror_images_in_folder(folder_path):
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)
    
    # Iterate through the files in the folder
    for file_name in file_list:
        # Check if the file is an image (you can add more image extensions if needed)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # Create the full file path
            file_path = os.path.join(folder_path, file_name)
            
            # Open the image
            with Image.open(file_path) as img:
                # Mirror the image horizontally
                mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                
                # Save the mirrored image back to the same path
                mirrored_img.save(file_path)
                
                # Optionally, you can also save the mirrored image with a new name or in a different folder

# Example usage
folder_path = "C:/Users/USER/Desktop/backup/640Data/Faulty/Prepped02"
mirror_images_in_folder(folder_path)
