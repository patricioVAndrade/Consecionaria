import re
from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from sqlalchemy.exc import IntegrityError
from Utils.enums import Estado
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


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


    @staticmethod
    def validar_marca(marca):
        # Verifica que la marca solo contenga letras y espacios
        return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', marca))

    @classmethod
    def registrar_auto(cls, codigo_vin, marca, modelo, anio, precio, estado):
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de tkinter

        # Validación del año
        if (anio < 1970 or datetime.now().year < anio):
            messagebox.showerror("Aviso!!", "Fecha inválida, ingrese otra.")
            root.destroy()
            return False
        
        # Validación de la marca
        elif not cls.validar_marca(marca):
            messagebox.showerror("Aviso!!", "La marca solo puede contener letras.")
            root.destroy()
            return False
        
        else:
            nuevo_auto = cls(codigo_vin=codigo_vin, marca=marca,
                           modelo=modelo, anio=anio, precio=precio, estado=estado)
            try:
                session.add(nuevo_auto)
                session.commit()
                print(f"Auto {marca} {modelo} registrado correctamente.")
                root.destroy()
                return True
            except IntegrityError:
                session.rollback()
                print(f"Error: el auto con código VIN {codigo_vin} ya existe.")
                root.destroy()
                return False
        
    @classmethod
    def vender_auto(cls, codigo_vin, cliente_id, vendedor_id, comision_fija=500):
        from Models.Venta import Venta

        # Buscar el auto
        auto = session.query(cls).filter_by(codigo_vin=codigo_vin).first()

        if auto and auto.cliente_id is None:
            # Asociar el cliente al auto (auto vendido)
            auto.cliente_id = cliente_id
            session.commit()  # Commit aquí para guardar el cliente asociado al auto

            # Registrar la venta en la base de datos, pasando la comisión fija
            Venta.registrar_venta(auto_id=auto.codigo_vin,
                                  cliente_id=cliente_id,
                                  vendedor_id=vendedor_id,
                                  comision_fija=comision_fija)
            print(f"El auto {codigo_vin} ha sido vendido.")
        else:
            print(f"El auto {codigo_vin} no está disponible para la venta.")

    def esta_disponible(self):
        return self.cliente_id is None

    @classmethod
    def consultar_autos_vendidos_por_cliente(cls, cliente_id):
        try:
            # Filtrar autos que tienen un cliente asignado específico
            autos_vendidos = session.query(cls).filter_by(
                cliente_id=cliente_id).all()

            if autos_vendidos:
                print(f"Autos vendidos al cliente con ID {cliente_id}:")
                for auto in autos_vendidos:
                    print(
                        f"VIN: {auto.codigo_vin}, Marca: {auto.marca}, Modelo: {auto.modelo}")
            else:
                print("No se encontraron autos vendidos para este cliente.")

            return autos_vendidos  # Devuelve la lista de autos vendidos
        except Exception as e:
            print(
                f"Error al consultar los autos vendidos para el cliente: {e}")
            return []

    @classmethod
    def consultar_autos_vendidos(cls):
        """Consulta todos los autos que tienen un cliente asociado (es decir, vendidos)."""
        try:
            # Filtrar autos que tienen un cliente asignado
            autos_vendidos = session.query(cls).filter(
                cls.cliente_id.isnot(None)).all()
            return autos_vendidos
        except Exception as e:
            print(f"Error al consultar los autos vendidos: {e}")
            return []

    @classmethod
    def obtener_autos_disponibles(cls):
        """Devuelve una lista de autos disponibles (sin cliente asignado)."""
        try:
            # Obtener instancias de Auto disponibles (sin cliente asignado)
            autos_disponibles = session.query(cls).filter(
                cls.cliente_id.is_(None)).all()
            return autos_disponibles  # Retorna las instancias de Auto
        except Exception as e:
            print(f"Error al obtener autos disponibles: {e}")
            return []

    @classmethod
    def obtener_autos(cls):
        """Devuelve una lista de todos los autos en el inventario."""
        try:
            autos = session.query(cls).all()
            return autos  # Devuelve todos los autos
        except Exception as e:
            print(f"Error al obtener los autos: {e}")
            return []