import tkinter as tk
import customtkinter as ctk
from Models.Auto import Auto
from Models.Cliente import Cliente


class ConsultaAutosVendidos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Consulta de Autos Vendidos a un Cliente")
        self.geometry("500x500")

        # Etiqueta para seleccionar cliente
        self.label_cliente = ctk.CTkLabel(self, text="Seleccionar Cliente:")
        self.label_cliente.pack(pady=5)

        # ComboBox para clientes
        self.combo_clientes = ctk.CTkComboBox(
            self, values=self.obtener_clientes())
        self.combo_clientes.pack(pady=5)

        # Botón de Consultar
        self.btn_consultar = ctk.CTkButton(
            self, text="Consultar Autos Vendidos", command=self.consultar_autos_vendidos_por_cliente)
        self.btn_consultar.pack(pady=20)

        # Lista para mostrar autos vendidos
        self.lista_autos = tk.Listbox(self, height=20, width=100)
        self.lista_autos.pack(pady=10)

    def obtener_clientes(self):
        """Devuelve una lista de clientes registrados ya formateados."""
        return Cliente.obtener_clientes()

    def consultar_autos_vendidos_por_cliente(self):
        """Consulta los autos vendidos al cliente seleccionado."""
        # Limpiar la lista de autos
        self.lista_autos.delete(0, tk.END)

        try:
            # Obtener el ID del cliente seleccionado
            # Asegúrate de que el ID del cliente esté en la primera posición
            cliente_seleccionado = self.combo_clientes.get().split(" ")[0]

            # Consultar autos vendidos a ese cliente
            autos_vendidos = Auto.consultar_autos_vendidos_por_cliente(
                cliente_id=cliente_seleccionado)

            # Mostrar los autos vendidos en la lista
            if autos_vendidos:
                for auto in autos_vendidos:
                    self.lista_autos.insert(
                        tk.END, f"VIN: {auto.codigo_vin}, Marca: {auto.marca}, Modelo: {auto.modelo}")
            else:
                self.lista_autos.insert(
                    tk.END, "No se encontraron autos vendidos para este cliente.")

        except Exception as e:
            print(f"Error al consultar los autos vendidos: {e}")
            self.lista_autos.insert(tk.END, "Error al realizar la consulta.")

    def run(self):
        self.mainloop()
