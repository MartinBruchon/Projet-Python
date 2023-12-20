import tkinter as tk
from customtkinter import *

colors = ["#1C1C1C" , "#282828"]

#def main(dossier):
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
canvas.create_window((200, 300), window=frame, anchor=tk.NW)

# Création de 10 canevas vides à l'intérieur du canvas principal
for i in range(10):
    sub_canvas = CTkLabel(frame, bg_color=colors[1], width=200, height=200)
    sub_canvas.pack(padx=5, pady=20)
    
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

root.title("main")
root.mainloop()
