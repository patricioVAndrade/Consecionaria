import customtkinter as ctk
from Models.Servicio import Servicio
from Models.Auto import Auto
from Utils.enums import TipoServicio


class RegistroServicios(ctk.CTk):
    def __init__(self, refresh_callback=None):
        super().__init__()
        self.title("Registrar Servicio Post-Venta")
        self.geometry("400x400")
        self.refresh_callback = refresh_callback

        # Etiqueta para seleccionar auto
        self.label_auto = ctk.CTkLabel(self, text="Seleccionar Auto Vendido:")
        self.label_auto.pack(pady=5)

        # ComboBox para autos vendidos
        self.combo_autos = ctk.CTkComboBox(
            self, values=self.consultar_autos_vendidos())
        self.combo_autos.pack(pady=5)

        # Etiqueta para seleccionar tipo de servicio
        self.label_servicio = ctk.CTkLabel(
            self, text="Seleccionar Tipo de Servicio:")
        self.label_servicio.pack(pady=5)

        # ComboBox para tipo de servicio
        self.combo_servicios = ctk.CTkComboBox(
            self, values=[TipoServicio.mantenimiento, TipoServicio.reparacion])
        self.combo_servicios.pack(pady=5)

        # Botón de Guardar Servicio
        self.btn_guardar = ctk.CTkButton(
            self, text="Guardar Servicio", command=self.guardar_servicio)
        self.btn_guardar.pack(pady=20)

    def consultar_autos_vendidos(self):
        """Devuelve una lista de autos vendidos (con cliente asignado)."""
        autos_vendidos = Auto.consultar_autos_vendidos()  # Método sin cliente_id
        return [f"{auto.codigo_vin} - {auto.marca} {auto.modelo}" for auto in autos_vendidos]

    def guardar_servicio(self):
        # Deshabilitar el botón para evitar múltiples clics
        self.btn_guardar.configure(state='disabled')

        try:
            # Capturar datos de las selecciones
            auto_seleccionado = self.combo_autos.get().split(" ")[
                0]  # VIN del auto
            tipo_servicio = self.combo_servicios.get()

            # Registrar el servicio en la base de datos utilizando el método de la clase Servicio
            Servicio.registrar_servicio(
                auto_id=auto_seleccionado, tipo_servicio=tipo_servicio)

            print(
                f"Servicio de {tipo_servicio} registrado correctamente para el auto {auto_seleccionado}.")
            if self.refresh_callback:
                self.refresh_callback()
            
        except Exception as e:
            print(f"Error al registrar el servicio: {e}")
        finally:
            # Rehabilitar el botón
            self.btn_guardar.configure(state='normal')

        # Cerrar la ventana después de guardar
        self.destroy()

    def run(self):
        self.mainloop()


# Ejecución del formulario de servicio
if __name__ == "__main__":
    app = RegistroServicios()
    app.run()
