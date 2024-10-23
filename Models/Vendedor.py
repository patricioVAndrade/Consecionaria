from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from Utils.database import Base, session


class Vendedor(Base):
    __tablename__ = 'vendedores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    comisiones = Column(Float, nullable=False)

    # Relación con Venta
    ventas = relationship("Venta", back_populates="vendedor")

    @classmethod
    def obtener_vendedores(cls):
        """Devuelve una lista de vendedores registrados."""
        try:
            vendedores = session.query(cls).all()
            return [f"{vendedor.id} - {vendedor.nombre} {vendedor.apellido}" for vendedor in vendedores]
        except Exception as e:
            print(f"Error al obtener vendedores: {e}")
            return []
