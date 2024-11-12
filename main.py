from Utils.database import create_tables
from Interfaces.main_window import MainWindow


def Main():
    create_tables()


if __name__ == "__main__":
    Main()
    app = MainWindow()
    app.mainloop()