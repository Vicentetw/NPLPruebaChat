import asyncio
import sys
sys.path.insert(0, './db')  # Agrega la ruta de la carpeta 'db' al sys.path
import db.database as database

async def insert_data(conn, datos_seeders):
    cursor = conn.cursor()
    for dato in datos_seeders:
        pregunta = dato[0]
        respuesta = dato[1]
        select_query = "SELECT * FROM respuestas_personalizadas WHERE pregunta = %s"
        cursor.execute(select_query, (pregunta,))
        result = cursor.fetchall()

        if result:
            print(f"La pregunta '{pregunta}' ya existe en la base de datos. Se omitirá.")
        else:
            insert_query = "INSERT INTO respuestas_personalizadas (pregunta, respuesta) VALUES (%s, %s)"
            try:
                cursor.execute(insert_query, dato)
                print(f"Se ha insertado exitosamente: {dato}")
            except mysql.connector.Error as err:
                print(f"Error al insertar: {err}")

async def main():
    datos_seeders = [
    ("¿Cómo estás?", "Bien, gracias por preguntar"),
    
]

    conn = database.establish_connection()

    await insert_data(conn, datos_seeders)

    database.close_connection(conn, None)

if __name__ == "__main__":
    asyncio.run(main())
