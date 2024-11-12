from logging import root
import re
from tkinter import messagebox
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Utils.database import Base, session
from sqlalchemy.exc import IntegrityError
import tkinter as tk


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

    @staticmethod
    def validar_nombre(nombre):
        # Verifica que el nombre solo contenga letras y espacios
        return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre))
    
    @staticmethod
    def validar_apellido(apellido):
        # Verifica que el apellido solo contenga letras y espacios
        return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', apellido))
    
    @staticmethod
    def validar_telefono(telefono):
        # Verifica que el telefono solo contenga números enteros positivos
        return bool(re.match(r'^\d+$', str(telefono)))


    @classmethod
    def registrar_cliente(cls, nombre, apellido, direccion, telefono):
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de tkinter

        if not cls.validar_nombre(nombre):
            messagebox.showerror("Aviso!!", "El nombre solo puede contener letras.")
            root.destroy()
            return False
        
        elif not cls.validar_apellido(apellido):
            messagebox.showerror("Aviso!!", "El apellido solo puede contener letras.")
            root.destroy()
            return False
        
        elif not cls.validar_telefono(telefono):
            messagebox.showerror("Aviso!!", "El telefono solo puede contener numeros")
            root.destroy()
            return False

        else:
            nuevo_cliente = cls(nombre=nombre, apellido=apellido, direccion=direccion,
                            telefono=telefono)
            try:
                session.add(nuevo_cliente)
                session.commit()
                print(f"Cliente {nombre} {apellido} registrado correctamente.")
            except IntegrityError:
                session.rollback()
                print(f"Error: el cliente con ID {id} ya existe.")

    @classmethod
    def obtener_clientes(cls):
        """Devuelve una lista de todos los clientes registrados."""
        try:
            clientes = session.query(cls).all()
            return [f"{cliente.id} - {cliente.nombre} {cliente.apellido}" for cliente in clientes]
        except Exception as e:
            print(f"Error al obtener la lista de clientes: {e}")
            return []
