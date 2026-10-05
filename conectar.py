"""
Módulo de Conexión a Base de Datos SQLite.
Conecta a 'inmobiliaria.db' y asegura el cumplimiento de claves foráneas (PRAGMA foreign_keys = ON).
"""
import sqlite3
import os

DB_NAME = "inmobiliaria.db"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)

def crear_conexion():
    """Crea y retorna una conexión activa a SQLite con Foreign Keys activadas."""
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
