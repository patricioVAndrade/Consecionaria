from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from Utils.database import Base


class Vendedor(Base):
    __tablename__ = 'vendedores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    comisiones = Column(Float, nullable=False)

    # Relación con Venta
    ventas = relationship("Venta", back_populates="vendedor")
