import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from Reports.autos_mas_vendidos_report import AutosMasVendidosReport
from Utils.export import exportar_a_csv, exportar_a_pdf


class AutosMasVendidosWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Reporte de Autos más Vendidos por Marca")
        self.geometry("700x600")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="Reporte de Autos más Vendidos por Marca",
            font=("Arial", 20)
        )
        self.label_titulo.pack(pady=20)

        # Frame para el filtro
        self.frame_filtro = ctk.CTkFrame(self)
        self.frame_filtro.pack(pady=10)

        # Label para el combo box
        self.label_marca = ctk.CTkLabel(
            self.frame_filtro,
            text="Seleccionar Marca:"
        )
        self.label_marca.pack(side=tk.LEFT, padx=5)

        # Obtener las marcas disponibles
        self.marcas = AutosMasVendidosReport.obtener_marcas()
        
        # Combo box para seleccionar marca
        self.combo_marca = ctk.CTkOptionMenu(
            self.frame_filtro,
            values=self.marcas,
            command=self.on_marca_selected
        )
        self.combo_marca.pack(side=tk.LEFT, padx=5)
        self.combo_marca.set("Todas")  # Valor por defecto

        # Caja de texto para mostrar el reporte (solo lectura)
        self.reporte_texto = tk.Text(
            self, 
            height=20, 
            width=80, 
            state='disabled'
        )
        self.reporte_texto.pack(pady=10)

        # Botones para exportar
        self.frame_exportar = ctk.CTkFrame(self)
        self.frame_exportar.pack(pady=10)

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
        self.resultados = []
        
        # Generar reporte inicial
        self.generar_reporte()

    def on_marca_selected(self, marca):
        self.generar_reporte()

    def generar_reporte(self):
        try:
            marca_seleccionada = self.combo_marca.get()
            
            # Obtener los resultados
            self.resultados = AutosMasVendidosReport.reporte_autos_mas_vendidos(
                marca_seleccionada if marca_seleccionada != "Todas" else None
            )
            
            # Permitir edición temporal
            self.reporte_texto.configure(state='normal')
            self.reporte_texto.delete(1.0, tk.END)  # Limpiar reporte anterior

            if self.resultados:
                for marca, cantidad in self.resultados:
                    reporte_line = f"Marca: {marca.capitalize()}, Cantidad Vendidos: {cantidad}\n"
                    self.reporte_texto.insert(tk.END, reporte_line)
            else:
                self.reporte_texto.insert(
                    tk.END, "No se encontraron ventas de autos para la marca seleccionada.")

            self.reporte_texto.configure(state='disabled')  # Bloquear edición
            
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
            marca_seleccionada = self.combo_marca.get()
            exportar_a_csv(self.resultados, tipo_reporte="autos_mas_vendidos", 
                         marca_filtro=marca_seleccionada)
            messagebox.showinfo(
                "Exportar CSV", "Reporte exportado a CSV exitosamente.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al exportar a CSV: {str(e)}")

    def exportar_pdf(self):
        if not self.resultados:
            messagebox.showwarning(
                "Advertencia", "No hay datos para exportar.")
            return
        try:
            marca_seleccionada = self.combo_marca.get()
            exportar_a_pdf(self.resultados, tipo_reporte="autos_mas_vendidos",
                         marca_filtro=marca_seleccionada)
            messagebox.showinfo(
                "Exportar PDF", "Reporte exportado a PDF exitosamente.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al exportar a PDF: {str(e)}")

    def run(self):
        self.mainloop()