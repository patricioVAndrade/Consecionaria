import tkinter as tk
import customtkinter as ctk
from Models.Cliente import Cliente


class RegistroClientes(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Registrar Clientes")
        self.geometry("300x600")

        # Etiquetas y Entradas
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.pack(pady=5)

        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        self.label_apellido.pack(pady=5)
        self.entry_apellido = ctk.CTkEntry(self)
        self.entry_apellido.pack(pady=5)

        self.label_direccion = ctk.CTkLabel(self, text="Dirección:")
        self.label_direccion.pack(pady=5)
        self.entry_direccion = ctk.CTkEntry(self)
        self.entry_direccion.pack(pady=5)

        self.label_telefono = ctk.CTkLabel(self, text="Teléfono:")
        self.label_telefono.pack(pady=5)
        self.entry_telefono = ctk.CTkEntry(self)
        self.entry_telefono.pack(pady=5)

        self.btn_guardar = ctk.CTkButton(
            self, text="Guardar", command=self.guardar_cliente)
        self.btn_guardar.pack(pady=20)

    def guardar_cliente(self):
        # Deshabilitar el botón para prevenir múltiples clics
        self.btn_guardar.configure(state='disabled')

        try:
            # Capturar datos de las entradas
            nombre = self.entry_nombre.get()
            apellido = self.entry_apellido.get()
            direccion = self.entry_direccion.get()
            telefono = self.entry_telefono.get()

            # Registrar cliente en la base de datos
            Cliente.registrar_cliente(nombre, apellido, direccion, telefono)
        except Exception as e:
            print(f"Error al guardar el cliente: {e}")
        finally:
            # Rehabilitar el botón después del intento de guardar
            self.btn_guardar.configure(state='normal')

        # Cerrar la ventana después de guardar
        self.destroy()

    def run(self):
        self.mainloop()
