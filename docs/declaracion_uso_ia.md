# Declaracion de uso de Inteligencia Artificial

En este Avance 2 usé bastante la IA para destrabarme con problemas de infraestructura, git y la documentación, además de resolver errores de código. Básicamente la usé para esto:

**1. Problemas con Git y Linux**
Me apoyé mucho en la IA cuando me salían errores en la terminal de AWS y me quedaba atorado. Me guio paso a paso para configurar mi token de acceso de GitHub cuando la terminal no me dejaba iniciar sesión con mi contraseña normal. También me ayudó a arreglar un problema de ramas divergentes al hacer pull que no sabía cómo fusionar. Además me dio los comandos exactos de git para limpiar mi repositorio porque subí por error carpetas ocultas de Linux como la de ssh y el historial de bash al no configurar bien el archivo gitignore desde el principio, lo cual era un riesgo de seguridad bastante grave.

**2. Hacer la documentacion y el diagrama**
Le fui pasando el contexto de lo que ya tenía levantado en AWS con S3, RDS y Flask. Le pedí que me ayudara a redactar y darle el formato correcto a los archivos Markdown como el README y el documento de decisiones técnicas. También le pedí que me generara el código en formato Mermaid para el diagrama de arquitectura, así solo tuve que pegar ese código en una página web y descargar la imagen en lugar de dibujarlo desde cero.

**3. Errores de Docker y Python**
Me ayudó a encontrar un error de sintaxis y unas variables mal declaradas en mi código de Flask cuando estaba intentando integrar Boto3 para generar las urls de las imágenes. También me explicó un problema que tenía con Docker porque yo reiniciaba mi contenedor y no se veían mis cambios en el servidor. Resulta que me faltaba agregar la instrucción de build al comando de docker compose para que realmente construyera la imagen con el código nuevo.

**4. Pulir mis entregables y el pipeline**
La usé para rebotar ideas sobre cómo explicar mejor la parte de seguridad. Me ayudó a organizar mis respuestas en el documento final para explicar de forma clara qué riesgos específicos estaba cubriendo mi pipeline, como los escaneos de código estático y vulnerabilidades, y a darle forma a la tabla de justificación de esas herramientas.

Yo levanté la infraestructura, conecté los servicios en la nube y configuré la seguridad, pero usé la IA como un apoyo para resolver los problemas de configuración en la terminal, sacar la entrega a tiempo y redactar la documentación técnica de una forma presentable.
