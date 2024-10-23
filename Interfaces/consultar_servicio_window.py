import tkinter as tk
import customtkinter as ctk
from Models.Auto import Auto
from Models.Servicio import Servicio


class ConsultaServicios(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Consultar Servicios de Auto")
        self.geometry("500x500")

        # Etiqueta para seleccionar auto
        self.label_auto = ctk.CTkLabel(self, text="Seleccionar Auto:")
        self.label_auto.pack(pady=5)

        # ComboBox para autos
        self.combo_autos = ctk.CTkComboBox(self, values=self.obtener_autos())
        self.combo_autos.pack(pady=5)

        # Botón para consultar servicios
        self.btn_consultar = ctk.CTkButton(
            self, text="Consultar Servicios", command=self.consultar_servicios)
        self.btn_consultar.pack(pady=20)

        # Lista para mostrar servicios
        self.lista_servicios = tk.Listbox(self, height=20, width=100)
        self.lista_servicios.pack(pady=10)

    def obtener_autos(self):
        """Devuelve una lista de todos los autos en el inventario."""
        autos = Auto.obtener_autos()  # Llama al nuevo método para obtener todos los autos
        return [f"{auto.codigo_vin} - {auto.marca} {auto.modelo}" for auto in autos]

    def consultar_servicios(self):
        """Consulta los servicios realizados al auto seleccionado."""
        # Limpiar la lista de servicios
        self.lista_servicios.delete(0, tk.END)

        auto_seleccionado = self.combo_autos.get().split(
            " ")[0]  # Obtener el VIN del auto seleccionado
        # Llama al método que consulta los servicios
        servicios = Servicio.consultar_servicios(auto_seleccionado)

        if servicios:
            # Mostrar los servicios en el Listbox
            for servicio in servicios:
                self.lista_servicios.insert(
                    tk.END, f"Tipo: {servicio.tipo_servicio}, Fecha: {servicio.fecha}, Costo: {servicio.costo}")
        else:
            self.lista_servicios.insert(
                tk.END, "No se encontraron servicios realizados para este auto.")

    def run(self):
        self.mainloop()
