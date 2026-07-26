from PIL import Image, ImageTk
import tkinter as tk
import customtkinter as ctk
import numpy as np
from tkinter import filedialog
import cv2
import functionality as fn

def start_app() :
    ctk.set_appearance_mode("dark")          # forces dark mode on launch
    ctk.set_default_color_theme("dark-blue") # base theme, buttons overridden to cyan below

    root = ctk.CTk()

    root.title("Image Processor")
    root.geometry("1280x720")
    def clear_controls():
        for widget in usage_space.winfo_children():
            widget.destroy()

    def get_display_image(np_array, box_w, box_h) :
        img = Image.fromarray(np_array)
        img_w, img_h = img.size

        scale = min(box_w / img_w, box_h / img_h)
        new_w, new_h = int(img_w * scale), int(img_h * scale)

        resized = img.resize((new_w, new_h), Image.LANCZOS)
        return ImageTk.PhotoImage(resized), new_w, new_h

    def choose_photo() :
        file = filedialog.askopenfilename()
        print(file)      #this is just to check an actual image is being carried
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      #converts the BGR(of opencv) to RGB format
        fright.originalarray = image
        fright.newimage = np.copy(image)

        photo, w, h = get_display_image(image, 900, 500)
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        return

    def revert_filter() :
        image = fright.originalarray
        fright.newimage = image

        photo, w, h = get_display_image(image, 900, 500)
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        return

    def save_photo() :
        if not hasattr(fright, "newimage") :   # guard: nothing loaded yet
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if not filepath:      # user hit Cancel
            return

        img = Image.fromarray(fright.newimage)
        img.save(filepath)
        return


    #BUTTON FUNCTIONS
    def fxngrey ():
        grey = fn.greyscale(fright.newimage)
        fright.newimage = grey
        photo, w, h = get_display_image(grey, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo

        return

    def fxninv () :
        inverse = fn.invert(fright.newimage)
        fright.newimage = inverse
        photo, w, h = get_display_image(inverse, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo

        return

    def fxnbright() :
        clear_controls()
        usage_space.slider = ctk.CTkSlider(usage_space, orientation = "horizontal",
                        from_ = -100, to = 100,
                        command= bright_change )
        usage_space.slider.pack()
        return

    def bright_change(val) :
        val = int(val)

        bright = fn.brightness(fright.newimage,val)
        fright.newimage = bright
        photo, w, h = get_display_image(bright, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        
        return

    def spawn_buttons() :
        clear_controls()
        ctk.CTkButton(usage_space, text="horizontal", corner_radius=15, fg_color="#277A85", hover_color="#0097A7", command= fliphor).pack()
        ctk.CTkButton(usage_space, text="vertical", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= flipver).pack()

        return

    def fliphor() :
        display = fn.flipped_array(fright.newimage, "horizontal")
        fright.newimage = display
        photo, w, h = get_display_image(display, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        return
    def flipver() :
        display = fn.flipped_array(fright.newimage, "vertical")
        fright.newimage = display
        photo, w, h = get_display_image(display, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        return

    def fxnrotate() :
        rotated = np.rot90(fright.newimage)
        fright.newimage = rotated
        photo, w, h = get_display_image(rotated, 900, 500)
        fright.delete("all")
        fright.create_image(900 // 2, 500 // 2, image = photo, anchor= tk.CENTER)
        fright.image = photo
        return


    # main framework of the project
    ftop1 = ctk.CTkFrame(root, width=300, height=40)
    ftop1.pack(side=tk.TOP, fill=tk.X)

    ftop2 = ctk.CTkFrame(root, width=300, height=30)
    ftop2.pack(side=tk.TOP, fill=tk.X)

    fleft = ctk.CTkFrame(root, width=80, height=1000)
    fleft.pack(side=tk.LEFT, fill=tk.Y, padx = 15)

    fright = tk.Canvas(bg = "#757575", width=900, height=500)
    fright.pack(anchor = tk.CENTER, pady= 100)

    usage_space = tk.Canvas(bg="#333333", width = 250, height=150, highlightthickness=0)
    usage_space.pack(pady= 10)

    #Letters in the programm

    top_title = ctk.CTkLabel(ftop1,text = "THIS IS AN IMAGE PROCESSING TOOL", font = ("Arial", 25)).pack()
    toolbar = ctk.CTkLabel(fleft, text = "Tools :").pack(side = tk.TOP , pady = 8)

    #Buttons for use
    imgopen = ctk.CTkButton(ftop2, text = "Open Image", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= choose_photo).pack(side = tk.LEFT, padx = 15)
    imgsave = ctk.CTkButton(ftop2, text = "Save", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= save_photo).pack(side = tk.LEFT, padx = 5)
    imgrevert = ctk.CTkButton(ftop2, text="revert", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= revert_filter).pack(side= tk.RIGHT, padx= 80)

    ctk.CTkButton(fleft, text= "greyscale", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command = fxngrey).pack(pady = 5)
    ctk.CTkButton(fleft, text= "invert", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= fxninv).pack()
    ctk.CTkButton(fleft, text= "bright", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= fxnbright).pack(pady = 5)
    ctk.CTkButton(fleft, text= "flip", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= spawn_buttons).pack()
    ctk.CTkButton(fleft, text= "rotate" , corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7", command= fxnrotate).pack(pady = 5)
    # ctk.CTkButton(fleft, text= "blah", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7").pack()
    # ctk.CTkButton(fleft, text= "blah", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7").pack(pady = 5)
    # ctk.CTkButton(fleft, text= "blah", corner_radius=15, fg_color="#00BCD4", hover_color="#0097A7").pack()  buttons for future

    root.mainloop()