"""
ContratoDAO: Manejo de persistencia para ContratoArriendo y sus líneas de detalle.
Aplica validación de reglas de negocio al registrar transacciones:
- Regla 1: PropiedadYaArrendadaException
- Regla 2: ClienteConMoraException
"""
from typing import List, Optional
from dao.dao import DAO
from dao.cliente_dao import ClienteDAO
from dao.propiedad_dao import PropiedadDAO
from model.contrato_arriendo import ContratoArriendo
from model.linea_detalle_contrato import LineaDetalleContrato
from model.excepciones import PropiedadYaArrendadaException, ClienteConMoraException

class ContratoDAO(DAO):
    def crear_tabla(self):
        """Crea las tablas contratos y lineas_detalle si no existen."""
        sql_contratos = """
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_propiedad INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT NOT NULL,
            garantia_uf REAL NOT NULL DEFAULT 0.0,
            estado TEXT NOT NULL DEFAULT 'Vigente',
            FOREIGN KEY (id_cliente) REFERENCES clientes(id),
            FOREIGN KEY (id_propiedad) REFERENCES propiedades(id)
        );
        """
        sql_lineas = """
        CREATE TABLE IF NOT EXISTS lineas_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_contrato INTEGER NOT NULL,
            concepto TEXT NOT NULL,
            monto_uf REAL NOT NULL,
            FOREIGN KEY (id_contrato) REFERENCES contratos(id) ON DELETE CASCADE
        );
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql_contratos)
        cursor.execute(sql_lineas)
        # Agregar columnas nuevas si la tabla ya existía (migración segura)
        try:
            cursor.execute("ALTER TABLE contratos ADD COLUMN garantia_uf REAL NOT NULL DEFAULT 0.0;")
        except Exception:
            pass
        try:
            cursor.execute("ALTER TABLE contratos ADD COLUMN estado TEXT NOT NULL DEFAULT 'Vigente';")
        except Exception:
            pass
        self.conexion.commit()

    def verificar_propiedad_arrendada(self, id_propiedad: int, fecha_inicio: str, fecha_fin: str) -> bool:
        """
        Verifica si la propiedad ya cuenta con un contrato activo que se solape con el rango [fecha_inicio, fecha_fin].
        Retorna True si existe solapamiento (está ocupada).
        """
        sql = """
        SELECT COUNT(*) FROM contratos
        WHERE id_propiedad = ?
          AND NOT (fecha_fin < ? OR fecha_inicio > ?);
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id_propiedad, fecha_inicio, fecha_fin))
        count = cursor.fetchone()[0]
        return count > 0

    def insertar(self, contrato: ContratoArriendo) -> ContratoArriendo:
        """
        Inserta un contrato con sus líneas de detalle.
        Valida las 2 reglas de negocio y lanza excepciones personalizadas si corresponden.
        """
        # Regla 2: Cliente con mora
        if contrato.cliente.tiene_mora:
            raise ClienteConMoraException(
                f"El cliente {contrato.cliente.nombre} (RUT {contrato.cliente.rut}) presenta MORA registrada. No se puede firmar el contrato."
            )

        # Regla 1: Propiedad ya arrendada en ese período
        if self.verificar_propiedad_arrendada(contrato.propiedad.id_propiedad, contrato.fecha_inicio, contrato.fecha_fin):
            raise PropiedadYaArrendadaException(
                f"La propiedad en '{contrato.propiedad.direccion}' ya se encuentra arrendada durante el período {contrato.fecha_inicio} al {contrato.fecha_fin}."
            )

        # Insertar transacción principal
        sql_c = """
        INSERT INTO contratos (id_cliente, id_propiedad, fecha_inicio, fecha_fin, garantia_uf)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor = self.conexion.cursor()
        cursor.execute(sql_c, (contrato.cliente.id_cliente, contrato.propiedad.id_propiedad, contrato.fecha_inicio, contrato.fecha_fin, contrato.garantia_uf))
        contrato.id_contrato = cursor.lastrowid

        # Insertar líneas de detalle
        sql_l = "INSERT INTO lineas_detalle (id_contrato, concepto, monto_uf) VALUES (?, ?, ?);"
        for linea in contrato.lineas_detalle:
            cursor.execute(sql_l, (contrato.id_contrato, linea.concepto, linea.monto_uf))
            linea.id_linea = cursor.lastrowid

        self.conexion.commit()
        return contrato

    def listar(self) -> List[ContratoArriendo]:
        """Lista todos los contratos registrados cargando cliente, propiedad y líneas de detalle."""
        sql = "SELECT id FROM contratos ORDER BY id ASC;"
        cursor = self.conexion.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        contratos = []
        for r in rows:
            c = self.buscar(r[0])
            if c:
                contratos.append(c)
        return contratos

    def buscar(self, id_contrato: int) -> Optional[ContratoArriendo]:
        """Busca un contrato por ID e instancia su cliente, propiedad y líneas de detalle."""
        sql_c = "SELECT id, id_cliente, id_propiedad, fecha_inicio, fecha_fin, garantia_uf, estado FROM contratos WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql_c, (id_contrato,))
        row_c = cursor.fetchone()
        if not row_c:
            return None

        c_id, id_cli, id_prop, f_ini, f_fin = row_c[0], row_c[1], row_c[2], row_c[3], row_c[4]
        garantia = row_c[5] if len(row_c) > 5 else 0.0
        estado = row_c[6] if len(row_c) > 6 else 'Vigente'
        cliente_dao = ClienteDAO(self.conexion)
        prop_dao = PropiedadDAO(self.conexion)

        cliente = cliente_dao.buscar(id_cli)
        propiedad = prop_dao.buscar(id_prop)

        contrato = ContratoArriendo(cliente=cliente, propiedad=propiedad, fecha_inicio=f_ini, fecha_fin=f_fin, id_contrato=c_id, garantia_uf=garantia)
        contrato.estado = estado

        # Cargar líneas de detalle
        sql_l = "SELECT id, concepto, monto_uf FROM lineas_detalle WHERE id_contrato = ? ORDER BY id ASC;"
        cursor.execute(sql_l, (c_id,))
        rows_l = cursor.fetchall()
        for r_l in rows_l:
            contrato.agregar_linea_detalle(LineaDetalleContrato(concepto=r_l[1], monto_uf=r_l[2], id_linea=r_l[0]))

        return contrato

    def finalizar(self, id_contrato: int) -> bool:
        """Cambia el estado de un contrato a 'Finalizado'."""
        sql = "UPDATE contratos SET estado = 'Finalizado' WHERE id = ?;"
        cursor = self.conexion.cursor()
        cursor.execute(sql, (id_contrato,))
        self.conexion.commit()
        return cursor.rowcount > 0

