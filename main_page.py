import tkinter as tk
import customtkinter as ctk

def main(dossier):
    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f'{screen_width}x{screen_height}+0+0')
    print(dossier)

    root.title("main")
    root.mainloop()