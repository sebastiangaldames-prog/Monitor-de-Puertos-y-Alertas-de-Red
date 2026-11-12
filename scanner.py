import socket
from datetime import datetime
import threading
from queue import Queue
import json
import os

# Cola de tareas y mecanismos de sincronización
cola_puertos = Queue()
bloqueo_impresion = threading.Lock()

# Lista para almacenar los resultados estructurados de forma segura
resultados_escaneo = []
bloqueo_resultados = threading.Lock()

def escanear_puerto(ip_objetivo, puerto):
    """
    Intenta establecer una conexión TCP con un puerto específico y registra el hallazgo si está abierto.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        resultado = s.connect_ex((ip_objetivo, puerto))
        
        with bloqueo_impresion:
            if resultado == 0:
                print(f"  [ALERTA] Puerto {puerto} está ABIERTO 🟢")
                # Guardamos el hallazgo de forma segura protegiendo la lista con un Lock
                with bloqueo_resultados:
                    resultados_escaneo.append({
                        "puerto": puerto,
                        "estado": "ABIERTO",
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
        s.close()
    except socket.error:
        pass

def trabajador(ip_objetivo):
    """
    Función que ejecuta cada hilo: extrae puertos de la cola y los escanea.
    """
    while not cola_puertos.empty():
        puerto = cola_puertos.get()
        escanear_puerto(ip_objetivo, puerto)
        cola_puertos.task_done()

def guardar_reporte(ip_objetivo):
    """
    Crea una carpeta 'logs' (si no existe) y exporta los resultados en un archivo JSON único.
    """
    directorio_logs = "logs"
    if not os.path.exists(directorio_logs):
        os.makedirs(directorio_logs)
        
    # Creamos un nombre de archivo único basado en la IP y la marca de tiempo exacta
    timestamp_archivo = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = os.path.join(directorio_logs, f"reporte_{ip_objetivo.replace('.', '_')}_{timestamp_archivo}.json")
    
    reporte_data = {
        "objetivo": ip_objetivo,
        "fecha_escaneo": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_puertos_abiertos": len(resultados_escaneo),
        "puertos_abiertos": sorted(resultados_escaneo, key=lambda x: x["puerto"])
    }
    
    # Escribimos el archivo JSON formateado con indentación limpia
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(reporte_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n[+] Reporte de auditoría guardado exitosamente en: {nombre_archivo}")

def main():
    print("-" * 50)
    print("  MONITOR DE PUERTOS Y ALERTAS DE RED (Con Sistema de Logs)")
    print("-" * 50)
    
    ip_objetivo = input("Introduce la IP o dominio a escanear (ej. 127.0.0.1): ").strip()
    if not ip_objetivo:
        ip_objetivo = "127.0.0.1"
        
    print(f"\n[+] Iniciando escaneo concurrente en: {ip_objetivo}")
    print(f"[+] Marca de tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    puertos_a_escanear = list(range(1, 1025))
    
    for puerto in puertos_a_escanear:
        cola_puertos.put(puerto)
        
    cantidad_hilos = 50
    hilos = []
    
    print(f"[+] Desplegando {cantidad_hilos} hilos de escaneo simultáneo...\n")
    print("Puertos abiertos encontrados:")

    for _ in range(cantidad_hilos):
        t = threading.Thread(target=trabajador, args=(ip_objetivo,))
        t.daemon = True
        t.start()
        hilos.append(t)
        
    cola_puertos.join()

    # Ejecutamos la función de guardado de logs al finalizar el escaneo
    guardar_reporte(ip_objetivo)

    print("-" * 50)
    print("Escaneo finalizado y registrado con éxito.")

if __name__ == "__main__":
    main()