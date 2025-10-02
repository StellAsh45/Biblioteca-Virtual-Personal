import re
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ManejoUsuarios import ManejoUsuarios
from ManejoLibros import ManejoLibros
import Biblioteca

# Clase principal que maneja la ventana de acceso (login y registro)
class VentanaAcceso:
    def __init__(self):
        # Gestores de usuarios y libros
        self.gestor_usuarios = ManejoUsuarios()
        self.gestor_libros = ManejoLibros(self.gestor_usuarios)
        # Ruta base del proyecto (esto para las imagenes)
        self.directorio_base = os.path.dirname(os.path.abspath(__file__))
        # Configuración de la ventana principal
        self.root = tk.Tk()
        self.root.title("Biblioteca Virtual")
        self.root.resizable(False, False)
        self.centrar_ventana(600, 400)
        # Frame central
        self.frame = None
        # Iniciar con la vista de login
        self.mostrar_login()
        # Mantener la ventana abierta
        self.root.mainloop()

    # Centra la ventana en la pantalla
    def centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Destruye el frame actual para cambiar de vista
    def limpiar_frame(self):
        if self.frame:
            self.frame.destroy()

    # ---------------- VISTA LOGIN ----------------
    def mostrar_login(self):
        self.limpiar_frame()
        self.root.title("Ingreso - Biblioteca Virtual")
        # Fondo
        try:
            img_path = os.path.join(self.directorio_base, "Imagenes", "Login.jpeg")
            img = Image.open(img_path).resize((600, 400), Image.Resampling.LANCZOS)
            self._bg_image = ImageTk.PhotoImage(img)
            background_label = tk.Label(self.root, image=self._bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#2B3F54")

        # Formulario
        self.frame = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        tk.Label(self.frame, text="Ingreso a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5))
        # Campo usuario
        tk.Label(self.frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.entry_usuario = tk.Entry(self.frame, width=20, font=("Arial", 10))
        self.entry_usuario.pack()
        # Campo contraseña
        tk.Label(self.frame, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        pass_frame = tk.Frame(self.frame, bg="white")
        pass_frame.pack(pady=5)
        self.entry_password = tk.Entry(pass_frame, width=16, font=("Arial", 10), show="*")
        self.entry_password.pack(side="left", padx=(0, 5))
        self.mostrar_contrasena = tk.BooleanVar(value=False)

        #Funcion para alternar la visibilidad de la contraseña
        def toggle_password():
            if self.mostrar_contrasena.get():
                self.entry_password.config(show="*")
                btn_toggle.config(text="👁")
                self.mostrar_contrasena.set(False)
            else:
                self.entry_password.config(show="")
                btn_toggle.config(text="🙈")
                self.mostrar_contrasena.set(True)
        # Boton para mostrar/ocultar contraseña
        btn_toggle = tk.Button(pass_frame, text="👁", command=toggle_password, bg="white", font=("Arial", 7))
        btn_toggle.pack(side="left")
        # Botones de accion
        tk.Button(self.frame, text="Iniciar sesión", font=("Arial", 10), command=self.login).pack(pady=10)
        tk.Button(self.frame, text="Registrarse", font=("Arial", 10), command=self.mostrar_registro).pack()

    # Funcion para manejar el login
    def login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_password.get().strip()
        # Validaciones básicas
        if not usuario and not contrasena:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        if not usuario:
            messagebox.showwarning("Error", "El usuario no puede estar vacío.")
            return
        if not contrasena:
            messagebox.showwarning("Error", "La contraseña no puede estar vacía.")
            return
        # Intentar la autenticacion
        try:
            if self.gestor_usuarios.login_usuario(usuario, contrasena):
                messagebox.showinfo("Login", f"Bienvenido {usuario}")
                self.root.destroy() # Cierra la ventana de login
                Biblioteca.BibliotecaGUI(usuario, self.gestor_libros) # Abre la ventana principal de la biblioteca
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

    # ---------------- VISTA REGISTRO ----------------
    def mostrar_registro(self):
        self.limpiar_frame()
        self.root.title("Registro - Biblioteca Virtual")
        # Fondo
        try:
            img_path = os.path.join(self.directorio_base, "Imagenes", "Registro.jpeg")
            img = Image.open(img_path).resize((600, 400), Image.Resampling.LANCZOS)
            self._bg_image = ImageTk.PhotoImage(img)
            background_label = tk.Label(self.root, image=self._bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#2B3F54")
        # Formulario
        self.frame = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        tk.Label(self.frame, text="Registro a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5))
        # Campo usuario
        tk.Label(self.frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.entry_usuario = tk.Entry(self.frame, width=20, font=("Arial", 10))
        self.entry_usuario.pack(pady=5)
        # Campo contraseña
        tk.Label(self.frame, text="Crear contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.entry_password = tk.Entry(self.frame, width=20, font=("Arial", 10), show="*")
        self.entry_password.pack(pady=5)
        # Botones de accion
        tk.Button(self.frame, text="Registrarse", font=("Arial", 10), command=self.registro).pack(pady=10)
        tk.Button(self.frame, text="Volver al ingreso", font=("Arial", 10), command=self.mostrar_login).pack()

    # Funcion para manejar el registro
    def registro(self):
        usuario = self.entry_usuario.get().strip() # Obtener y limpiar espacios en blanco
        contrasena = self.entry_password.get().strip() # Obtener y limpia espacios en blanco
        errores = [] # Lista para acumular errores de validación
        # Validaciones básicas
        if not usuario and not contrasena:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        if not usuario:
            messagebox.showwarning("Error", "El usuario no puede estar vacío.")
            return
        if not contrasena:
            messagebox.showwarning("Error", "La contraseña no puede estar vacía.")
            return
        # Validar complejidad de la contraseña
        if len(contrasena) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", contrasena):
            errores.append("Debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", contrasena):
            errores.append("Debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
            errores.append("Debe contener al menos un carácter especial.")
        # Si hay errores, mostrarlos con un mensaje
        if errores:
            mensaje = "La contraseña debe contener:\n- " + "\n- ".join(errores)
            messagebox.showwarning("Error", mensaje)
            return
        # Intentar registrar el usuario
        try:
            if self.gestor_usuarios.registrar_usuario(usuario, contrasena):
                messagebox.showinfo("Registro", "Usuario registrado correctamente")
                self.mostrar_login()
            else:
                messagebox.showerror("Error", "El usuario ya existe")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{e}")
# Inicio del programa
if __name__ == "__main__":
    VentanaAcceso()
