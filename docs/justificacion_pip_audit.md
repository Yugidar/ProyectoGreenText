# Justificación de Excepciones en pip-audit

Durante la ejecución del escáner de dependencias en el Avance 2, `pip-audit` marcó paquetes ignorados/no encontrados.

**Justificación Técnica:**
Las advertencias señalaban paquetes como `awscli`, `cloud-init`, `selinux`, `rpm` y `ec2-hibinit-agent`. Estas no son dependencias de nuestra aplicación web (Greentext), sino utilidades nativas del sistema operativo huésped (Amazon Linux) y agentes de AWS preinstalados en la instancia EC2. Dado que son paquetes del sistema y no están alojados en el repositorio público PyPI, `pip-audit` los omite arrojando la advertencia "Dependency not found on PyPI and could not be audited". 

**Acción Correctiva:**
Para la Entrega Final, el pipeline fue reconfigurado para auditar exclusivamente el archivo `requirements.txt` del proyecto (`pip-audit -r app/requirements.txt`), aislando correctamente las dependencias de la aplicación (Flask, Boto3) de los paquetes del sistema operativo.

**Actualización (Fase de Producción): Aceptación de Riesgo por SO**
Durante el escaneo estricto, se detectaron 3 vulnerabilidades (PYSEC-2026-141 en urllib3, PYSEC-2026-2275 en requests, PYSEC-2026-2132 en click) cuyos parches requieren obligatoriamente Python >= 3.10. Dado que la AMI de Amazon Linux en la instancia EC2 opera con una versión anterior (3.9) y una actualización mayor del SO rompería dependencias de AWS, se procedió a actualizar las librerías a la versión máxima soportada (ej. urllib3==2.6.3, remediando 4 de 5 CVEs). Las 3 excepciones restantes se añadieron al pipeline como riesgo aceptado documentado.

**Actualización: Aceptación de Riesgo por Conflicto con boto3**
Al intentar actualizar `urllib3` a una versión sin vulnerabilidades (2.x), se detectó un conflicto de dependencias crítico: `boto3` (esencial para la conexión con AWS S3) no es compatible y rompe la instalación (`ResolutionImpossible`). Por lo tanto, se decidió por arquitectura permitir que `boto3` instale la versión de `urllib3` compatible (1.26.x) y añadir las 5 vulnerabilidades derivadas de esto (PYSEC-2026-141, 1999, 1998, 1994, 1996) a la lista de excepciones formales del pipeline, documentando el riesgo aceptado por limitación de dependencias del proveedor (AWS).
