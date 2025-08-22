import tkinter as tk
from tkinter import messagebox
import json
import os

ARCHIVO_USUARIOS = "Usuarios.json"

# Función encargada de cargar los usuarios desde el archivo JSON

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS): # Verifica si el archivo existe, si no, crea uno vacío
        return []
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f: # Abre el archivo en modo lectura (Read)
        try:
            return json.load(f) # Carga los usuarios desde el archivo JSON
        except json.JSONDecodeError: # Maneja errores de decodificación JSON
            messagebox.showerror("Error", "Pasa algo con el archivo de usuarios")
            return []
        
# Funcion encargada de guardar los usuarios en el archivo JSON

def guardar_usuarios(Usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(Usuarios, f, indent=4, ensure_ascii=False)


# Funcion encargada de abrir la GUI de Biblioteca despues del login

def abrir_biblioteca(Usuario):
    import Biblioteca  # Importar la GUI de biblioteca
    Biblioteca.iniciar_gui(Usuario) # Inicia el GUI de la biblioteca con el usuario autenticado

# Proceso de Login

def login():
    usuario = entry_usuario.get() # Obtiene el usuario del campo de entrada
    if not usuario:  # Verifica si el campo de usuario está vacío
        messagebox.showerror("Error", "Por favor, ingresa un usuario")
        return
    contraseña = entry_password.get() # Obtiene la contraseña del campo de entrada
    if not contraseña:  # Verifica si el campo de contraseña está vacío
        messagebox.showerror("Error", "Por favor, ingresa una contraseña")
        return
    usuarios = cargar_usuarios() # Carga los usuarios desde el archivo JSON

    for u in usuarios:
        if u["Usuario"] == usuario and u["Contraseña"] == contraseña: # Verifica si el usuario y la contraseña coinciden
            messagebox.showinfo("Login", f"Bienvenido {usuario}")
            root.destroy() # "Destruye" la interfaz del Login
            abrir_biblioteca(usuario)
            return
    messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# Registro de un nuevo usuario

def registrar():
    usuario = entry_usuario.get()
    if not usuario: 
        messagebox.showerror("Error", "Por favor, ingresa un usuario")
        return
    contraseña = entry_password.get()
    if not contraseña:
        messagebox.showerror("Error", "Por favor, ingresa una contraseña")
        return
    usuarios = cargar_usuarios()

    # Validar si ya existe
    for u in usuarios:
        if u["Usuario"] == usuario:
            messagebox.showerror("Error", "El usuario ya existe")
            return

    usuarios.append({"Usuario":usuario , "Contraseña": contraseña}) # Agrega el nuevo usuario al listado
    guardar_usuarios(usuarios) # Guarda el nuevo usuario en el archivo JSON
    messagebox.showinfo("Registro", "Usuario registrado correctamente")

# Interfaz del Login
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login - Biblioteca Virtual") # Título de la ventana
    root.geometry("300x300") # Tamaño de la ventana

    tk.Label(root, text="Login", font=("Arial", 18, "bold")).pack(pady=10) # Un label que se añadio para que se vea que es el login
    tk.Label(root, text="Usuario:").pack(pady=5) # Label para el campo de usuario
    entry_usuario = tk.Entry(root) # Campo de entrada para el usuario
    entry_usuario.pack(pady=5) # Añade un padding para que se vea mejor (Como en CSS)

    tk.Label(root, text="Contraseña:").pack(pady=5) # Label para el campo de contraseña
    entry_password = tk.Entry(root, show="*") # Campo de entrada para la contraseña, con el caracter * para ocultar la contraseña
    entry_password.pack(pady=5) 

    tk.Button(root, text="Iniciar Sesión", command=login).pack(pady=5) # Botón para iniciar sesión
    tk.Button(root, text="Registrar", command=registrar).pack(pady=5) # Botón para registrar un nuevo usuario

    root.mainloop() # Mantiene la ventana abierta hasta que se cierre
