"""
Módulo de Excepciones Personalizadas para Inmobiliaria Terrenos del Sur.
Define los errores de reglas de negocio según la pauta de evaluación:
1. PropiedadYaArrendadaException: Impide arrendar una propiedad ya arrendada en ese período.
2. ClienteConMoraException: Impide firmar contrato a un cliente que tiene mora registrada.
"""

class PropiedadYaArrendadaException(Exception):
    """Excepción lanzada cuando se intenta arrendar una propiedad ocupada en un período."""
    def __init__(self, mensaje="La propiedad ya se encuentra arrendada en el período indicado."):
        super().__init__(mensaje)

class ClienteConMoraException(Exception):
    """Excepción lanzada cuando se intenta firmar contrato con un cliente en mora."""
    def __init__(self, mensaje="El cliente presenta deudas/mora pendientes. No se puede firmar el contrato."):
        super().__init__(mensaje)
