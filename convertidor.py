import json

# Lee el archivo JSON
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convierte los datos al nuevo formato
converted_data = [[item["pregunta"], item["respuesta"]] for item in data]

# Guarda los datos convertidos en un nuevo archivo JSON
with open('data2.json', 'w', encoding='utf-8') as file:
    json.dump(converted_data, file, ensure_ascii=False, indent=4)