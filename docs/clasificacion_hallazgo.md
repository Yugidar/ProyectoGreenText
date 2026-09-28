# Clasificación del Hallazgo - Fase QA

**Herramienta que detectó el fallo:** Semgrep
**Archivo afectado:** app/moderador/vista_previa_resena.py
**Regla vulnerada:** python.flask.security.audit.render-template-string.render-template-string

**1. Tipo de Vulnerabilidad:**
Inyección de Plantillas del Lado del Servidor SSTI y Cross-Site Scripting XSS.

**2. Severidad:**
CRÍTICA. Permite a un atacante inyectar código malicioso a través del campo de la reseña. Al usar el filtro `| safe` en la plantilla, el motor de Jinja2 ejecuta el texto sin sanitizar, lo que podría derivar en el robo de sesiones del moderador o ejecución de comandos remotos en el servidor.

**3. Estrategia de Remediación:**
Se eliminó el uso de la función `render_template_string` y el filtro `| safe`. En su lugar, se implementó la función `escape` de la librería `markupsafe` nativa de Flask. Esto garantiza que el texto original introducido por el usuario se convierta en texto plano inofensivo antes de aplicar el formato de negritas y saltos de línea.
