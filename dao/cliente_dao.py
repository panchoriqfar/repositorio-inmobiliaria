"""
ClienteDAO: Manejo de persistencia para la entidad Cliente.
"""
from typing import List, Optional
from dao.dao import DAO
from model.cliente import Cliente

class ClienteDAO(DAO):
    def crear_tabla(self):
        """Crea la tabla clientes si no existe."""
        sql = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            tiene_mora INTEGER NOT NULL DEFAULT 0
        );
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        self.conexion.commit()

    def insertar(self, cliente: Cliente) -> Cliente:
        """Inserta un cliente en la base de datos."""
        sql = "INSERT INTO clientes (rut, nombre, tiene_mora) VALUES (?, ?, ?);"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (cliente.rut, cliente.nombre, 1 if cliente.tiene_mora else 0))
        self.conexion.commit()
        cliente.id_cliente = cursor.lastrowid
        return cliente

    def buscar(self, id_cliente: int) -> Optional[Cliente]:
        """Busca un cliente por ID."""
        sql = "SELECT id, rut, nombre, tiene_mora FROM clientes WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id_cliente,))
        row = cursor.fetchone()
        if not row:
            return None
        return Cliente(rut=row[1], nombre=row[2], tiene_mora=bool(row[3]), id_cliente=row[0])

    def buscar_por_rut(self, rut: str) -> Optional[Cliente]:
        """Busca un cliente por RUT."""
        sql = "SELECT id, rut, nombre, tiene_mora FROM clientes WHERE rut = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (rut.strip().upper(),))
        row = cursor.fetchone()
        if not row:
            return None
        return Cliente(rut=row[1], nombre=row[2], tiene_mora=bool(row[3]), id_cliente=row[0])

    def listar(self) -> List[Cliente]:
        """Lista todos los clientes."""
        sql = "SELECT id, rut, nombre, tiene_mora FROM clientes ORDER BY id ASC;"
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [Cliente(rut=row[1], nombre=row[2], tiene_mora=bool(row[3]), id_cliente=row[0]) for row in rows]

    def actualizar_mora(self, id_cliente: int, tiene_mora: bool) -> bool:
        """Actualiza el estado de mora de un cliente."""
        sql = "UPDATE clientes SET tiene_mora = ? WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (1 if tiene_mora else 0, id_cliente))
        self.conexion.commit()
        return cursor.rowcount > 0
