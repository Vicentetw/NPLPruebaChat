import json
from transformers import BertTokenizer, BertForNextSentencePrediction

# Cargar los pares de patrones y respuestas personalizados desde el archivo JSON
with open('respuestas_personalizadas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    pares_personalizados = data['pares']

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
        # Lógica para verificar coincidencias con pares personalizados y proporcionar respuestas
        for par in pares_personalizados:
            if entrada.lower() in par[0]:
                print("ChatBot:", par[1][0])
                break
        else:
            print("ChatBot: Lo siento, no entendí lo que dijiste.")

# Resto del código para procesar la entrada y generar respuestas

# Iniciar el chat
if __name__ == "__main__":
    chat()
