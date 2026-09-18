# Foro Greentext - Avance 2 (Arquitectura Segura en AWS)

## Descripción del Proyecto
Este proyecto es una aplicación web estilo foro anónimo (Greentext), desarrollada con Flask (Python) y desplegada en una arquitectura de nube segura utilizando contenedores Docker. 

## Arquitectura y Seguridad
La infraestructura está alojada en AWS y fue diseñada bajo el principio de "mínimo privilegio":
- **Backend:** Contenedor Docker ejecutando Flask en una instancia EC2.
- **Base de Datos:** AWS RDS (MySQL) para almacenamiento persistente y estructurado.
- **Almacenamiento de Imágenes:** AWS S3 configurado como **Privado**. El acceso a las imágenes se realiza estrictamente a través de *Presigned URLs* generadas dinámicamente por la API usando Boto3, garantizando que el bucket nunca esté expuesto al internet público.
- **DevSecOps:** Implementación de un pipeline de seguridad local (`ejecutar.sh`) que escanea exposición de secretos y credenciales antes del despliegue.

## Instrucciones de Ejecución
Para levantar este proyecto en la instancia EC2:
1. Clonar el repositorio.
2. Configurar las credenciales seguras en un archivo `.env` (ignorado en git).
3. Ejecutar el comando de construcción:
   `docker compose up --build -d`
