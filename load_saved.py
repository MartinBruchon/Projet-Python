from customtkinter import *
from platform import system
from metadata_functions import load_and_print

def read(file):

        colors = ["#1C1C1C" , "#282828"]
        set_appearance_mode("dark")
        root = CTk()
        root.title("Main page")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f'{screen_width}x{screen_height}+0+0')
        if system() == "Linux":root.attributes('-zoomed', True)
        else : root.state("zoomed")
        
        canvas = CTkCanvas(root, bg=colors[0], highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = CTkScrollbar(root, orientation=VERTICAL, command=canvas.yview, corner_radius=0)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        data = load_and_print(file)
        
        label = CTkLabel(canvas, text=data, anchor=N)
        label.pack(fill=X, padx=100)
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        label.bind("<Configure>", on_frame_configure)
        root.mainloop()

def main():
    
    file = filedialog.askopenfile()
    if file:
        read(file.name)   
