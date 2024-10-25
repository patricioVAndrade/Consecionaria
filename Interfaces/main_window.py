import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from Models import *
from Reports import *
from Interfaces.registrar_auto_window import RegistroAutos
from Interfaces.registrar_cliente_window import RegistroClientes
from Interfaces.registrar_venta_window import RegistroVentas
from Interfaces.registrar_servicio_window import RegistroServicios
from Interfaces.consultar_auto_vendido_window import ConsultaAutosVendidos
from Interfaces.consultar_servicio_window import ConsultaServicios
from Interfaces.ventas_report_window import VentasReportWindow
from Utils.database import session
from Models.Auto import *
from Models.Venta import *
from Models.Servicio import *
from Models.Cliente import *
from Models.Vendedor import *
from PIL import Image, ImageTk


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Autos")
        self.geometry("1600x700")

        # PanedWindow para dividir en dos áreas
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # Marco izquierdo para botones
        self.frame_izquierda = ctk.CTkFrame(self, width=200)
        self.paned_window.add(self.frame_izquierda)

        # Marco derecho para la tabla (TabView)
        self.frame_derecha = ctk.CTkFrame(self)
        self.paned_window.add(self.frame_derecha)

        # Botones en la parte izquierda
        self.create_buttons()

        # Barra de selección para tablas
        self.create_table_selector()

        # Tabla que se actualizará
        self.tree = ttk.Treeview(self.frame_derecha, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar tabla inicial (autos registrados)
        self.mostrar_tabla("Autos")

        self.agregar_logo()

    def create_buttons(self):
        self.label_title = ctk.CTkLabel(
            self.frame_izquierda, text="Operaciones", font=("Arial", 20))
        self.label_title.pack(pady=20)

        self.btn_registro_autos = ctk.CTkButton(
            self.frame_izquierda, text="Registrar Autos", command=self.abrir_registro_autos)
        self.btn_registro_autos.pack(pady=10)

        self.btn_registro_clientes = ctk.CTkButton(
            self.frame_izquierda, text="Registrar Clientes", command=self.abrir_registro_clientes)
        self.btn_registro_clientes.pack(pady=10)

        self.btn_registro_ventas = ctk.CTkButton(
            self.frame_izquierda, text="Registrar Ventas", command=self.abrir_registro_ventas)
        self.btn_registro_ventas.pack(pady=10)

        self.btn_registro_servicios = ctk.CTkButton(
            self.frame_izquierda, text="Registrar Servicios", command=self.abrir_registro_servicios)
        self.btn_registro_servicios.pack(pady=10)

        self.btn_consultas = ctk.CTkButton(
            self.frame_izquierda, text="Consultar Autos Vendidos", command=self.abrir_consultas)
        self.btn_consultas.pack(pady=10)

        self.btn_consultas = ctk.CTkButton(
            self.frame_izquierda, text="Consultar Servicios Realizados", command=self.abrir_consultas_servicios)
        self.btn_consultas.pack(pady=10)

        self.btn_reporte_ventas = ctk.CTkButton(
            self.frame_izquierda, text="Generar Reporte de Ventas", command=self.abrir_reporte_ventas)
        self.btn_reporte_ventas.pack(pady=10)

    def create_table_selector(self):
        self.label_select = ctk.CTkLabel(
            self.frame_derecha, text="Seleccionar Tabla:")
        self.label_select.pack(pady=10)

        # Incluir "Vendedores" en las opciones del selector de tablas
        self.table_selector = ctk.CTkOptionMenu(
            self.frame_derecha,
            values=["Autos", "Ventas", "Clientes", "Servicios", "Vendedores"],
            command=self.mostrar_tabla
        )
        self.table_selector.pack(pady=10)

    def mostrar_tabla(self, tabla_seleccionada):
        # Limpiar configuración previa de la tabla
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()

        # Definir columnas y cargar datos según la tabla seleccionada
        if tabla_seleccionada == "Autos":
            columnas = ("Codigo VIN", "Marca", "Modelo", "Año",
                        "Precio", "Estado", "Cliente ID")
            datos = session.query(Auto).all()
            filas = [(auto.codigo_vin, auto.marca, auto.modelo, auto.anio,
                      auto.precio, auto.estado.capitalize(), auto.cliente_id if auto.cliente_id is not None else "") for auto in datos]

        elif tabla_seleccionada == "Clientes":
            columnas = ("ID", "Nombre", "Apellido", "Direccion", "Telefono")
            datos = session.query(Cliente).all()
            filas = [(cliente.id, cliente.nombre, cliente.apellido,
                      cliente.direccion, cliente.telefono) for cliente in datos]

        elif tabla_seleccionada == "Ventas":
            columnas = ("ID", "Auto ID", "Cliente ID",
                        "Vendedor ID", "Fecha Venta")
            datos = session.query(Venta).all()
            filas = [(venta.id, venta.auto_id, venta.cliente_id,
                      venta.vendedor_id, venta.fecha_venta) for venta in datos]

        elif tabla_seleccionada == "Servicios":
            columnas = ("ID", "Auto ID", "Tipo Servicio", "Fecha", "Costo")
            datos = session.query(Servicio).all()
            filas = [(servicio.id, servicio.auto_id, servicio.tipo_servicio,
                      servicio.fecha, servicio.costo) for servicio in datos]

        elif tabla_seleccionada == "Vendedores":
            columnas = ("ID", "Nombre", "Apellido", "Comisiones")
            datos = session.query(Vendedor).all()
            filas = [(vendedor.id, vendedor.nombre, vendedor.apellido,
                      vendedor.comisiones) for vendedor in datos]

        # Configurar columnas en el Treeview
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        # Insertar datos en el Treeview
        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    def agregar_logo(self):
        # Cargar la imagen del logo
        logo_image = Image.open("Utils/logo.jpg")  # Ruta de la imagen
        # Ajustar el tamaño si es necesario
        logo_image = logo_image.resize((150, 150), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Crear un label con la imagen y colocarlo abajo a la izquierda
        self.label_logo = tk.Label(
            self.frame_izquierda, image=logo_photo, bg="#2B2B2B")
        self.label_logo.image = logo_photo  # Necesario para que la imagen no se borre
        self.label_logo.pack(side=tk.BOTTOM, pady=20)

    def abrir_registro_autos(self):
        registro_autos = RegistroAutos()
        registro_autos.run()

    def abrir_registro_clientes(self):
        registro_clientes = RegistroClientes()
        registro_clientes.run()

    def abrir_registro_ventas(self):
        registro_ventas = RegistroVentas()
        registro_ventas.run()

    def abrir_registro_servicios(self):
        registro_servicios = RegistroServicios()
        registro_servicios.run()

    def abrir_consultas(self):
        consultar_autos_vendidos = ConsultaAutosVendidos()
        consultar_autos_vendidos.run()

    def abrir_consultas_servicios(self):
        consultar_servicios = ConsultaServicios()
        consultar_servicios.run()

    def abrir_reporte_ventas(self):
        reporte_ventas_window = VentasReportWindow()
        reporte_ventas_window.run()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
