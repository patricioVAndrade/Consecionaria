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


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Autos")
        self.geometry("1000x600")

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
        self.tree = ttk.Treeview(self.frame_derecha, columns=(
            "ID", "VIN", "Cliente", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("VIN", text="VIN")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Cargar tabla inicial (autos registrados)
        self.mostrar_tabla("Autos")

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

        self.table_selector = ctk.CTkOptionMenu(self.frame_derecha, values=[
                                                "Autos", "Ventas", "Clientes", "Servicios"], command=self.mostrar_tabla)
        self.table_selector.pack(pady=10)

    def mostrar_tabla(self, tabla_seleccionada):
        # Limpiar la tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        if tabla_seleccionada == "Autos":
            # Consulta de autos registrados
            autos = session.query(Auto).all()
            for auto in autos:
                self.tree.insert("", tk.END, values=(
                    auto.codigo_vin, auto.cliente_id, auto.estado))

        elif tabla_seleccionada == "Ventas":
            ventas = session.query(Venta).all()
            for venta in ventas:
                self.tree.insert("", tk.END, values=(
                    venta.id, venta.auto_id, venta.cliente_id, venta.fecha_venta))

        # Agregar más opciones de tablas aquí (Clientes, Servicios...)

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
