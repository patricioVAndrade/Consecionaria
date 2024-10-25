from Utils.database import create_tables
from Interfaces.main_window import MainWindow


def Main():
    # Crear las tablas si no existen
    create_tables()


if __name__ == "__main__":
    Main()
    app = MainWindow()
    app.mainloop()
