from flask import Flask, request, jsonify
from flask_cors import CORS
#import mysql.connector
from chat2.db.database import establich_connection, close_connection
from transformers import BertTokenizer, BertForNextSentencePrediction

app = Flask(__name__)
CORS(app)

# Establecer la conexión a la base de datos
conn = establich_connection()
cursor = conn.cursor()

# Carga del modelo preentrenado
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')

# Función para procesar la entrada del usuario
def procesar_entrada(entrada):
    inputs = tokenizer(entrada, return_tensors="pt", padding=True, truncation=True)
    return inputs

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']

    query = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
    cursor.execute(query)
    pares_personalizados = cursor.fetchall()

    for pregunta, respuesta in pares_personalizados:
        if user_message.lower() in pregunta.lower():
            return jsonify({'message': respuesta})
    
    return jsonify({'message': "Lo siento, no entendí lo que dijiste."})

if __name__ == '__main__':
    app.run(debug=True)

# Cerrar la conexión
cursor.close()
conn.close()
