import os
import json
import shutil
import discord
import telebot
import requests
from dotenv import load_dotenv
from telebot.types import File

class CopyBot(discord.Client):
    def __init__(self, test_server_tg, test_server_ds, telegran_api, copy_server_ds, input_servers = [], server_list = [], *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self._tele_bot = telebot.TeleBot(telegran_api)
        self._test_server_tg = int(test_server_tg)
        self._test_server_ds = int(test_server_ds)
        self._copy_server_ds = copy_server_ds
        self._server_list = server_list if len(server_list[0]) != 0 else []
        self._input_servers = input_servers

    async def _read_img_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open("img.png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            f.close()
            return open("img.png", 'rb');
        else:
            raise ValueError("Error while loading img: " + r.status_code);

    async def _send_message_to_tg_servers(self, message, server_list):
        for server in server_list:
            if(len(message.content) != 0):              
                self._tele_bot.send_message(server, message.content)

        for emb in message.embeds:
            if(len(emb.description) != 0 and emb.image.url != discord.Embed.Empty and (".png" in emb.image.url or ".jpg" in emb.image.url)):
                try:
                    img = await self._read_img_url(emb.image.url)
                    for server in server_list:
                        self._tele_bot.send_photo(server, img, caption=emb.description)
                    img.close()
                except Exception as e:
                    print(e)
            elif(len(emb.description) != 0):
                for server in server_list:
                    self._tele_bot.send_message(server, emb.description)
            elif(emb.image.url != discord.Embed.Empty and (".png" in emb.image.url or ".jpg" in emb.image.url)):
                try:
                    img = await self._read_img_url(emb.image.url)
                    for server in server_list:
                        self._tele_bot.send_photo(server, img)
                    img.close()
                except Exception as e:
                    print(e)

        if(len(message.attachments) != 0):
            for intem in message.attachments:
                if(".png" in intem.url or ".jpg" in intem.url):
                    try:
                        img = await self._read_img_url(intem.url)
                        for server in server_list:
                            self._tele_bot.send_photo(server, img)
                        img.close()
                    except Exception as e:
                        print(e)

    async def _send_message_to_disc_server(self, message, channel_id):
        channel = self.get_channel(int(channel_id))
        if(len(message.content) != 0 and len(message.attachments) != 0):
            for intem in message.attachments:
                if(".png" in intem.url or ".jpg" in intem.url):
                    try:
                        img = await self._read_img_url(intem.url)
                        img.close()
                        await channel.send(content = message.content, file = discord.File('./img.png'))
                    except Exception as e:
                        print(e)
        elif(len(message.content) != 0):
            await channel.send(content = message.content)
        elif(len(message.attachments) != 0):
            for intem in message.attachments:
                if(".png" in intem.url or ".jpg" in intem.url):
                    try:
                        img = await self._read_img_url(intem.url)
                        img.close()
                        await channel.send(file = discord.File('./img.png'))
                    except Exception as e:
                        print(e)
    
        for emb in message.embeds:
            if(len(emb.description) != 0 and emb.image.url != discord.Embed.Empty and (".png" in emb.image.url or ".jpg" in emb.image.url)):
                try:
                    img = await self._read_img_url(emb.image.url)
                    img.close()
                    await channel.send(content = emb.description, file = discord.File('./img.png'))
                except Exception as e:
                    print(e)
            elif(len(emb.description) != 0):
                await channel.send(content = emb.description)
            elif(emb.image.url != discord.Embed.Empty and (".png" in emb.image.url or ".jpg" in emb.image.url)):
                try:
                    img = await self._read_img_url(emb.image.url)
                    img.close()
                    await channel.send(file = discord.File('./img.png'))
                except Exception as e:
                    print(e)

    async def on_message(self, message): 
        flag = False

        for server in self._input_servers:
            if(message.channel.id == int(server)):
                flag = True
                break
    
        print("====================================================================")
        print(message.channel.name)
        print(message.guild.name)
        print(message.content)
        for emb in message.embeds:
            print(emb.description)
            print(emb.image)
        print("====================================================================")
        
        if(flag):
            await self._send_message_to_tg_servers(message, self._server_list)
            await self._send_message_to_disc_server(message, self._copy_server_ds)
        if(message.guild.name == "Bots"):
            if(message.channel.id != self._test_server_ds):
                await self._send_message_to_tg_servers(message, [self._test_server_tg])
            if(message.channel.id != self._test_server_ds and message.channel.id != self._copy_server_ds):
                await self._send_message_to_disc_server(message, self._test_server_ds)

    async def on_ready(self):
        print("Connected")

load_dotenv()
copyBot = CopyBot(
    test_server_tg = os.getenv('TEST_SERVER_TG'),
    telegran_api = os.getenv('TELEGRAN_API'),
    test_server_ds = os.getenv('TEST_SERVER_DS'),
    copy_server_ds = os.getenv('COPY_SERVER_DS'),
    server_list = os.getenv('SERVER_LIST').split(';'),
    input_servers = os.getenv('INPUT_SERVERS').split(';')
)
copyBot.run(os.getenv('DISCORD_TOKEN'))
