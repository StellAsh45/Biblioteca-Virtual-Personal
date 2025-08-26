import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re

def iniciar_gui(usuario, gestor_libros):
    root = tk.Tk()
    root.title("Biblioteca Virtual Personal")
    root.geometry("1000x750")

    tk.Label(root, text=f"Bienvenido {usuario} a tu Biblioteca Virtual Personal",
             font=("Arial", 14, "bold")).pack(pady=10)

    # Frame principal
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Campos del formulario
    labels = ["Referencia", "Nombre", "Autor", "Año", "Genero", "Estado", "Fecha Inicio", "Fecha Fin"]
    entradas = {}

    for i, label in enumerate(labels):
        tk.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")

        if label == "Referencia":
            ref_frame = tk.Frame(frame)
            ref_frame.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            entry_ref = tk.Entry(ref_frame)
            entry_ref.pack(side="left")
            entradas[label] = entry_ref

            # Label de ayuda para la referencia
            tk.Label(ref_frame, text="Formato: AAA999 (A-Z,0-9)", fg="gray").pack(side="left", padx=8)

        elif label == "Genero":
            combo = ttk.Combobox(frame, values=["Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"])
            combo.grid(row=i, column=1, padx=5, pady=5)
            entradas[label] = combo

        elif label == "Estado":
            combo = ttk.Combobox(frame, values=["Leído", "Pendiente"])
            combo.grid(row=i, column=1, padx=5, pady=5)
            entradas[label] = combo

        elif label in ["Fecha Inicio", "Fecha Fin"]:
            subframe = tk.Frame(frame)
            subframe.grid(row=i, column=1, padx=5, pady=5)

            dias = [str(d).zfill(2) for d in range(1, 32)]
            meses = [str(m).zfill(2) for m in range(1, 13)]
            anio_actual = datetime.datetime.now().year
            anios = [str(a) for a in range(1900, anio_actual + 1)]

            combo_dia = ttk.Combobox(subframe, values=dias, width=5)
            combo_mes = ttk.Combobox(subframe, values=meses, width=5)
            combo_anio = ttk.Combobox(subframe, values=anios, width=7)

            combo_dia.grid(row=0, column=0, padx=2)
            combo_mes.grid(row=0, column=1, padx=2)
            combo_anio.grid(row=0, column=2, padx=2)

            entradas[label] = (combo_dia, combo_mes, combo_anio)

        else:
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entradas[label] = entry

    # Tabla de libros
    columnas = ("referencia", "nombre", "autor", "anio", "genero", "estado", "fecha_inicio", "fecha_fin")
    tabla = ttk.Treeview(root, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=120, anchor="center")
    tabla.pack(pady=15)

    def actualizar_lista():
        tabla.delete(*tabla.get_children())
        libros = gestor_libros.listar_libros(usuario)
        for libro in libros:
            tabla.insert("", "end", values=(
                libro['referencia'], libro['nombre'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))

    def guardar_libro():
        try:
            referencia = entradas["Referencia"].get().strip()
            nombre = entradas["Nombre"].get().strip()
            autor = entradas["Autor"].get().strip()
            anio = entradas["Año"].get().strip()
            genero = entradas["Genero"].get().strip()
            estado = entradas["Estado"].get().strip()

            fi_dia, fi_mes, fi_anio = [c.get().strip() for c in entradas["Fecha Inicio"]]
            ff_dia, ff_mes, ff_anio = [c.get().strip() for c in entradas["Fecha Fin"]]

            # Validaciones
            faltantes = []
            if not referencia: faltantes.append("Referencia")
            if not nombre: faltantes.append("Nombre")
            if not autor: faltantes.append("Autor")
            if not anio: faltantes.append("Año")
            if not genero: faltantes.append("Genero")
            if not estado: faltantes.append("Estado")
            if not (fi_dia and fi_mes and fi_anio): faltantes.append("Fecha Inicio")
            if not (ff_dia and ff_mes and ff_anio): faltantes.append("Fecha Fin")

            if faltantes:
                raise ValueError(f"Faltan campos obligatorios: {', '.join(faltantes)}")

            # Validar referencia
            if not re.match(r"^[A-Z]{3}[0-9]{3}$", referencia):
                raise ValueError("La referencia debe tener el formato AAA999 (3 letras y 3 números)")

            # Validar año
            if not anio.isdigit():
                raise ValueError("El año debe ser un número válido")
            anio_actual = datetime.datetime.now().year
            if not (1900 <= int(anio) <= anio_actual):
                raise ValueError(f"El año debe estar entre 1900 y {anio_actual}")

            if nombre.isdigit():
                raise ValueError("El nombre no puede ser solo números")

            fecha_inicio = f"{fi_dia}/{fi_mes}/{fi_anio}"
            fecha_fin = f"{ff_dia}/{ff_mes}/{ff_anio}"

            # Guardar en gestor
            gestor_libros.agregar_libro(usuario, referencia, nombre, autor, int(anio),
                                        genero, estado, fecha_inicio, fecha_fin)

            messagebox.showinfo("Éxito", "Libro guardado correctamente")
            actualizar_lista()

            # Limpiar entradas
            for key, entry in entradas.items():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("")
                elif isinstance(entry, tuple):
                    for c in entry: c.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_libro():
        try:
            seleccion = tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para eliminar")

            libro_seleccionado = tabla.item(seleccion[0])["values"]
            referencia = libro_seleccionado[0]

            gestor_libros.eliminar_libro(usuario, referencia)
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def salir():
        root.destroy()
        import Main
        Main.ventana_login()

    # Botones
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Guardar Libro", command=guardar_libro).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Eliminar Libro", command=eliminar_libro).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Actualizar Lista", command=actualizar_lista).grid(row=0, column=2, padx=10)
    tk.Button(btn_frame, text="Salir", command=salir).grid(row=0, column=3, padx=10)

    actualizar_lista()
    root.mainloop()