from flask import Flask, request, jsonify
from flask_cors import CORS
from chat2.db.database import establish_connection, close_connection
from textblob import TextBlob
from transformers import pipeline
import spacy

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

nlp = spacy.load("es_core_news_sm")
preguntas_respondidas = []
conn = establish_connection()
cursor = conn.cursor()

nlp_pipeline = pipeline("text-generation", model="distilgpt2")

def procesar_entrada(entrada):
    doc = nlp(entrada)
    respuesta = "No pude entender tu mensaje. ¿Podrías reformularlo?"
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    if entidades:
        for ent, label in entidades:
            if label == 'PER':  # Verificar si la entidad identificada es una persona
                respuesta = f"Hola {ent}! ¿En qué puedo ayudarte hoy?"
                break
        else:
            respuesta = f"Las entidades identificadas son: {entidades}"
    analysis = TextBlob(entrada)
    if analysis.sentiment.polarity > 0:
        respuesta += "\n¡Me alegra escuchar eso!"
    elif analysis.sentiment.polarity == 0:
        respuesta += "\nEstoy neutral al respecto."
    else:
        respuesta += "\nLamento escuchar eso. ¿Hay algo en lo que pueda ayudarte?"

    respuesta_generada = nlp_pipeline(entrada, max_length=50, num_return_sequences=1)
    respuesta += f"\nRespuesta generada: {respuesta_generada[0]['generated_text']}"
    return respuesta
# Función para verificar preguntas personalizadas en la base de datos
def verificar_preguntas_personalizadas(user_message):
    conn = establish_connection()
    cursor = conn.cursor()
    try:
        query_personalizadas = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
        cursor.execute(query_personalizadas)
        pares_personalizados = cursor.fetchall()
        for pregunta, respuesta in pares_personalizados:
            if user_message.lower() in pregunta.lower():
                return respuesta

        query_retroalimentacion = "SELECT pregunta, respuesta_alternativa FROM retroalimentacion"
        cursor.execute(query_retroalimentacion)
        respuesta_generada = cursor.fetchall()
        for pregunta, respuesta_alternativa in respuesta_generada:
            if user_message.lower() in pregunta.lower():
                return respuesta_alternativa

    except Exception as e:
        print(f"Error: {e}")
    finally:
        close_connection(conn, cursor)  

    return None



# Función para registrar la retroalimentación en la base de datos 
def registrar_retroalimentacion(user_message, respuesta_generada, util, respuesta_alternativa):
    conn = establish_connection()
    cursor = conn.cursor()
    try:
        check_query = "SELECT id FROM retroalimentacion WHERE pregunta = %s"
        cursor.execute(check_query, (user_message,))
        result = cursor.fetchone()
        if result is not None:
            return jsonify({'message': 'Esta pregunta ya está registrada'})
        insert_query = "INSERT INTO retroalimentacion (pregunta, respuesta_generada, util, respuesta_alternativa) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_message, respuesta_generada, util, respuesta_alternativa))
        conn.commit()
        return jsonify({'message': 'Retroalimentación registrada correctamente'})
    except Exception as e:
        print(f"Error: {e}")
    finally:
        close_connection(conn, cursor)

# Rutas para procesar la solicitud del usuario y la retroalimentación
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    respuesta_personalizada = verificar_preguntas_personalizadas(user_message)
    if respuesta_personalizada:
        return jsonify({'message': respuesta_personalizada})
    spacy_response = procesar_entrada(user_message)
    return jsonify({'message': spacy_response})

@app.route('/retroalimentacion', methods=['POST'])
def procesar_retroalimentacion_request():
    data = request.get_json()
    user_message = data['user_message']
    respuesta_generada = data['respuesta_generada']
    util = data['util']
    respuesta_alternativa = data['respuesta_alternativa']
    if user_message and respuesta_alternativa and util is not None:
        registrar_retroalimentacion(user_message, respuesta_generada, util, respuesta_alternativa)
        return jsonify({'message': 'Retroalimentación registrada correctamente'})
    else:
        return jsonify({'message': 'Error al procesar la retroalimentación'})

if __name__ == '__main__':
    app.run(debug=True)
