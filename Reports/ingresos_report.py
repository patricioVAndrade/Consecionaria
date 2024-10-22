from Models.Venta import Venta
from Models.Servicio import Servicio
from Models.Auto import Auto
from Utils.database import session
from sqlalchemy import func
from datetime import datetime


class IngresosReport:

    @staticmethod
    def reporte_ingresos_totales(fecha_inicio, fecha_fin):
        try:
            # Sumar los ingresos por ventas de autos (sumando el precio de los autos vendidos)
            ingresos_autos = session.query(func.sum(Auto.precio).label('total_ventas')).join(Venta).filter(
                Venta.fecha_venta.between(fecha_inicio, fecha_fin)
            ).scalar()

            # Sumar los ingresos por servicios
            ingresos_servicios = session.query(func.sum(Servicio.costo).label('total_servicios')).filter(
                Servicio.fecha.between(fecha_inicio, fecha_fin)
            ).scalar()

            return {
                "total_ventas_autos": ingresos_autos if ingresos_autos else 0,
                "total_ingresos_servicios": ingresos_servicios if ingresos_servicios else 0
            }

        except Exception as e:
            print(f"Error al generar el reporte: {str(e)}")
            return {
                "total_ventas_autos": 0,
                "total_ingresos_servicios": 0
            }
