from Models.Venta import Venta
from Models.Auto import Auto
from Utils.database import session
from sqlalchemy import func
from sqlalchemy.sql import label


class AutosMasVendidosReport:

    @staticmethod
    def reporte_autos_mas_vendidos():
        try:
            # Consulta para contar los autos vendidos por marca (sin diferenciar entre mayúsculas y minúsculas)
            resultados = session.query(
                # Convertimos la marca a minúsculas
                func.lower(Auto.marca).label('marca'),
                func.count(Auto.codigo_vin).label('cantidad_vendidos')
            ).join(Venta).group_by(func.lower(Auto.marca)).order_by(
                # Ordenamos por cantidad descendente
                func.count(Auto.codigo_vin).desc(),
                # Ordenamos alfabéticamente las marcas si las cantidades son iguales
                func.lower(Auto.marca).asc()
            ).all()

            # Devolvemos los resultados
            if resultados:
                print("Autos más vendidos por marca:")
                for marca, cantidad in resultados:
                    print(
                        f"Marca: {marca.capitalize()}, Cantidad Vendidos: {cantidad}")
            else:
                print("No se encontraron ventas de autos.")

        except Exception as e:
            print(
                f"Error al generar el reporte de autos más vendidos por marca: {e}")
