# Tabla de Decisiones del Pipeline DevSecOps

| Control de Seguridad / Herramienta | Etapa del Pipeline | Justificación y Configuración |
| :--- | :--- | :--- |
| **Escaneo de Secretos (Gitleaks / Regex)** | Pre-Build | Evita la exposición accidental de credenciales (ej. `AWS_ACCESS_KEY_ID`). Se validó su funcionamiento inyectando un `secreto_falso.txt`, garantizando el bloqueo de la ejecución (Corrida Roja). |
| **Análisis Estático (Semgrep)** | Código Fuente (SAST) | Revisa el código Python (Flask) en busca de malas prácticas, errores de sintaxis o vulnerabilidades antes de permitir la construcción de la imagen. |
| **Escaneo de Contenedores (Trivy)** | Imagen Docker | Analiza las capas del contenedor para detectar vulnerabilidades (CVEs) conocidas en el sistema operativo base antes de autorizar el despliegue a la instancia EC2. |
| **Generación de SBOM (CycloneDX)** | Release / Documentación | Crea un inventario transparente y estructurado de todas las dependencias (`sbom.json`) cumpliendo con las políticas de auditoría del proyecto. |
