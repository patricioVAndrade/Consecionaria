from enum import Enum


class Estado(str, Enum):
    nuevo = "nuevo"
    usado = "usado"


class TipoServicio(str, Enum):
    mantenimiento = "mantenimiento"
    reparacion = "reparación"
