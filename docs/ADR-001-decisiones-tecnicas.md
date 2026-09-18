# ADR 001: Arquitectura de Almacenamiento Seguro en la Nube

## Contexto
El foro Greentext requiere almacenar imágenes subidas por los usuarios y texto, desplegando la aplicación en AWS. La rúbrica y las mejores prácticas de ciberseguridad prohíben la exposición pública de buckets y exigen un manejo seguro de credenciales.

## Decisiones Técnicas Adoptadas

1. **Uso de AWS S3 Privado con URLs Prefirmadas (Presigned URLs):**
   - **Decisión:** Se bloqueó completamente el acceso público al bucket de S3. En su lugar, el backend de Flask utiliza la librería `boto3` para generar URLs temporales (caducidad de 3600 segundos) cada vez que el frontend solicita cargar una imagen.
   - **Justificación:** Previene el escaneo de directorios y el robo masivo de datos (data exfiltration), cumpliendo con el control de acceso estricto.

2. **Separación de Capas (EC2 + RDS):**
   - **Decisión:** La base de datos no corre en el mismo contenedor que la aplicación web. Se delegó a AWS RDS (MySQL).
   - **Justificación:** Aísla el procesamiento de la API del almacenamiento de datos relacional, facilitando respaldos automáticos y reduciendo la superficie de ataque del servidor web.

3. **Orquestación con Docker Compose:**
   - **Decisión:** Se empaquetó la aplicación usando Dockerfiles y se orquestó con `docker-compose.yml`.
   - **Justificación:** Asegura la reproducibilidad del entorno de desarrollo a producción y evita conflictos de dependencias de Python (como `boto3`, `flask`, `pymysql`).
