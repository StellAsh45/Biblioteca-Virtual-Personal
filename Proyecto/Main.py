import re # Para validación de contraseñas
import os # Para manejar rutas de archivos
import tkinter as tk # Interfaz gráfica
from tkinter import messagebox # Para mostrar mensajes emergentes
from PIL import Image, ImageTk  # Para trabajar con imágenes (fondo con Pillow)
from ManejoUsuarios import ManejoUsuarios 
from ManejoLibros import ManejoLibros 
import Biblioteca as Biblioteca 

gestor_usuarios = ManejoUsuarios()
gestor_libros = ManejoLibros(gestor_usuarios)
directorio_base = os.path.dirname(os.path.abspath(__file__)) # Directorio base del proyecto

# Función para centrar ventana

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks() # Actualiza el estado de la ventana
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2) # Calcula coordenada X
    y = (ventana.winfo_screenheight() // 2) - (alto // 2) # Calcula coordenada Y
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}") # Establece el tamaño y posición de la ventana

# Ventana de Login

def ventana_login():
    root = tk.Tk()
    root.title("Ingreso de usuario - Biblioteca Virtual")
    root.resizable(False, False) # Evita redimensionar la ventana
    centrar_ventana(root, 600, 400) # Llama a la función para centrar la ventana

    # Fondo de la ventana del login

    try:
        img_path = os.path.join(directorio_base, "Imagenes", "Login.jpeg")
        img = Image.open(img_path) #Carga la imagen
        img = img.resize((600, 400), Image.Resampling.LANCZOS) # Simplemente redimensiona la imagen
        background_image = ImageTk.PhotoImage(img) # Convierte la imagen para Tkinter
        background_label = tk.Label(root, image=background_image) # Crea una etiqueta con la imagen
        background_label.place(x=0, y=0, relwidth=1, relheight=1) # Coloca la imagen en la ventana
    except:
        root.configure(bg="#2B3F54") # Si por algun motivo no carga la imagen, pone este color de fondo indicando que pasa algo

    # Frame y Labels

    frame = tk.Frame(root, bg="white", bd=2 , relief="solid") # Crea un frame blanco con borde solido
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300) # Centra el frame en la ventana se fija en ejes x e y lo ubica en el centro y cambia tamaño

    tk.Label(frame, text="Ingreso a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5)) # Label del frame

    tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(20, 5)) # Label usuario
    entry_usuario = tk.Entry(frame, width=30, font=("Arial", 10)) # Campo de texto usuario
    entry_usuario.pack() # Pone el cuadro de texto en el frame

    tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
    entry_password = tk.Entry(frame, width=30, font=("Arial", 10), show="*")
    entry_password.pack(pady=5)

    # Validacion de credenciales

    def login():
        usuario = entry_usuario.get().strip() # Obtiene el usuario escrito en el campo de texto
        contraseña = entry_password.get().strip() # Obtiene la contraseña escrita en el campo de texto
        
        if not usuario and not contraseña:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        elif not usuario:
            messagebox.showwarning("Error", "El campo de usuario no puede estar vacío.")
            return
        elif not contraseña:
            messagebox.showwarning("Error", "El campo de contraseña no puede estar vacío.")
            return
        elif gestor_usuarios.login_usuario(usuario, contraseña):  # Llama al gestor de usuarios para verificar credenciales
            messagebox.showinfo("Login", f"Bienvenido {usuario}")
            root.destroy()
            Biblioteca.iniciar_gui(usuario,gestor_libros) # Si credenciales correctas, abrir biblioteca
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos") #Mensaje de error si credenciales incorrectas

    # Cambio de ventana de login a registro

    def ir_a_registro():
        root.destroy() # Cierra la ventana de login
        ventana_registro() # Abre la ventana de registro

    # Botones
    tk.Button(frame, text="Iniciar sesión", font=("Arial", 10), command=login).pack(pady=10) # Llama a la función login al hacer click
    tk.Button(frame, text="Registrarse", font=("Arial", 10), command=ir_a_registro).pack() # Llama a la función ir_a_registro al hacer click

    root.mainloop() # Inicia el bucle principal de la ventana

# Ventana de Registro

def ventana_registro():
    root = tk.Tk()
    root.title("Registro de usuario - Biblioteca Virtual")
    root.resizable(False, False)
    centrar_ventana(root, 600, 400)

    # Fondo
    try:
        img_path = os.path.join(directorio_base, "Imagenes", "Registro.jpeg")
        img = Image.open(img_path)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)
        background_image = ImageTk.PhotoImage(img)
        background_label = tk.Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
    except:
        root.configure(bg="#2B3F54")

    # Frame
    frame = tk.Frame(root, bg="white", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

    tk.Label(frame, text="Registro a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5))

    tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(20, 5))
    entry_usuario = tk.Entry(frame, width=30, font=("Arial", 10))
    entry_usuario.pack(pady=5)

    tk.Label(frame, text="Crear contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
    entry_password = tk.Entry(frame, width=30, font=("Arial", 10), show="*")
    entry_password.pack(pady=5)

    def registro():
        usuario = entry_usuario.get().strip()
        contraseña = entry_password.get().strip()
        errores_registro = [] # Array para guardar errores de validación

        if not usuario and not contraseña:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        elif not usuario:
            messagebox.showwarning("Error", "El campo de usuario no puede estar vacío.")
            return
        elif not contraseña:
            messagebox.showwarning("Error", "El campo de contraseña no puede estar vacío.")
            return

        if len(contraseña)<8:
            errores_registro.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", contraseña):
            errores_registro.append("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", contraseña):
            errores_registro.append("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contraseña):
            errores_registro.append("La contraseña debe contener al menos un carácter especial.")

        if errores_registro:
            mensaje = "La contraseña debe contener:\n- " + "\n- ".join(errores_registro)
            messagebox.showwarning("Error", mensaje)
            return

        if gestor_usuarios.registrar_usuario(usuario, contraseña):
            messagebox.showinfo("Registro", "Usuario registrado correctamente")
            root.destroy()
            ventana_login()
        else:
            messagebox.showerror("Error", "El usuario ya existe")

    # Para que la persona regrese al login si se equivoca

    def ir_a_login():
        root.destroy()
        ventana_login()

    tk.Button(frame, text="Registrarse", font=("Arial", 10), command=registro).pack(pady=10)
    tk.Button(frame, text="Volver al ingreso", font=("Arial", 10), command=ir_a_login).pack()
    
    root.mainloop()

# Inicio del programa

if __name__ == "__main__":
    ventana_login()