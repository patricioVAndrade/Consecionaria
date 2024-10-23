from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from datetime import datetime


class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_id = Column(String, ForeignKey('autos.codigo_vin'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'))
    fecha_venta = Column(DateTime, nullable=False)

    # Relaciones
    auto = relationship("Auto", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")

    @classmethod
    def registrar_venta(cls, auto_id, cliente_id, vendedor_id, comision_fija=500):
        from Models.Vendedor import Vendedor
        nueva_venta = cls(
            auto_id=auto_id,
            cliente_id=cliente_id,
            vendedor_id=vendedor_id,
            fecha_venta=datetime.now()
        )
        try:
            # Actualizar comisiones del vendedor
            vendedor = session.query(Vendedor).filter_by(
                id=vendedor_id).first()
            if vendedor:
                vendedor.comisiones += comision_fija
            else:
                print(f"Vendedor con ID {vendedor_id} no encontrado.")
                return
            # Agregar la venta a la base de datos
            session.add(nueva_venta)
            session.commit()
            print(
                f"Venta registrada correctamente para el auto {auto_id}. Comisión de {comision_fija} agregada al vendedor.")
        except Exception as e:
            session.rollback()
            print(f"Error al registrar la venta: {str(e)}")
