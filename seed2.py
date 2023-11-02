import asyncio
import aiomysql

async def insert_data(pool, datos_seeders):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            for dato in datos_seeders:
                pregunta = dato[0]
                respuesta = dato[1]
                select_query = "SELECT * FROM respuestas_personalizadas WHERE pregunta = %s"
                await cursor.execute(select_query, (pregunta,))
                result = await cursor.fetchone()

                if result:
                    print(f"La pregunta '{pregunta}' ya existe en la base de datos. Se omitirá.")
                else:
                    insert_query = "INSERT INTO respuestas_personalizadas (pregunta, respuesta) VALUES (%s, %s)"
                    try:
                        await cursor.execute(insert_query, dato)
                        print(f"Se ha insertado exitosamente: {dato}")
                    except aiomysql.Error as err:
                        print(f"Error al insertar: {err}")

async def main():
    datos_seeders = [
          ("hola", "¡Hola! ¿Cómo estás?"),
    ("hola de nuevo", "¡Hola! ¿Qué tal tu día?"),
    ("hey", "¡Hey! ¿Cómo va todo?"),
    ("saludos", "¡Saludos! ¿Cómo ha ido tu día?"),
    ("buenas", "¡Buenas! ¿Cómo te encuentras?"),
    ("bien", "¡Qué bueno! Me gusta escuchar eso"),
    ("muy bien", "¡Genial! ¿Qué te trae por aquí hoy?"),
    ("excelente", "¡Maravilloso! ¿En qué puedo ayudarte?"),
    ("¿Cómo te llamas?", "Me llamo VincentBot, encantado de conocerte"),
    ("Cómo te llamas?", "Me llamo VincentBot, encantado de conocerte"),
    ("como te llamas?", "Me llamo VincentBot, encantado de conocerte, recuerda poner tilde en -cómo- cuando realizas una pregunta"),
    ("te llamas?", "Me llamo VincentBoot, encantado de conocerte"),
    ("cual es tu nombre?", "Mi nombre es VincentBot, ¿y el tuyo?"),
    ("tienes un nombre?", "Sí, me llamo VincentBot. ¿Cómo puedo ayudarte hoy?"),
    ("tienes razón", "Es cierto"),
    ("tienes razon", "Es cierto, recuerda que razón lleva tilde"),
    ("estoy de acuerdo", "Totalmente de acuerdo contigo"),
    ("correcto", "Así es, has entendido perfectamente"),
    ("buenos días", "Hey, buenos días!"),
    ("buenos dias", "Hey, buenos días!. recuerda poner tilde en -días-"),
    ("qué tal tu mañana", "¡Buenos días! Mi mañana está yendo bien, ¿y la tuya?"),
    ("cómo ha amanecido", "¡Buenos días! El día ha amanecido radiante, ¿verdad?"),
    ("que tengas lindo día", "Eres muy amable, igualmente para tí"),
    ("espero que tengas un gran día", "¡Gracias! Igualmente para ti, que tengas un día maravilloso"),
    ("qué haces?", "Chateo contigo, haha"),
    ("que haces?", "Chateo contigo, haha, recuerda que -qué- lleva tilde cuando estás realizando una pregunta"),
    ("qué estás haciendo?", "Estoy aquí contigo, ¿en qué puedo ayudarte?"),
    ("cómo estas?", "Bien, gracias por preguntar, recuerda que -cómo- y -estás- lleva tilde cuando estás realizando una pregunta"),
    ("como estás?", "Bien, gracias por preguntar, recuerda que -estás- lleva tilde cuando estás realizando una pregunta"),
    ("cómo te sientes hoy?", "Hoy me siento bien, listo para ayudarte en lo que necesites"),
    ("cómo te encuentras hoy?", "Hoy estoy genial, listo para conversar contigo"),
    ("y tú", "¡Genial! Gracias por preguntar"),
    ("y tu", "¡Genail! Gracias por preguntar. recuerda que -tú- lleva tilde"),
    ("¿Cómo has estado?", "He estado bien, gracias. ¿Y tú?"),
    ("cómo te ha ido recientemente", "Me ha ido bien, gracias por preguntar. ¿Y a ti?"),
    ("adios", "¡Hasta luego! Que tengas un buen día"),
    ("hasta luego", "¡Adiós! Espero verte pronto de nuevo"),
    ("nos vemos", "¡Hasta la próxima! Cuídate mucho"),
    ("gracias", "¡De nada! Estoy aquí para ayudarte."),
    ("muchas gracias", "¡Con gusto! No dudes en pedir ayuda cuando lo necesites"),
    ("triste", "Lamento escuchar eso. ¿Hay algo en lo que pueda ayudarte?"),
    ("feliz", "Me alegra escuchar eso. ¿En qué puedo ayudarte hoy?"),
    ("me siento triste", "Comprendo, ¿quieres hablar al respecto?"),
    ("estoy muy contento", "¡Eso es genial! ¿Hay algo en lo que pueda contribuir a tu felicidad?"),
    ("vincent", "¡Vincent! es mi amigo genial"),
    ("quien es vincent", "¡Vincent! es un tipo y amigo genial"),
    ("quién es tori", "¡Tori! es mi amiga genial de Brasil"),
    ("quien eres tu", "Soy VincentBot, un asistente virtual aquí para ayudarte"),
    ("adios", "¡Hasta luego! Que tengas un buen día"),
    ("nos vemos después", "¡Hasta la próxima! Que tengas un día maravilloso"),
    ("(.*)", "Aún no puedo contestar eso. Pero por favor, continúa, me encanta charlar contigo.")
    ]

    pool = await aiomysql.create_pool(host="localhost", user="root", password="", db="chat_vincent")

    await insert_data(pool, datos_seeders)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
