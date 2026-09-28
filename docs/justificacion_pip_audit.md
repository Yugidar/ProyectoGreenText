# Justificación de Excepciones en pip-audit

Durante la ejecución del escáner de dependencias en el Avance 2, `pip-audit` marcó paquetes ignorados/no encontrados.

**Justificación Técnica:**
Las advertencias señalaban paquetes como `awscli`, `cloud-init`, `selinux`, `rpm` y `ec2-hibinit-agent`. Estas no son dependencias de nuestra aplicación web (Greentext), sino utilidades nativas del sistema operativo huésped (Amazon Linux) y agentes de AWS preinstalados en la instancia EC2. Dado que son paquetes del sistema y no están alojados en el repositorio público PyPI, `pip-audit` los omite arrojando la advertencia "Dependency not found on PyPI and could not be audited". 

**Acción Correctiva:**
Para la Entrega Final, el pipeline fue reconfigurado para auditar exclusivamente el archivo `requirements.txt` del proyecto (`pip-audit -r app/requirements.txt`), aislando correctamente las dependencias de la aplicación (Flask, Boto3) de los paquetes del sistema operativo.
