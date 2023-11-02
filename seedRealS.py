import asyncio
import sys
sys.path.insert(0, './db')  # Agrega la ruta de la carpeta 'db' al sys.path
import db.database as database

async def insert_data(conn, datos_seeders):
    cursor = conn.cursor()
    for dato in datos_seeders:
        question = dato[0]
        response = dato[1]
        select_query = "SELECT * FROM real_estate_queries WHERE question = %s"
        cursor.execute(select_query, (question,))
        result = cursor.fetchall()

        if result:
            print(f"The question '{question}' already exists in the database. It will be skipped.")
        else:
            insert_query = "INSERT INTO real_estate_queries (question, response) VALUES (%s, %s)"
            try:
                cursor.execute(insert_query, dato)
                print(f"Successfully inserted: {dato}")
            except mysql.connector.Error as err:
                print(f"Error while inserting: {err}")

async def main():
    datos_seeders = [
        ["Looking for a two-bedroom apartment", "We have several options for two-bedroom apartments available. Please check our listings for more details."],
        ["Need to rent a house with a garden", "We offer a variety of rental houses with spacious gardens. Feel free to explore our listings for more information."],
        ["Interested in buying a commercial property", "We have a range of commercial properties available for purchase. Explore our listings to find the perfect option for your needs."],
        ["Looking for a studio apartment", "Our studio apartments offer modern amenities and convenient locations. Check our listings to find the perfect studio apartment for you."],
        ["Need a furnished apartment", "We provide fully furnished apartments with modern amenities. Explore our listings to find the furnished apartment that meets your requirements."],
        ["Searching for a condominium with parking", "Our condominiums offer dedicated parking spaces for residents. Explore our listings to find the ideal condominium with parking for you."],
        ["Interested in a beachfront property", "We offer stunning beachfront properties with breathtaking views. Explore our listings to find the perfect beachfront property for you."],
        ["Looking for a townhouse with a backyard", "Our townhouses come with spacious backyards, perfect for outdoor activities. Explore our listings to find the ideal townhouse for you."],
        ["Need to rent a pet-friendly apartment", "We have pet-friendly apartments available for rent. Check our listings to find the ideal pet-friendly apartment for you and your furry friend."],
        ["Interested in buying a luxury villa", "Our luxury villas offer unparalleled comfort and elegance. Explore our listings to find the perfect luxury villa for your lifestyle."],
     ["Buscando un apartamento de dos habitaciones", "Tenemos varias opciones de apartamentos de dos habitaciones disponibles. Consulta nuestros listados para obtener más detalles."],
        ["Necesito alquilar una casa con jardín", "Ofrecemos una variedad de casas en alquiler con amplios jardines. Siéntete libre de explorar nuestros listados para obtener más información."],
        ["Interesado en comprar una propiedad comercial", "Tenemos una variedad de propiedades comerciales disponibles para la compra. Explora nuestros listados para encontrar la opción perfecta para tus necesidades."],
        ["Buscando un apartamento estudio", "Nuestros apartamentos estudio ofrecen comodidades modernas y ubicaciones convenientes. Consulta nuestros listados para encontrar el apartamento estudio perfecto para ti."],
        ["Necesito un apartamento amueblado", "Ofrecemos apartamentos completamente amueblados con comodidades modernas. Explora nuestros listados para encontrar el apartamento amueblado que satisfaga tus requisitos."],
        ["Buscando un condominio con estacionamiento", "Nuestros condominios ofrecen espacios de estacionamiento dedicados para los residentes. Explora nuestros listados para encontrar el condominio ideal con estacionamiento para ti."],
        ["Interesado en una propiedad frente a la playa", "Ofrecemos impresionantes propiedades frente a la playa con vistas increíbles. Explora nuestros listados para encontrar la propiedad frente a la playa perfecta para ti."],
        ["Buscando un adosado con patio trasero", "Nuestros adosados vienen con patios traseros espaciosos, perfectos para actividades al aire libre. Explora nuestros listados para encontrar el adosado ideal para ti."],
        ["Necesito alquilar un apartamento apto para mascotas", "Tenemos apartamentos aptos para mascotas disponibles para alquilar. Consulta nuestros listados para encontrar el apartamento apto para mascotas ideal para ti y tu amigo peludo."],
        ["Interesado en comprar una villa de lujo", "Nuestras villas de lujo ofrecen un confort y elegancia incomparables. Explora nuestros listados para encontrar la villa de lujo perfecta para tu estilo de vida."]
    ]

    conn = database.establish_connection()

    await insert_data(conn, datos_seeders)

    database.close_connection(conn, None)

if __name__ == "__main__":
    asyncio.run(main())
