import mysql.connector
from transformers import BertTokenizer, BertForNextSentencePrediction

# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chat_vincent"
)
cursor = conn.cursor()

# Carga del modelo preentrenado
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForNextSentencePrediction.from_pretrained('bert-base-uncased')

# Función para procesar la entrada del usuario
def procesar_entrada(entrada):
    inputs = tokenizer(entrada, return_tensors="pt", padding=True, truncation=True)
    return inputs

# Función principal de chat
def chat():
    print("¡Bienvenido! Inicia tu conversación conmigo. Si quieres salir, escribe 'salir'")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            break
        # Lógica para verificar coincidencias con pares personalizados y proporcionar respuestas desde la base de datos
        query = "SELECT pregunta, respuesta FROM respuestas_personalizadas"
        cursor.execute(query)
        pares_personalizados = cursor.fetchall()

        for pregunta, respuesta in pares_personalizados:
            if entrada.lower() in pregunta.lower():
                print("ChatBot:", respuesta)
                break
        else:
            print("ChatBot: Lo siento, no entendí lo que dijiste.")

# Resto del código para procesar la entrada y generar respuestas

# Iniciar el chat
if __name__ == "__main__":
    chat()

# Cerrar la conexión
cursor.close()
conn.close()
