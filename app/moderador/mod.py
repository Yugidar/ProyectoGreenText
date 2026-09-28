from flask import Flask, request, jsonify
from vista_previa_resena import vista_previa_bp

app = Flask(__name__)
app.register_blueprint(vista_previa_bp)

# Palabras que nuestro bot "Janny" va a bloquear
PROHIBIDAS = ["spam", "estafa", "publicidad", "bot"]

@app.route('/moderar', methods=['POST'])
def moderar():
    data = request.json or {}
    texto = data.get("texto", "").lower()

    for palabra in PROHIBIDAS:
        if palabra in texto:
            return jsonify({"pasa": False, "motivo": f"Contiene la palabra prohibida: {palabra}"})

    return jsonify({"pasa": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # nosemgrep
