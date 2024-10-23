from Models.Venta import Venta
from Models.Auto import Auto
from Utils.database import session


class VentasReport:

    @staticmethod
    def listar_ventas_por_periodo(fecha_inicio, fecha_fin):
        try:
            # Consulta todas las ventas en el rango de fechas, uniendo con Auto para obtener detalles del auto
            ventas = session.query(Venta, Auto).join(Auto, Venta.auto_id == Auto.codigo_vin).filter(
                Venta.fecha_venta.between(fecha_inicio, fecha_fin)
            ).all()
            return ventas  # Retorna una lista de tuplas (Venta, Auto)
        except Exception as e:
            print(f"Error al generar el reporte: {str(e)}")
            return []
