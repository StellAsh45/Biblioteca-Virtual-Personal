# Módulo principal de la Biblioteca Virtual Personal
import tkinter as tk

def iniciar_gui(usuario):
    root = tk.Tk()
    root.title("Biblioteca Virtual Personal")
    root.geometry("800x900")

    label = tk.Label(root, text=f"Bienvenido {usuario} a tu Biblioteca Virtual Personal")
    label.pack()

    root.mainloop()

print("Esto es prueba, la biblioteca no se debe abrir ejecutando este archivo si no el login.py")