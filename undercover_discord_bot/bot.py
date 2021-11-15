import os
import json
import shutil
import discord
import telebot
import requests
from dotenv import load_dotenv

class CopyBot(discord.Client):
    def __init__(self, test_server, telegran_api, input_servers_file, server_list = [], *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self._tele_bot = telebot.TeleBot(telegran_api)
        self._test_serve_id = test_server
        self._server_list = server_list if len(server_list[0]) != 0 else []
        try:
            with open(input_servers_file, "r") as read_file:
                self._imput_servers = json.load(read_file)
        except Exception as e:
            print(e)
            self._imput_servers = {"Servers" : []}

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

    async def on_message(self, message): 
        flag = len(self._imput_servers['Servers']) == 0

        for server in self._imput_servers['Servers']:
            if(message.guild.name == server['server_name']):
                for chanel in server['chanels']:
                    if(message.channel.name == chanel['chanel_name']):
                        flag = True
                        break
                break

        print("====================================================================")
        print(message)
        print(message.channel.name)
        print(message.guild.name)
        print(message.embeds)
        print(message.content)
        for emb in message.embeds:
            print(emb.description)
            print(emb.footer)
        print("====================================================================")
        
        if(flag):
            for server in self._server_list:
                if(len(message.content) != 0):              
                        self._tele_bot.send_message(server, message.content)
                for emb in message.embeds:
                    if(len(emb.description) != 0):
                        self._tele_bot.send_message(server, emb.description)
            
            if(len(message.attachments) != 0):
                print(message.attachments)
                for intem in message.attachments:
                    if(".png" in intem.url or ".jpg" in intem.url):
                        print(intem.url)
                        try:
                            img = await self._read_img_url(intem.url)

                            self._tele_bot.send_photo(self._test_serve_id, img)
                            for server in self._server_list:
                                self._tele_bot.send_photo(server, img)

                            img.close()
                        except Exception as e:
                            print(e)

                

        if(True):
            self._tele_bot.send_message(self._test_serve_id, message.content)
            for intem in message.attachments:
                if(".png" in intem.url or ".jpg" in intem.url):
                    try:
                        img = await self._read_img_url(intem.url)
                        self._tele_bot.send_photo(self._test_serve_id, img)
                        img.close()
                    except Exception as e:
                        print(e)
            for emb in message.embeds:
                self._tele_bot.send_message(self._test_serve_id, emb.description)

    async def on_ready(self):
        print("Connected")

load_dotenv()
copyBot = CopyBot(
    test_server = os.getenv('TEST_SERVER'),
    telegran_api = os.getenv('TELEGRAN_API'),
    server_list = os.getenv('SERVER_LIST').split(';'),
    input_servers_file = "./imputs.json"
)
copyBot.run(os.getenv('DISCORD_TOKEN'))
