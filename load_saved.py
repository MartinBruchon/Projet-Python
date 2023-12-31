from customtkinter import *
from platform import system
from metadata_functions import load_and_print
from json import dumps
from tkinter import Text 

def read(file):
    """Load, read and display the content of the previously saved JSON file
    Args:
        file (str): Path of the JSON file
    """    
    
    # Create the window
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

    # Get the datas from JSON as String
    data = dumps(load_and_print(file), indent=2)

    text_widget = Text(root, wrap='word', bg=colors[1], fg='white', borderwidth=-1, padx=20, pady=20)
    text_widget.pack(fill=BOTH, expand=True, side=LEFT)

    scrollbar = CTkScrollbar(root, command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.configure(state='normal')
    text_widget.insert('1.0', data)
    text_widget.configure(state='disabled')

    root.mainloop()


def main():
    """Open a file dialog to visualize JSON files and to select the one the user want to load
    """    
    file = filedialog.askopenfile(filetypes=[("JSON files", "*.json")])
    if file:
        read(file.name)   
