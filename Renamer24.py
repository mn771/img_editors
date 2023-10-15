import os

def rename_files(folder_path, start_number, padding):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    files = os.listdir(folder_path)
    files.sort()

    for idx, file_name in enumerate(files):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_extension = os.path.splitext(file_name)[1]
            new_name = f"{start_number + idx:0{padding}d}{file_extension}"
            os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_name))
            print(f"Renamed '{file_name}' to '{new_name}'")

if __name__ == "__main__":
    folder_path = input("Input folder path: ")
    if not os.path.exists(folder_path):
        print("The folder does not exist.")
        exit()
    start_number = int(input("Input starting number: "))
    padding = int(input("Input zero padding: "))
    rename_files(folder_path, start_number, padding)
    x = input("Input anything to exit: ")
