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
        result = cursor.fetchone()

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
    ("Quiero practicar español", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica?"),
    ("quiero practicar español", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica?"),
    ("Quiero practicar Espanol", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica? Recuerda usar la letra 'ñ'"),
    ("quiero practicar espanol", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica? Recuerda usar la letra 'ñ'"),
    ("Quiero practicar español por favor", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica?"),
    ("Quisiera practicar español", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica?"),
    ("Me gustaría practicar español", "¡Por supuesto! ¿En qué puedo ayudarte con tu práctica?"),

    ("¿Cómo puedo practicar español?", "Existen varias formas de practicar, ¿tienes alguna preferencia?"),
    ("Como puedo practicar español", "Existen varias formas de practicar, ¿tienes alguna preferencia?"),
    ("¿Cómo puedo practicar Espanol?", "Existen varias formas de practicar, ¿tienes alguna preferencia? Recuerda usar la letra 'ñ'"),
    ("¿como puedo practicar español?", "Existen varias formas de practicar, ¿tienes alguna preferencia? Recuerda usar la letra 'ñ'"),
    ("Cómo puedo practicar español eficientemente", "Existen varias formas de practicar, ¿tienes alguna preferencia?"),
    ("Cómo practicar español de manera efectiva", "Existen varias formas de practicar, ¿tienes alguna preferencia?"),
    ("Dime cómo puedo practicar español", "Existen varias formas de practicar, ¿tienes alguna preferencia?"),

    ("Quiero mejorar mi español", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte?"),
    ("quiero mejorar mi español", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte?"),
    ("Quiero mejorar mi Espanol", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte? Recuerda usar la letra 'ñ'"),
    ("quiero mejorar mi espanol", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte? Recuerda usar la letra 'ñ'"),
    ("Quiero mejorar mi español hablado", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte?"),
    ("Me gustaría perfeccionar mi español", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte?"),
    ("Necesito mejorar mi español", "Excelente, la práctica te ayudará a mejorar. ¿Cómo puedo asistirte?"),

    ("¿Alguna sugerencia para practicar español?", "Claro, ¿tienes preferencia por algún método en particular?"),
    ("Alguna sugerencia para practicar español", "Claro, ¿tienes preferencia por algún método en particular?"),
    ("¿Alguna sugerencia para practicar Espanol?", "Claro, ¿tienes preferencia por algún método en particular? Recuerda usar la letra 'ñ'"),
    ("alguna sugerencia para practicar espanol", "Claro, ¿tienes preferencia por algún método en particular? Recuerda usar la letra 'ñ'"),
    ("Tienes alguna idea para practicar español?", "Claro, ¿tienes preferencia por algún método en particular?"),
    ("Puedes sugerirme cómo practicar español", "Claro, ¿tienes preferencia por algún método en particular?"),
    ("¿Tienes recomendaciones para practicar español?", "Claro, ¿tienes preferencia por algún método en particular?"),

    ("¿Dónde practicar español?", "Puedes intentar practicar en grupos de conversación o con tutores en línea"),
    ("Donde practicar español", "Puedes intentar practicar en grupos de conversación o con tutores en línea"),
    ("¿Dónde practicar Espanol?", "Puedes intentar practicar en grupos de conversación o con tutores en línea. Recuerda usar la letra 'ñ'"),
    ("donde practicar espanol", "Puedes intentar practicar en grupos de conversación o con tutores en línea. Recuerda usar la letra 'ñ'"),
    ("Dónde puedo practicar español en línea", "Puedes intentar practicar en grupos de conversación o con tutores en línea"),
    ("Dónde practicar español de forma efectiva", "Puedes intentar practicar en grupos de conversación o con tutores en línea"),
    ("Me podrías decir dónde practicar español", "Puedes intentar practicar en grupos de conversación o con tutores en línea"),

    ("¿Cuál es la mejor manera de practicar español?", "La mejor manera puede variar según tus preferencias y habilidades"),
    ("Cual es la mejor manera de practicar español", "La mejor manera puede variar según tus preferencias y habilidades"),
    ("¿Cuál es la mejor manera de practicar Espanol?", "La mejor manera puede variar según tus preferencias y habilidades. Recuerda usar la letra 'ñ'"),
    ("cuál es la mejor manera de practicar espanol", "La mejor manera puede variar según tus preferencias y habilidades. Recuerda usar la letra 'ñ'"),
    ("Qué método recomiendas para practicar español?", "La mejor manera puede variar según tus preferencias y habilidades"),
    ("Podrías sugerirme la forma más efectiva de practicar español", "La mejor manera puede variar según tus preferencias y habilidades"),
    ("Cuéntame la mejor forma de practicar español", "La mejor manera puede variar según tus preferencias y habilidades"),

    ("¿Hay ejercicios para practicar español?", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica"),
    ("Hay ejercicios para practicar español", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica"),
    ("¿Hay ejercicios para practicar Espanol?", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica. Recuerda usar la letra 'ñ'"),
    ("hay ejercicios para practicar espanol", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica. Recuerda usar la letra 'ñ'"),
    ("Conoces algún ejercicio para practicar español", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica"),
    ("Puedes recomendarme algunos ejercicios de práctica en español", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica"),
    ("¿Tienes ejercicios específicos para practicar español?", "Sí, hay varios ejercicios disponibles en línea y en libros de práctica"),

    ("¿Cómo mejorar mi comprensión oral en español?", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones"),
    ("Como mejorar mi comprensión oral en español", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones"),
    ("¿Cómo mejorar mi comprension oral en Espanol?", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones. Recuerda usar la letra 'ñ'"),
    ("cómo mejorar mi comprension oral en espanol", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones. Recuerda usar la letra 'ñ'"),
    ("Cómo puedo entender mejor el español hablado", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones"),
    ("Qué hago para mejorar mi comprensión auditiva en español", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones"),
    ("Podrías ayudarme a mejorar mi comprensión oral en español", "Puedes intentar escuchar podcasts, ver videos y practicar conversaciones"),

    ("¿Algún consejo para hablar español con fluidez?", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),
    ("Algún consejo para hablar español con fluidez", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),
    ("¿Algun consejo para hablar español con fluidez?", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),
    ("algún consejo para hablar espanol con fluidez", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez. Recuerda usar la letra 'ñ'"),
    ("Cómo puedo hablar español con más fluidez", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),
    ("Consejos para mejorar la fluidez al hablar español", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),
    ("Podrías darme consejos para hablar español fluidamente", "La práctica constante y la exposición al idioma te ayudarán a mejorar tu fluidez"),

    ("¿Es útil hablar con hablantes nativos de español?", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español"),
    ("Es útil hablar con hablantes nativos de español", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español"),
    ("¿Es util hablar con hablantes nativos de Espanol?", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español. Recuerda usar la letra 'ñ'"),
    ("es util hablar con hablantes nativos de espanol", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español. Recuerda usar la letra 'ñ'"),
    ("Hablar con nativos de español, ¿es beneficioso?", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español"),
    ("Cómo puedo aprovechar hablar con hispanohablantes nativos", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español"),
    ("Me recomiendas hablar con hablantes nativos de español", "Definitivamente, conversar con hablantes nativos puede mejorar tu habilidad en español")
]

    conn = database.establish_connection()

    await insert_data(conn, datos_seeders)

    database.close_connection(conn, None)

if __name__ == "__main__":
    asyncio.run(main())