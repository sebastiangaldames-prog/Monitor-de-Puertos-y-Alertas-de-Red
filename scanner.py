import socket
from datetime import datetime

def escanear_puerto(ip_objetivo, puerto):
    """
    Función que intenta establecer una conexión TCP con un puerto específico.
    Retorna True si está abierto, False si está cerrado.
    """
    try:
        # Creamos un socket IPv4 (AF_INET) y TCP (SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Configuramos un tiempo límite de espera (timeout) de 1 segundo 
        # para que el script no se quede pegado si el puerto no responde.
        s.settimeout(1.0)
        
        # Intentamos conectar al objetivo y puerto
        resultado = s.connect_ex((ip_objetivo, puerto))
        
        # connect_ex retorna 0 si la conexión fue exitosa (puerto abierto)
        if resultado == 0:
            s.close()
            return True
        else:
            s.close()
            return False
            
    except socket.error:
        # Si ocurre un error de red general, asumimos puerto cerrado/inaccesible
        return False

def main():
    print("-" * 50)
    print("  MONITOR DE PUERTOS Y ALERTAS DE RED (Versión Base)")
    print("-" * 50)
    
    # Definimos el objetivo (por defecto usaremos localhost para pruebas seguras)
    ip_objetivo = input("Introduce la IP o dominio a escanear (ej. 127.0.0.1): ").strip()
    if not ip_objetivo:
        ip_objetivo = "127.0.0.1" # Si no escribe nada, escanea su propio equipo
        
    print(f"\n[+] Iniciando escaneo en el objetivo: {ip_objetivo}")
    print(f"[+] Marca de tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Escanearemos un rango común de puertos prioritarios para probar
    # (por ejemplo: 21 (FTP), 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL))
    puertos_comunes = [21, 22, 23, 53, 80, 443, 3306, 8080]
    
    print("Puertos abiertos encontrados:")
    abiertos_encontrados = 0
    
    for puerto in puertos_comunes:
        if escanear_puerto(ip_objetivo, puerto):
            print(f"  [ALERTA] Puerto {puerto} está ABIERTO 🟢")
            abiertos_encontrados += 1
        else:
            print(f"  [Info] El puerto {puerto} está cerrado o filtrado.")

    print("-" * 50)
    print(f"Escaneo finalizado. Puertos abiertos detectados: {abiertos_encontrados}")

if __name__ == "__main__":
    main()