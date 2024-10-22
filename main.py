from Utils.database import create_tables
from Models.Auto import Auto
from Models.Cliente import Cliente
from Models.Vendedor import Vendedor
from Models.Venta import Venta
from Models.Servicio import Servicio
from Utils.database import session
from Utils.enums import Estado
from Models.Servicio import Servicio, TipoServicio


def Main():
    # Crear las tablas si no existen
    create_tables()

    """
    nuevo_cliente = Cliente(nombre="Juan", apellido="Pérez",
                            direccion="Calle Falsa 123", telefono="123456789")
    session.add(nuevo_cliente)
    session.commit()
    """

    """
    codigo_vin = input("Ingrese el código VIN: ")
    marca = input("Ingrese la marca: ")
    modelo = input("Ingrese el modelo: ")
    anio = int(input("Ingrese el año: "))
    precio = float(input("Ingrese el precio: "))
    estado_input = input("Ingrese el estado (nuevo/usado): ")

    # Verificar si el estado ingresado es válido
    if estado_input not in ['nuevo', 'usado']:
        print("Estado no válido. Debe ser 'nuevo' o 'usado'.")
        return

    estado = Estado(estado_input)
    cliente_id = int(input("Ingrese el ID del cliente: "))

    # Registrar el auto utilizando el método de la clase Auto
    Auto.registrar_auto(codigo_vin=codigo_vin, marca=marca,
                        modelo=modelo, anio=anio, precio=precio, estado=estado, cliente_id=cliente_id)

    # Consultar clientes
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(f'Cliente: {cliente.nombre} {cliente.apellido}')
    """
    # Registrar Cliente
    """
    nombre = input("Ingrese el nombre del cliente: ")
    apellido = input("Ingrese el apellido del cliente: ")
    direccion = input("Ingrese la dirección del cliente: ")
    telefono = int(input("Ingrese el teléfono del cliente: "))
    Cliente.registrar_cliente(nombre=nombre, apellido=apellido,
                              direccion=direccion, telefono=telefono)
    """
    """
    # Ingresar los datos del auto por teclado
    codigo_vin = input("Ingrese el código VIN del auto: ")
    marca = input("Ingrese la marca del auto: ")
    modelo = input("Ingrese el modelo del auto: ")
    anio = int(input("Ingrese el año del auto: "))
    precio = float(input("Ingrese el precio del auto: "))

    # Ingresar si el auto es nuevo o usado
    estado = input("Ingrese el estado del auto (nuevo/usado): ").lower()
    estado_auto = None
    if estado == 'nuevo':
        estado_auto = Estado.nuevo
    elif estado == 'usado':
        estado_auto = Estado.usado
    else:
        print("Estado inválido. Ingrese 'nuevo' o 'usado'.")
        exit()

    # Registrar el nuevo auto
    Auto.registrar_auto(codigo_vin=codigo_vin, marca=marca,
                        modelo=modelo, anio=anio, precio=precio, estado=estado_auto)
    """
    """
    # Simular la venta de un auto
    codigo_vin = input("Ingrese el código VIN del auto que desea vender: ")
    cliente_id = int(input("Ingrese el ID del cliente que comprará el auto: "))

    # Intentar vender el auto
    Auto.vender_auto(codigo_vin=codigo_vin, cliente_id=cliente_id)

    # Verificar si el auto está disponible
    auto = session.query(Auto).filter_by(codigo_vin=codigo_vin).first()
    if auto.esta_disponible():
        print("El auto está disponible para la venta.")
    else:
        print("El auto ya ha sido vendido.")
    """
    """
    # Obtener el código VIN del auto disponible
    codigo_vin = input("Ingrese el código VIN del auto a vender: ")

    # Obtener el ID del cliente registrado que comprará el auto
    cliente_id = int(input("Ingrese el ID del cliente que comprará el auto: "))

    # Obtener el ID del vendedor registrado que realizará la venta
    vendedor_id = int(
        input("Ingrese el ID del vendedor que realizará la venta: "))

    # Simular la venta del auto
    Auto.vender_auto(codigo_vin=codigo_vin,
                     cliente_id=cliente_id, vendedor_id=vendedor_id)

    # Actualizar la comisión del vendedor
    vendedor = session.query(Vendedor).filter_by(id=vendedor_id).first()
    if vendedor:
        vendedor.comisiones += 5  # Incrementar la comisión del vendedor
        session.commit()
        print(f"Comisión del vendedor {vendedor.nombre} actualizada.")
    else:
        print("Vendedor no encontrado.")

    # Verificar si el auto está disponible o ya ha sido vendido
    auto = session.query(Auto).filter_by(codigo_vin=codigo_vin).first()
    if auto.esta_disponible():
        print("El auto está disponible para la venta.")
    else:
        print("El auto ya ha sido vendido.")
    """
    """
    def registrar_servicio_auto():
        # Obtener el código VIN de un auto que ya tiene cliente
        codigo_vin = input("Ingrese el código VIN del auto: ")

        # Verificar si el auto existe y tiene un cliente asignado
        auto = session.query(Auto).filter_by(codigo_vin=codigo_vin).first()

        if auto and auto.cliente:
            print(
                f"Auto encontrado: {auto.marca} {auto.modelo}, Cliente: {auto.cliente.nombre} {auto.cliente.apellido}")

            # Elegir el tipo de servicio
            print("Seleccione el tipo de servicio:")
            print("1. Mantenimiento")
            print("2. Reparación")
            tipo_servicio = int(
                input("Ingrese el número del servicio (1 o 2): "))

            if tipo_servicio == 1:
                tipo_servicio = TipoServicio.mantenimiento
            elif tipo_servicio == 2:
                tipo_servicio = TipoServicio.reparacion
            else:
                print("Opción no válida.")
                return

            # Registrar el servicio en la base de datos
            Servicio.registrar_servicio(
                auto_id=codigo_vin, tipo_servicio=tipo_servicio)
            print(f"Servicio de {tipo_servicio} registrado correctamente.")

        else:
            print("El auto no tiene un cliente asignado o no existe.")

    # Ejecutar la función para registrar un servicio
    registrar_servicio_auto()
    """
    """
    # Consultar servicios para un auto específico
     auto_id = input(
        "Ingrese el código VIN del auto para consultar los servicios: ")
     Servicio.consultar_servicios(auto_id)

    # Consultar autos vendidos a un cliente específico
    cliente_id = int(
        input("Ingrese el ID del cliente para consultar los autos vendidos: "))
    Auto.consultar_autos_vendidos(cliente_id)
    """


if __name__ == "__main__":
    Main()
