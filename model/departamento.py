"""
Subtipo Departamento de Propiedad.
Agrega gastos comunes base en UF.
"""
from model.propiedad import Propiedad

class Departamento(Propiedad):
    def __init__(self, direccion: str, metros_cuadrados: float, valor_uf: float, gastos_comunes_base_uf: float = 0.3, id_propiedad: int = None):
        super().__init__(direccion, metros_cuadrados, valor_uf, id_propiedad)
        self.gastos_comunes_base_uf = float(gastos_comunes_base_uf)

    def tipo(self) -> str:
        return "Departamento"

    def calcular_arriendo(self, valor_uf_dia: float) -> int:
        """
        Fórmula para Departamento: (Valor Base UF + Gastos Comunes Base UF) * Valor UF en CLP.
        """
        total_uf = self.valor_uf + self.gastos_comunes_base_uf
        return int(round(total_uf * valor_uf_dia))

    def __str__(self):
        return f"[Dpto ID {self.id_propiedad or 'N/A'}] {self.direccion} - {self.metros_cuadrados} m² - {self.valor_uf} UF (+{self.gastos_comunes_base_uf} UF Gastos Comunes)"
