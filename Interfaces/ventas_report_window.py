import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry  # Selector de fecha
from Reports.ventas_report import VentasReport
from Utils.export import exportar_a_csv, exportar_a_pdf
from datetime import datetime


class VentasReportWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reporte de Ventas")
        self.geometry("700x600")

        # Etiqueta para selección de fecha de inicio
        self.label_fecha_inicio = ctk.CTkLabel(self, text="Fecha de Inicio:")
        self.label_fecha_inicio.pack(pady=5)

        # Selector de fecha de inicio
        self.date_inicio = DateEntry(self, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_inicio.pack(pady=5)

        # Etiqueta para selección de fecha de fin
        self.label_fecha_fin = ctk.CTkLabel(self, text="Fecha de Fin:")
        self.label_fecha_fin.pack(pady=5)

        # Selector de fecha de fin
        self.date_fin = DateEntry(self, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_fin.pack(pady=5)

        # Botón para generar reporte
        self.btn_generar_reporte = ctk.CTkButton(
            self, text="Generar Reporte", command=self.generar_reporte)
        self.btn_generar_reporte.pack(pady=20)

        # Caja de texto para mostrar el reporte (solo lectura)
        self.reporte_texto = tk.Text(
            self, height=20, width=80, state='disabled')
        self.reporte_texto.pack(pady=10)

        # Botones para exportar
        self.frame_exportar = ctk.CTkFrame(self)
        self.frame_exportar.pack(pady=10)

        self.btn_exportar_csv = ctk.CTkButton(
            self.frame_exportar, text="Exportar a CSV", command=self.exportar_csv)
        self.btn_exportar_csv.grid(row=0, column=0, padx=10)

        self.btn_exportar_pdf = ctk.CTkButton(
            self.frame_exportar, text="Exportar a PDF", command=self.exportar_pdf)
        self.btn_exportar_pdf.grid(row=0, column=1, padx=10)

        # Variable para almacenar las ventas generadas
        self.ventas = []
        self.fecha_inicio_str = ""
        self.fecha_fin_str = ""

    def generar_reporte(self):
        # Obtener fechas seleccionadas
        fecha_inicio = self.date_inicio.get_date()
        fecha_fin = self.date_fin.get_date()

        # Validar que fecha_inicio <= fecha_fin
        if fecha_inicio > fecha_fin:
            messagebox.showerror(
                "Error de Fecha", "La fecha de inicio no puede ser posterior a la fecha de fin.")
            return

        self.fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
        self.fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")

        try:
            # Obtener las ventas
            self.ventas = VentasReport.listar_ventas_por_periodo(
                fecha_inicio, fecha_fin)
            # Permitir edición temporal
            self.reporte_texto.configure(state='normal')
            self.reporte_texto.delete(1.0, tk.END)  # Limpiar reporte anterior

            if self.ventas:
                for venta, auto in self.ventas:
                    reporte_line = f"Venta ID: {venta.id}, Auto: {auto.codigo_vin} - {auto.marca} {auto.modelo}, Fecha: {venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    self.reporte_texto.insert(tk.END, reporte_line)
            else:
                self.reporte_texto.insert(
                    tk.END, "No se encontraron ventas en el periodo seleccionado.")

            self.reporte_texto.configure(state='disabled')  # Bloquear edición
        except Exception as e:
            print(f"Error al generar el reporte: {str(e)}")
            messagebox.showerror(
                "Error", "Ocurrió un error al generar el reporte.")

    def exportar_csv(self):
        if not self.ventas:
            messagebox.showwarning(
                "Advertencia", "No hay ventas para exportar.")
            return
        exportar_a_csv(self.ventas, self.fecha_inicio_str, self.fecha_fin_str)
        messagebox.showinfo(
            "Exportar CSV", "Reporte exportado a CSV exitosamente.")

    def exportar_pdf(self):
        if not self.ventas:
            messagebox.showwarning(
                "Advertencia", "No hay ventas para exportar.")
            return
        exportar_a_pdf(self.ventas, self.fecha_inicio_str, self.fecha_fin_str)
        messagebox.showinfo(
            "Exportar PDF", "Reporte exportado a PDF exitosamente.")

    def run(self):
        self.mainloop()
