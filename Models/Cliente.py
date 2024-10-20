from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Utils.database import Base


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)

    # Relación con Auto
    # Usamos "Auto" como cadena de texto
    autos = relationship("Auto", back_populates="cliente")
    ventas = relationship("Venta", back_populates="cliente")
