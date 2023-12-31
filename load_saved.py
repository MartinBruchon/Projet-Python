from customtkinter import *
from platform import system
from metadata_functions import load_and_print
from json import dumps
from tkinter import Text 

def read(file):
    colors = ["#1C1C1C", "#282828"]
    set_appearance_mode("dark")
    root = CTk()
    root.title("Loaded Data")  # Set the correct title here
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    if system() == "Linux":
        root.attributes('-zoomed', True)
    else:
        root.state("zoomed")

    data = dumps(load_and_print(file), indent=2)

    text_widget = Text(root, wrap='word', bg=colors[1], fg='white', padx=20, pady=20)
    text_widget.pack(fill=BOTH, expand=True, side=LEFT)  # Pack to fill the window and expand

    scrollbar = CTkScrollbar(root, command=text_widget.yview)  # Create the scrollbar
    scrollbar.pack(side=RIGHT, fill=Y)  # Pack it to the right side
    text_widget.configure(yscrollcommand=scrollbar.set)  # Link scrollbar to the text widget

    text_widget.configure(state='normal')
    text_widget.insert('1.0', data)
    text_widget.configure(state='disabled')

    root.mainloop()


def main():
    
    file = filedialog.askopenfile(filetypes=[("JSON files", "*.json")])
    if file:
        read(file.name)   
