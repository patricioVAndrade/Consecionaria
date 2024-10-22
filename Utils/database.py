from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Conexión
engine = create_engine('sqlite:///Utils/autos.db')

#  Sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Función para crear las tablas en la base de datos


def create_tables():
    Base.metadata.create_all(engine)
