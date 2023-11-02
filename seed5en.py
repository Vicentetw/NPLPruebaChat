import asyncio
import sys
sys.path.insert(0, './db')  # Agrega la ruta de la carpeta 'db' al sys.path
import db.database as database

async def insert_data(conn, datos_seeders):
    cursor = conn.cursor()
    for dato in datos_seeders:
        pregunta = dato[0]
        respuesta = dato[1]
        select_query = "SELECT * FROM respuestas_personalizadas WHERE pregunta_en = %s"
        cursor.execute(select_query, (pregunta,))
        result = cursor.fetchall()

        if result:
            print(f"La pregunta '{pregunta}' ya existe en la base de datos. Se omitirá.")
        else:
            insert_query = "INSERT INTO respuestas_personalizadas (pregunta_en, respuesta_en) VALUES (%s, %s)"
            try:
                cursor.execute(insert_query, dato)
                print(f"Se ha insertado exitosamente: {dato}")
            except mysql.connector.Error as err:
                print(f"Error al insertar: {err}")

async def main():
    datos_seeders = [
    ["hello", "Hello! How are you?"],
    ["fine", "Great to hear that!"],
    ["What's your name?", "My name is VincentBot, nice to meet you. And what's your name?"],
    ["What are you doing?", "I'm chatting with you, haha"],
    ["how are you?", "I'm fine, thanks for asking"],
    ["good", "Great to hear that!"],
    ["good and you", "Great to hear that! I'm doing great, thanks for asking"],
    ["and you", "Great! Thanks for asking"],
    ["goodbye", "Goodbye! Have a nice day"],
    ["thanks", "You're welcome! I'm here to help you."],
    ["sad", "I'm sorry to hear that. Is there anything I can help you with?"],
    ["happy", "I'm glad to hear that. How can I assist you today?"],
    ["Vincent", "Vincent! He's my cool friend"],
    ["who is Vincent", "Vincent! He's a cool guy and my friend"],
    ["who is Tori", "Tori! She's my awesome friend from Brazil"],
    ["bye", "Goodbye! Have a nice day"],
    [".*", "I can't answer that yet, but please continue. I love chatting with you."],
    ["I want to practice Spanish", "Of course! How can I help you with your practice?"],
    ["I would like to practice Spanish", "Of course! How can I help you with your practice?"],
    ["I'd like to practice Spanish", "Of course! How can I help you with your practice?"],
    ["How can I practice Spanish?", "There are several ways to practice. Do you have any preference?"],
    ["Tell me how I can practice Spanish", "There are several ways to practice. Do you have any preference?"],
    ["I want to improve my Spanish", "Great, practice will help you improve. How can I assist you?"],
    ["I need to improve my Spanish", "Great, practice will help you improve. How can I assist you?"],
    ["Any suggestions for practicing Spanish?", "Of course! Do you have a preference for any particular method?"],
    ["Where to practice Spanish?", "You can try practicing in conversation groups or with online tutors"],
    ["Where can I practice Spanish online", "You can try practicing in conversation groups or with online tutors"],
    ["Where to practice Spanish effectively", "You can try practicing in conversation groups or with online tutors"],
    ["Can you suggest how to practice Spanish", "Of course! Do you have a preference for any particular method?"],
    ["Do you have recommendations for practicing Spanish?", "Of course! Do you have a preference for any particular method?"],
    ["What is the best way to practice Spanish?", "The best way can vary depending on your preferences and skills"],
    ["What method do you recommend for practicing Spanish?", "The best way can vary depending on your preferences and skills"]
]



    conn = database.establish_connection()

    await insert_data(conn, datos_seeders)

    database.close_connection(conn, None)

if __name__ == "__main__":
    asyncio.run(main())
