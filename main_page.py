from customtkinter import *
from scan_folder import scan
from PIL import Image
import image_info, pdf_info, office_info, video_info, audio_info
from metadata_functions import main_process_folder
import subprocess

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

def main(dossier):
    
    def test(f,t):
        if t == "Image" : image_info.main(os.path.join(dossier, f))
        elif t == "PDF Document" : pdf_info.main(os.path.join(dossier, f))
        elif t in ["PowerPoint Presentation", "Excel", "Word Document"] : office_info.main(os.path.join(dossier, f))
        elif t == "Audio File" : audio_info.main(os.path.join(dossier, f))
        elif t == "Video" : video_info.main(os.path.join(dossier, f))
    
    def optionmenu_callback(choice):
        match choice:
            case "Change directory": 
                root.quit()
                root.destroy()
                subprocess.Popen([sys.executable,"folder_selection.py"])
                exit()
            case "Save as Pickle": main_process_folder(dossier, False, "pickle")
            case "Save as CSV": main_process_folder(dossier, False, "csv")
            case "Exit": exit()
    
    set_appearance_mode("dark")
    deactivate_automatic_dpi_awareness()
    root = CTk()
    root.title("Main page")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    root.attributes('-zoomed', True)

    canvas = CTkCanvas(root, bg='red', highlightthickness=0) #colors[0]
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = CTkScrollbar(root, orientation=VERTICAL, command=canvas.yview, corner_radius=0)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    frame = CTkFrame(canvas, fg_color=colors[0])
    root.update()
    canvas.create_window((root.winfo_width()//2, 0), window=frame, anchor=N, width=root.winfo_width())
    
    optionmenu = CTkOptionMenu(frame, values=["Save as Pickle", "Save as CSV", "Change directory", "Exit"], command=optionmenu_callback)
    optionmenu.set("Options")
    optionmenu.pack(anchor=NW, padx=100)
    
    padding_label = CTkLabel(frame, text="", height=30)
    padding_label.pack()
    
    filetype_list = scan(dossier)

    for key, values in filetype_list.items():
                
        label = CTkLabel(frame, text=key, font=('', 20), anchor='w')
        label.pack(fill=X, padx=100)
        sub_frame = CTkFrame(frame, bg_color=colors[1])
        sub_frame.pack(padx=100, pady=20, fill=X, expand=True)
        
        sub_frame.update()
        maxwg = (sub_frame.winfo_width())//270
        n=0
        row=0
        
        for i,files in enumerate(values) :

            if key == "PDF Document" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=pdf_img, command=lambda f=files, t=key:test(f,t))
            elif key == "Image" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=img_img, command=lambda f=files, t=key:test(f,t))
            elif key == "PowerPoint Presentation" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=ppt_img, command=lambda f=files, t=key:test(f,t))
            elif key == "Word Document" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=word_img, command=lambda f=files, t=key:test(f,t))
            elif key == "Excel" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=xls_img, command=lambda f=files, t=key:test(f,t))
            elif key == "Audio File" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=sound_img, command=lambda f=files, t=key:test(f,t))
            elif key == "Video" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=video_img, command=lambda f=files, t=key:test(f,t))
            else : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=warn_img, command=lambda f=files, t=key:test(f,t))
            
            if n >= maxwg : row += 1; n =0
            n += 1
            panel.grid(row=row, column=n, padx=10, sticky=N)
            panel.configure(text=files, compound="top", width=250)
            panel._text_label.configure(wraplength=300)
        
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)
    root.mainloop()
    
#main("./test_dir")