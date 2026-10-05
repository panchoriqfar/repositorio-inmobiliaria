"""
Clase Cliente que hereda de Persona y agrega el estado de mora.
"""
from model.persona import Persona

class Cliente(Persona):
    def __init__(self, rut: str, nombre: str, tiene_mora: bool = False, id_cliente: int = None):
        super().__init__(rut, nombre)
        self.id_cliente = id_cliente
        self._tiene_mora = bool(tiene_mora)

    @property
    def tiene_mora(self) -> bool:
        return self._tiene_mora

    @tiene_mora.setter
    def tiene_mora(self, valor: bool):
        self._tiene_mora = bool(valor)

    def __str__(self):
        mora_str = "Con Mora ⚠️" if self.tiene_mora else "Al día ✅"
        return f"Cliente ID: {self.id_cliente or 'N/A'} - {super().__str__()} [{mora_str}]"
