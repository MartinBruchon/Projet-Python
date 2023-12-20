import tkinter as tk
from customtkinter import *
from scan_folder import scan

colors = ["#1C1C1C" , "#282828"]

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
                
        label = CTkLabel(frame, text=key)
        label.pack(padx=20)
        sub_frame = CTkFrame(frame, bg_color=colors[1])
        sub_frame.pack(padx=100, pady=20, fill=X, expand=True)
        
        for i,files in enumerate(values) :
            file_label = CTkLabel(sub_frame, text=files)
            file_label.grid(row=0, column=i, padx=10)
        
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)

    root.title("main")
    root.mainloop()