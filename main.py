from Utils.database import create_tables
from Models.Auto import Auto
from Models.Cliente import Cliente
from Models.Vendedor import Vendedor
from Models.Venta import Venta
from Models.Servicio import Servicio
from Utils.database import session

# Crear las tablas si no existen
create_tables()

# Aquí puedes agregar la lógica para interactuar con la base de datos,
# por ejemplo, insertar datos en las tablas.

# Ejemplo de insertar un cliente
nuevo_cliente = Cliente(nombre="Juan", apellido="Pérez",
                        direccion="Calle Falsa 123", telefono="123456789")
session.add(nuevo_cliente)
session.commit()

# Consultar clientes
clientes = session.query(Cliente).all()
for cliente in clientes:
    print(f'Cliente: {cliente.nombre} {cliente.apellido}')
