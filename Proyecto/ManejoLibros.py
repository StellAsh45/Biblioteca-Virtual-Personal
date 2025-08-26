import json

class ManejoLibros:
    def __init__(self, gestor_usuarios):
        self.gestor_usuarios = gestor_usuarios

    # Agrega un libro a la lista de un usuario
    def agregar_libro(self, usuario, referencia, nombre, autor, anio, genero, estado, fecha_inicio, fecha_fin):
        for u in self.gestor_usuarios.usuarios:
            if u["usuario"] == usuario:
                # Validar que la referencia no exista ya
                for libro in u.get("libros", []):
                    if libro["referencia"] == referencia:
                        raise ValueError("La referencia del libro ya existe")

                if "libros" not in u:
                    u["libros"] = []

                nuevo_libro = {
                    "referencia": referencia,
                    "nombre": nombre,
                    "autor": autor,
                    "anio": anio,
                    "genero": genero,
                    "estado": estado,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }

                u["libros"].append(nuevo_libro)
                self.gestor_usuarios.guardar_usuarios()
                return True

        raise ValueError("Usuario no encontrado")

    def listar_libros(self, usuario):
        """Devuelve la lista de libros de un usuario"""
        for u in self.gestor_usuarios.usuarios:
            if u["usuario"] == usuario:
                return u.get("libros", [])
        return []

    def eliminar_libro(self, usuario, referencia):
        """Elimina un libro de un usuario por su referencia"""
        for u in self.gestor_usuarios.usuarios:
            if u["usuario"] == usuario:
                libros = u.get("libros", [])
                nuevos_libros = [libro for libro in libros if libro["referencia"] != referencia]
                if len(libros) != len(nuevos_libros):
                    u["libros"] = nuevos_libros
                    self.gestor_usuarios.guardar_usuarios()
                    return True
        raise ValueError("Libro no encontrado o usuario inválido")