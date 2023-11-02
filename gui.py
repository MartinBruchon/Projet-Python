import tkinter as tk
import customtkinter as ctk
import folium
from tkintermapview import TkinterMapView
import os
import tempfile

def choisir_dossier():
    dossier = ctk.filedialog.askdirectory()
    if dossier:
        label_dossier.configure(text=f"Dossier choisi : {dossier}")

def show_map():
    # Create a map object centered at Paris coordinates
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Save the map to a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
        m.save(f.name)
        # Use the webview library to create a new window to display the map HTML
        webview.create_window('Map of Paris', f.name)

# Créer la fenêtre principale
root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}+0+0")
root.title("Page d'accueil")

# Créer et placer les widgets
label_instructions = ctk.CTkLabel(root, text="Choisissez un dossier local :")
label_instructions.pack(pady=10)

button_choisir = ctk.CTkButton(root, text="Choisir un dossier", command=choisir_dossier)
button_choisir.pack(pady=10)

label_dossier = ctk.CTkLabel(root, text="Dossier choisi :")
label_dossier.pack(pady=10)


# Create the map widget
map_widget = TkinterMapView(root, width=screen_width, height=screen_height, corner_radius=0)
map_widget.set_position(48.8566, 2.3522)  # Coordinates for Paris
map_widget.set_zoom(12)
map_widget.pack(fill="both", expand=True)

# Lancer l'application
root.mainloop()