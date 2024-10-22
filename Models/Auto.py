from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from sqlalchemy.exc import IntegrityError
from Utils.enums import Estado


class Auto(Base):
    __tablename__ = 'autos'
    codigo_vin = Column(String, primary_key=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    estado = Column(Enum(Estado), nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)

    # Relación con Cliente

    cliente = relationship("Cliente", back_populates="autos")
    servicios = relationship("Servicio", back_populates="auto")
    ventas = relationship("Venta", back_populates="auto")

    @classmethod
    def registrar_auto(cls, codigo_vin, marca, modelo, anio, precio, estado):
        nuevo_auto = cls(codigo_vin=codigo_vin, marca=marca,
                         modelo=modelo, anio=anio, precio=precio, estado=estado)
        try:
            session.add(nuevo_auto)
            session.commit()
            print(f"Auto {marca} {modelo} registrado correctamente.")
        except IntegrityError:
            session.rollback()
            print(f"Error: el auto con código VIN {codigo_vin} ya existe.")

    @classmethod
    def vender_auto(cls, codigo_vin, cliente_id, vendedor_id):
        from Models.Venta import Venta
        # Buscar el auto
        auto = session.query(cls).filter_by(codigo_vin=codigo_vin).first()

        if auto and auto.cliente_id is None:
            # Asociar el cliente al auto (auto vendido)
            auto.cliente_id = cliente_id
            Venta.registrar_venta(auto_id=auto.codigo_vin,
                                  cliente_id=cliente_id, vendedor_id=vendedor_id)
            session.commit()
            print(f"El auto {codigo_vin} ha sido vendido.")
        else:
            print(f"El auto {codigo_vin} no está disponible para la venta.")

    def esta_disponible(self):
        return self.cliente_id is None

    @classmethod
    def consultar_autos_vendidos(cls, cliente_id):
        try:
            autos_vendidos = session.query(cls).filter_by(
                cliente_id=cliente_id).all()
            if autos_vendidos:
                print(f"Autos vendidos al cliente con ID {cliente_id}:")
                for auto in autos_vendidos:
                    print(
                        f"VIN: {auto.codigo_vin}, Marca: {auto.marca}, Modelo: {auto.modelo}, Año: {auto.anio}, Precio: {auto.precio}")
            else:
                print("No se encontraron autos vendidos a este cliente.")
        except Exception as e:
            print(f"Error al consultar los autos vendidos: {e}")
