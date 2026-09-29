import os
import uuid
import requests
import pymysql
import boto3
from flask import Flask, request, jsonify, render_template, redirect
from markupsafe import escape

app = Flask(__name__)

# Configuracion AWS
S3_BUCKET = os.environ.get("S3_BUCKET")
s3_client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
)

def obtener_conexion():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

def inicializar_bd():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    texto TEXT NOT NULL,
                    imagen_url VARCHAR(255)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comentarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    post_id INT NOT NULL,
                    texto TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
                )
            """)
        conexion.commit()
        conexion.close()
    except Exception as e:
        print("Error conectando a BD al iniciar:", e)

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({"estado": "ok"})

@app.route('/post', methods=['POST'])
def crear_post():
    texto_original = request.form.get("texto", "")
    imagen = request.files.get("imagen")

    if not texto_original:
        return jsonify({"error": "El texto es obligatorio"}), 400

    # 1. Consultar al servicio moderador 
    try:
        resp_mod = requests.post("http://moderador:5001/moderar", json={"texto": texto_original}, timeout=5)  # nosemgrep
        resultado = resp_mod.json()
        if not resultado.get("pasa"):
            return jsonify({"error": "Post rechazado por moderacion", "detalle": resultado.get("motivo")}), 403
    except Exception as e:
        return jsonify({"error": "El servicio de moderacion no responde"}), 500

    # 2. Aplicar formato Greentext (> ser yo)
    lineas = texto_original.split('\n')
    texto_greentext = '\n'.join([f"> {linea.strip()}" if linea.strip() else "" for linea in lineas])

    # 3. Subir imagen a S3 (si hay)
    imagen_url = None
    if imagen and imagen.filename:
        nombre_archivo = f"{uuid.uuid4().hex}_{imagen.filename}"
        try:
            s3_client.upload_fileobj(imagen, S3_BUCKET, nombre_archivo)
            imagen_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{nombre_archivo}"  # nosemgrep
        except Exception as e:
            return jsonify({"error": f"Fallo al subir a S3: {str(e)}"}), 500

    # 4. Guardar en MySQL (RDS)
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO posts (texto, imagen_url) VALUES (%s, %s)", (texto_greentext, imagen_url))
        conexion.commit()
        conexion.close()
    except Exception as e:
        return jsonify({"error": f"Fallo al guardar en base de datos: {str(e)}"}), 500

    return jsonify({"mensaje": "Post creado exitosamente con estilo greentext", "texto": texto_greentext, "imagen_url": imagen_url})

@app.route('/posts', methods=['GET'])
def listar_posts():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM posts ORDER BY id DESC")
            posts = cursor.fetchall()
            
            bucket_name = os.environ.get('S3_BUCKET')
            
            for post in posts:
                # Buscar comentarios de cada post
                cursor.execute("SELECT texto FROM comentarios WHERE post_id = %s ORDER BY fecha ASC", (post['id'],))
                post['comentarios'] = cursor.fetchall()
                
                # Generar URL segura de S3 si hay imagen
                if post.get('imagen_url'):
                    nombre_archivo = post['imagen_url'].split('/')[-1] 
                    url_segura = s3_client.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': bucket_name, 'Key': nombre_archivo},
                        ExpiresIn=3600
                    )
                    post['imagen_url'] = url_segura
    finally:
        conexion.close()
            
    return jsonify(posts)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/comentar/<int:post_id>', methods=['POST'])
def comentar(post_id):
    texto = request.form.get('comentario')
    if not texto:
        return redirect('/')
        
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        texto_seguro = str(escape(texto))
        cursor.execute(
            "INSERT INTO comentarios (post_id, texto) VALUES (%s, %s)",
            (post_id, texto_seguro) 
        )
    conexion.commit()
    conexion.close()
    return redirect('/')

@app.route('/upvote/<int:post_id>', methods=['POST'])
def upvote(post_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE posts SET upvotes = COALESCE(upvotes, 0) + 1 WHERE id = %s", (post_id,))
    conexion.commit()
    conexion.close()
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    inicializar_bd()
    app.run(host='0.0.0.0', port=5000)  # nosemgrep
