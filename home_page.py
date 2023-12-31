from customtkinter import *
from scan_folder import scan
from PIL import Image
import image_info, pdf_info, office_info, video_info, audio_info, load_saved
from metadata_functions import main_process_folder
import subprocess
from platform import system

# Visual parameter initialisation
colors = ["#1C1C1C" , "#282828"]
size=(96, 96)

# Load filetype logos and create CTkImages
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

def main(folder_path):
    """Window to visualize the content of the selected folder and to see the metadatas of the different files
    Args:
        folder_path (str or Path): The folder to process
    """    
    def button_callback(f,t):
        """Redirect to a specific page when a button is clicked, depending on the type of the file
        Args:
            f (str or Path): Selected file name
            t (str): Type of the selected file
        """             
        if t == "Image" : image_info.main(os.path.join(folder_path, f))
        elif t == "PDF Document" : pdf_info.main(os.path.join(folder_path, f))
        elif t in ["PowerPoint Presentation", "Excel", "Word Document"] : office_info.main(os.path.join(folder_path, f))
        elif t == "Audio File" : audio_info.main(os.path.join(folder_path, f))
        elif t == "Video" : video_info.main(os.path.join(folder_path, f))
    
    def optionmenu_callback(choice):
        """Execute some tasks depending on the selected option of the menu
        Args:
            choice (str): The chosen option
        """        
        match choice:
            case "Change directory": 
                root.quit()
                root.destroy()
                subprocess.Popen([sys.executable,"main.py"])
                exit()
            case "Save as JSON": main_process_folder(folder_path, False, "json")
            case "Load JSON" : load_saved.main()
            case "Exit": exit()
    
    # Creation and setting of the page
    set_appearance_mode("dark")
    deactivate_automatic_dpi_awareness()
    root = CTk()
    root.title("Main page")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    if system() == "Linux":root.attributes('-zoomed', True)
    else : root.state("zoomed")
    
    # Creation of a scrollable canvas
    canvas = CTkCanvas(root, bg=colors[0], highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = CTkScrollbar(root, orientation=VERTICAL, command=canvas.yview, corner_radius=0)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Creation of the main frame
    frame = CTkFrame(canvas, fg_color=colors[0])
    root.update()
    canvas.create_window((root.winfo_width()//2, 0), window=frame, anchor=N, width=root.winfo_width())
    
    # Creation of the multiple-choices menu
    optionmenu = CTkOptionMenu(frame, values=["Save as JSON", "Change directory", "Load JSON", "Exit"], command=optionmenu_callback)
    optionmenu.set("Options")
    optionmenu.pack(anchor=NW, padx=100)
    
    padding_label = CTkLabel(frame, text="", height=30)
    padding_label.pack()
    
    # Get the list of files ordered by type (in a dict)  
    filetype_list = scan(folder_path)

    # Creation of a container for each file type
    for key, values in filetype_list.items():
                
        label = CTkLabel(frame, text=key, font=('', 20), anchor='w')
        label.pack(fill=X, padx=100)
        sub_frame = CTkFrame(frame, bg_color=colors[1])
        sub_frame.pack(padx=100, pady=20, fill=X, expand=False)
        #sub_frame.pack(padx=100, pady=20, fill=BOTH, expand=True)
        
        sub_frame.update()
        maxwg = (sub_frame.winfo_width())//270
        n=0
        row=0
        
        # Plotting buttons corresponding to files in their respective frame
        for i,files in enumerate(values) :

            if key == "PDF Document" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=pdf_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "Image" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=img_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "PowerPoint Presentation" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=ppt_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "Word Document" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=word_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "Excel" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=xls_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "Audio File" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=sound_img, command=lambda f=files, t=key:button_callback(f,t))
            elif key == "Video" : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=video_img, command=lambda f=files, t=key:button_callback(f,t))
            else : panel = CTkButton(sub_frame, fg_color="transparent", text="", image=warn_img, command=lambda f=files, t=key:button_callback(f,t))
            
            if n >= maxwg : row += 1; n =0
            n += 1
            panel.grid(row=row, column=n, padx=10, sticky=N)
            panel.configure(text=files, compound="top", width=250)
            panel._text_label.configure(wraplength=200)

    # Configure the scroll region
    def update_scrollregion():
        root.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    

    root.after(100, update_scrollregion) 
    
    # Enable the mouse scroll
    def mouse_scroll(event):
        if event.num == 5 or event.delta == -120:  # Scroll down
            canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:  # Scroll up
            canvas.yview_scroll(-1, "units")

    for widget in [canvas, frame]:
        widget.bind("<MouseWheel>", mouse_scroll)  # For Windows and MacOS
        widget.bind("<Button-4>", mouse_scroll)  # For Linux scrolling up
        widget.bind("<Button-5>", mouse_scroll)  # For Linux scrolling down
    
    root.mainloop()