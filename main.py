# IMPORTS
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image, ImageFilter

#APPLICATION COLOR CONSTANTS
BACKGROUND_COLOR = "#F7CCAC"
BUTTON_COLOR = "#826F66"
TEXT_COLOR = "#3A3845"
FONT_NAME = "Courier"


# LIST TO HOLD FILE PATH
# LIST TO HOLD ORIGINAL IMAGES
# LIST TO HOLD IMAGES TO BE PREVIEWED
f_names_list = []
images_available = []
display_images = []


# TODO: 2. UPLOAD IMAGE
# FUNCTION TO SELECT IMAGE FROM PC
def open_image(w:int, h:int, **kwargs:int):
    """opens dialog panel to read image in binary mode
        makes copy of selected image
        updates file name list
        updates images_available_list
        updates display_images_list

    Arguments:
    w -- image render width,
    h -- image render height,
    
    Keyword arguments:
    wm_width -- watermark image render width,
    wm_height -- watermark image render height,
    """

    # SPECIFY FILETYPES FOR FILEDIALOG MODULE
    # RETURN IMAGE AS BINARY FILE
    filetypes =(("PNG", "*.png"),("JPG", "*.jpg"),("All Files","*.*"),("Image Files", ".png .jfif, .jpg, .jpeg"))
    file_name = filedialog.askopenfile(initialdir=os.path.normpath('C:/Users/SAMSON/Pictures'), title='Watermark app', filetypes=filetypes, mode='rb')

    # STORE NAME/PATH OF OPENED FILE
    f_names_list.append(file_name.name)

    # CONVERT IMAGE TO RGBA EDITABLE MODE 
    # STORE ORIGINAL IMAGE AND IMAGE TO BE PREVIEWED SEPARATELY
    with Image.open(file_name) as raw_img:
        work_img = raw_img.copy().convert('RGBA')
        if not kwargs:
            images_available.append(work_img)
        else:
            wm_img = work_img.resize((kwargs['wm_width'], kwargs['wm_height']))
            images_available.append(wm_img)

        canvas_display_image = raw_img.resize((w, h))
        display_images.append(canvas_display_image)


def display_image():
    """ creates a PhotoImage object of Image to be displayed on canvas
        creates a canvas image with Photoimage object
    """
    global canvas
    global display_img
    global base_img
    try:    
        open_image(300, 300)
        base_img = ImageTk.PhotoImage(display_images[0])
        display_img = canvas.create_image(150, 150, image=base_img)
    except ValueError:
        clear_canvas()
        canvas.itemconfig(upload_text, text="Image format not supported")
        window.after(2000, home_message)


# TODO: 3. UPLOAD WATERMARK IMAGE IN SMALLER SIZE
# TODO: 4. JOIN BOTH IMAGES
def watermark_image():
    global canvas
    global new_transparent_img
    global transparent
    global save_img
    if images_available[0]:
        try:
            # WATERMARK ORIGINAL IMAGE
            w, h = images_available[0].size
            open_image(90,90, wm_width=w//3, wm_height=h//3)
            transparent = Image.new('RGBA', (w, h), (0,0,0,0))
            transparent.paste(images_available[0], (0,0))
            position = (w-(w//3), h-(h//3))
            save_img = transparent.paste(images_available[1], position, mask=images_available[1])

            #WATERMARK PREVIEW
            display_transparent = Image.new("RGBA", (300,300), (0,0,0,0))
            display_transparent.paste(display_images[0], (0,0))
            display_transparent.paste(display_images[1], (300-90, 300-90), mask=display_images[1])
            new_transparent_img = ImageTk.PhotoImage(display_transparent)
            canvas.itemconfig(display_img, image=new_transparent_img)
        except ValueError:
            clear_canvas()
            canvas.itemconfig(upload_text, text="Image format not supported")
            window.after(2000, home_message)


# TODO: 5. SAVE IMAGE AND REFRESH PAGE TO INITIAL USER UI  
# HOME IMAGE
def home_message():
    global canvas
    canvas.itemconfig(upload_text, text="Upload an image")


def save_image():
    """save proccessed image
        give feedback
        clear canvas
    """
    global canvas
    global transparent
    save_path =f_names_list[0]
    formatted_save_path = save_path.replace(save_path[-4:], f"_wm{save_path[-4:]}")
    # CREATES NEW SAVE PATH IF IMAGE HAS BEEN SAVED PREVIOUSLY
    if os.path.isfile(formatted_save_path):
        formatted_save_path = formatted_save_path.replace(formatted_save_path[-4:], f"{0}{formatted_save_path[-4:]}")
    transparent.convert("RGB").save(formatted_save_path)
    clear_canvas()
    canvas.itemconfig(upload_text, text="Image Saved")
    window.after(2000, home_message)
    
    
def clear_canvas():
    """Clear canvas"""
    
    global canvas
    canvas.delete(display_img)
    f_names_list.clear()
    images_available.clear()
    display_images.clear()


# TODO: 1. CREATE USER INTERFACE
# TKINTER OBJECT AND WINDOW CONFIGs
window = Tk()
window.title('WATERMARK APPLICATION')
window.config(padx=50, pady=80, bg=BACKGROUND_COLOR)

# HEADING LABEL
heading_label = Label(text="WATERMARK YOUR IMAGE", wraplength=500, justify='center')
heading_label.config(fg=TEXT_COLOR, width=30, font=(FONT_NAME, 30), bg=BACKGROUND_COLOR, pady=20)
heading_label.grid(row=0, column=1)

# CANVAS TO CONTAIN IMAGE
canvas = Canvas(highlightthickness=0, width=300, height=300, bg="#fff")
upload_text = canvas.create_text(150, 150, text="Upload an image", fill=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))

canvas.grid(row=1, column=1)

# UPLOAD BUTTON
upload_button = Button(text='UPLOAD IMAGE', fg="#fff", bg=BUTTON_COLOR, pady=5, width=15, command=display_image)
upload_button.grid(row=3, column=1)

# SELECT WATERMARK BUTTON
save_button = Button(text='SELECT WATERMARK', fg="#fff", bg=BUTTON_COLOR, pady=5, width=15,  command=watermark_image)
save_button.grid(row=4, column=1)

# SAVE BUTTON
save_button = Button(text='SAVE', fg="#fff", bg=BUTTON_COLOR, pady=5, width=15, command=save_image)
save_button.grid(row=5, column=1)










window.mainloop()