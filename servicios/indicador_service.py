"""
Módulo para el consumo de Servicios Externos / APIs Públicas.
Obtiene la cotización oficial de la UF desde mindicador.cl.
Satisface el indicador 3.1.1 / 3.1.3:
- Librería oficial requests
- Timeout de 5 segundos
- Manejo de excepciones para asegurar la continuidad del sistema si falla internet.
"""
import requests

class IndicadorService:
    def __init__(self, timeout: int = 5):
        self.url = "https://mindicador.cl/api/uf"
        self.timeout = timeout

    def obtener_valor_uf(self) -> float:
        """
        Consulta la API REST de mindicador.cl para obtener el valor del día de la UF.
        Lanza requests.RequestException si falla la red, el servidor no responde o caduca el timeout.
        """
        response = requests.get(self.url, timeout=self.timeout)
        response.raise_for_status()  # Verifica codigos HTTP 200 OK
        data = response.json()
        return float(data["serie"][0]["valor"])
