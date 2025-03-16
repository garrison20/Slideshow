import os
import random
import tkinter as tk
from PIL import Image, ImageOps, ImageTk

# Constants
NO_IMAGES_FILENAME = f"{os.path.dirname(os.path.realpath(__file__))}/no_images.png"
SITE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/ImageUploadSite"
IMAGES_PATH = f"{SITE_PATH}/files"
TIME_BETWEEN_IMAGES = 10000

# Screen info
screenwidth = 0
screenheight = 0

# Display algo items
curr_place_in_show = 0
show_order = []

def get_next_image_name():
    global curr_place_in_show
    global show_order

    # Get the list of images in the database
    images = os.listdir(IMAGES_PATH)

    ####################################
    # NO IMAGES UPLOADED
    ####################################

    # If there are no images uploaded, stop and return the "no images" image
    if (len(images) == 0):
        return NO_IMAGES_FILENAME
    
    ####################################
    # IMAGES WERE UPLOADED
    ####################################

    # Restart if we hit the end of the slideshow, but also re-shuffle the ordering.
    # This will run at bounds (first get call and when list is full).
    if (curr_place_in_show >= len(show_order)):
        curr_place_in_show = 0
        show_order = []

    # Create the scrambled list of indices if not already made
    if (show_order == []):
        show_order = list(range(0,len(images)))
        random.shuffle(show_order)

    # Images were added to the database. Take the new list of indices, shuffle them,
    # and then add them if the front of the order list
    if (len(images) > len(show_order)):
        new_indices = list(range(len(show_order),len(images)))
        random.shuffle(new_indices)
        temp_curr_place_in_order = curr_place_in_show
        for new_index in new_indices:
            show_order.insert(temp_curr_place_in_order, new_index)
            temp_curr_place_in_order += 1

    # Get the current image name
    image_name = f"{IMAGES_PATH}/{images[show_order[curr_place_in_show]]}"
    curr_place_in_show += 1

    return image_name

def get_next_image(width, height):
    pil_image = Image.open(get_next_image_name())
    # https://github.com/python-pillow/Pillow/issues/4703
    pil_image = ImageOps.exif_transpose(pil_image)

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

    root.after(TIME_BETWEEN_IMAGES, update_image) # if you pass args to the function being called, the slideshow doesn't work

# Ensure the files path is available
if not os.path.exists(IMAGES_PATH):
    os.makedirs(IMAGES_PATH)

# Set up TK and start the app
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
