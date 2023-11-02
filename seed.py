import mysql.connector

# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chat_vincent"
)
cursor = conn.cursor()

# Datos personalizados para insertar
datos_seeders = [
    ("hola", "¡Hola! ¿Cómo estás?"),
    ("bien", "¡Que bueno! Me gusta escuchar eso"),
    ("¿Cómo te llamas?", "Me llamo VincentBot, encantado de conocerte"),
    ("Cómo te llamas?", "Me llamo VincentBot, encantado de conocerte"),
    ("como te llamas?", "Me llamo VincentBot, encantado de conocerte, recuerda poner tilde en -cómo- cuando realizas una pregunta"),
    ("te llamas?", "Me llamo VincentBoot, encantado de conocerte"),
    ("tienes razón", "Es cierto"),
    ("tienes razon", "Es cierto, recuerda que razón lleva tilde"),
    ("buenos días", "Hey, buenos días!"),
    ("buenos dias", "Hey, buenos días!. recuerda poner tilde en -días-"),
    ("que tengas lindo día", "Eres muy amable, igualmente para tí"),
    ("qué haces?", "Chateo contigo, haha"),
    ("que haces?", "Chateo contigo, haha, recuerda que -qué- lleva tilde cuando estás realizando una pregunta"),
    ("como estas?", "Bien, gracias por preguntar, recuerda que -cómo- y -estás- lleva tilde cuando estás realizando una pregunta"),
    ("como estás?", "Bien, gracias por preguntar, recuerda que -estás- lleva tilde cuando estás realizando una pregunta"),
    ("cómo estas?", "Bien, gracias por preguntar"),
    ("bien", "¡Que bueno! Me gusta escuchar eso"),
    ("bien y tu", "¡Que bueno! Me gusta escuchar eso, yo estoy genial gracias por preguntar"),
    ("y tu", "¡Genail! Gracias por preguntar. recuerda que -tú- lleva tilde"),
    ("y tú", "¡Genial! Gracias por preguntar"),
    ("adios", "¡Hasta luego! Que tengas un buen día"),
    ("gracias", "¡De nada! Estoy aquí para ayudarte."),
    ("triste", "Lamento escuchar eso. ¿Hay algo en lo que pueda ayudarte?"),
    ("feliz", "Me alegra escuchar eso. ¿En qué puedo ayudarte hoy?"),
    ("hola", "¡Hola! ¿Cómo estás?"),
    ("¿cómo te llamas?", "Me llamo VincentBot, tu amigo virtual para practicar español"),
    ("adios", "¡Hasta luego! Que tengas un buen día"),
    ("mal", "Lamento escuchar eso, espero que todo mejore pronto."),
    ("vincent", "¡Vincent! es mi amigo genial"),
    ("quien es vincent", "¡Vincent! es un tipo y amigo genial"),
    ("quien es tori", "¡Tori! es mi amiga genial de Brasil"),
    ("adios", "¡Hasta luego! Que tengas un buen día"),
    ("(.*)", "Aún no puedo contestar eso. Pero por favor, continúa, me encanta charlar contigo.")
]

for dato in datos_seeders:
    insert_query = "INSERT INTO respuestas_personalizadas (pregunta, respuesta) VALUES (%s, %s)"
    try:
        cursor.execute(insert_query, dato)
        print(f"Se ha insertado exitosamente: {dato}")
    except mysql.connector.Error as err:
        print(f"Error al insertar: {err}")

# Hacer commit para guardar los cambios
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()
