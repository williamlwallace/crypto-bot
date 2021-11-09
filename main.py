import os
import discord
from discord import channel
import requests
import json
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

def get_data(symbol):
    response = requests.get('http://127.0.0.1:3000/crypto/{0}'.format(symbol))
    data = json.loads(response.text)
    return data


@client.event
async def on_ready():
    print('Connected to Discord as {0.user}'.format(client))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('>>> Hey there! I am CryptoBot!\n`$- "Symbol"` for basic data e.g. `$- SOL`\n`$+ "Symbol"` for advanced data e.g. `$+ SOL`')
        break


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$-'):
        await message.author.send('HA HA U SMELL SHAME LOL XD GOT U\n*farts on you*')
        symbol = message.content.split('$- ', 1)[-1].upper()
        data = get_data(symbol)
        chart_emoji = ':chart_with_upwards_trend:' if data[
            'percent_change_24h'] > 0 else ':chart_with_downwards_trend:'
        await message.channel.send('>>> [**{0}**] Current Price: ${1} USD ({2} {3}%)'.format(symbol, round(data["price"], 5), chart_emoji, round(data["percent_change_24h"], 2)))

    if message.content.startswith('$+'):
        symbol = message.content.split('$+ ', 1)[-1].upper()
        data = get_data(symbol)
        chart_emoji = ':chart_with_upwards_trend:' if data[
            'percent_change_24h'] > 0 else ':chart_with_downwards_trend:'
        await message.channel.send('>>> [**{0}**] Current Price: ${1} USD ({2} {3}%)\nFully Diluted Market Cap: ${4:,}\nCirculating Supply: {5:,}\nTotal Supply: {6:,}'.format(symbol, round(data['price'], 5), chart_emoji, round(data['percent_change_24h'], 2), round(data['fully_diluted_market_cap'], 2), round(data['circulating_supply'], 2), round(data['total_supply'], 2)))

client.run(os.getenv("token"))
