import re
import nltk
from nltk.chat.util import Chat, reflections

# Configuración del procesamiento del lenguaje natural (NLP)
nltk.download('punkt')

# Pares de patrones y respuestas
pares = [
    [r'(?i).*\bhola\b.*', ['¡Hola! ¿Cómo estás?', '¡Hola! Encantado de hablar contigo']],
    [r'(?i).*\b(?:cómo )?te llamas\b.*', ['Me llamo VincentBot, tu amigo virtual para pacticar español']],
    [r'(?i).*\b(?:como )?te llamas\b.*', ['Me llamo VincentBot, tu amigo virtual para pacticar español']],
    [r'(?i).*\b(?:cómo )?es tu nombre\b.*', ['Me llamo ChatBot, tu amigo virtual para pacticar español']],
    [r'(?i).*\b(?:como )?estas\b.*', ['Yo estoy genial. Gracias por preguntar, recuerda que "cómo" y "estás" llevan tilde en este caso, tú ¿Tu cómo estás?']],
    [r'(?i).*\badios\b.*', ['Upps!, recuerda que "adiós" lleva tilde en la "ó" ¡Hasta luego! Que tengas un día genial']],
    [r'(?i).*\bmal\b.*', ['Lamento escuchar eso, espero que todo mejore pronto.']],
    [r'(?i).*\bvincent\b.*', ['¡Vincent! es mi amigo genial ']],
    [r'(?i).*\badiós\b.*', ['¡Hasta luego! Que tengas un buen día']],
    [r'(?i).*\bbine\b.*', ['¡Upps! Creo que quisiste decir "bien"']],
    [r'(.*)', ['Aún no puedo contestar eso. Pero por favor, continúa, me encanta charlar contigo.']]
]

# Crear el chatbot
chatbot = Chat(pares, reflections)

# Función principal de chat
def chat():
    print("¡Bienvenido! Inicia tu conversación conmigo. Si quieres salir, escribe 'salir'")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            break
        respuesta = chatbot.respond(entrada)
        print("VincentBot:", respuesta)

# Iniciar el chat
if __name__ == "__main__":
    chat()