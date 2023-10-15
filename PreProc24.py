import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

class CropperTool:
    def __init__(self):
        self.image = None
        self.photo = None
        self.root = None
        self.canvas = None
        
        self.start_x = None
        self.start_y = None
        self.rect = None

        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        print("Cropper Tool Initiated")
    
    def set_canvas(self):
        if self.canvas is not None:
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.root, width=self.image.width, height=self.image.height)
        self.canvas.pack() 
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        print("Canvas is set")
    def set_root(self, root):
        print("New Root Set")
        self.root = root
    def set_image(self, input_path):
        self.image = Image.open(input_path)
        w, h = self.image.size
        if w > 1500 or h > 1500:
            self.image.thumbnail((1000, 1000)) #Comment this out for full size
            print("Image Thumbnail is used")
        self.photo = ImageTk.PhotoImage(self.image)
        print("New Image Set")

    def on_mouse_press(self, event):
        print("Mouse pressed")
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="black", width=5)
    def on_mouse_drag(self, event):
        print("Mouse being dragged")
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        square_side = min(abs(cur_x - self.start_x), abs(cur_y - self.start_y))
        if cur_x < self.start_x:
            cur_x = self.start_x - square_side
        else:
            cur_x = self.start_x + square_side

        if cur_y < self.start_y:
            cur_y = self.start_y - square_side
        else:
            cur_y = self.start_y + square_side
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
    def on_mouse_release(self, event):
        print("mouse released")
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.x1 = min(self.start_x, end_x)
        self.y1 = min(self.start_y, end_y)
        self.x2 = max(self.start_x, end_x)
        self.y2 = max(self.start_y, end_y)

class CropperUI:
    def __init__(self, tool: CropperTool):
        #Start Window Set Theme
        self.root = tk.Tk()
        self.root.title("PreProcessor 2024")
        self.root.tk.call('source', 'img_edit/src/themes/forest-light.tcl')
        ttk.Style().theme_use('forest-light')
        
        #Start Cropper Tool
        self.tool = tool
        self.tool.set_root(self.root)

        #Initiate UI elements
        self.browse_group_UI()
        self.control_group_UI()
        self.seek_group_UI()

        #Initiate
        self.isDark = False
        self.source_files = None
        self.n = 0
        self.input_path = None
        self.cropped_image = None
        self.gray_image = None
        self.rotated_image = None
        self.flipped_image = None
        self.resized_image = None
        self.input_path = ""
        self.crop_size = 640

        print("UI Initiated")

    def browse_group_UI(self):
        #Browse source folder button
        self.folder_path = tk.StringVar()
        self.selected_folder_label = ttk.Label(self.root, text="Source Folder:")
        self.selected_folder_label.pack()
        browse_button = ttk.Button(self.root, text="Browse Source Folder", command=self.browse_button)
        browse_button.pack()
        
        #Browse target folder button
        self.save_folder_path = tk.StringVar()
        self.selected_save_folder_label = ttk.Label(self.root, text="Save Folder:")
        self.selected_save_folder_label.pack()
        target_button = ttk.Button(self.root, text="Browse Save Folder", command=self.target_button)
        target_button.pack()
    def control_group_UI(self):
        #Control buttons group
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10, side="top")
            #Crop Button
        self.crop_button = ttk.Button(self.button_frame, text="Crop", command=self.crop_button)
        self.crop_button.pack(side="left", padx=10)
            #Process Button
        self.proc_button = ttk.Button(self.button_frame, text="Process", command=self.proc_button)
        self.proc_button.pack(side="left", padx=10)
            #Save Button
        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_button, style='Accent.TButton')
        self.save_button.pack(side="left", padx=10)
            #Next Button
        self.next_button = ttk.Button(self.button_frame, text="Next", command=self.next_button) 
        self.next_button.pack(side="left", padx=10) 
    def seek_group_UI(self):
        #Seek Group
        self.seek_frame = ttk.Frame(self.root)
        self.seek_frame.pack(pady=10, side="top")
            #Seek Button
        self.crop_button = ttk.Button(self.seek_frame, text="Seek", command=self.seek_button)
        self.crop_button.pack(side="left", padx=10)
            #Seek Spinbox
        self.spinbox = ttk.Spinbox(self.seek_frame, from_=0, to=999)
        self.spinbox.pack()

        #Position Label
        self.label = ttk.Label(self.root, text="Image: ")
        self.label.pack()

    def browse_button(self):
        #Declaration
        print("Source Browse Button Clicked")
        #Ask for folder
        self.selected_folder = filedialog.askdirectory()
        #Set path
        if self.selected_folder:
            self.folder_path.set(self.selected_folder)
            print("Source Folder Set, Source is:")
            print(self.folder_path.get())
        #Check if path exists    
        if not os.path.exists(self.folder_path.get()):
            print(f"Folder '{self.folder_path.get()}' does not exist.")
            return
        #Get list of files in folder
        self.source_files = os.listdir(self.folder_path.get())
    def target_button(self):
        #Declaration
        print("Target Browse Button Clicked")
        #Ask for folder
        self.selected_save_folder = filedialog.askdirectory()
        #Set path
        if self.selected_save_folder:
            self.save_folder_path.set(self.selected_save_folder)
            print("Target Folder Set, Target is:")
            print(self.save_folder_path.get())
    def crop_button(self):
        #Declaration
        print("Crop Button Clicked")
        #Check for path availability
        self.target_error()
        self.source_error()
        #Crop Image
        self.cropped_image = self.tool.image.crop((self.tool.x1, self.tool.y1, self.tool.x2, self.tool.y2))
        #End Process
        print("Image Cropped")
    def save_button(self):
        #Declaration
        print("Save Button Clicked")
        #Check for path availability
        self.target_error()
        self.source_error()
        #File name
        name = self.input_path[-8:]
        #Save: grayscaled, rotated, and flipped images
        self.gray_image.save(self.save_folder_path.get() + name[:4] + "00" + name[-4:])
        #self.rotated_image.save(self.save_folder_path.get() + name[:4] + "01" + name[-4:])
        #self.flipped_image.save(self.save_folder_path.get() + name[:4] + "02" + name[-4:])
        #End Process
        print("Image Saved")
    def proc_button(self):
        #Declaration
        print("Process Button Clicked")
        #Check for path availability
        self.target_error()
        self.source_error()
        #Resize Image
        self.resized_image = self.cropped_image.resize((self.crop_size, self.crop_size))
        #Grayscale Image
        self.gray_image = self.resized_image.convert("L")
        #Rotate Image
        #self.rotated_image = self.gray_image.rotate(90)
        #Mirror and Rotate Image
        #self.flipped_image = self.gray_image.transpose(Image.FLIP_LEFT_RIGHT).rotate(-90)
        #End Process
        print("Image Processed")
    def next_button(self):
        #Declaration
        print("Next Button Clicked")
        #Check for path availability
        self.target_error()
        self.source_error()
        #Get next input path
        self.input_path = os.path.join(self.folder_path.get(), self.source_files[self.n])
        #Iterate file and go to next path, refresh canvas
        #WORK IN PROGRESS
        self.tool.set_image(self.input_path)
        self.tool.set_canvas()
        self.tool.rect = None
        self.label.config(text="Image: {}".format(self.n))

        #Declare next file
        print(self.input_path)
        print(self.n)
        #Iterate file counter
        self.n += 1
    def seek_button(self):
        #Declaration
        print("Seek Button Clicked")
        #Check for path availability
        self.target_error()
        self.source_error()
        #Get number from Spinbox
        self.n = int(self.spinbox.get())
        #Go To File
        self.input_path = os.path.join(self.folder_path.get(), self.source_files[self.n])
        self.tool.set_image(self.input_path)
        self.tool.set_canvas()
        self.tool.rect = None
        self.label.config(text="Image: {}".format(self.n))
        self.n += 1
    
    def target_error(self):

        if self.save_folder_path.get() == "":
            print("Error: No target folder selected!")
            messagebox.showerror("No target folder selected!")
            
        else:
            pass
    def source_error(self):
        if self.folder_path.get() == "":
            print("Error: No source folder selected!")
            messagebox.showerror("No source folder selected!")
            
        else:
            pass

def splash_screen(delay):
    root = tk.Tk()
    root.overrideredirect(1)
    root.geometry("800x800+250+100")
    image = Image.open("C:/Users/USER/Documents/Research Project/project_one/project_one/src/imgs/splash.jpg")
    img = ImageTk.PhotoImage(image)
    label = ttk.Label(root, image=img)
    label.image = img 
    label.pack(fill=tk.BOTH, expand=tk.YES)
    root.after(int(delay*1000), root.destroy)

def main(): 
    tool = CropperTool()
    ui = CropperUI(tool)
    ui.root.mainloop()

main()

