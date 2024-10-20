from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from Utils.database import Base


class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True)
    auto_id = Column(String, ForeignKey('autos.codigo_vin'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'))
    fecha_venta = Column(Date, nullable=False)

    # Relaciones
    auto = relationship("Auto", back_populates="ventas")
    cliente = relationship("Cliente", back_populates="ventas")
    vendedor = relationship("Vendedor", back_populates="ventas")
