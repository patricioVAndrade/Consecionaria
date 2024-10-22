from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from datetime import datetime
from Utils.enums import TipoServicio


class Servicio(Base):
    __tablename__ = 'servicios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_id = Column(String, ForeignKey('autos.codigo_vin'))
    tipo_servicio = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)
    costo = Column(Float, nullable=False)

    # Relación con Auto
    auto = relationship("Auto", back_populates="servicios")

    # Diccionario costos (Preguntar si se puede tener un diccionario dentro de la clase o es mejor tenerlo aparte)
    COSTOS_SERVICIOS = {
        TipoServicio.mantenimiento: 100.0,  # Costo de mantenimiento
        TipoServicio.reparacion: 200.0      # Costo de reparación
    }

    @classmethod
    def registrar_servicio(cls, auto_id, tipo_servicio):
        from Models.Auto import Auto
        try:
            # Buscar el auto por código VIN
            auto = session.query(Auto).filter_by(codigo_vin=auto_id).first()

            # Verificar si el auto tiene un cliente asociado
            if auto and auto.cliente:
                # Obtener el costo del servicio desde el diccionario
                costo = cls.COSTOS_SERVICIOS.get(tipo_servicio)
                if costo is None:
                    print("Tipo de servicio no válido.")
                    return

                # Crear una nueva instancia de Servicio
                nuevo_servicio = cls(
                    auto_id=auto_id,
                    tipo_servicio=tipo_servicio,
                    fecha=datetime.now(),  # Fecha y hora actual
                    costo=costo  # Costo basado en el tipo de servicio
                )

                # Agregar el servicio a la sesión y hacer commit
                session.add(nuevo_servicio)
                session.commit()
                print(
                    f"Servicio de {tipo_servicio} registrado exitosamente con costo de {costo}.")

            else:
                print(
                    "El auto no tiene un cliente asociado y no se puede registrar el servicio.")

        except Exception as e:
            # Si ocurre un error, hacer rollback y mostrar el mensaje de error
            session.rollback()
            print(f"Ocurrió un error al registrar el servicio: {e}")

        finally:
            # Opción para cerrar la sesión si es necesario, aunque generalmente en transacciones cortas no es obligatorio
            session.close()

    @classmethod
    def consultar_servicios(cls, auto_id):
        try:
            servicios = session.query(cls).filter_by(auto_id=auto_id).all()
            if servicios:
                print(f"Servicios realizados para el auto {auto_id}:")
                for servicio in servicios:
                    print(
                        f"Tipo: {servicio.tipo_servicio}, Fecha: {servicio.fecha}, Costo: {servicio.costo}")
            else:
                print("No se encontraron servicios para el auto especificado.")
        except Exception as e:
            print(f"Error al consultar los servicios: {e}")
