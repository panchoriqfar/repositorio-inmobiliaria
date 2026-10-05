"""
Subtipo Oficina de Propiedad.
Agrega recargo comercial en UF.
"""
from model.propiedad import Propiedad

class Oficina(Propiedad):
    def __init__(self, direccion: str, metros_cuadrados: float, valor_uf: float, recargo_comercial_uf: float = 1.0, id_propiedad: int = None):
        super().__init__(direccion, metros_cuadrados, valor_uf, id_propiedad)
        self.recargo_comercial_uf = float(recargo_comercial_uf)

    def tipo(self) -> str:
        return "Oficina"

    def calcular_arriendo(self, valor_uf_dia: float) -> int:
        """
        Fórmula para Oficina: (Valor Base UF + Recargo Comercial UF) * Valor UF en CLP.
        """
        total_uf = self.valor_uf + self.recargo_comercial_uf
        return int(round(total_uf * valor_uf_dia))

    def __str__(self):
        return f"[Oficina ID {self.id_propiedad or 'N/A'}] {self.direccion} - {self.metros_cuadrados} m² - {self.valor_uf} UF (+{self.recargo_comercial_uf} UF Recargo Comercial)"
