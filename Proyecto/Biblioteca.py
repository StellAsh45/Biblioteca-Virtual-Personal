import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import re
import csv
import Main

# Clase principal de la aplicación de la biblioteca virtual
class BibliotecaGUI:
    def __init__(self, usuario, gestor_libros):
        # Usuario actual y gestor de libros para la logica de libros
        self.usuario = usuario
        self.gestor_libros = gestor_libros

        # -------- Ventana principal --------
        self.root = tk.Tk()
        self.root.title("Biblioteca Virtual Personal")
        self.root.resizable(False, False) # Evita redimensionamiento
        self.root.configure(bg="#AE9C8F") # Color de fondo
        self.centrar_ventana(1400, 600) # Centra la ventana en pantalla
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

    # Centra la ventana en la pantalla con el tamaño dado
    def centrar_ventana(self, ancho, alto):
        #Centra la ventana self.root en pantalla.
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Crea la interfaz gráfica de la aplicación
    def crear_interfaz(self):
        # --- Título superior ---
        tk.Label(self.root, text=f" 📚 Bienvenido, {self.usuario}, a tu Biblioteca Virtual Personal 📚",font=("Arial", 16, "bold"),bg="#AE9C8F",fg="#381D03").pack(pady=10)
        # --- Contenedor ---
        frame = tk.Frame(self.root, height=400,bg="#AE9C8F")
        frame.pack(side="top", fill="x", padx=20, pady=10)
        # ----------- FORMULARIO -----------
        form_frame = tk.Frame(frame,bg='#E5D2C4', bd=2, padx=15, pady=15)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)
        # Titulo formulario
        tk.Label(form_frame, text="Formulario para añadir un libro",font=("Arial", 14, "bold"),bg='#E5D2C4',fg="#381D03").grid(row=0, column=0, columnspan=2, pady=(0, 15)) # columnspan para centrar y pady para separar
        # Campos del formulario
        labels = ["Referencia*", "Título*", "Autor*", "Año*", "Género*", "Estado*", "Fecha Inicio*", "Fecha Fin*"]
        # Se crean los campos del formulario de forma dinamica
        for i, label in enumerate(labels, start=1):
            tk.Label(form_frame, text=label,font=("Arial",12,"bold"),bg='#E5D2C4',fg="#381D03").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            # Subframe para entradas y etiquetas de ayuda
            field_frame = tk.Frame(form_frame)
            field_frame.grid(row=i, column=1, padx=5, pady=5, sticky="w") # Sticky para alinear a la izquierda
            # Diferentes configuraciones segun el campo
            if label == "Referencia*":
                entry_ref = tk.Entry(field_frame)
                entry_ref.pack(side="left")
                self.entradas[label] = entry_ref
                tk.Label(field_frame, text="Formato: AAA999 (A-Z,0-9)",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both")
            elif label == "Título*":
                entry = tk.Entry(field_frame)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Título del libro",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both")
            elif label == "Autor*":
                entry = tk.Entry(field_frame)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Nombre del autor",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both")
            elif label == "Año*":
                entry = tk.Entry(field_frame, width=10)
                entry.pack(side="left")
                self.entradas[label] = entry
                tk.Label(field_frame, text="Año de publicación (número)",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both")
            elif label == "Género*":
                # Combobox permite seleccionar de una lista
                genero_var = tk.StringVar()
                combo = ttk.Combobox(field_frame, textvariable=genero_var,
                                     values=["Novela", "Cuento", "Poesía", "Drama", "Ensayo", "Fábula", "Ciencia Ficción", 
                                             "Historia", "Fantasía", "Filosofía", "Psicología", "Política", "Economía",
                                             "Matematicas", "Física", "Química", "Biología", "Medicina", "Informática", 
                                             "Distopía", "Misterio", "Terror", "Aventura", "Otro"],
                                     state="readonly", width=18)
                combo.pack(side="left")
                self.entradas[label] = genero_var
                tk.Label(field_frame, text="Selecciona el género",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both")
            elif label == "Estado*":
                estado_var = tk.StringVar()
                combo = ttk.Combobox(field_frame, textvariable=estado_var,
                                     values=["Leído", "Pendiente"], state="readonly", width=15)
                combo.pack(side="left")
                self.entradas[label] = estado_var
                tk.Label(field_frame, text="Estado de lectura (Leído/Pendiente)",bg='#E5D2C4',fg="#381D03",font=("Arial",8,"italic")).pack(side="left",fill="both") 
            elif label in ["Fecha Inicio*", "Fecha Fin*"]:
                subframe = tk.Frame(field_frame,bg='#E5D2C4') # Subframe para organizar los Combobox
                subframe.pack(side="left")
                dias = [str(d).zfill(2) for d in range(1, 32)] # zfill para rellenar con ceros a la izquierda
                meses = [str(m).zfill(2) for m in range(1, 13)] 
                anio_actual = datetime.datetime.now().year # Año actual
                anios = [str(a) for a in range(1900, anio_actual + 1)] # Desde 1900 hasta el año actual
                combo_dia = ttk.Combobox(subframe, values=dias, width=4, state="readonly") # readonly para no permitir escribir
                combo_mes = ttk.Combobox(subframe, values=meses, width=4, state="readonly")
                combo_anio = ttk.Combobox(subframe, values=anios, width=6, state="readonly")
                combo_dia.pack(side="left", padx=2)
                combo_mes.pack(side="left", padx=2)
                combo_anio.pack(side="left", padx=2)
                self.entradas[label] = (combo_dia, combo_mes, combo_anio)
                tk.Label(field_frame, text="Selecciona la fecha (DD/MM/AAAA)",bg='#E5D2C4', fg="#381D03", font=("Arial",8,"italic")).pack(side="left",fill="both") # Fill para que ocupe todo el espacio disponible
        
        # ----------- BOTONES DEL FORMULARIO (CRUD) -----------
        style=ttk.Style() # Estilos para los botones y tabla
        style.theme_use("clam")  # Tema flexible
        btn_frame = tk.Frame(form_frame, pady=20,bg='#E5D2C4') # Subframe para los botones
        btn_frame.grid(row=len(self.entradas) + 1, column=0, columnspan=2) # columnspan para centrar
        tk.Button(btn_frame, text="Guardar Libro", command=self.guardar_libro,width=15,bg="#4CAF50",fg="white").grid(row=0,column=0,padx=5)
        tk.Button(btn_frame, text="Eliminar Libro", command=self.eliminar_libro,width=15,bg="#f44336",fg="white").grid(row=0,column=1,padx=5) 
        tk.Button(btn_frame, text="Editar Libro", command=self.editar_libro,width=15,bg="#2196F3",fg="white").grid(row=0,column=2,padx=5)
        tk.Button(btn_frame, text="Exportar a CSV", command=self.exportar_csv,width=15,bg="#FF9800",fg="white").grid(row=1,column=0,padx=5)
        tk.Button(btn_frame, text="Salir", command=self.salir,width=15,bg="#A29191",fg="White").grid(row=1,column=1,padx=5)
        # Titulo inferior
        tk.Label(self.root, text=f"Gracias, {self.usuario}, por usar nuestros servicios 👍",font=("Arial", 16, "bold"),bg="#AE9C8F",fg="#381D03").pack(pady=10)
        # ----------- FILTROS, TABLA Y ESTADÍSTICAS -----------
        tabla_frame_container = tk.Frame(frame,bg="#AE9C8F") # Contenedor para filtros, tabla y estadísticas
        tabla_frame_container.pack(side="right", padx=5, pady=10, fill="both") # Fill both para que ocupe todo el espacio disponible
        # ----------- FILTROS -----------
        # Seccion de busqueda con criterios: Referencia, Autor, Género, Estado
        filtro_frame = tk.LabelFrame(tabla_frame_container, text="Filtros de búsqueda",font=("Arial", 12, "bold"),bg='#F2E8E1',fg="#381D03",bd=0,labelanchor="n") # LabelFrame para agrupar los filtros
        filtro_frame.pack(side="top", fill="x", pady=(0, 10)) # pady para separar de la tabla
        # Filtro por referencia
        tk.Label(filtro_frame, text="Referencia:",bg='#F2E8E1',fg="#381D03").grid(row=0, column=0, padx=5)
        tk.Entry(filtro_frame, textvariable=self.Referencia_var, width=20).grid(row=0, column=1, padx=5)
        # Filtro por autor
        tk.Label(filtro_frame, text="Autor:",bg='#F2E8E1',fg="#381D03").grid(row=0, column=2, padx=5)
        tk.Entry(filtro_frame, textvariable=self.autor_var, width=20).grid(row=0, column=3, padx=5)
        # Filtro por género
        tk.Label(filtro_frame, text="Género:",bg='#F2E8E1',fg="#381D03").grid(row=0, column=4, padx=5)
        ttk.Combobox(filtro_frame, textvariable=self.genero_var,
                     values=["Novela", "Cuento", "Poesía", "Drama", "Ensayo", "Fábula", "Ciencia Ficción", 
                                             "Historia", "Fantasía", "Filosofía", "Psicología", "Política", "Economía",
                                             "Matematicas", "Física", "Química", "Biología", "Medicina", "Informática", 
                                             "Distopía", "Misterio", "Terror", "Aventura", "Otro"],
                     state="readonly", width=15).grid(row=0, column=5, padx=5)
        # Filtro por estado
        tk.Label(filtro_frame, text="Estado:",bg='#F2E8E1',fg="#381D03").grid(row=0, column=6, padx=5)
        ttk.Combobox(filtro_frame, textvariable=self.estado_var,
                     values=["", "Leído", "Pendiente"], state="readonly", width=15).grid(row=0, column=7, padx=5)
        # Botones de aplicar y limpiar filtros
        tk.Button(filtro_frame, text="Aplicar filtros", command=self.aplicar_filtros, width=15,bg="#A29191",fg="White").grid(row=1, column=3, padx=10, pady=3)
        tk.Button(filtro_frame, text="Limpiar filtros", command=self.limpiar_filtros, width=15,bg="#A29191",fg="White").grid(row=1, column=4, padx=10)
        # ----------- TABLA -----------
        tabla_frame = tk.Frame(tabla_frame_container) # Contenedor para la tabla y los scrollbars
        tabla_frame.pack(side="top", fill="both",expand=True)
        # Definir columnas de la tabla
        columnas = ("Referencia", "Título", "Autor", "Año publicación", "Género", "Estado", "Iniciado en", "Terminado en")
        # Estilos para la tabla
        style.configure("Treeview.Heading",background="#F2E8E1",foreground="#381D03",font=("Arial", 11, "bold"))
        style.configure("Treeview",background="#F2E8E1",fieldbackground="#F2E8E1",foreground="#381D03",font=("Arial", 9))
        # Crear scrollbars
        self.scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", style="Custom.Vertical.TScrollbar") # Scroll vertical
        self.scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", style="Custom.Horizontal.TScrollbar")  # Scroll horizontal
        # Estilo para los scrollbars
        style.configure("Custom.Vertical.TScrollbar",background="#CBB8AA",arrowcolor="#381D03",troughcolor="#F2E8E1",bordercolor="#381D03")
        style.configure("Custom.Horizontal.TScrollbar",background="#CBB8AA",arrowcolor="#381D03",troughcolor="#F2E8E1",bordercolor="#381D03")
        # Crear la tabla
        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas, # T
            show="headings", # Sin columna vacía inicial
            height=10, 
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
            style="Treeview"
        )

        #Configurar scrollbars para mover la tabla
        self.scroll_y.config(command=self.tabla.yview)
        self.scroll_x.config(command=self.tabla.xview)
        # Posicionar tabla y scrollbars
        self.scroll_y.pack(side="right", fill="y") # Scroll vertical a la derecha de la tabla
        self.scroll_x.pack(side="bottom", fill="x")  # Scroll horizontal debajo de la tabla
        self.tabla.pack(side="left", fill="both")
        # Configurar encabezados y columnas tamaño fijo y centrado
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="center", stretch=False)

        # ----------- ESTADISTICAS -----------
        resumen_frame = tk.Frame(tabla_frame_container,bg="#F2E8E1") # Contenedor para las estadísticas
        resumen_frame.pack(side="bottom", fill="x", pady=(10,0))
        tk.Label(resumen_frame, text="📊 Resumen de Libros", font=("Arial", 12, "bold"),bg="#F2E8E1", fg="#381D03").pack(pady=5)
        # Contenedor de contadores de libros
        contador_frame = tk.Frame(resumen_frame,bg="#F2E8E1")
        contador_frame.pack(pady=5)
        # Cantidad de libros leidos
        self.lbl_leidos = tk.Label(contador_frame, text="Leídos: 0", font=("Arial", 11, "bold"), fg="green",bg="#F2E8E1")
        self.lbl_leidos.pack(side="left",padx=20,fill="both")
        # Cantidad de libros pendientes
        self.lbl_pendientes = tk.Label(contador_frame, text="Pendientes: 0", font=("Arial", 11, "bold"), fg="red",bg="#F2E8E1")
        self.lbl_pendientes.pack(side="left",padx=20,fill="both")
        # Cantidad total de libros
        self.lbl_total = tk.Label(contador_frame, text="Total: 0", font=("Arial", 11, "bold"), fg="black",bg="#F2E8E1")
        self.lbl_total.pack(side="left",padx=20,fill="both")

    # ---------------- MÉTODOS ----------------
    # Aplica los filtros seleccionados y actualiza la tabla
    def aplicar_filtros(self):
        self.tabla.delete(*self.tabla.get_children()) # Limpia la tabla y actualiza con los libros filtrados
        libros = self.gestor_libros.listar_libros(self.usuario)
        if self.genero_var.get():
            libros = [l for l in libros if l["genero"].lower() == self.genero_var.get().lower()] # Filtra por género 
        if self.estado_var.get():
            libros = [l for l in libros if l["estado"].lower() == self.estado_var.get().lower()] # Filtra por estado
        if self.autor_var.get():
            libros = [l for l in libros if self.autor_var.get().lower() in l["autor"].lower()] # Filtra por autor
        if self.Referencia_var.get():
            libros = [l for l in libros if self.Referencia_var.get().upper() in l["referencia"].upper()] # Filtra por referencia 
        for libro in libros:
            self.tabla.insert("", "end", values=(
                libro['referencia'], libro['titulo'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            )) # Inserta los libros filtrados en la tabla

    # Limpia los filtros y muestra todos los libros
    def limpiar_filtros(self):
        self.genero_var.set("") # Resetea las variables de filtro
        self.estado_var.set("")
        self.autor_var.set("")
        self.Referencia_var.set("")
        self.actualizar_lista()

    # Limpiar el formulario despues de ciertas acciones para
    # Que el usuario no tenga que hacerlo de forma manual
    def limpiar_formulario(self):
        for key, entry in self.entradas.items():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.StringVar):
                entry.set("")
            elif isinstance(entry, tuple):
                for c in entry: c.set("")

    # Actualiza las estadísticas de libros leídos, pendientes y total
    def actualizar_estadisticas(self,libros=None):
        if libros is None: 
            libros = self.gestor_libros.listar_libros(self.usuario) 
        total=len(libros) # Cuenta total de libros
        leidos = sum(1 for l in libros if l["estado"].lower() == "leído") # Cuenta libros leidos
        pendientes = sum(1 for l in libros if l["estado"].lower() == "pendiente") # Cuenta libros pendientes
        # Actualizar labels
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_leidos.config(text=f"Leídos: {leidos}")
        self.lbl_pendientes.config(text=f"Pendientes: {pendientes}")

    # Actualiza la lista de libros en la tabla
    def actualizar_lista(self):
        self.tabla.delete(*self.tabla.get_children())
        libros = self.gestor_libros.listar_libros(self.usuario)
        for libro in libros:
            self.tabla.insert("", "end", values=(
                libro['referencia'], libro['titulo'], libro['autor'],
                libro['anio'], libro['genero'], libro['estado'],
                libro['fecha_inicio'], libro['fecha_fin']
            ))
        self.actualizar_estadisticas()

    # Edita un libro seleccionado en la tabla
    def editar_libro(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para editar")
            libro_seleccionado = self.tabla.item(seleccion[0])["values"]
            self.libro_editando["referencia"] = libro_seleccionado[0]
            # Borra el formulario y rellena con los datos del libro seleccionado
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

    # Guarda un libro nuevo o editado
    def guardar_libro(self):
        try:
            referencia = self.entradas["Referencia*"].get().strip().upper() # Mayusculas y sin espacios
            titulo = self.entradas["Título*"].get().strip()
            autor = self.entradas["Autor*"].get().strip()
            anio = self.entradas["Año*"].get().strip()
            genero = self.entradas["Género*"].get().strip()
            estado = self.entradas["Estado*"].get().strip()
            fi_dia, fi_mes, fi_anio = [c.get().strip() for c in self.entradas["Fecha Inicio*"]]
            ff_dia, ff_mes, ff_anio = [c.get().strip() for c in self.entradas["Fecha Fin*"]]
            # Validaciones
            campos_faltantes = []
            if not referencia: campos_faltantes.append("Referencia*")
            if not titulo: campos_faltantes.append("Título*")
            if not autor: campos_faltantes.append("Autor*")
            if not anio: campos_faltantes.append("Año*")
            if not genero: campos_faltantes.append("Género*")
            if not estado: campos_faltantes.append("Estado*")
            if not (fi_dia and fi_mes and fi_anio): campos_faltantes.append("Fecha Inicio*")
            if not (ff_dia and ff_mes and ff_anio): campos_faltantes.append("Fecha Fin*")
            # Si faltan campos obligatorios, mostrar mensaje
            if campos_faltantes:
                mensaje = "Por favor completa:\n- " + "\n- ".join(campos_faltantes)
                messagebox.showwarning("Campos incompletos", mensaje)
                return
            # Validaciones adicionales
            errores = []
            if not re.match(r"^[A-Z]{3}\d{3}$", referencia):
                errores.append("Formato de referencia inválido (AAA999).")
            anio_int=None
            try:
                anio_int = int(anio)
                anio_actual = datetime.datetime.now().year
                if anio_int > anio_actual:  # Año mayor al actual
                    errores.append(f"El año no puede ser mayor a {anio_actual}.")
            except ValueError:
                errores.append("El año debe ser un número válido.")
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
            # Verifica los errores y muestra mensaje
            if errores:
                mensaje = "Se encontraron problemas:\n- " + "\n- ".join(errores)
                messagebox.showwarning("Errores", mensaje)
                return
            # Si se está editando, eliminar el libro antiguo
            if self.libro_editando["referencia"]:
                try:
                    self.gestor_libros.eliminar_libro(self.usuario, self.libro_editando["referencia"])
                except ValueError:
                    pass
                self.libro_editando["referencia"] = None
            # Agregar el libro (nuevo o editado)
            self.gestor_libros.agregar_libro(self.usuario, referencia, titulo, autor, anio_int, genero, estado,fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"))
            messagebox.showinfo("Éxito", "Libro guardado correctamente")
            self.actualizar_lista()
            self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Elimina un libro seleccionado en la tabla
    def eliminar_libro(self):
        try:
            seleccion = self.tabla.selection()
            if not seleccion:
                raise ValueError("Debe seleccionar un libro para eliminar")
            libro_seleccionado = self.tabla.item(seleccion[0])["values"] # Valores del libro seleccionado
            referencia = libro_seleccionado[0] # Primera columna es la referencia
            # Confirmar eliminación
            confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar el libro {referencia}?")
            if not confirmar:
                return
            # Eliminar libro
            self.gestor_libros.eliminar_libro(self.usuario, referencia)
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Exporta la lista de libros a un archivo CSV
    def exportar_csv(self):
        try:
            libros = self.gestor_libros.listar_libros(self.usuario)
            if not libros:
                messagebox.showwarning("Aviso", "No hay libros para exportar.")
                return
            # Seleccionar ruta de guardado
            archivo = filedialog.asksaveasfilename( # Diálogo para seleccionar archivo
                defaultextension=".csv", # Extensión por defecto
                filetypes=[("CSV files", "*.csv")], # Tipo de archivo
                title="Guardar como", # Título del diálogo
                initialfile=f"{self.usuario}_biblioteca.csv" # Nombre por defecto del archivo
                )
            if not archivo:
                return  # cancelado
            # Escribir archivo CSV
            with open(archivo, "w", newline="", encoding="utf-8-sig") as f: # utf-8-sig para evitar problemas con tildes
                writer = csv.writer(f)
                writer.writerow(["Referencia", "Título", "Autor", "Año publicación", "Género", "Estado", "Iniciado en", "Terminado en"]) # Encabezados
                for libro in libros:
                    writer.writerow([
                        libro['referencia'], libro['titulo'], libro['autor'],
                        libro['anio'], libro['genero'], libro['estado'],
                        libro['fecha_inicio'], libro['fecha_fin']
                    ]) # Filas de datos
            messagebox.showinfo("Éxito", f"📁 Exportado correctamente a:\n{archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    # Sale de la aplicación y vuelve a la ventana de acceso
    def salir(self):
        self.root.destroy()
        Main.VentanaAcceso()