"""
Subtipo Casa de Propiedad.
Agrega el concepto de mantenimiento de jardín en UF.
"""
from model.propiedad import Propiedad

class Casa(Propiedad):
    def __init__(self, direccion: str, metros_cuadrados: float, valor_uf: float, gastos_jardin_uf: float = 0.5, id_propiedad: int = None):
        super().__init__(direccion, metros_cuadrados, valor_uf, id_propiedad)
        self.gastos_jardin_uf = float(gastos_jardin_uf)

    def tipo(self) -> str:
        return "Casa"

    def calcular_arriendo(self, valor_uf_dia: float) -> int:
        """
        Fórmula para Casa: (Valor Base UF + Mantención Jardín UF) * Valor UF en CLP.
        """
        total_uf = self.valor_uf + self.gastos_jardin_uf
        return int(round(total_uf * valor_uf_dia))

    def __str__(self):
        return f"[Casa ID {self.id_propiedad or 'N/A'}] {self.direccion} - {self.metros_cuadrados} m² - {self.valor_uf} UF (+{self.gastos_jardin_uf} UF Jardín)"
