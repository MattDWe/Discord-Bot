# Discord-Bot
Bot for the voice chat program Discord. Bot posts images from an SQL database as well as plays audio files from any YouTube link.

To run the bot just run the start.bat file.

# Requirements

Needs Python (Using 3.6.1)

Needs pip

Using pip install following libraries: discord, asyncio, psycopg2, sys, logging, time, and discord.py[voice], youtube_dl

Installing a libaries can be done by using "python -m pip install -U [library]

Also need to setup a sql database for images.

#Config File

In order to run the bot you need to set the token and sql server information. To do this create a file named config.py and add the variables for token and postgres_server.
