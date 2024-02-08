from typing import Final
import os
import aiohttp
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty because intents were not enabled probably')
        return
        
    try:
        response: str = get_response(user_message)
        if not response:
            return
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message) -> None:
    
    if message.attachments: 
        for attachment in message.attachments:
            await attachment.save(f'./imagine/{attachment.filename}')
            print(f"Saved {attachment.filename}")
    

    if message.author == client.user: 
        return 
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    if user_message == 'stop':
        exit(0)

    await send_message(message, user_message)


def main() -> None: 
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
