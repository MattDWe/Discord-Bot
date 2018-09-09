import discord
import asyncio
import logging
import time

class DiscordBot:
    def __init__(self):
        logging.basicConfig(filename="logfile.text", level=logging.DEBUG)
        self.client = discord.Client()
        @self.client.event
        async def on_ready():
            print('Logged in as')
            print("Test Bot")
            print(self.client.user.id)
            print('------')
