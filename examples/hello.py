import asyncio

from tinychain.client.ollama_client import OllamaClient

client = OllamaClient(name="demo")

async def main():
    reseponse = await client.async_chat(
        {
            "model":"qwen2.5",
            "messages":[{'role': 'user', 'content': 'Why is the sky blue?'}],
            "stream":True
            }
            )
    async for part  in reseponse:
        print(part['message']['content'], end='', flush=True)


if __name__ == "__main__":
    asyncio.run(main())