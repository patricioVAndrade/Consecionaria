from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class DatabaseSingleton:
    _instance = None
    _session = None
    _engine = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa la conexion a la base de datos"""
        if self._engine is None:
            self._engine = create_engine('sqlite:///Utils/autos.db')
            Session = sessionmaker(bind=self._engine)
            self._session = Session()
    
    @property
    def session(self):
        """Obtener la sesion de la base de datos"""
        return self._session
    
    @property
    def engine(self):
        """Obtener el motor de la base de datos"""
        return self._engine
    
    def create_tables(self):
        """Creacion de las Tablas"""
        Base.metadata.create_all(self._engine)
    
    def __del__(self):
        """Cerrar la sesion de la base de datos"""
        if self._session:
            self._session.close()

db = DatabaseSingleton()

session = db.session
engine = db.engine

def create_tables():
    db.create_tables()