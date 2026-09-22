import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
async def test_ai():
    response = await client.chat.completions.create(
        model="openrouter/free",
        messages=[{
            "role": "user",
            "content":"привет ты работаешь? будешь трудится с моим приложением)))"
        }]
    )
    print(response.choices[0].message.content)

asyncio.run(test_ai())