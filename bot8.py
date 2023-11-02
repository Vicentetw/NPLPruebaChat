from flask import Flask, request, jsonify
from flask_cors import CORS
from chat2.db.database import establish_connection, close_connection
from textblob import TextBlob
from transformers import BertTokenizer, BertForNextSentencePrediction
import spacy
import tensorflow as tf

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

nlp = spacy.load("es_core_news_sm")
# Lista para almacenar las preguntas ya respondidas
preguntas_respondidas = []
conn = establish_connection()
cursor = conn.cursor()

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertForNextSentencePrediction.from_pretrained('bert-base-multilingual-cased')

# Función para procesar la entrada del usuario
def procesar_entrada(entrada):
    doc = nlp(entrada)
    respuesta = "No pude entender tu mensaje. ¿Podrías reformularlo?"
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    if entidades:
        respuesta = f"Las entidades identificadas son: {entidades}"
    analysis = TextBlob(entrada)
    if analysis.sentiment.polarity > 0:
        respuesta += "\n¡Me alegra escuchar eso!"
    elif analysis.sentiment.polarity == 0:
        respuesta += "\nEstoy neutral al respecto."
    else:
        respuesta += "\nLamento escuchar eso. ¿Hay algo en lo que pueda ayudarte?"
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            respuesta = f"El sujeto de tu mensaje es {token.text} y el verbo principal es {token.head.text}"
            break
        elif token.pos_ == "VERB":
            respuesta = f"El verbo en tu mensaje es {token.text}, pero no puedo identificar el sujeto"
    sustantivos = [token.text for token in doc if token.pos_ == "NOUN"]
    adjetivos = [token.text for token in doc if token.pos_ == "ADJ"]
    if sustantivos or adjetivos:
        respuesta += f"\nSustantivos identificados: {sustantivos}, Adjetivos identificados: {adjetivos}"
    frases_nominales = [chunk.text for chunk in doc.noun_chunks]
    if frases_nominales:
        respuesta += f"\nFrases nominales identificadas: {frases_nominales}"
    oraciones = [sent.text for sent in doc.sents]
    if oraciones:
        respuesta += f"\nOraciones identificadas: {oraciones}"
    inputs = tokenizer.encode_plus(entrada, add_special_tokens=True, return_tensors="pt")
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=-1)
    respuesta += f"\nPredicción de la siguiente oración: {predictions}"
    return respuesta

# Función para verificar preguntas personalizadas en la base de datos
# def verificar_preguntas_personalizadas(user_message):
#     query = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
#     cursor.execute(query)
#     pares_personalizados = cursor.fetchall()
#     for pregunta, respuesta in pares_personalizados:
#         if user_message.lower() in pregunta.lower():
#             if pregunta not in preguntas_respondidas:  # Verifica si la pregunta ya se ha respondido
#                 preguntas_respondidas.append(pregunta)  # Agrega la pregunta a la lista de preguntas respondidas
#                 return respuesta
#             else:
#                 return "Ya respondí a esta pregunta anteriormente. ¿Hay algo más en lo que pueda ayudarte?"
#     return None
# def verificar_preguntas_personalizadas(user_message):
#     conn = establish_connection()
#     cursor = conn.cursor()
#     try:
#         query = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
#         cursor.execute(query)
#         pares_personalizados = cursor.fetchall()
#         for pregunta, respuesta in pares_personalizados:
#             if user_message.lower() in pregunta.lower():
#                 return respuesta

#         check_query = "SELECT respuesta_generada FROM retroalimentacion WHERE pregunta = %s"
#         cursor.execute(check_query, (user_message,))
#         respuesta_generada = cursor.fetchone()
#         if respuesta_generada:
#             return respuesta_generada[0]

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         close_connection(conn, cursor)

#     return None

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

        query_retroalimentacion = "SELECT pregunta, respuesta_alternativa FROM retroalimentacion WHERE pregunta = %s"
        cursor.execute(query_retroalimentacion, (user_message,))
        respuesta_generada = cursor.fetchone()
        if respuesta_generada:
            return respuesta_generada[0]

    except Exception as e:
        print(f"Error: {e}")
    finally:
        close_connection(conn, cursor)  # Asegúrate de pasar 'conn' y 'cursor' como argumentos

    return None


# Función para registrar la retroalimentación en la base de datos
# def registrar_retroalimentacion(user_message, respuesta, util, respuesta_alternativa):
#     conn = establish_connection()
#     cursor = conn.cursor()
#     check_query = "SELECT * FROM respuestas_alternativas WHERE respuesta = %s"
#     cursor.execute(check_query, (respuesta_alternativa,))
#     existing_response = cursor.fetchone()
#     if existing_response:
#         close_connection(conn, cursor)  # Asegúrate de cerrar la conexión si ya existe una respuesta alternativa
#         return jsonify({'message': 'La respuesta alternativa ya está registrada'})
#     insert_query = "INSERT INTO retroalimentacion (pregunta, respuesta_generada, util, respuesta_alternativa) VALUES (%s, %s, %s, %s)"
#     cursor.execute(insert_query, (user_message, respuesta, util, respuesta_alternativa))
#     conn.commit()
#     close_connection(conn, cursor)
def registrar_retroalimentacion(user_message, respuesta_generada, util, respuesta_alternativa):
    conn = establish_connection()
    cursor = conn.cursor()
    try:
        check_query = "SELECT id FROM respuestas_personalizadas WHERE pregunta = %s"
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
    respuesta_alternativa = data['respuesta_alternativa']  # Asegúrate de obtener 'respuesta_alternativa' del JSON
    if user_message and respuesta_generada and util is not None:
        registrar_retroalimentacion(user_message, respuesta_generada, util, respuesta_alternativa)  # Asegúrate de pasar 'respuesta_alternativa'
        return jsonify({'message': 'Retroalimentación registrada correctamente'})
    else:
        return jsonify({'message': 'Error al procesar la retroalimentación'})

if __name__ == '__main__':
    app.run(debug=True)
