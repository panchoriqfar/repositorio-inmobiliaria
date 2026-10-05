"""
Clase Base Persona con encapsulamiento y validación estricta de RUT chileno.
"""

class Persona:
    def __init__(self, rut: str, nombre: str):
        self._nombre = None
        self._rut = None
        self.nombre = nombre
        self.rut = rut  # Llama al setter con validación de DV

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 2:
            raise ValueError("El nombre debe contener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def rut(self) -> str:
        return self._rut

    @rut.setter
    def rut(self, valor: str):
        if not self.validar_rut(valor):
            raise ValueError(f"El RUT '{valor}' no es válido (formato o dígito verificador incorrecto).")
        self._rut = self.formatear_rut(valor)

    @staticmethod
    def validar_rut(rut_str: str) -> bool:
        """Valida cuerpo y dígito verificador módulo 11 de RUT chileno (multiplicadores 2 al 7)."""
        if not rut_str or not isinstance(rut_str, str):
            return False
        limpio = rut_str.replace(".", "").replace("-", "").strip().upper()
        if len(limpio) < 8 or len(limpio) > 9:
            return False
        
        cuerpo = limpio[:-1]
        dv = limpio[-1]
        if not cuerpo.isdigit():
            return False
        
        suma = 0
        multiplicador = 2
        for d in reversed(cuerpo):
            suma += int(d) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
        resto = suma % 11
        dv_esperado = 11 - resto
        if dv_esperado == 11:
            dv_calc = "0"
        elif dv_esperado == 10:
            dv_calc = "K"
        else:
            dv_calc = str(dv_esperado)
            
        return dv == dv_calc

    @staticmethod
    def formatear_rut(rut_str: str) -> str:
        limpio = rut_str.replace(".", "").replace("-", "").strip().upper()
        cuerpo = limpio[:-1]
        dv = limpio[-1]
        cuerpo_fmt = f"{int(cuerpo):,}".replace(",", ".")
        return f"{cuerpo_fmt}-{dv}"

    def __str__(self):
        return f"{self.nombre} (RUT: {self.rut})"
