"""
Clase Base DAO (Data Access Object).
Recibe la conexión a la base de datos y provee la estructura general.
"""

class DAO:
    def __init__(self, conexion):
        self.conexion = conexion
