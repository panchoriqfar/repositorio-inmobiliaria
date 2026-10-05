# 🏢 Inmobiliaria Terrenos del Sur - Sistema de Gestión

**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Sección:** 114-2A-F2  
**Integrantes:** Francisco Riquelme y Javiera Monsalve  
**Evaluación:** Sumativa N°2 - Primavera 2026  

---

## 📋 Descripción del Sistema

Este repositorio contiene la solución informática para **Inmobiliaria Terrenos del Sur**, desarrollada bajo los principios de **Programación Orientada a Objetos Seguro**, persistencia en **SQLite con patrón DAO**, y consumo de servicios externos (**API UF de mindicador.cl**).

El programa gestiona el catálogo de propiedades (`Casa`, `Departamento`, `Oficina`), registro de clientes con validación estricta de RUT, cálculo polimórfico de arriendos, emisión de contratos con detalle transaccional y control de reglas de negocio mediante excepciones personalizadas.

---

## 🛠️ Requisitos e Instalación

### 1. Requisitos Previos
* Python 3.10 o superior instalado.
* Conexión a Internet (opcional para el consumo inicial de la API UF).

### 2. Instalación de Dependencias
Abre la terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

### 3. Ejecución del Programa
Ejecuta el menú interactivo con el siguiente comando:

```bash
python main.py
```

---

## 🛡️ Decisiones Técnicas y Seguridad del Código

1. **Prevención de Inyección SQL (Consultas Parametrizadas):**
   * Ninguna consulta SQL concatena valores directamente. Se utilizan marcadores de posición `?` en todos los métodos de `PropiedadDAO`, `ClienteDAO` y `ContratoDAO` (ej: `cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))`).

2. **Encapsulamiento y Validación en Setters:**
   * La clase `Persona` encapsula el RUT en su setter `@rut.setter`. Valida la estructura y calcula el dígito verificador mediante el algoritmo chileno módulo 11. Si se ingresa un RUT inválido (como `12.345.678-9`), el sistema lanza un `ValueError` amigable y el programa sigue funcionando sin caerse.

3. **Integridad Referencial en SQLite:**
   * El módulo [conectar.py](file:///C:/Users/admin/Desktop/archivos%20evaluacion/repositorio%20inmobiliaria/conectar.py) ejecuta explícitamente `PRAGMA foreign_keys = ON;` al abrir la base de datos `inmobiliaria.db`, garantizando que no existan contratos huérfanos sin cliente o propiedad válida.

4. **Resiliencia en el Consumo de Servicios Externos:**
   * La clase `IndicadorService` consume `https://mindicador.cl/api/uf` definiendo un tiempo máximo de espera de `timeout=5`. Si la API no responde o el equipo está sin internet, el sistema captura la excepción de red, notifica el aviso al usuario y activa un valor UF de contingencia para garantizar la **continuidad del servicio**.

5. **Excepciones Personalizadas para Reglas del Negocio:**
   * `PropiedadYaArrendadaException`: Impide solapamientos de fechas en alquileres.
   * `ClienteConMoraException`: Bloquea firmas de contratos a clientes con deudas pendientes.

---

## 🤖 Ejemplo Concreto de Uso de Inteligencia Artificial (IA)

* **Sugerencia de la IA:** Durante el diseño, la IA sugirió implementar la validación del dígito verificador del RUT dentro de la función de inserción del DAO.
* **Decisión Técnica Adoptada y Modificación:** Se modificó la sugerencia de la IA para mover la validación directamente al **setter de la propiedad `@rut.setter`** en la clase de dominio `Persona`. 
* **Justificación:** Validar en el modelo respeta el principio de encapsulamiento de POO y evita propagar objetos inconsistentes o corruptos hacia la capa de datos o la interfaz de usuario, cumpliendo con los estándares de **código seguro**.
