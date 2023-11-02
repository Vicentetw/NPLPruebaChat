from flask import Flask, request, jsonify
from flask_cors import CORS
from chat2.db.database import establish_connection, close_connection
from textblob import TextBlob
from transformers import pipeline
import spacy
import unidecode
import re
import unicodedata
from sentence_transformers import SentenceTransformer, util
from langdetect import detect

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:4200", "http://localhost:4200", "http://172.155.0.0/24", "http://10.0.3.0/24"]}})
#CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
#CORS(app, resources={r"/*": {"origins": "*"}})

nlp = spacy.load("es_core_news_sm")
preguntas_respondidas = []
conn = establish_connection()
cursor = conn.cursor()

nlp_pipeline = pipeline("text-generation", model="distilgpt2")
sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# Función para detectar el idioma
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return None


def procesar_entrada(entrada):
    lang = detect_language(entrada)

    if lang == "es":
        entrada = normalizar_texto(entrada)  # Normalizar el texto de entrada
        doc = nlp(entrada)
        respuesta = "No pude entender tu mensaje. ¿Podrías reformularlo? / Could you rephrase it?"
        entidades = [(ent.text, ent.label_) for ent in doc.ents]
        if entidades:
            for ent, label in entidades:
                if label == 'PER':  # Verificar si la entidad identificada es una persona
                    respuesta = f"Hola {ent}! Chateamos hoy? / Shall we chat today?"
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
        generated_text = respuesta_generada[0]['generated_text']
        #respuesta += f"\nRespuesta generada: {respuesta_generada[0]['generated_text']}"
        # Verificar si la respuesta generada es coherente
        if es_coherente(generated_text) and is_spanish(generated_text):
            respuesta += f"\nSorry I'm still learning, possible answer: {generated_text}"
        else:
            respuesta += f"\nIf I answered you it would not be coherent or it would not be in Spanish. \U0001F937"  # Emoji de persona encogiéndose de hombros

        return respuesta

    elif lang == "en":
        entrada = normalize_text(entrada)  # Normalize the input text
        analysis = TextBlob(entrada)
        response = "I couldn't understand your message. Could you rephrase it?"
        if analysis.sentiment.polarity > 0:
            response += "\nI'm glad to hear that!"
        elif analysis.sentiment.polarity == 0:
            response += "\nI'm neutral about it."
        else:
            response += "\nI'm sorry to hear that. Is there anything I can help you with?"

        response_generated = nlp_pipeline(entrada, max_length=50, num_return_sequences=1)
        generated_text = response_generated[0]['generated_text']
        if is_coherent(generated_text) and is_english(generated_text):
            response += f"\nSorry I'm still learning, possible answer: {generated_text}"
        else:
            response += f"\nIf I answered you, it would not be coherent or it would not be in English. \U0001F937"

        return response

    else:
        return "I couldn't detect the language of the input. Could you write in Spanish or English?"
# Función para verificar si una oración es coherente
def es_coherente(entrada):
    sentences = [entrada]
    sentence_embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(sentence_embeddings, sentence_embeddings)
    return cosine_scores[0][0] > 0.3  # Umbral de similitud

# Function to verify if a sentence is coherent
def is_coherent(entrada):
    sentences = [entrada]
    sentence_embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(sentence_embeddings, sentence_embeddings)
    return cosine_scores[0][0] > 0.3  # Similarity threshold

# Function to verify if a text is in English
def is_english(text):
    return all(unicodedata.category(c).startswith('L') or c in [' '] for c in text)

# Función para verificar si un texto está en español
def is_spanish(text):
    return all(unicodedata.category(c).startswith('L') or c in [' ', 'á', 'é', 'í', 'ó', 'ú', 'ñ'] for c in text)

# Función para verificar preguntas personalizadas en la base de datos
def verificar_preguntas_personalizadas(user_message):
    conn = establish_connection()
    cursor = conn.cursor()
    try:
        
        query_property = "SELECT question, response FROM real_estate_queries"
        cursor.execute(query_property)
        pares_property = cursor.fetchall()

        # Normalizar el mensaje del usuario para la comparación
        normalized_user_message = unidecode.unidecode(user_message.lower())

        for question, response in pares_property:
            # Normalizar la pregunta para la comparación
            normalized_pregunta = unidecode.unidecode(question.lower())

            # Usar expresiones regulares para verificar si hay coincidencias parciales
            if re.search(normalized_user_message, normalized_pregunta):
                return response


        query_personalizadas = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
        cursor.execute(query_personalizadas)
        pares_personalizados = cursor.fetchall()

        # Normalizar el mensaje del usuario para la comparación
        normalized_user_message = unidecode.unidecode(user_message.lower())

        for pregunta, respuesta in pares_personalizados:
            # Normalizar la pregunta para la comparación
            normalized_pregunta = unidecode.unidecode(pregunta.lower())

            # Usar expresiones regulares para verificar si hay coincidencias parciales
            if re.search(normalized_user_message, normalized_pregunta):
                return respuesta

        query_retroalimentacion = "SELECT pregunta, respuesta_alternativa FROM retroalimentacion"
        cursor.execute(query_retroalimentacion)
        respuesta_generada = cursor.fetchall()
        for pregunta, respuesta_alternativa in respuesta_generada:
            normalized_pregunta = unidecode.unidecode(pregunta.lower())
            if re.search(normalized_user_message, normalized_pregunta):
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
    
    # Función para normalizar el texto
def normalizar_texto(texto):
    texto = texto.lower()  # Convertir el texto a minúsculas
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')  # Quitar tildes y diacríticos

    abreviaciones_espanol = {"qué": "que", "dónde": "donde", "cómo": "como"}  # Agrega más abreviaciones según sea necesario
    for abreviacion, forma_completa in abreviaciones_espanol.items():
        texto = texto.replace(abreviacion, forma_completa)

    return texto


def normalize_text(text):
    text = text.lower()  # Convert the text to lowercase
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')  # Remove accents and diacritics

    abreviaciones_ingles = {"i'm": "I am", "what's": "what is", "can't": "cannot", "don't": "do not"}  # Agrega más abreviaciones según sea necesario
    for abreviacion, forma_completa in abreviaciones_ingles.items():
        text = text.replace(abreviacion, forma_completa)

    return text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
