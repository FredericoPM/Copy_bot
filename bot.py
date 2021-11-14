import discord
import telebot
import os
import requests
import shutil
from dotenv import load_dotenv
load_dotenv()

class CopyBot(discord.Client):
    def __init__(self, test_server, telegran_api, server_list = [], input_list = [], *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self._tele_bot = telebot.TeleBot(telegran_api)
        self._test_serve_id = test_server
        self._server_list = server_list if len(server_list[0]) != 0 else []
        self._input_list = input_list if len(input_list[0]) != 0 else []
        self._input_flag = len(self._input_list) > 0

    async def read_img_url(self, url):
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
        print(message)

        if(len(message.content) != 0):
            print("Mensage content: " + message.content)
            self._tele_bot.send_message(self._test_serve_id, message.content)
            for server in self._server_list:
                self._tele_bot.send_message(server, message.content)

        if(len(message.attachments) != 0):
            print(message.attachments)
            for intem in message.attachments:
                if(".png" in intem.url or ".jpg" in intem.url):
                    print(intem.url)
                    try:
                        img = await self.read_img_url(intem.url)

                        self._tele_bot.send_photo(self._test_serve_id, img)
                        for server in self._server_list:
                            self._tele_bot.send_photo(server, img)

                        img.close()
                    except Exception as e:
                        print(e)


    async def on_ready(self):
        print("Connected")

copyBot = CopyBot(
    test_server = os.getenv('TEST_SERVER'),
    telegran_api = os.getenv('TELEGRAN_API'),
    server_list = os.getenv('SERVER_LIST').split(';'),
    input_list = os.getenv('IMPUT_LIST').split(';')
)
copyBot.run(os.getenv('DISCORD_TOKEN'))