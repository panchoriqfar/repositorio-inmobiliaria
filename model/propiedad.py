"""
Clase Abstracta Propiedad.
Defines base attributes (direccion, metros_cuadrados, valor_uf) with setters and validations,
and the abstract method calcular_arriendo(valor_uf_dia).
"""
import abc

class Propiedad(abc.ABC):
    def __init__(self, direccion: str, metros_cuadrados: float, valor_uf: float, id_propiedad: int = None):
        self.id_propiedad = id_propiedad
        self._direccion = None
        self._metros_cuadrados = None
        self._valor_uf = None

        self.direccion = direccion
        self.metros_cuadrados = metros_cuadrados
        self.valor_uf = valor_uf

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, valor: str):
        if not valor or len(str(valor).strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres.")
        self._direccion = str(valor).strip()

    @property
    def metros_cuadrados(self) -> float:
        return self._metros_cuadrados

    @metros_cuadrados.setter
    def metros_cuadrados(self, valor: float):
        try:
            val = float(valor)
            if val <= 0:
                raise ValueError
            self._metros_cuadrados = val
        except (ValueError, TypeError):
            raise ValueError("Los metros cuadrados deben ser un número positivo.")

    @property
    def valor_uf(self) -> float:
        return self._valor_uf

    @valor_uf.setter
    def valor_uf(self, valor: float):
        try:
            val = float(valor)
            if val <= 0:
                raise ValueError
            self._valor_uf = val
        except (ValueError, TypeError):
            raise ValueError("El valor en UF debe ser un número positivo.")

    @abc.abstractmethod
    def calcular_arriendo(self, valor_uf_dia: float) -> int:
        """Calcula el valor mensual del arriendo en CLP según la fórmula del subtipo."""
        pass

    @abc.abstractmethod
    def tipo(self) -> str:
        """Devuelve el tipo de propiedad como string."""
        pass
