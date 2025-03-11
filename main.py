import os
import random
import tkinter as tk
from PIL import Image, ImageTk

FILES_PATH = "./ImageUploadSite/files"
screenwidth = 0
screenheight = 0

def get_next_image_name():
    return f"{FILES_PATH}/{random.choice(os.listdir(FILES_PATH))}"

def get_next_image(width, height):
    pil_image = Image.open(get_next_image_name())

    img_width, img_height = pil_image.size
    ratio = min(width / img_width, height / img_height)
    img_width = int(img_width * ratio)
    img_height = int(img_height * ratio)
    pil_image = pil_image.resize((img_width, img_height))
    
    return pil_image

def update_image():
    # update image
    tkimg = ImageTk.PhotoImage(get_next_image(screenwidth, screenheight))
    label.config(image=tkimg)
    label.image = tkimg # save a reference to avoid garbage collected

    root.after(10000, update_image) # if you pass args to the function being called, the slideshow doesn't work

root = tk.Tk()
root.attributes("-fullscreen", 1, "-topmost", 1)
root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()

# label for showing image
label = tk.Label(root, bg="black")
label.pack(fill="both", expand=1)

update_image() # start the slide show
root.mainloop()
