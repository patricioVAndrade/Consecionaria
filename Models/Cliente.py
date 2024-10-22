from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from sqlalchemy.exc import IntegrityError


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)

    # Relación con Auto
    # Usamos "Auto" como cadena de texto
    autos = relationship("Auto", back_populates="cliente")
    ventas = relationship("Venta", back_populates="cliente")

    @classmethod
    def registrar_cliente(cls, nombre, apellido, direccion, telefono):
        nuevo_cliente = cls(nombre=nombre, apellido=apellido, direccion=direccion,
                            telefono=telefono)

        try:
            session.add(nuevo_cliente)
            session.commit()
            print(f"Cliente {nombre} {apellido} registrado correctamente.")
        except IntegrityError:
            session.rollback()
            print(f"Error: el cliente con ID {id} ya existe.")
