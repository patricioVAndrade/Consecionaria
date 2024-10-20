from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from Utils.database import Base


class Servicio(Base):
    __tablename__ = 'servicios'
    id = Column(Integer, primary_key=True)
    auto_id = Column(String, ForeignKey('autos.codigo_vin'))
    tipo_servicio = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    costo = Column(Float, nullable=False)

    # Relación con Auto
    auto = relationship("Auto", back_populates="servicios")
