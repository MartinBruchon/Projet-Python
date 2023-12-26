from customtkinter import *
from PIL import Image
from metadata_functions import get_office_metadata as office

colors = ["#1C1C1C" , "#282828"]

def main(file):
    root = CTkToplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    
    frame = CTkFrame(root, fg_color=colors[0])
    frame.pack(fill=BOTH, expand=True)
    frame.grid_rowconfigure([0,1], weight=1)
    frame.grid_columnconfigure([0,1], weight=1)
        
    data_panel = CTkLabel(frame, bg_color=colors[1])
    data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
    
    preview_panel = CTkLabel(frame, bg_color=colors[1])
    preview_panel.grid(row=0, column=1, sticky=NSEW,  padx = 30, pady=30)
    
    map_panel = CTkLabel(frame, bg_color=colors[1])
    map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)
    print(office(file))

    root.title("Office document metadata")
    root.mainloop()