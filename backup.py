import asyncio
import aiomysql
import json

async def retrieve_data_and_store_json(pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            select_query = "SELECT * FROM respuestas_personalizadas"
            await cursor.execute(select_query)
            results = await cursor.fetchall()

            data_to_store = [{"pregunta": row[1], "respuesta": row[2]} for row in results]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_store, f, ensure_ascii=False, indent=4)

async def main():
    pool = await aiomysql.create_pool(host="localhost", user="root", password="", db="chat_vincent")

    await retrieve_data_and_store_json(pool)

    pool.close()
    await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
