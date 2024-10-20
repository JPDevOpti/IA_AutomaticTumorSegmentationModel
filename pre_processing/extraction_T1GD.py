import os
import shutil
import tkinter as tk
from tkinter import filedialog

def select_folder():
    # Crear ventana para seleccionar carpeta
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    folder_selected = filedialog.askdirectory()  # Abrir selector de carpetas
    return folder_selected

def extract_t1gd_files(source_folder, destination_folder):
    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Recorrer todas las subcarpetas en el directorio de origen
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Verificar si el archivo termina en '_T1GD_unstripped.nii.gz'
            if file.endswith('_T1GD_unstripped.nii.gz'):
                file_path = os.path.join(root, file)
                # Copiar el archivo a la carpeta de destino
                shutil.copy(file_path, destination_folder)
                print(f"Archivo copiado: {file}")

if __name__ == "__main__":
    # Seleccionar carpeta de origen
    source_folder = select_folder()
    # Definir la carpeta de destino (dentro de la carpeta de origen)
    destination_folder = os.path.join(source_folder, 'T1GD')
    # Extraer y copiar archivos
    extract_t1gd_files(source_folder, destination_folder)
    print("Extracción completada.")
