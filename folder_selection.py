import customtkinter as ctk
import home_page

dossier = ""

def main():
    """Small window for working folder selection
    """    
    def choisir_dossier():
        """ Show a dialog window for directory selection and launch the home page with this folder
        """        
        dossier = ctk.filedialog.askdirectory()
        if dossier:
            root.destroy()
            home_page.main(dossier)
            
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.title("Start Page")

    label_instructions = ctk.CTkLabel(root, text="Choose a folder", font=('',20))
    label_instructions.pack(pady=10)

    button_choisir = ctk.CTkButton(root, text="Choose a folder", command=choisir_dossier, font=('',20))
    button_choisir.pack(pady=20)

    root.eval('tk::PlaceWindow . center')
    root.mainloop()