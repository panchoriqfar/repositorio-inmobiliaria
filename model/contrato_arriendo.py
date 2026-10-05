"""
Clase ContratoArriendo (Transacción con Líneas de Detalle).
Guarda la información completa de un arriendo firmado entre un Cliente y una Propiedad.
"""
from typing import List
from model.cliente import Cliente
from model.propiedad import Propiedad
from model.linea_detalle_contrato import LineaDetalleContrato

class ContratoArriendo:
    def __init__(self, cliente: Cliente, propiedad: Propiedad, fecha_inicio: str, fecha_fin: str, id_contrato: int = None):
        self.id_contrato = id_contrato
        self.cliente = cliente
        self.propiedad = propiedad
        self.fecha_inicio = fecha_inicio  # Formato YYYY-MM-DD
        self.fecha_fin = fecha_fin        # Formato YYYY-MM-DD
        self.lineas_detalle: List[LineaDetalleContrato] = []

    def agregar_linea_detalle(self, linea: LineaDetalleContrato):
        """Agrega un concepto de cobro al detalle del contrato."""
        self.lineas_detalle.append(linea)

    def total_uf(self) -> float:
        """Suma el monto en UF de todas las líneas de detalle."""
        return sum(linea.monto_uf for linea in self.lineas_detalle)

    def total_clp(self, valor_uf_dia: float) -> int:
        """Suma el monto en CLP de todas las líneas de detalle."""
        return sum(linea.subtotal_clp(valor_uf_dia) for linea in self.lineas_detalle)

    def __str__(self):
        return (f"Contrato N° {self.id_contrato or 'Nuevo'} | Cliente: {self.cliente.nombre} | "
                f"Propiedad: {self.propiedad.direccion} ({self.propiedad.tipo()}) | "
                f"Período: {self.fecha_inicio} al {self.fecha_fin} | Total UF: {self.total_uf():.2f} UF")
