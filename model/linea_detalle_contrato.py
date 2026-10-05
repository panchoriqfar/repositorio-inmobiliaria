"""
Clase LineaDetalleContrato.
Representa un ítem o concepto específico dentro de una transacción/contrato de arriendo
(ej: Arriendo del mes, Gastos comunes, Garantía).
"""

class LineaDetalleContrato:
    def __init__(self, concepto: str, monto_uf: float, id_linea: int = None):
        self.id_linea = id_linea
        self.concepto = str(concepto).strip()
        self.monto_uf = float(monto_uf)

    def subtotal_clp(self, valor_uf_dia: float) -> int:
        """Calcula el monto del concepto convertido a CLP segun el valor de la UF."""
        return int(round(self.monto_uf * valor_uf_dia))

    def __str__(self):
        return f"- {self.concepto}: {self.monto_uf:.2f} UF"
