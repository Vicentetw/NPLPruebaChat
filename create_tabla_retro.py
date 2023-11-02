import mysql.connector

# Establecer la conexión con la base de datos
conn = mysql.connector.connect(
 host="localhost",
        user="root",
        password="",
        database="chat_vincent"
)
cursor = conn.cursor()

# Código para crear la tabla 'retroalimentacion'
create_table_query = """
CREATE TABLE retroalimentacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT,
    respuesta_generada TEXT,
    util BOOLEAN,
    respuesta_alternativa TEXT
)
"""
cursor.execute(create_table_query)

conn.commit()

# Cerrar la conexión con la base de datos
conn.close()
