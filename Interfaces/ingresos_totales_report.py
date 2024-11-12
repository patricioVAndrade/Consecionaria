import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry
from Reports.ingresos_report import IngresosReport
from Utils.export import exportar_a_csv, exportar_a_pdf


class IngresosReportWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reporte de Ingresos Totales")
        self.geometry("700x600")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self,
            text="Reporte de Ingresos Totales",
            font=("Arial", 20)
        )
        self.label_titulo.pack(pady=20)

        # Frame para los filtros de fecha
        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.pack(pady=10)

        # Fecha inicio
        self.label_fecha_inicio = ctk.CTkLabel(
            self.frame_filtros,
            text="Fecha Inicio:"
        )
        self.label_fecha_inicio.grid(row=0, column=0, padx=5, pady=5)

        self.fecha_inicio = DateEntry(
            self.frame_filtros,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.fecha_inicio.grid(row=0, column=1, padx=5, pady=5)

        # Fecha fin
        self.label_fecha_fin = ctk.CTkLabel(
            self.frame_filtros,
            text="Fecha Fin:"
        )
        self.label_fecha_fin.grid(row=0, column=2, padx=5, pady=5)

        self.fecha_fin = DateEntry(
            self.frame_filtros,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.fecha_fin.grid(row=0, column=3, padx=5, pady=5)

        # Botón para generar reporte
        self.btn_generar = ctk.CTkButton(
            self.frame_filtros,
            text="Generar Reporte",
            command=self.generar_reporte
        )
        self.btn_generar.grid(row=0, column=4, padx=10, pady=5)

        # Caja de texto para mostrar el reporte (solo lectura)
        self.reporte_texto = tk.Text(
            self,
            height=20,
            width=80,
            state='disabled'
        )
        self.reporte_texto.pack(pady=10)

        # Frame para botones de exportación
        self.frame_exportar = ctk.CTkFrame(self)
        self.frame_exportar.pack(pady=10)

        # Botones para exportar
        self.btn_exportar_csv = ctk.CTkButton(
            self.frame_exportar,
            text="Exportar a CSV",
            command=self.exportar_csv
        )
        self.btn_exportar_csv.grid(row=0, column=0, padx=10)

        self.btn_exportar_pdf = ctk.CTkButton(
            self.frame_exportar,
            text="Exportar a PDF",
            command=self.exportar_pdf
        )
        self.btn_exportar_pdf.grid(row=0, column=1, padx=10)

        # Variable para almacenar los resultados del reporte
        self.resultados = {}

    def generar_reporte(self):
        try:
            fecha_inicio = self.fecha_inicio.get_date()
            fecha_fin = self.fecha_fin.get_date()

            if fecha_inicio > fecha_fin:
                messagebox.showerror(
                    "Error", "La fecha de inicio debe ser anterior a la fecha fin")
                return

            # Obtener los resultados
            self.resultados = IngresosReport.reporte_ingresos_totales(
                fecha_inicio, fecha_fin)

            # Permitir edición temporal
            self.reporte_texto.configure(state='normal')
            self.reporte_texto.delete(1.0, tk.END)

            # Formatear y mostrar los resultados
            total_ventas = self.resultados["total_ventas_autos"]
            total_servicios = self.resultados["total_ingresos_servicios"]
            total_general = total_ventas + total_servicios

            reporte = f"""Período: {fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')}

Ingresos por Venta de Autos: ${total_ventas:,.2f}
Ingresos por Servicios: ${total_servicios:,.2f}
----------------------------------------
Total General: ${total_general:,.2f}
"""
            self.reporte_texto.insert(tk.END, reporte)
            self.reporte_texto.configure(state='disabled')

        except Exception as e:
            print(f"Error al generar el reporte: {str(e)}")
            messagebox.showerror(
                "Error", "Ocurrió un error al generar el reporte.")

    def exportar_csv(self):
        if not self.resultados:
            messagebox.showwarning(
                "Advertencia", "No hay datos para exportar.")
            return
        try:
            fecha_inicio = self.fecha_inicio.get_date()
            fecha_fin = self.fecha_fin.get_date()
            
            # Formatear los datos para la exportación
            datos = [
                ["Ingresos por Venta de Autos", f"${self.resultados['total_ventas_autos']:,.2f}"],
                ["Ingresos por Servicios", f"${self.resultados['total_ingresos_servicios']:,.2f}"],
                ["Total General", f"${self.resultados['total_ventas_autos'] + self.resultados['total_ingresos_servicios']:,.2f}"]
            ]
            
            exportar_a_csv(
                datos, 
                tipo_reporte="ingresos_totales",
                fecha_inicio=fecha_inicio.strftime('%Y-%m-%d'),
                fecha_fin=fecha_fin.strftime('%Y-%m-%d')
            )
            messagebox.showinfo("Exportar CSV", "Reporte exportado a CSV exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a CSV: {str(e)}")

    def exportar_pdf(self):
        if not self.resultados:
            messagebox.showwarning(
                "Advertencia", "No hay datos para exportar.")
            return
        try:
            fecha_inicio = self.fecha_inicio.get_date()
            fecha_fin = self.fecha_fin.get_date()
            datos = [
                ["Período", f"{fecha_inicio.strftime('%Y-%m-%d')} al {fecha_fin.strftime('%Y-%m-%d')}"],
                ["Ingresos por Venta de Autos", f"${self.resultados['total_ventas_autos']:,.2f}"],
                ["Ingresos por Servicios", f"${self.resultados['total_ingresos_servicios']:,.2f}"],
                ["Total General", f"${self.resultados['total_ventas_autos'] + self.resultados['total_ingresos_servicios']:,.2f}"]
            ]
            exportar_a_pdf(datos, tipo_reporte="ingresos_totales",
                         fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            messagebox.showinfo(
                "Exportar PDF", "Reporte exportado a PDF exitosamente.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al exportar a PDF: {str(e)}")

    def run(self):
        self.mainloop()