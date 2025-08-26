import tkinter as tk
from tkinter import messagebox
import json
import os

class ManejoUsuarios:
    ARCHIVO_USUARIOS = "Proyecto/usuarios.json"

    def __init__(self):
        self.usuarios=self.cargar_usuarios()

    def cargar_usuarios(self):
        if not os.path.exists(self.ARCHIVO_USUARIOS): # Verifica si el archivo existe, si no, crea uno vacío
            return []
        with open(self.ARCHIVO_USUARIOS, "r", encoding="utf-8") as f: # Abre el archivo en modo lectura (Read)
            try:
                return json.load(f) # Carga los usuarios desde el archivo JSON
            except json.JSONDecodeError: # Maneja errores de decodificación JSON
                return []
            
    def guardar_usuarios(self):
        with open(self.ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(self.usuarios, f, indent=4, ensure_ascii=False)
    
    def registrar_usuario(self, usuario, contraseña):
        for u in self.usuarios:
            if u["usuario"] == usuario:
                return False
        self.usuarios.append({"usuario": usuario, "contraseña": contraseña, "libros": []})
        self.guardar_usuarios()
        return True
    
    def login_usuario(self, usuario, contraseña):
        for u in self.usuarios:
            if u["usuario"] == usuario and u["contraseña"] == contraseña:
                return True
        return False