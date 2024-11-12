import tkinter as tk
import customtkinter as ctk
from Models.Auto import Auto
from Utils.enums import Estado

class RegistroAutos(ctk.CTk):
    def __init__(self, refresh_callback=None):  # Add callback parameter
        super().__init__()
        self.title("Registrar Autos")
        self.geometry("300x600")
        self.refresh_callback = refresh_callback  # Store the callback

        # Etiquetas y Entradas
        self.label_vin = ctk.CTkLabel(self, text="Código VIN:")
        self.label_vin.pack(pady=5)
        self.entry_vin = ctk.CTkEntry(self)
        self.entry_vin.pack(pady=5)
        
        self.label_marca = ctk.CTkLabel(self, text="Marca:")
        self.label_marca.pack(pady=5)
        self.entry_marca = ctk.CTkEntry(self)
        self.entry_marca.pack(pady=5)

        self.label_modelo = ctk.CTkLabel(self, text="Modelo:")
        self.label_modelo.pack(pady=5)
        self.entry_modelo = ctk.CTkEntry(self)
        self.entry_modelo.pack(pady=5)

        self.label_anio = ctk.CTkLabel(self, text="Año:")
        self.label_anio.pack(pady=5)
        self.entry_anio = ctk.CTkEntry(self)
        self.entry_anio.pack(pady=5)

        self.label_precio = ctk.CTkLabel(self, text="Precio:")
        self.label_precio.pack(pady=5)
        self.entry_precio = ctk.CTkEntry(self)
        self.entry_precio.pack(pady=5)

        self.label_estado = ctk.CTkLabel(self, text="Estado:")
        self.label_estado.pack(pady=5)

        self.combo_estado = ctk.CTkComboBox(
            self, values=[estado.value for estado in Estado])
        self.combo_estado.set(Estado.nuevo.value)
        self.combo_estado.pack(pady=5)

        self.btn_guardar = ctk.CTkButton(
            self, text="Guardar", command=self.guardar_auto)
        self.btn_guardar.pack(pady=20)

    def guardar_auto(self):
        self.btn_guardar.configure(state='disabled')

        try:
            vin = self.entry_vin.get()
            marca = self.entry_marca.get()
            modelo = self.entry_modelo.get()
            anio = int(self.entry_anio.get())
            precio = float(self.entry_precio.get())
            estado = self.combo_estado.get()

            Auto.registrar_auto(vin, marca, modelo, anio, precio, estado)
            
            # Call the refresh callback if it exists
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            print(f"Error al guardar el auto: {e}")
        finally:
            self.btn_guardar.configure(state='normal')
            self.destroy()

    def run(self):
        self.mainloop()

