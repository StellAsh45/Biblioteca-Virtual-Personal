import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import Main as m

# Gui para la biblioteca virtual personal
def iniciar_gui(usuario, gestor_libros):
    root = tk.Tk()
    root.title("Biblioteca Virtual Personal")
    root.resizable(False, False)
    m.centrar_ventana(root, 1600, 800)

    # Título superior
    tk.Label(root,text=f"Bienvenido {usuario} a tu Biblioteca Virtual Personal",font=("Arial", 14, "bold")).pack(pady=10)

    # --- Contenedor principal dividido en 2 secciones ---
    top_frame = tk.Frame(root, height=400)   # Parte superior
    top_frame.pack(side="top", fill="x", padx=20, pady=10)

    bottom_frame = tk.Frame(root, height=350, bg="#f5f5f5")  # Parte inferior reservada
    bottom_frame.pack(side="bottom", fill="both", expand=True)
    tk.Label(bottom_frame, text="Esto es para añadir otras cositas despues",
             fg="gray", font=("Arial", 11)).pack(pady=20)

    # ----------- FORMULARIO -----------
    form_frame = tk.Frame(top_frame, bd=2, relief="groove", padx=15, pady=15)
    form_frame.pack(side="left", fill="y", padx=10, pady=10)

    tk.Label(form_frame,text="Formulario para añadir o actualizar un libro",font=("Arial", 12, "bold"),fg="navy").grid(row=0, column=0, columnspan=2, pady=(0, 15))

    # Campos del formulario
    labels = ["Referencia*", "Título*", "Autor*", "Año*", "Género*", "Estado*", "Fecha Inicio*", "Fecha Fin*"]
    entradas = {}

    for i, label in enumerate(labels, start=1):
        tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)

        ayuda = ""
        field_frame = tk.Frame(form_frame)
        field_frame.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        if label == "Referencia*":
            ayuda = "Formato: AAA999 (A-Z,0-9)"
            entry_ref = tk.Entry(field_frame)
            entry_ref.pack(side="left")
            entradas[label] = entry_ref
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label == "Título*":
            ayuda = "Título del libro"
            entry = tk.Entry(field_frame)
            entry.pack(side="left")
            entradas[label] = entry
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label == "Autor*":
            ayuda = "Nombre del autor"
            entry = tk.Entry(field_frame)
            entry.pack(side="left")
            entradas[label] = entry
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label == "Año*":
            ayuda = "Año de publicacion (número)"
            entry = tk.Entry(field_frame, width=10)
            entry.pack(side="left")
            entradas[label] = entry
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label == "Género*":
            ayuda = "Selecciona el género"
            genero_var = tk.StringVar()
            combo = ttk.Combobox(
                field_frame, textvariable=genero_var,
                values=["Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"],
                state="readonly", width=18
            )
            combo.pack(side="left")
            entradas[label] = genero_var
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label == "Estado*":
            ayuda = "Estado de lectura (Leído/Pendiente)"
            estado_var = tk.StringVar()
            combo = ttk.Combobox(
                field_frame, textvariable=estado_var,
                values=["Leído", "Pendiente"],
                state="readonly", width=15
            )
            combo.pack(side="left")
            entradas[label] = estado_var
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        elif label in ["Fecha Inicio*", "Fecha Fin*"]:
            ayuda = "Selecciona la fecha(DD/MM/AAAA)"
            subframe = tk.Frame(field_frame)
            subframe.pack(side="left")

            dias = [str(d).zfill(2) for d in range(1, 32)]
            meses = [str(m).zfill(2) for m in range(1, 13)]
            anio_actual = datetime.datetime.now().year
            anios = [str(a) for a in range(1900, anio_actual + 1)]

            combo_dia = ttk.Combobox(subframe, values=dias, width=4, state="readonly")
            combo_mes = ttk.Combobox(subframe, values=meses, width=4, state="readonly")
            combo_anio = ttk.Combobox(subframe, values=anios, width=6, state="readonly")

            combo_dia.grid(row=0, column=0, padx=2)
            combo_mes.grid(row=0, column=1, padx=2)
            combo_anio.grid(row=0, column=2, padx=2)

            entradas[label] = (combo_dia, combo_mes, combo_anio)
            tk.Label(field_frame, text=ayuda, fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

    # ----------- TABLA -----------
    tabla_frame = tk.Frame(top_frame, bd=2, relief="groove")
    tabla_frame.pack(side="right", padx=10, pady=10)

    columnas = ("Referencia", "Título", "Autor", "Año publicación", "Género", "Estado", "Iniciado en", "Terminado en")

    scroll_y = tk.Scrollbar(tabla_frame, orient="vertical")
    tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                         height=10, yscrollcommand=scroll_y.set)  # 👈 menos altura

    scroll_y.config(command=tabla.yview)
    scroll_y.pack(side="right", fill="y")
    tabla.pack(side="left", fill="both")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=120, anchor="center")



    # --- Frame de filtros ---
    filtro_frame = tk.LabelFrame(root, text="Filtros de búsqueda")
    filtro_frame.pack(pady=10, fill="x")

    # Filtro por género
    genero_var = tk.StringVar()
    tk.Label(filtro_frame, text="Género:").grid(row=0, column=0, padx=5)
    combo_genero = ttk.Combobox(filtro_frame, textvariable=genero_var,
                               values=["", "Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"],
                               state="readonly", width=15)
    combo_genero.grid(row=0, column=1, padx=5)

        # Filtro por estado
    estado_var = tk.StringVar()
    tk.Label(filtro_frame, text="Estado:").grid(row=0, column=2, padx=5)
    combo_estado = ttk.Combobox(filtro_frame, textvariable=estado_var,
                               values=["", "Leído", "Pendiente"],
                               state="readonly", width=15)
    combo_estado.grid(row=0, column=3, padx=5)

    # Filtro por autor
    autor_var = tk.StringVar()
    tk.Label(filtro_frame, text="Autor:").grid(row=0, column=4, padx=5)
    entry_autor = tk.Entry(filtro_frame, textvariable=autor_var, width=20)
    entry_autor.grid(row=0, column=5, padx=5)

    # Botones de filtros
    tk.Button(filtro_frame, text="Aplicar filtros", command=lambda: aplicar_filtros()).grid(row=0, column=8, padx=10)
    tk.Button(filtro_frame, text="Limpiar filtros", command=lambda: limpiar_filtros()).grid(row=0, column=9, padx=10)




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
                libro['referencia'], libro['titulo'], libro['autor'],
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

            entradas["Referencia*"].delete(0, tk.END)
            entradas["Referencia*"].insert(0, libro_seleccionado[0])
            entradas["Título*"].delete(0, tk.END)
            entradas["Título*"].insert(0, libro_seleccionado[1])
            entradas["Autor*"].delete(0, tk.END)
            entradas["Autor*"].insert(0, libro_seleccionado[2])
            entradas["Año*"].delete(0, tk.END)
            entradas["Año*"].insert(0, libro_seleccionado[3])
            entradas["Género*"].set(libro_seleccionado[4])
            entradas["Estado*"].set(libro_seleccionado[5])

            fi_dia, fi_mes, fi_anio = libro_seleccionado[6].split("/")
            ff_dia, ff_mes, ff_anio = libro_seleccionado[7].split("/")

            entradas["Fecha Inicio*"][0].set(fi_dia)
            entradas["Fecha Inicio*"][1].set(fi_mes)
            entradas["Fecha Inicio*"][2].set(fi_anio)
            entradas["Fecha Fin*"][0].set(ff_dia)
            entradas["Fecha Fin*"][1].set(ff_mes)
            entradas["Fecha Fin*"][2].set(ff_anio)

            messagebox.showinfo("Editar", "Modifique los campos y presione 'Guardar Libro'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar_libro():
        try:
            referencia = entradas["Referencia*"].get().strip().upper()
            titulo = entradas["Título*"].get().strip()
            autor = entradas["Autor*"].get().strip()
            anio = entradas["Año*"].get().strip()
            genero = entradas["Género*"].get().strip()
            estado = entradas["Estado*"].get().strip()
            fi_dia, fi_mes, fi_anio = [c.get().strip() for c in entradas["Fecha Inicio*"]]
            ff_dia, ff_mes, ff_anio = [c.get().strip() for c in entradas["Fecha Fin*"]]

            # --- Validación de campos vacíos ---
            campos_faltantes = []
            if not referencia: campos_faltantes.append("Referencia*")
            if not titulo: campos_faltantes.append("Título*")
            if not autor: campos_faltantes.append("Autor*")
            if not anio: campos_faltantes.append("Año*")
            if not genero: campos_faltantes.append("Género*")
            if not estado: campos_faltantes.append("Estado*")
            if not (fi_dia and fi_mes and fi_anio): campos_faltantes.append("Fecha Inicio*")
            if not (ff_dia and ff_mes and ff_anio): campos_faltantes.append("Fecha Fin*")

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
                usuario, referencia, titulo, autor, anio_int, genero, estado,
                fecha_inicio.strftime("%d/%m/%Y"),
                fecha_fin.strftime("%d/%m/%Y")
            )

            messagebox.showinfo("Éxito", "Libro guardado correctamente")
            actualizar_lista()
            limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))



    def aplicar_filtros():
        tabla.delete(*tabla.get_children())
        libros = gestor_libros.listar_libros(usuario)

        # Aplicar filtros
        if genero_var.get():
            libros = [l for l in libros if l["genero"].lower() == genero_var.get().lower()]
        if estado_var.get():
            libros = [l for l in libros if l["estado"].lower() == estado_var.get().lower()]
        if autor_var.get():
            libros = [l for l in libros if autor_var.get().lower() in l["autor"].lower()]
       

        # Mostrar en tabla
        for libro in libros:
            tabla.insert("", "end", values=(
                libro['referencia'], libro['nombre'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))

    def limpiar_filtros():
        genero_var.set("")
        estado_var.set("")
        autor_var.set("")
        actualizar_lista()



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
    btn_frame = tk.Frame(form_frame, pady=20)
    btn_frame.grid(row=len(labels) + 1, column=0, columnspan=2)

    tk.Button(btn_frame, text="Guardar Libro",command=guardar_libro, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Eliminar Libro",command=eliminar_libro, width=15, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Editar Libro",command=editar_libro, width=15, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Salir",command=salir,width=15, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)
    
    actualizar_lista()
    root.mainloop()