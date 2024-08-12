import tkinter as tk
from tkinter import filedialog

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    folder_selected = filedialog.askdirectory()  # Abre el diálogo para seleccionar carpeta
    return folder_selected

if __name__ == "__main__":
    folder = select_folder()
    print(folder)  # Imprime la ruta de la carpeta seleccionada
