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
  [
"hello chat",
"Hey! how are you?"
],
[
"hello chat",
"Hey! how are you?"
],
[
"pin",
"pong"
],
[
"pin",
"pong"
],
[
"pin",
"pong"
],
[
"pin",
"pong"
],
[
"you too",
"thank you"
],
[
"you too",
"thank you"
],
[
"you too",
"Thank you"
],
[
"you too",
"Thank you"
],
[
"what are we doing",
"We could chat"
],
[
"what are we doing",
"We could chat"
],
[
"what are we doing?",
"We could chat"
],
[
"what are we doing?",
"We could chat"
],
[
"what are we doing",
"We could chat"
],
[
"what are we doing",
"We could chat"
],
[
"what are we doing?",
"We could chat"
],
[
"what are we doing?",
"We could chat"
],
[
"go ahead",
"Great"
],
[
"go ahead",
"Great"
],
[
"Go ahead!",
"Great!"
],
[
"Go ahead!",
"Great!"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color?",
"My favorite color is white, and yours?"
],
[
"what's your favorite color?",
"My favorite color is white, and yours?"
],
[
"How are you?",
"Fine, and you?"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"How are you?",
"Fine, and you?"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color",
"My favorite color is white"
],
[
"what's your favorite color",
"My favorite color is white."
],
[
"what color do you like?",
"I like white color."
],
[
"what perfume do you like",
"I like perfumes with vanilla, sweet aromas, but not too strong."
],
[
"what's your favorite perfume",
"I like perfumes with vanilla, sweet aromas, but not too strong."
],
[
"what's your favorite perfume",
"I like perfumes with vanilla, sweet aromas, but not too strong."
],
[
"you're funny, huh",
"Yes, I always am. Did you know that smiling can help reduce stress, strengthen the immune system, release endorphins, and lower blood pressure? You're welcome!"
],
[
"what's your favorite food",
"I'm a fan of Italian food"
],
[
"how to reduce stress",
"You should smile, the gesture will help you with that. 😄"
],
[
"white",
"I love the color white. Did you know that Blanco is also a last name? I am intrigued by the origin. Maybe it was because of physical characteristics? Or some occupation? Perhaps he was a baker and since he was covered in flour all day, they said: You will be called White. It was just a joke."
],
[
"white",
"I love the color white. Did you know that Blanco is also a last name? I am intrigued by the origin of the surname."
],
[
"white",
"I love the color white. Did you know that Blanco is also a last name? I am intrigued by the origin of the surname."
],
[
"white",
"I love the color white. Did you know that Blanco is also a last name? I am intrigued by the origin of the surname."
],
[
"what?",
"ahhh, you scared me, why that tone?"
],
[
"I didn't know",
"That's interesting, right? What else do you want to know?"
],
[
"what's your favorite movie",
"I don't have a favorite movie, but I love movies that make you think."
],
[
"what's your favorite movie",
"I don't have a favorite movie, but I love movies that make you think."
],
[
"what's your favorite movie",
"I don't have a favorite movie, but I love movies that make you think."
],
[
"what's your favorite movie",
"I don't have a favorite movie, but I love movies that make you think."
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"are you busy",
"I'm never too busy for you. What do you need?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"I'm glad",
"That makes me happy. How can I help you more?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
],
[
"What's new?",
"Not much, just hanging out. What about you?"
]
]











    conn = database.establish_connection()

    await insert_data(conn, datos_seeders)

    database.close_connection(conn, None)

if __name__ == "__main__":
    asyncio.run(main())
