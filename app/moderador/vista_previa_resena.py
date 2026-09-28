from flask import Blueprint, request
from markupsafe import escape

vista_previa_bp = Blueprint("vista_previa", __name__)

def formatear_texto_enriquecido(texto_original):
    texto_seguro = str(escape(texto_original))
    
    formateado = texto_seguro.replace("\n", "<br>")
    while "**" in formateado:
        formateado = formateado.replace("**", "<b>", 1)
        formateado = formateado.replace("**", "</b>", 1)
    return formateado

@vista_previa_bp.route("/moderacion/resenas/<int:resena_id>/vista-previa", methods=["POST"])
def vista_previa_resena(resena_id):
    contenido_original = request.form.get("contenido", "")
    contenido_formateado = formatear_texto_enriquecido(contenido_original)
    id_seguro = escape(resena_id)

    html_seguro = f"""
    <div class="resena-preview">
      <h3>Vista previa de la resena #{id_seguro}</h3>
      <div class="contenido">{contenido_formateado}</div>
    </div>
    """
    return html_seguro
