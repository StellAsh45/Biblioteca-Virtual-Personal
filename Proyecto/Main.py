import re
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ManejoUsuarios import ManejoUsuarios
from ManejoLibros import ManejoLibros
import Biblioteca

class Ventana_Ingreso:
    def __init__(self):
        # gestores
        self.gestor_usuarios = ManejoUsuarios()
        self.gestor_libros = ManejoLibros(self.gestor_usuarios)
        self.directorio_base = os.path.dirname(os.path.abspath(__file__))

        # ventana principal
        self.root = tk.Tk()
        self.root.title("Ingreso de usuario - Biblioteca Virtual")
        self.root.resizable(False, False)

        # centrar y mostrar login
        self.centrar_ventana(600, 400)
        self.mostrar_login()
        self.root.mainloop()

    def centrar_ventana(self, ancho, alto):
        """Centra la ventana self.root en pantalla."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def mostrar_login(self):
        """Construye la interfaz de login (incluye toggle del password)."""
        # fondo (si existe la imagen)
        try:
            img_path = os.path.join(self.directorio_base, "Imagenes", "Login.jpeg")
            img = Image.open(img_path).resize((600, 400), Image.Resampling.LANCZOS)
            self._bg_image = ImageTk.PhotoImage(img)  # guardamos en self para evitar GC
            background_label = tk.Label(self.root, image=self._bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#2B3F54")

        # frame central
        frame = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

        tk.Label(frame, text="Ingreso a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5))

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.entry_usuario = tk.Entry(frame, width=20, font=("Arial", 10))
        self.entry_usuario.pack()

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))

        # frame para entry + botón toggle (ojito)
        pass_frame = tk.Frame(frame, bg="white")
        pass_frame.pack(pady=5)

        self.entry_password = tk.Entry(pass_frame, width=16, font=("Arial", 10), show="*")
        self.entry_password.pack(side="left", padx=(0, 5))

        self.mostrar_contrasena = tk.BooleanVar(value=False)

        def toggle_password():
            if self.mostrar_contrasena.get():
                self.entry_password.config(show="*")
                btn_toggle.config(text="👁")
                self.mostrar_contrasena.set(False)
            else:
                self.entry_password.config(show="")
                btn_toggle.config(text="🙈")
                self.mostrar_contrasena.set(True)

        btn_toggle = tk.Button(pass_frame, text="👁", command=toggle_password, bg="white", font=("Arial", 7))
        btn_toggle.pack(side="left")

        # botones principales
        tk.Button(frame, text="Iniciar sesión", font=("Arial", 10), command=self.login).pack(pady=10)
        tk.Button(frame, text="Registrarse", font=("Arial", 10), command=self.ir_a_registro).pack()

    def login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_password.get().strip()

        if not usuario and not contrasena:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        if not usuario:
            messagebox.showwarning("Error", "El campo de usuario no puede estar vacío.")
            return
        if not contrasena:
            messagebox.showwarning("Error", "El campo de contraseña no puede estar vacío.")
            return

        try:
            if self.gestor_usuarios.login_usuario(usuario, contrasena):
                messagebox.showinfo("Login", f"Bienvenido {usuario}")
                self.root.destroy()
                # mantenemos compatibilidad con tu Biblioteca existente
                Biblioteca.BibliotecaGUI(usuario, self.gestor_libros)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al intentar iniciar sesión:\n{e}")

    def ir_a_registro(self):
        """Cierra login y abre el registro (instancia la ventana de registro)."""
        self.root.destroy()
        Ventana_Registro(self.gestor_usuarios, self.directorio_base)


class Ventana_Registro:
    def __init__(self, gestor_usuarios, directorio_base=None):
        self.gestor_usuarios = gestor_usuarios
        self.directorio_base = directorio_base or os.path.dirname(os.path.abspath(__file__))

        self.root = tk.Tk()
        self.root.title("Registro de usuario - Biblioteca Virtual")
        self.root.resizable(False, False)
        self.centrar_ventana(600, 400)
        self.mostrar_registro()
        self.root.mainloop()

    def centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def mostrar_registro(self):
        # fondo (opcional)
        try:
            img_path = os.path.join(self.directorio_base, "Imagenes", "Registro.jpeg")
            img = Image.open(img_path).resize((600, 400), Image.Resampling.LANCZOS)
            self._bg_image = ImageTk.PhotoImage(img)
            background_label = tk.Label(self.root, image=self._bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.root.configure(bg="#2B3F54")

        frame = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

        tk.Label(frame, text="Registro a tu biblioteca virtual", font=("Arial", 16), bg="white").pack(pady=(20, 5))

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="white").pack(pady=(10, 5))
        self.entry_usuario = tk.Entry(frame, width=20, font=("Arial", 10))
        self.entry_usuario.pack(pady=5)

        tk.Label(frame, text="Crear contraseña:", font=("Arial", 12), bg="white").pack(pady=(10, 5))

        pass_frame = tk.Frame(frame, bg="white")
        pass_frame.pack(pady=5)

        self.entry_password = tk.Entry(pass_frame, width=20, font=("Arial", 10), show="*")
        self.entry_password.pack(side="left", padx=(0, 5))

        tk.Button(frame, text="Registrarse", font=("Arial", 10), command=self.registro).pack(pady=10)
        tk.Button(frame, text="Volver al ingreso", font=("Arial", 10), command=self.volver_login).pack()

    def registro(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_password.get().strip()
        errores_registro = []

        if not usuario and not contrasena:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return
        if not usuario:
            messagebox.showwarning("Error", "El campo de usuario no puede estar vacío.")
            return
        if not contrasena:
            messagebox.showwarning("Error", "El campo de contraseña no puede estar vacío.")
            return

        if len(contrasena) < 8:
            errores_registro.append("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r"[A-Z]", contrasena):
            errores_registro.append("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", contrasena):
            errores_registro.append("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
            errores_registro.append("La contraseña debe contener al menos un carácter especial.")

        if errores_registro:
            mensaje = "La contraseña debe contener:\n- " + "\n- ".join(errores_registro)
            messagebox.showwarning("Error", mensaje)
            return

        try:
            if self.gestor_usuarios.registrar_usuario(usuario, contrasena):
                messagebox.showinfo("Registro", "Usuario registrado correctamente")
                self.root.destroy()
                Ventana_Ingreso()
            else:
                messagebox.showerror("Error", "El usuario ya existe")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al registrar:\n{e}")

    def volver_login(self):
        self.root.destroy()
        Ventana_Ingreso()


if __name__ == "__main__":
    Ventana_Ingreso()
