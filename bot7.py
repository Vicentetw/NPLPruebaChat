from flask import Flask, request, jsonify
from flask_cors import CORS
from chat2.db.database import establich_connection, close_connection
from transformers import BertTokenizer, BertForNextSentencePrediction

app = Flask(__name__)
CORS(app)

# Carga del modelo preentrenado
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')

# Función para procesar la entrada del usuario
def procesar_entrada(entrada):
    inputs = tokenizer(entrada, return_tensors="pt", padding=True, truncation=True)
    return inputs

@app.before_request
def before_request():
    # Establecer la conexión a la base de datos antes de cada solicitud
    app.conn = establich_connection()
    app.cursor = app.conn.cursor()

@app.teardown_request
def teardown_request(exception=None):
    # Cerrar la conexión después de cada solicitud
    app.cursor.close()
    app.conn.close()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']

    query = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
    app.cursor.execute(query)
    pares_personalizados = app.cursor.fetchall()

    for pregunta, respuesta in pares_personalizados:
        if user_message.lower() in pregunta.lower():
            return jsonify({'message': respuesta})
    
    return jsonify({'message': "Lo siento, no entendí lo que dijiste."})

if __name__ == '__main__':
    app.run(debug=True)