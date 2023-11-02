import mysql.connector

# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chat_vincent"
)
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS respuestas_personalizadas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pregunta VARCHAR(255) NOT NULL,
        respuesta TEXT NOT NULL
    )
""")

# Cerrar la conexión
cursor.close()
conn.close()
