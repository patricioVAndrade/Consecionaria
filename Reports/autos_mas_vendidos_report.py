from Models.Venta import Venta
from Models.Auto import Auto
from Utils.database import session
from sqlalchemy import func
from sqlalchemy.sql import label


class AutosMasVendidosReport:

    @staticmethod
    def obtener_marcas():
        try:
            # Consulta para obtener todas las marcas únicas
            marcas = session.query(
                func.distinct(func.lower(Auto.marca))
            ).order_by(
                func.lower(Auto.marca)
            ).all()
            
            # Convertir el resultado a una lista de strings y agregar "Todas"
            marcas_list = ["Todas"] + [marca[0].capitalize() for marca in marcas]
            return marcas_list
        except Exception as e:
            print(f"Error al obtener las marcas: {e}")
            return ["Todas"]

    @staticmethod
    def reporte_autos_mas_vendidos(marca_seleccionada=None):
        try:
            # Consulta base para contar los autos vendidos por marca
            query = session.query(
                func.lower(Auto.marca).label('marca'),
                func.count(Auto.codigo_vin).label('cantidad_vendidos')
            ).join(Venta)

            # Si se seleccionó una marca específica (diferente de "Todas")
            if marca_seleccionada and marca_seleccionada != "Todas":
                query = query.filter(
                    func.lower(Auto.marca) == func.lower(marca_seleccionada)
                )

            # Agrupar y ordenar los resultados
            resultados = query.group_by(
                func.lower(Auto.marca)
            ).order_by(
                func.count(Auto.codigo_vin).desc(),
                func.lower(Auto.marca).asc()
            ).all()

            return resultados if resultados else []

        except Exception as e:
            print(f"Error al generar el reporte de autos más vendidos por marca: {e}")
            return []