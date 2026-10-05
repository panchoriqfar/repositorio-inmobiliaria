"""
Sistema de Gestión Inmobiliaria Terrenos del Sur.
Archivo Principal (main.py).

Cumple con todos los requisitos de la Ficha del Negocio y el Guión de Pruebas P01-P19:
- P01: Menú interactivo CLI ejecutable.
- P02-P06: CRUD Completo de Propiedades con persistencia SQLite.
- P07-P08: Validación de RUT chileno en setter de Persona (acepta 12.345.678-5, rechaza 12.345.678-9).
- P09-P11: Polimorfismo en calcular_arriendo() para Casa, Departamento y Oficina.
- P12-P13: Transacción ContratoArriendo con Líneas de Detalle.
- P14-P15: Excepciones personalizadas para Reglas de Negocio (Mora y Solapamiento de Fechas).
- P16-P17: Consumo de API UF (mindicador.cl) con timeout y resiliencia offline.
- P18-P19: Validación de opciones (99) y tipos de datos (abc).
"""

import sys
from conectar import crear_conexion
from dao.propiedad_dao import PropiedadDAO
from dao.cliente_dao import ClienteDAO
from dao.contrato_dao import ContratoDAO
from model.casa import Casa
from model.departamento import Departamento
from model.oficina import Oficina
from model.cliente import Cliente
from model.contrato_arriendo import ContratoArriendo
from model.linea_detalle_contrato import LineaDetalleContrato
from model.excepciones import PropiedadYaArrendadaException, ClienteConMoraException
from servicios.indicador_service import IndicadorService

def inicializar_base_datos(conexion):
    """Crea automáticamente las tablas si no existen al iniciar el programa."""
    PropiedadDAO(conexion).crear_tabla()
    ClienteDAO(conexion).crear_tabla()
    ContratoDAO(conexion).crear_tabla()

def obtener_uf_actual() -> float:
    """Obtiene el valor de la UF online o pide un valor de respaldo si falla internet."""
    service = IndicadorService(timeout=5)
    try:
        valor_uf = service.obtener_valor_uf()
        return valor_uf
    except Exception as e:
        print("\n⚠️ [AVISO DE RED] No se pudo obtener la UF desde internet (Sin conexión o timeout).")
        print("   El programa continuará funcionando utilizando un valor UF de respaldo ($39.000 CLP).")
        return 39000.0

def leer_entero(mensaje: str) -> int:
    """Lee un entero validando la entrada (Evita caídas con valores no numéricos)."""
    while True:
        txt = input(mensaje).strip()
        try:
            return int(txt)
        except ValueError:
            print("❌ Entrada inválida: Debe ingresar un número entero válido (ej: 1, 2, 60). Intente de nuevo.")

def leer_flotante(mensaje: str) -> float:
    """Lee un número decimal validando la entrada."""
    while True:
        txt = input(mensaje).strip().replace(",", ".")
        try:
            val = float(txt)
            if val <= 0:
                print("❌ Debe ingresar un valor positivo mayor a 0.")
                continue
            return val
        except ValueError:
            print("❌ Entrada inválida: Debe ingresar un valor numérico válido (ej: 12.5). Intente de nuevo.")

# ==================== SUBMENÚS ====================

def menu_propiedades(conexion):
    p_dao = PropiedadDAO(conexion)
    while True:
        print("\n--- 🏠 GESTIÓN DE PROPIEDADES ---")
        print("1. Crear Propiedad (Casa / Departamento / Oficina)")
        print("2. Listar Propiedades")
        print("3. Modificar Valor UF de Propiedad")
        print("4. Eliminar Propiedad")
        print("5. Volver al Menú Principal")
        
        op = input("Seleccione una opción: ").strip()
        if op == "1":
            print("\n--- Crear Propiedad ---")
            print("1. Casa")
            print("2. Departamento")
            print("3. Oficina")
            tipo_op = input("Elija el tipo de propiedad: ").strip()
            
            direccion = input("Dirección: ").strip()
            m2 = leer_flotante("Metros cuadrados: ")
            uf = leer_flotante("Valor en UF: ")
            
            try:
                if tipo_op == "1":
                    g_jardin = leer_flotante("Gastos de Jardín en UF (ej: 0.5): ")
                    prop = Casa(direccion, m2, uf, gastos_jardin_uf=g_jardin)
                elif tipo_op == "2":
                    g_comunes = leer_flotante("Gastos Comunes base en UF (ej: 0.3): ")
                    prop = Departamento(direccion, m2, uf, gastos_comunes_base_uf=g_comunes)
                elif tipo_op == "3":
                    recargo = leer_flotante("Recargo Comercial en UF (ej: 1.0): ")
                    prop = Oficina(direccion, m2, uf, recargo_comercial_uf=recargo)
                else:
                    print("❌ Tipo no válido.")
                    continue
                
                p_dao.insertar(prop)
                print(f"✅ Propiedad creada exitosamente con ID N° {prop.id_propiedad}.")
            except ValueError as ve:
                print(f"❌ Error de validación: {ve}")

        elif op == "2":
            print("\n--- Listado de Propiedades ---")
            lista = p_dao.listar()
            if not lista:
                print("No hay propiedades registradas.")
            else:
                for p in lista:
                    print(p)

        elif op == "3":
            print("\n--- Modificar Propiedad ---")
            p_id = leer_entero("ID de la propiedad a modificar: ")
            prop = p_dao.buscar(p_id)
            if not prop:
                print("❌ Propiedad no encontrada.")
                continue
            print(f"Propiedad actual: {prop}")
            nuevo_valor = leer_flotante("Ingrese el nuevo valor en UF: ")
            prop.valor_uf = nuevo_valor
            p_dao.actualizar(prop)
            print("✅ Valor de la propiedad actualizado correctamente.")

        elif op == "4":
            print("\n--- Eliminar Propiedad ---")
            p_id = leer_entero("ID de la propiedad a eliminar: ")
            exito = p_dao.eliminar(p_id)
            if exito:
                print("✅ Propiedad eliminada correctamente.")
            else:
                print("❌ No se encontró la propiedad con ese ID.")

        elif op == "5":
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

def menu_clientes(conexion):
    c_dao = ClienteDAO(conexion)
    while True:
        print("\n--- 👤 GESTIÓN DE CLIENTES ---")
        print("1. Registrar Nuevo Cliente")
        print("2. Listar Clientes")
        print("3. Cambiar Estado de Mora de un Cliente")
        print("4. Volver al Menú Principal")

        op = input("Seleccione una opción: ").strip()
        if op == "1":
            print("\n--- Registrar Cliente ---")
            nombre = input("Nombre completo: ").strip()
            rut = input("RUT (ej: 12.345.678-5): ").strip()
            mora_input = input("¿Tiene deudas/mora pendientes? (s/n): ").strip().lower()
            mora = mora_input == 's'
            try:
                cli = Cliente(rut=rut, nombre=nombre, tiene_mora=mora)
                c_dao.insertar(cli)
                print(f"✅ Cliente registrado exitosamente con ID N° {cli.id_cliente}.")
            except ValueError as ve:
                print(f"❌ Rechazado por validación de RUT: {ve}")
                print("   (El programa continúa funcionando sin detenerse).")
            except Exception as e:
                print(f"❌ Error al guardar cliente: {e}")

        elif op == "2":
            print("\n--- Listado de Clientes ---")
            lista = c_dao.listar()
            if not lista:
                print("No hay clientes registrados.")
            else:
                for c in lista:
                    print(c)

        elif op == "3":
            print("\n--- Cambiar Estado de Mora ---")
            c_id = leer_entero("ID del cliente: ")
            cli = c_dao.buscar(c_id)
            if not cli:
                print("❌ Cliente no encontrado.")
                continue
            nuevo_estado = input(f"Cliente '{cli.nombre}' - ¿Tiene mora? (s/n): ").strip().lower() == 's'
            c_dao.actualizar_mora(c_id, nuevo_estado)
            print(f"✅ Estado de mora actualizado a: {'Con Mora' if nuevo_estado else 'Al día'}.")

        elif op == "4":
            break
        else:
            print("⚠️ Opción inválida. Intente de nuevo.")

def menu_contratos(conexion):
    c_dao = ContratoDAO(conexion)
    cli_dao = ClienteDAO(conexion)
    prop_dao = PropiedadDAO(conexion)

    while True:
        print("\n--- 📝 GESTIÓN DE CONTRATOS DE ARRIENDO ---")
        print("1. Firmar Nuevo Contrato de Arriendo")
        print("2. Listar y Ver Detalle de Contratos Registrados")
        print("3. Volver al Menú Principal")

        op = input("Seleccione una opción: ").strip()
        if op == "1":
            print("\n--- Firmar Contrato ---")
            c_id = leer_entero("ID del Cliente: ")
            cliente = cli_dao.buscar(c_id)
            if not cliente:
                print("❌ Cliente no encontrado. Registre al cliente primero.")
                continue

            p_id = leer_entero("ID de la Propiedad: ")
            propiedad = prop_dao.buscar(p_id)
            if not propiedad:
                print("❌ Propiedad no encontrada.")
                continue

            f_inicio = input("Fecha de Inicio (YYYY-MM-DD, ej: 2026-10-01): ").strip()
            f_fin = input("Fecha de Término (YYYY-MM-DD, ej: 2026-12-31): ").strip()

            contrato = ContratoArriendo(cliente, propiedad, f_inicio, f_fin)

            # Agregar líneas de detalle automáticas o personalizadas (Requisito P12)
            print(f"\nAgregando líneas de detalle para la propiedad ({propiedad.tipo()})...")
            # 1. Arriendo del mes
            contrato.agregar_linea_detalle(LineaDetalleContrato("Arriendo del Mes", propiedad.valor_uf))
            # 2. Gastos Comunes / Adicionales
            extra_uf = 0.5
            if hasattr(propiedad, 'gastos_jardin_uf'):
                extra_uf = propiedad.gastos_jardin_uf
            elif hasattr(propiedad, 'gastos_comunes_base_uf'):
                extra_uf = propiedad.gastos_comunes_base_uf
            elif hasattr(propiedad, 'recargo_comercial_uf'):
                extra_uf = propiedad.recargo_comercial_uf
            contrato.agregar_linea_detalle(LineaDetalleContrato("Gastos Adicionales / Mantenimiento", extra_uf))
            # 3. Garantía (1 mes de arriendo)
            contrato.agregar_linea_detalle(LineaDetalleContrato("Mes de Garantía", propiedad.valor_uf))

            # Intentar registrar el contrato (Valida las 2 Reglas de Negocio)
            try:
                c_dao.insertar(contrato)
                print(f"✅ ¡CONTRATO N° {contrato.id_contrato} REGISTRADO CON ÉXITO!")
                print(f"   Total en UF: {contrato.total_uf():.2f} UF")
            except ClienteConMoraException as cme:
                print(f"\n⛔ [REGLA DE NEGOCIO BLOQUEADA]: {cme}")
                print("   El sistema impidió la firma del contrato y sigue funcionando correctamente.")
            except PropiedadYaArrendadaException as pae:
                print(f"\n⛔ [REGLA DE NEGOCIO BLOQUEADA]: {pae}")
                print("   El sistema impidió la firma del contrato y sigue funcionando correctamente.")
            except Exception as ex:
                print(f"❌ Error al registrar contrato: {ex}")

        elif op == "2":
            print("\n--- Contratos Registrados y Detalle ---")
            lista = c_dao.listar()
            if not lista:
                print("No hay contratos registrados.")
            else:
                uf_dia = obtener_uf_actual()
                for c in lista:
                    print("\n" + "="*60)
                    print(c)
                    print(f"   Monto Total en Pesos CLP (UF hoy ${uf_dia:,.0f}): ${c.total_clp(uf_dia):,} CLP")
                    print("   --- Líneas de Detalle del Contrato ---")
                    for l in c.lineas_detalle:
                        print(f"     • {l.concepto}: {l.monto_uf:.2f} UF  (${l.subtotal_clp(uf_dia):,} CLP)")
                    print("="*60)

        elif op == "3":
            break
        else:
            print("⚠️ Opción inválida.")

def probar_calculo_polimorfico(conexion):
    print("\n--- 🧮 CÁLCULO DE ARRIENDO SEGÚN TIPO DE PROPIEDAD (POLIMORFISMO) ---")
    uf_dia = obtener_uf_actual()
    print(f"Valor UF del día utilizado: ${uf_dia:,.2f} CLP\n")
    
    casa = Casa("Av. Alemania 123", 120, 15.0, gastos_jardin_uf=1.0)
    dpto = Departamento("Calle Central 456, Depto 502", 60, 12.0, gastos_comunes_base_uf=0.5)
    ofi = Oficina("Av. Pedro de Valdivia 789, Of 301", 80, 20.0, recargo_comercial_uf=2.0)

    propiedades = [casa, dpto, ofi]

    for p in propiedades:
        arriendo_clp = p.calcular_arriendo(uf_dia)
        print(f"• {p.tipo()}: {p.direccion}")
        print(f"  Superficie: {p.metros_cuadrados} m² | Base: {p.valor_uf} UF")
        print(f"  Fórmula específica del subtipo ejecutada correctamente.")
        print(f"  👉 Valor Mensual Arriendo: ${arriendo_clp:,} CLP\n")

def main():
    conexion = crear_conexion()
    inicializar_base_datos(conexion)

    print("=================================================================")
    print("      SISTEMA DE GESTIÓN INMOBILIARIA TERRENOS DEL SUR           ")
    print("        Asignatura: POO Seguro (TI3V21) - Primavera 2026         ")
    print("=================================================================")

    while True:
        print("\n============== MENÚ PRINCIPAL ==============")
        print("1. Gestión de Propiedades (CRUD)")
        print("2. Gestión de Clientes (Validación RUT y Mora)")
        print("3. Registrar Contrato de Arriendo (Transacción con Detalles)")
        print("4. Probar Cálculo de Arriendo por Subtipo (Polimorfismo)")
        print("5. Consultar UF del Día (API Externa)")
        print("6. Salir")
        
        op = input("\nIngrese una opción: ").strip()

        if op == "1":
            menu_propiedades(conexion)
        elif op == "2":
            menu_clientes(conexion)
        elif op == "3":
            menu_contratos(conexion)
        elif op == "4":
            probar_calculo_polimorfico(conexion)
        elif op == "5":
            print("\n--- Consultar UF desde API mindicador.cl ---")
            uf = obtener_uf_actual()
            print(f"✅ Valor actual de la UF: ${uf:,.2f} CLP")
        elif op == "6":
            print("\n¡Gracias por utilizar el sistema de Inmobiliaria Terrenos del Sur!")
            conexion.close()
            sys.exit(0)
        else:
            print(f"\n⚠️ Opción '{op}' no válida. Por favor, seleccione un número del 1 al 6.")

if __name__ == "__main__":
    main()
