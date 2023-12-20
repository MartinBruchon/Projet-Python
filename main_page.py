import tkinter as tk
from customtkinter import *
from scan_folder import scan
from PIL import Image

colors = ["#1C1C1C" , "#282828"]
size=(96, 96)
pdf_img = Image.open("./src/pdf.png")
pdf_img = CTkImage(light_image=pdf_img, dark_image=pdf_img, size=size)
img_img = Image.open("./src/img.png")
img_img = CTkImage(light_image=img_img, dark_image=img_img, size=size)
ppt_img = Image.open("./src/ppt.png")
ppt_img = CTkImage(light_image=ppt_img, dark_image=ppt_img, size=size)
word_img = Image.open("./src/word.png")
word_img = CTkImage(light_image=word_img, dark_image=word_img, size=size)
xls_img = Image.open("./src/xls.png")
xls_img = CTkImage(light_image=xls_img, dark_image=xls_img, size=size)
sound_img = Image.open("./src/sound.png")
sound_img = CTkImage(light_image=sound_img, dark_image=sound_img, size=size)
video_img = Image.open("./src/video.png")
video_img = CTkImage(light_image=video_img, dark_image=video_img, size=size)
warn_img = Image.open("./src/warn.png")
warn_img = CTkImage(light_image=warn_img, dark_image=warn_img, size=size)

def test():
    print("ok")    

def main(dossier):
    root = CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')

    canvas = CTkCanvas(root, bg=colors[0], highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = CTkScrollbar(root, orientation=VERTICAL, command=canvas.yview, corner_radius=0)
    scrollbar.pack(side=RIGHT, fill=Y)        
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = CTkFrame(canvas, fg_color=colors[0])
    canvas.create_window((screen_width//2, 0), window=frame, anchor=N, width=screen_width)
    
    filetype_list = scan(dossier)

    for key, values in filetype_list.items():
                
        label = CTkLabel(frame, text=key, font=('', 20), anchor='w')
        label.pack(fill=X, padx=100)
        sub_frame = CTkFrame(frame, bg_color=colors[1])
        sub_frame.pack(padx=100, pady=20, fill=X, expand=True)
        
        for i,files in enumerate(values) :

            if key == "pdf" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=pdf_img, command=test)
            elif key in ["png", "jpg" ,"jpeg"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=img_img, command=test)
            elif key in ["ppt", "pptx"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=ppt_img, command=test)
            elif key in ["doc", "docx"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=word_img, command=test)
            elif key in ["xls", "xlsx"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=xls_img, command=test)
            elif key in ["mp3"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=sound_img, command=test)
            elif key in ["mp4"] : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=video_img, command=test)
            else : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=warn_img, command=test)
            panel.grid(row=0, column=i, padx=10)
            
            file_label = CTkLabel(sub_frame, text=files)
            file_label.grid(row=1, column=i, padx=10)
        
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    root.title("main")
    root.mainloop()
    
main("./test_dir")