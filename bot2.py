import spacy
import unicodedata
import re

# Carga del modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

# Función para normalizar texto eliminando tildes y reemplazando 'ñ' con 'n'
def normalizar_texto(texto):
    texto_sin_tildes = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return texto_sin_tildes.replace('ñ', 'n')

# Función de procesamiento del lenguaje
def procesar_entrada(entrada):
    doc = nlp(entrada)
    return [normalizar_texto(token.text.lower()) for token in doc]

# Pares de patrones y respuestas
pares = [
    ["hola", ["¡Hola! ¿Cómo estás?", "¡Hola! Encantado de hablar contigo"]],
    ["¿cómo te llamas?", ["Me llamo VincentBot, tu amigo virtual para practicar español"]],
    ["adios", ["¡Hasta luego! Que tengas un buen día"]],
    ["mal", ["Lamento escuchar eso, espero que todo mejore pronto."]],
    ["vincent", ["¡Vincent! es mi amigo genial"]],
    ["quien es vincent", ["¡Vincent! es un tipo y amigo genial"]],
    ["quien es tori", ["¡Tori! es mi amiga genial de Brasil"]],
    [r'(?i).*\btori\b', ['¡Tori! es mi amiga genial de Brasil']],
    [r'(?i)\btoro\b', ['¡Toro! es un animal muy poderoso']],
    [r'(?i)\btoro\b', ['¡Toro! es un animal muy poderoso']],
    ["adios", ["¡Hasta luego! Que tengas un buen día"]],
    ["(.*)", ["Aún no puedo contestar eso. Pero por favor, continúa, me encanta charlar contigo."]],
]

# Función principal de chat
def chat():
    print("¡Bienvenido! Inicia tu conversación conmigo. Si quieres salir, escribe 'salir'")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() == 'salir':
            break
        entrada_procesada = procesar_entrada(entrada)
        for patron, respuestas in pares:
            if any(word in entrada_procesada for word in procesar_entrada(normalizar_texto(patron.lower()))):
                print("VincentBot:", respuestas[0])
                break
            # Añadir coincidencia específica para "toro" y "Toro"
            if re.search(r'\btoro\b', entrada) or re.search(r'\bToro\b', entrada):
                print("VincentBot:", pares[7][1][0])
                break
        else:
            print("VincentBot:", pares[-1][1][0])

# Iniciar el chat
if __name__ == "__main__":
    chat()
