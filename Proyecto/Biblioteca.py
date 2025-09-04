import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import Main as m

# Gui para la biblioteca virtual personal
def iniciar_gui(usuario, gestor_libros):
    root = tk.Tk()
    root.title("Biblioteca Virtual Personal")
    root.geometry("1700x800")
    root.resizable(False, False)
    m.centrar_ventana(root, 1700, 800)
    tk.Label(root, text=f"Bienvenido {usuario} a tu Biblioteca Virtual Personal",
             font=("Arial", 14, "bold")).pack(pady=10)

    # Frame principal
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Campos del formulario
    labels = ["Referencia", "Nombre", "Autor", "Año", "Genero", "Estado", "Fecha Inicio", "Fecha Fin"]
    entradas = {}
    ref_frame = tk.Frame(frame)
    ref_frame.grid(column=1, padx=5, pady=5)

    for i, label in enumerate(labels):
        tk.Label(frame, text=label).grid(row=i, column=0)

        ayuda = ""
        if label == "Referencia":
            ayuda = "Formato: AAA999 (A-Z,0-9)"
            entry_ref = tk.Entry(ref_frame)
            entry_ref.pack(side="left")
            entradas[label] = entry_ref
            tk.Label(ref_frame, text=ayuda, fg="gray").pack(side="left", padx=8)

        elif label == "Nombre":
            ayuda = "Título del libro"
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entradas[label] = entry
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Autor":
            ayuda = "Nombre del autor"
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entradas[label] = entry
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Año":
            ayuda = "Año de publicación (0-actual)"
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entradas[label] = entry
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Genero":
            ayuda = "Selecciona el género"
            genero_var = tk.StringVar()
            combo = ttk.Combobox(frame, textvariable=genero_var,
                                values=["Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"],
                                state="readonly")
            combo.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entradas[label] = genero_var
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Estado":
            ayuda = "¿Leído o pendiente?"
            estado_var = tk.StringVar()
            combo = ttk.Combobox(frame, textvariable=estado_var,
                                values=["Leído", "Pendiente"],
                                state="readonly")
            combo.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            entradas[label] = estado_var
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Fecha Inicio":
            ayuda = "Fecha en que comenzaste"
            subframe = tk.Frame(frame)
            subframe.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            dias = [str(d).zfill(2) for d in range(1, 32)]
            meses = [str(m).zfill(2) for m in range(1, 13)]
            anio_actual = datetime.datetime.now().year
            anios = [str(a) for a in range(1800, anio_actual + 1)]

            combo_dia = ttk.Combobox(subframe, values=dias, width=5,state="readonly")
            combo_mes = ttk.Combobox(subframe, values=meses, width=5,state="readonly")
            combo_anio = ttk.Combobox(subframe, values=anios, width=7,state="readonly")

            combo_dia.grid(row=0, column=0, padx=2)
            combo_mes.grid(row=0, column=1, padx=2)
            combo_anio.grid(row=0, column=2, padx=2)

            entradas[label] = (combo_dia, combo_mes, combo_anio)
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

        elif label == "Fecha Fin":
            ayuda = "Fecha en que terminaste"
            subframe = tk.Frame(frame)
            subframe.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            dias = [str(d).zfill(2) for d in range(1, 32)]
            meses = [str(m).zfill(2) for m in range(1, 13)]
            anio_actual = datetime.datetime.now().year
            anios = [str(a) for a in range(1800, anio_actual + 1)]

            combo_dia = ttk.Combobox(subframe, values=dias, width=5,state="readonly")
            combo_mes = ttk.Combobox(subframe, values=meses, width=5,state="readonly")
            combo_anio = ttk.Combobox(subframe, values=anios, width=7,state="readonly")

            combo_dia.grid(row=0, column=0, padx=2)
            combo_mes.grid(row=0, column=1, padx=2)
            combo_anio.grid(row=0, column=2, padx=2)

            entradas[label] = (combo_dia, combo_mes, combo_anio)
            tk.Label(frame, text=ayuda, fg="gray").grid(row=i, column=2, padx=8, sticky="w")

    # Tabla de libros
    columnas = ("Referencia", "Nombre", "Autor", "Año", "Género", "Estado", "Iniciado en", "Terminado en")
    tabla = ttk.Treeview(root, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")
    tabla.pack(pady=15)

    # Estado de edición
    libro_editando = {"referencia": None}

    # --- Helpers ---
    def limpiar_formulario():
        for key, entry in entradas.items():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.StringVar):
                entry.set("")
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
                try: entry.current(-1)
                except: pass
            elif isinstance(entry, tuple):
                for c in entry: c.set("")

    def actualizar_lista():
        tabla.delete(*tabla.get_children())
        libros = gestor_libros.listar_libros(usuario)
        for libro in libros:
            tabla.insert("", "end", values=(
                libro['referencia'], libro['nombre'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))

    def editar_libro():
        try:
            seleccion = tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para editar")

            libro_seleccionado = tabla.item(seleccion[0])["values"]
            libro_editando["referencia"] = libro_seleccionado[0]

            entradas["Referencia"].delete(0, tk.END)
            entradas["Referencia"].insert(0, libro_seleccionado[0])
            entradas["Nombre"].delete(0, tk.END)
            entradas["Nombre"].insert(0, libro_seleccionado[1])
            entradas["Autor"].delete(0, tk.END)
            entradas["Autor"].insert(0, libro_seleccionado[2])
            entradas["Año"].delete(0, tk.END)
            entradas["Año"].insert(0, libro_seleccionado[3])
            entradas["Genero"].set(libro_seleccionado[4])
            entradas["Estado"].set(libro_seleccionado[5])

            fi_dia, fi_mes, fi_anio = libro_seleccionado[6].split("/")
            ff_dia, ff_mes, ff_anio = libro_seleccionado[7].split("/")

            entradas["Fecha Inicio"][0].set(fi_dia)
            entradas["Fecha Inicio"][1].set(fi_mes)
            entradas["Fecha Inicio"][2].set(fi_anio)
            entradas["Fecha Fin"][0].set(ff_dia)
            entradas["Fecha Fin"][1].set(ff_mes)
            entradas["Fecha Fin"][2].set(ff_anio)

            messagebox.showinfo("Editar", "Modifique los campos y presione 'Guardar Libro'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar_libro():
        try:
            referencia = entradas["Referencia"].get().strip().upper()
            nombre = entradas["Nombre"].get().strip()
            autor = entradas["Autor"].get().strip()
            anio = entradas["Año"].get().strip()
            genero = entradas["Genero"].get().strip()
            estado = entradas["Estado"].get().strip()
            fi_dia, fi_mes, fi_anio = [c.get().strip() for c in entradas["Fecha Inicio"]]
            ff_dia, ff_mes, ff_anio = [c.get().strip() for c in entradas["Fecha Fin"]]

            # --- Validación de campos vacíos ---
            campos_faltantes = []
            if not referencia: campos_faltantes.append("Referencia")
            if not nombre: campos_faltantes.append("Nombre")
            if not autor: campos_faltantes.append("Autor")
            if not anio: campos_faltantes.append("Año")
            if not genero: campos_faltantes.append("Género")
            if not estado: campos_faltantes.append("Estado")
            if not (fi_dia and fi_mes and fi_anio): campos_faltantes.append("Fecha Inicio")
            if not (ff_dia and ff_mes and ff_anio): campos_faltantes.append("Fecha Fin")

            if campos_faltantes:
                mensaje = "Por favor completa:\n- " + "\n- ".join(campos_faltantes)
                messagebox.showwarning("Campos incompletos", mensaje)
                return

            # --- Validaciones específicas ---
            errores = []

            # Referencia
            if not re.match(r"^[A-Z]{3}\d{3}$", referencia):
                errores.append("Formato de referencia inválido (AAA999).")

            # Año
            if not anio.isdigit():
                errores.append("El año debe ser un número.")
                anio_int = None
            else:
                anio_int = int(anio)
                anio_actual = datetime.datetime.now().year
                if anio_int < 0 or anio_int > anio_actual:
                    errores.append(f"Año entre 0 y {anio_actual}.")

            # Fechas
            try:
                fecha_inicio = datetime.date(int(fi_anio), int(fi_mes), int(fi_dia))
                fecha_fin = datetime.date(int(ff_anio), int(ff_mes), int(ff_dia))

                if fecha_inicio > fecha_fin:
                    errores.append("La fecha de inicio no puede ser posterior a la fecha de fin.")

                # ✅ Nueva validación: no se puede leer antes del año de publicación
                if anio_int and fecha_inicio.year < anio_int:
                    errores.append(f"No puedes empezar a leer antes del año de publicación ({anio_int}).")
                if anio_int and fecha_fin.year < anio_int:
                    errores.append(f"No puedes terminar de leer antes del año de publicación ({anio_int}).")

            except ValueError:
                errores.append("Las fechas no son válidas.")

            if errores:
                mensaje = "Se encontraron problemas:\n- " + "\n- ".join(errores)
                messagebox.showwarning("Errores", mensaje)
                return

            # --- Guardar ---
            if libro_editando["referencia"]:
                try:
                    gestor_libros.eliminar_libro(usuario, libro_editando["referencia"])
                except ValueError:
                    pass
                libro_editando["referencia"] = None

            gestor_libros.agregar_libro(
                usuario, referencia, nombre, autor, anio_int, genero, estado,
                fecha_inicio.strftime("%d/%m/%Y"),
                fecha_fin.strftime("%d/%m/%Y")
            )

            messagebox.showinfo("Éxito", "Libro guardado correctamente")
            actualizar_lista()
            limpiar_formulario()

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

            if libro_editando.get("referencia") == referencia:
                libro_editando["referencia"] = None
                limpiar_formulario()

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
    tk.Button(btn_frame, text="Editar Libro", command=editar_libro).grid(row=0, column=2, padx=10)
    tk.Button(btn_frame, text="Salir", command=salir).grid(row=0, column=3, padx=10)

    actualizar_lista()
    root.mainloop()