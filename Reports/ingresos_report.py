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
            # Sumar los ingresos por ventas de autos (solo los autos vendidos)
            ingresos_autos = session.query(func.sum(Auto.precio).label('total_ventas')).join(
                # Hacemos explícita la relación entre Auto y Venta
                Venta, Auto.codigo_vin == Venta.auto_id
            ).filter(
                Venta.fecha_venta.between(fecha_inicio, fecha_fin),
                # Asegurarse de que el auto tenga cliente asignado (vendido)
                Auto.cliente_id.isnot(None)
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
