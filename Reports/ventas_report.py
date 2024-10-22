from Models.Venta import Venta
from Utils.database import session


class VentasReport:

    @staticmethod
    def listar_ventas_por_periodo(fecha_inicio, fecha_fin):
        try:
            # Consulta todas las ventas en el rango de fechas
            ventas = session.query(Venta).filter(
                Venta.fecha_venta.between(fecha_inicio, fecha_fin)).all()
            return ventas
        except Exception as e:
            print(f"Error al generar el reporte: {str(e)}")
            return []
