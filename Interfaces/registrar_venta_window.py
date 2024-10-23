import tkinter as tk
import customtkinter as ctk
from Models.Auto import Auto
from Models.Cliente import Cliente
from Models.Vendedor import Vendedor
from Models.Venta import Venta


class RegistroVentas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Registrar Venta de Auto")
        self.geometry("400x400")

        # Etiqueta para seleccionar auto
        self.label_auto = ctk.CTkLabel(self, text="Seleccionar Auto:")
        self.label_auto.pack(pady=5)

        # ComboBox para autos disponibles
        self.combo_autos = ctk.CTkComboBox(
            self, values=self.obtener_autos_disponibles())
        self.combo_autos.pack(pady=5)

        # Etiqueta para seleccionar cliente
        self.label_cliente = ctk.CTkLabel(self, text="Seleccionar Cliente:")
        self.label_cliente.pack(pady=5)

        # ComboBox para clientes
        self.combo_clientes = ctk.CTkComboBox(
            self, values=self.obtener_clientes())
        self.combo_clientes.pack(pady=5)

        # Etiqueta para seleccionar vendedor
        self.label_vendedor = ctk.CTkLabel(self, text="Seleccionar Vendedor:")
        self.label_vendedor.pack(pady=5)

        # ComboBox para vendedores
        self.combo_vendedores = ctk.CTkComboBox(
            self, values=self.obtener_vendedores())
        self.combo_vendedores.pack(pady=5)

        # Botón de Guardar
        self.btn_guardar = ctk.CTkButton(
            self, text="Guardar Venta", command=self.guardar_venta)
        self.btn_guardar.pack(pady=20)

    def obtener_autos_disponibles(self):
        """Devuelve una lista de autos disponibles (sin cliente asignado)."""
        autos_disponibles = Auto.obtener_autos_disponibles()
        return [f"{auto.codigo_vin} - {auto.marca} {auto.modelo}" for auto in autos_disponibles]

    def obtener_clientes(self):
        """Devuelve una lista de clientes registrados ya formateados."""
        return Cliente.obtener_clientes()

    def obtener_vendedores(self):
        """Devuelve una lista de vendedores registrados."""
        return Vendedor.obtener_vendedores()

    def guardar_venta(self):
        # Deshabilitar el botón para prevenir múltiples clics
        self.btn_guardar.configure(state='disabled')

        try:
            # Capturar datos de las selecciones
            auto_seleccionado = self.combo_autos.get().split(" ")[
                0]  # VIN del auto
            cliente_seleccionado = self.combo_clientes.get().split(" ")[
                0]  # ID del cliente
            vendedor_seleccionado = self.combo_vendedores.get().split(" ")[
                0]  # ID del vendedor

            # Llamar al método vender_auto para asociar el cliente y registrar la venta
            Auto.vender_auto(codigo_vin=auto_seleccionado,
                             cliente_id=cliente_seleccionado,
                             vendedor_id=vendedor_seleccionado, comision_fija=500)

            print(
                f"Venta del auto {auto_seleccionado} registrada correctamente.")
        except Exception as e:
            print(f"Error al registrar la venta: {e}")
        finally:
            # Rehabilitar el botón
            self.btn_guardar.configure(state='normal')

        # Cerrar la ventana después de guardar
        self.destroy()

    def run(self):
        self.mainloop()
