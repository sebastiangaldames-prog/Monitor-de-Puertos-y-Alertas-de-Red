import socket
from datetime import datetime
import threading
from queue import Queue

# Cola de tareas para manejar los puertos de forma concurrente
cola_puertos = Queue()
# Bloqueo para evitar que múltiples hilos escriban en la consola al mismo tiempo y se mezcle el texto
bloqueo_impresion = threading.Lock()

def escanear_puerto(ip_objetivo, puerto):
    """
    Intenta establecer una conexión TCP con un puerto específico.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8) # Reducimos ligeramente el timeout para mayor velocidad
        resultado = s.connect_ex((ip_objetivo, puerto))
        
        with bloqueo_impresion:
            if resultado == 0:
                print(f"  [ALERTA] Puerto {puerto} está ABIERTO 🟢")
        s.close()
    except socket.error:
        pass

def trabajador(ip_objetivo):
    """
    Función que ejecuta cada hilo: extrae puertos de la cola y los escanea
    hasta que la cola quede vacía.
    """
    while not cola_puertos.empty():
        puerto = cola_puertos.get()
        escanear_puerto(ip_objetivo, puerto)
        cola_puertos.task_done()

def main():
    print("-" * 50)
    print("  MONITOR DE PUERTOS Y ALERTAS DE RED (Versión Concurrente)")
    print("-" * 50)
    
    ip_objetivo = input("Introduce la IP o dominio a escanear (ej. 127.0.0.1): ").strip()
    if not ip_objetivo:
        ip_objetivo = "127.0.0.1"
        
    print(f"\n[+] Iniciando escaneo concurrente en: {ip_objetivo}")
    print(f"[+] Marca de tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Ampliaremos el rango de prueba para notar el poder de los hilos (puertos del 1 al 1024)
    # O puedes usar una lista de puertos clave si prefieres rapidez inicial.
    puertos_a_escanear = list(range(1, 1025))
    
    for puerto in puertos_a_escanear:
        cola_puertos.put(puerto)
        
    # Definimos cuántos hilos (trabajadores simultáneos) queremos lanzar
    cantidad_hilos = 50
    hilos = []
    
    print(f"[+] Desplegando {cantidad_hilos} hilos de escaneo simultáneo...\n")
    print("Puertos abiertos encontrados:")

    # Creamos e iniciamos los hilos
    for _ in range(cantidad_hilos):
        t = threading.Thread(target=trabajador, args=(ip_objetivo,))
        t.daemon = True
        t.start()
        hilos.append(t)
        
    # Esperamos a que todos los hilos terminen su trabajo
    cola_puertos.join()

    print("-" * 50)
    print("Escaneo concurrente finalizado con éxito.")

if __name__ == "__main__":
    main()