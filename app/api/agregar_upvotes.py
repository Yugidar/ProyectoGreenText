import pymysql
import os

conexion = pymysql.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
)
with conexion.cursor() as cursor:
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN upvotes INT DEFAULT 0;")
    except Exception as e:
        pass
conexion.commit()
conexion.close()
print("¡Columna de upvotes lista!")
