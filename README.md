# 🛡️ Network Port Monitor & Logger

Herramienta desarrollada en Python orientada a redes y ciberseguridad, diseñada para realizar escaneos de puertos TCP de forma concurrente, detectar servicios activos y generar reportes de auditoría automatizados con marcas de tiempo.

## 🚀 Características Principales
* **Escaneo Concurrente con Hilos (`Threading`):** Implementa subprocesos y colas (`Queue`) para analizar rangos masivos de puertos en segundos.
* **Manejo Seguro de Concurrencia:** Uso de bloqueos (`Lock`) para evitar condiciones de carrera en la consola y en el almacenamiento de datos.
* **Sistema de Alertas y Trazabilidad:** Detección en tiempo real de puertos abiertos y exportación de reportes detallados en formato **JSON**.
* **Control de Versiones Profesional:** Desarrollado bajo un flujo estricto de Git con commits estructurados y bitácora técnica.

---

## 🛠️ Tecnologías y Librerías Utilizadas
* **Python 3.x**
* `socket` (Gestión de conexiones de red a nivel de transporte TCP)
* `threading` y `queue` (Concurrencia y sincronización de hilos)
* `json` y `os` (Generación estructurada de logs y manejo de directorios)
* **Git & GitHub** (Control de versiones)

---

## ⚙️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/sebastiangaldames-prog/Monitor-de-Puertos-y-Alertas-de-Red.git](https://github.com/sebastiangaldames-prog/Monitor-de-Puertos-y-Alertas-de-Red.git)
   cd Monitor-de-Puertos-y-Alertas-de-Red
