"""
PropiedadDAO: Manejo seguro de persistencia para la entidad Propiedad y sus subtipos (Casa, Departamento, Oficina).
Todas las consultas utilizan parámetros con (?) para evitar Inyección SQL.
"""
from typing import List, Optional
from dao.dao import DAO
from model.propiedad import Propiedad
from model.casa import Casa
from model.departamento import Departamento
from model.oficina import Oficina

class PropiedadDAO(DAO):
    def crear_tabla(self):
        """Crea la tabla propiedades si no existe."""
        sql = """
        CREATE TABLE IF NOT EXISTS propiedades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direccion TEXT NOT NULL,
            metros_cuadrados REAL NOT NULL,
            valor_uf REAL NOT NULL,
            tipo TEXT NOT NULL,
            extra_uf REAL NOT NULL DEFAULT 0.0
        );
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        self.conexion.commit()

    def insertar(self, propiedad: Propiedad) -> Propiedad:
        """Inserta una propiedad en la base de datos usando consulta parametrizada."""
        extra = 0.0
        if isinstance(propiedad, Casa):
            extra = propiedad.gastos_jardin_uf
        elif isinstance(propiedad, Departamento):
            extra = propiedad.gastos_comunes_base_uf
        elif isinstance(propiedad, Oficina):
            extra = propiedad.recargo_comercial_uf

        sql = """
        INSERT INTO propiedades (direccion, metros_cuadrados, valor_uf, tipo, extra_uf)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql, (propiedad.direccion, propiedad.metros_cuadrados, propiedad.valor_uf, propiedad.tipo(), extra))
        self.conexion.commit()
        propiedad.id_propiedad = cursor.lastrowid
        return propiedad

    def buscar(self, id_propiedad: int) -> Optional[Propiedad]:
        """Busca una propiedad por ID y retorna la instancia del subtipo correcto."""
        sql = "SELECT id, direccion, metros_cuadrados, valor_uf, tipo, extra_uf FROM propiedades WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id_propiedad,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._instanciar_propiedad(row)

    def listar(self) -> List[Propiedad]:
        """Listar todas las propiedades registradas."""
        sql = "SELECT id, direccion, metros_cuadrados, valor_uf, tipo, extra_uf FROM propiedades ORDER BY id ASC;"
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [self._instanciar_propiedad(row) for row in rows]

    def actualizar(self, propiedad: Propiedad) -> bool:
        """Actualiza los datos de una propiedad existente."""
        extra = 0.0
        if isinstance(propiedad, Casa):
            extra = propiedad.gastos_jardin_uf
        elif isinstance(propiedad, Departamento):
            extra = propiedad.gastos_comunes_base_uf
        elif isinstance(propiedad, Oficina):
            extra = propiedad.recargo_comercial_uf

        sql = """
        UPDATE propiedades
        SET direccion = ?, metros_cuadrados = ?, valor_uf = ?, extra_uf = ?
        WHERE id = ?;
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql, (propiedad.direccion, propiedad.metros_cuadrados, propiedad.valor_uf, extra, propiedad.id_propiedad))
        self.conexion.commit()
        return cursor.rowcount > 0

    def eliminar(self, id_propiedad: int) -> bool:
        """Elimina una propiedad por su ID."""
        sql = "DELETE FROM propiedades WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id_propiedad,))
        self.conexion.commit()
        return cursor.rowcount > 0

    def _instanciar_propiedad(self, row) -> Propiedad:
        p_id, direccion, m2, valor_uf, tipo, extra = row
        if tipo == "Casa":
            return Casa(direccion, m2, valor_uf, gastos_jardin_uf=extra, id_propiedad=p_id)
        elif tipo == "Departamento":
            return Departamento(direccion, m2, valor_uf, gastos_comunes_base_uf=extra, id_propiedad=p_id)
        elif tipo == "Oficina":
            return Oficina(direccion, m2, valor_uf, recargo_comercial_uf=extra, id_propiedad=p_id)
        else:
            raise ValueError(f"Tipo de propiedad desconocido: {tipo}")
