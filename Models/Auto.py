from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Utils.database import Base


class Auto(Base):
    __tablename__ = 'autos'
    codigo_vin = Column(String, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    estado = Column(Enum, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))

    # Relación con Cliente
    # Usamos "Cliente" como cadena de texto
    cliente = relationship("Cliente", back_populates="autos")
    servicios = relationship("Servicio", back_populates="auto")
    ventas = relationship("Venta", back_populates="auto")
