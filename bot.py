import discord
import telebot
from dotenv import load_dotenv
import os
load_dotenv()

# TODO: adicionar qual servidor replicar
# TODO: adicionar lista de servidores do telegran para quais se replicar
# TODO: conseguir uma forma de enviar imagens
class MyClient(discord.Client):
    _tele_bot = telebot.TeleBot(os.getenv('TELEGRAN_API'))
    _test_serve_id = os.getenv('TEST_SERVER')

    async def on_message(self, message):
        print(message)
        print(message.attachments)
        print("Mensage content: "+message.content)
        self._tele_bot.send_message(self._test_serve_id, message.content)

    async def on_ready(self):
        print("deu bom")

Client = MyClient()
Client.run(os.getenv('DISCORD_TOKEN'))