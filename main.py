import discord
import asyncio
import psycopg2
import sys
import logging
import time
import config

logging.basicConfig(filename="logfile.text", level=logging.DEBUG)


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(config.postgres_server)
            self.cur = self.conn.cursor()
        except:
            print("Unable to connect to database. Please make sure database is online. Error was logged.")
            logging.exception("Issue connecting to database " + time.asctime())
            sys.exit()
            
    def refreshList(self):
        self.cur.close()
        self.cur = self.conn.cursor()
        self.cur.execute("""SELECT urls FROM websites""")
        urls = self.cur.fetchall()
        return urls
    
    def addImage(self, url):
        self.cur.execute("""INSERT INTO websites(urls) VALUES(\'%s\');""" % (url))
        self.conn.commit()
        
    def deleteImage(self, index):
        urls = self.refreshList()
        url = urls[int(index) - 1][0]
        self.cur.execute("""DELETE FROM websites WHERE urls = \'%s\';""" % (url))
        self.conn.commit()


class DiscordBot:
    def __init__(self):
        self.client = discord.Client()
        @self.client.event
        async def on_ready():
            print('Logged in as')
            print("Test Bot")
            print(self.client.user.id)
            print('------')


def main():
    database = Database()
    bot = DiscordBot()
    @bot.client.event
    async def on_message(message):
        if message.content.startswith("!commands"):
            await bot.client.send_message(message.channel, """
        ---Commands--- :D
!urls - display urls in database
!add [url] - add a url to the database
!delete [index] - delete an image from database. You can find the images index by using !urls
!display [index] - display certain image from database
!summon - bot will join the current voice channel of the user
!goaway - rudely tell the bot to leave the channel
!play [url] - bot will start playing the audio of the url (youtube only)
        """)
            
        if message.content.startswith("!urls"):
            urls = database.refreshList()
            s = ""
            i = 1
            for url in urls:
                s += str(i) + " - <" + url[0] + "> - \n"
                i += 1
            await bot.client.send_message(message.channel, "Urls in Database: \n" + s)
            
        if message.content.startswith("!add"):
            url = message.content[5:]
            try:
                database.addImage(url)
            except:
                await bot.client.send_message(message.channel, "Sorry, there was an issue adding that url. Error was logged.")
                logging.exception("Issue adding image " + time.asctime())
                
        if message.content.startswith("!display"):
            index = message.content[9:]
            urls = database.refreshList()
            try:
                await bot.client.send_message(message.channel, embed = discord.Embed().set_image(url=urls[int(index) - 1][0]))
            except:
                await bot.client.send_message(message.channel, "Sorry, there was an error dispalying image at index " + index + " Error was logged.")
                logging.exception("Issue displaying image " + time.asctime())
                
        if message.content.startswith("!delete"):
            index = message.content[8:]
            try:
                database.deleteImage(index)
                await bot.client.send_message(message.channel, "Image at index " + str(index) + " was deleted.")
            except:
                await bot.client.send_message(message.channel, "There was a problem deleting that image. Please make sure the index exiss. Error was logged.")
                logging.exception("Issue deleting image " + time.asctime())
                
        if message.content.startswith("!summon"):
            try:
                await bot.client.join_voice_channel(message.author.voice.voice_channel)
            except Exception as e:
                await bot.client.send_message(message.channel, e)

        if message.content.startswith("!goaway"):
            try:
                await bot.client.voice_client_in(message.server).disconnect()
            except AttributeError:
                await bot.client.send_message(message.channel, "I'm not in a channel.")

        if message.content.startswith("!play"):
            try:
                players = {}
                url = message.content[6:]
                player = await bot.client.voice_client_in(message.server).create_ytdl_player(url)
                players[message.server.id] = player
                player.start()
            except:
                await bot.client.send_message(message.channel, "I am not in a channel.")

    bot.client.run(config.token)

            
if __name__ == '__main__':
    main()
