import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re

class BibliotecaGUI:
    def __init__(self, usuario, gestor_libros):
        self.usuario = usuario
        self.gestor_libros = gestor_libros

        # --- Ventana principal ---
        self.root = tk.Tk()
        self.root.title("Biblioteca Virtual Personal")
        self.root.resizable(False, False)
        self.centrar_ventana(1600, 800)

        # Diccionario para entradas del formulario
        self.entradas = {}
        # Variables de filtros
        self.Referencia_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        # Estado de edición
        self.libro_editando = {"referencia": None}

        # Construcción de la interfaz
        self.crear_interfaz()

        # Actualizar lista de libros
        self.actualizar_lista()

        # Iniciar loop principal
        self.root.mainloop()

    def centrar_ventana(self, ancho, alto):
        """Centra la ventana self.root en pantalla."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        # Título superior
        tk.Label(self.root, text=f"Bienvenido {self.usuario} a tu Biblioteca Virtual Personal",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Contenedores
        top_frame = tk.Frame(self.root, height=400)
        top_frame.pack(side="top", fill="x", padx=20, pady=10)

        bottom_frame = tk.Frame(self.root, height=350, bg="#f5f5f5")
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        tk.Label(bottom_frame, text="Esto es para añadir otras cositas después",
                 fg="gray", font=("Arial", 11)).pack(pady=20)

        # ----------- FORMULARIO -----------
        form_frame = tk.Frame(top_frame, bd=2, relief="groove", padx=15, pady=15)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form_frame, text="Formulario para añadir o actualizar un libro",
                 font=("Arial", 12, "bold"), fg="navy").grid(row=0, column=0, columnspan=2, pady=(0, 15))

        labels = ["Referencia*", "Título*", "Autor*", "Año*", "Género*", "Estado*", "Fecha Inicio*", "Fecha Fin*"]

        for i, label in enumerate(labels, start=1):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            field_frame = tk.Frame(form_frame)
            field_frame.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            if label == "Referencia*":
                entry_ref = tk.Entry(field_frame)
                entry_ref.pack(side="left")
                self.entradas[label] = entry_ref
                tk.Label(field_frame, text="Formato: AAA999 (A-Z,0-9)", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label == "Título*":
                entry = tk.Entry(field_frame)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Título del libro", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label == "Autor*":
                entry = tk.Entry(field_frame)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Nombre del autor", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label == "Año*":
                entry = tk.Entry(field_frame, width=10)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Año de publicación (número)", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label == "Género*":
                genero_var = tk.StringVar()
                combo = ttk.Combobox(field_frame, textvariable=genero_var,
                                     values=["Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"],
                                     state="readonly", width=18)
                combo.pack(side="left")
                self.entradas[label] = genero_var
                tk.Label(field_frame, text="Selecciona el género", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label == "Estado*":
                estado_var = tk.StringVar()
                combo = ttk.Combobox(field_frame, textvariable=estado_var,
                                     values=["Leído", "Pendiente"], state="readonly", width=15)
                combo.pack(side="left")
                self.entradas[label] = estado_var
                tk.Label(field_frame, text="Estado de lectura (Leído/Pendiente)", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)
            elif label in ["Fecha Inicio*", "Fecha Fin*"]:
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
                self.entradas[label] = (combo_dia, combo_mes, combo_anio)
                tk.Label(field_frame, text="Selecciona la fecha (DD/MM/AAAA)", fg="gray", font=("Arial", 8)).pack(side="left", padx=8)

        # ----------- FILTROS Y TABLA -----------
        tabla_frame_container = tk.Frame(top_frame)
        tabla_frame_container.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Filtros
        filtro_frame = tk.LabelFrame(tabla_frame_container, text="Filtros de búsqueda")
        filtro_frame.pack(side="top", fill="x", pady=(0, 10))

        tk.Label(filtro_frame, text="Referencia:").grid(row=0, column=0, padx=5)
        tk.Entry(filtro_frame, textvariable=self.Referencia_var, width=20).grid(row=0, column=1, padx=5)

        tk.Label(filtro_frame, text="Género:").grid(row=0, column=2, padx=5)
        ttk.Combobox(filtro_frame, textvariable=self.genero_var,
                     values=["", "Novela", "Ciencia Ficción", "Historia", "Fantasía", "Ensayo", "Otro"],
                     state="readonly", width=15).grid(row=0, column=3, padx=5)

        tk.Label(filtro_frame, text="Estado:").grid(row=0, column=4, padx=5)
        ttk.Combobox(filtro_frame, textvariable=self.estado_var,
                     values=["", "Leído", "Pendiente"], state="readonly", width=15).grid(row=0, column=5, padx=5)

        tk.Label(filtro_frame, text="Autor:").grid(row=0, column=6, padx=5)
        tk.Entry(filtro_frame, textvariable=self.autor_var, width=20).grid(row=0, column=7, padx=5)

        tk.Button(filtro_frame, text="Aplicar filtros", command=self.aplicar_filtros).grid(row=0, column=8, padx=10, pady=3)
        tk.Button(filtro_frame, text="Limpiar filtros", command=self.limpiar_filtros).grid(row=0, column=9, padx=10)

        # Tabla
        tabla_frame = tk.Frame(tabla_frame_container, bd=2, relief="groove")
        tabla_frame.pack(side="top", fill="both", expand=True)

        columnas = ("Referencia", "Título", "Autor", "Año publicación", "Género", "Estado", "Iniciado en", "Terminado en")
        self.scroll_y = tk.Scrollbar(tabla_frame, orient="vertical")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings",
                                  height=10, yscrollcommand=self.scroll_y.set)
        self.scroll_y.config(command=self.tabla.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")

        # Botones
        btn_frame = tk.Frame(form_frame, pady=20)
        btn_frame.grid(row=len(self.entradas) + 1, column=0, columnspan=2)

        tk.Button(btn_frame, text="Guardar Libro", command=self.guardar_libro, width=15, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Eliminar Libro", command=self.eliminar_libro, width=15, bg="#f44336", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Editar Libro", command=self.editar_libro, width=15, bg="#2196F3", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Salir", command=self.salir, width=15, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)

    # ---------------- MÉTODOS ----------------
    def aplicar_filtros(self):
        self.tabla.delete(*self.tabla.get_children())
        libros = self.gestor_libros.listar_libros(self.usuario)
        if self.genero_var.get():
            libros = [l for l in libros if l["genero"].lower() == self.genero_var.get().lower()]
        if self.estado_var.get():
            libros = [l for l in libros if l["estado"].lower() == self.estado_var.get().lower()]
        if self.autor_var.get():
            libros = [l for l in libros if self.autor_var.get().lower() in l["autor"].lower()]
        if self.Referencia_var.get():
            libros = [l for l in libros if self.Referencia_var.get().upper() in l["referencia"].upper()]
        for libro in libros:
            self.tabla.insert("", "end", values=(
                libro['referencia'], libro['titulo'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))

    def limpiar_filtros(self):
        self.genero_var.set("")
        self.estado_var.set("")
        self.autor_var.set("")
        self.Referencia_var.set("")
        self.actualizar_lista()

    def limpiar_formulario(self):
        for key, entry in self.entradas.items():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.StringVar):
                entry.set("")
            elif isinstance(entry, tuple):
                for c in entry: c.set("")

    def actualizar_lista(self):
        self.tabla.delete(*self.tabla.get_children())
        libros = self.gestor_libros.listar_libros(self.usuario)
        for libro in libros:
            self.tabla.insert("", "end", values=(
                libro['referencia'], libro['titulo'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))

    def editar_libro(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para editar")
            libro_seleccionado = self.tabla.item(seleccion[0])["values"]
            self.libro_editando["referencia"] = libro_seleccionado[0]

            self.entradas["Referencia*"].delete(0, tk.END)
            self.entradas["Referencia*"].insert(0, libro_seleccionado[0])
            self.entradas["Título*"].delete(0, tk.END)
            self.entradas["Título*"].insert(0, libro_seleccionado[1])
            self.entradas["Autor*"].delete(0, tk.END)
            self.entradas["Autor*"].insert(0, libro_seleccionado[2])
            self.entradas["Año*"].delete(0, tk.END)
            self.entradas["Año*"].insert(0, libro_seleccionado[3])
            self.entradas["Género*"].set(libro_seleccionado[4])
            self.entradas["Estado*"].set(libro_seleccionado[5])

            fi_dia, fi_mes, fi_anio = libro_seleccionado[6].split("/")
            ff_dia, ff_mes, ff_anio = libro_seleccionado[7].split("/")

            self.entradas["Fecha Inicio*"][0].set(fi_dia)
            self.entradas["Fecha Inicio*"][1].set(fi_mes)
            self.entradas["Fecha Inicio*"][2].set(fi_anio)
            self.entradas["Fecha Fin*"][0].set(ff_dia)
            self.entradas["Fecha Fin*"][1].set(ff_mes)
            self.entradas["Fecha Fin*"][2].set(ff_anio)

            messagebox.showinfo("Editar", "Modifique los campos y presione 'Guardar Libro'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar_libro(self):
        try:
            referencia = self.entradas["Referencia*"].get().strip().upper()
            titulo = self.entradas["Título*"].get().strip()
            autor = self.entradas["Autor*"].get().strip()
            anio = self.entradas["Año*"].get().strip()
            genero = self.entradas["Género*"].get().strip()
            estado = self.entradas["Estado*"].get().strip()
            fi_dia, fi_mes, fi_anio = [c.get().strip() for c in self.entradas["Fecha Inicio*"]]
            ff_dia, ff_mes, ff_anio = [c.get().strip() for c in self.entradas["Fecha Fin*"]]

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

            errores = []
            if not re.match(r"^[A-Z]{3}\d{3}$", referencia):
                errores.append("Formato de referencia inválido (AAA999).")
            if not anio.isdigit():
                errores.append("El año debe ser un número.")
                anio_int = None
            else:
                anio_int = int(anio)
                anio_actual = datetime.datetime.now().year
                if anio_int < 0 or anio_int > anio_actual:
                    errores.append(f"Año entre 0 y {anio_actual}.")
            try:
                fecha_inicio = datetime.date(int(fi_anio), int(fi_mes), int(fi_dia))
                fecha_fin = datetime.date(int(ff_anio), int(ff_mes), int(ff_dia))
                if fecha_inicio > fecha_fin:
                    errores.append("La fecha de inicio no puede ser posterior a la fecha de fin.")
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

            if self.libro_editando["referencia"]:
                try:
                    self.gestor_libros.eliminar_libro(self.usuario, self.libro_editando["referencia"])
                except ValueError:
                    pass
                self.libro_editando["referencia"] = None

            self.gestor_libros.agregar_libro(
                self.usuario, referencia, titulo, autor, anio_int, genero, estado,
                fecha_inicio.strftime("%d/%m/%Y"),
                fecha_fin.strftime("%d/%m/%Y")
            )

            messagebox.showinfo("Éxito", "Libro guardado correctamente")
            self.actualizar_lista()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_libro(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para eliminar")
            libro_seleccionado = self.tabla.item(seleccion[0])["values"]
            referencia = libro_seleccionado[0]

            confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar el libro {referencia}?")
            if not confirmar:
                return

            self.gestor_libros.eliminar_libro(self.usuario, referencia)
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def salir(self):
        self.root.destroy()
        import Main
        Main.Ventana_Ingreso()

