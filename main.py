import os
import discord
import requests
import json
from discord import channel
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()


def get_data(symbol):
    response = requests.get(
        'https://crypto-data-api.herokuapp.com/crypto/{0}'.format(symbol))
    data = json.loads(response.text)
    return data


@client.event
async def on_ready():
    print('Connected to Discord as {0.user}'.format(client))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            # await channel.send('>>> Hey there! I am CryptoBot!\n`$- "Symbol"` for basic data e.g. `$- BTC`\n`$+ "Symbol"` for advanced data e.g. `$+ BTC`')
            embed = discord.Embed(title='**Kia Ora!** :wave:', description='I am **CryptoBot**\nUse me to quickly retrieve coin prices, data and *more!*', color=0x201f55)
            # embed.set_author(name='Kia Ora! I am CryptoBot! Use me to quickly retrieve coin prices, data and more')
            embed.add_field(name='Basic request', value='`$- {symbol}` e.g. `$- BTC`', inline=False)
            embed.add_field(name='Advanced request', value='`$+ {symbol}` e.g. `$+ BTC`', inline=False)
            embed.add_field(name='Help', value='`$- help`', inline=False)
            await channel.send(embed=embed)
        break


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$- help'):
        embed = discord.Embed(title='**Commands** :wrench:', description='', color=0x201f55)
        embed.add_field(name='Basic request', value='`$- {symbol}` e.g. `$- BTC`', inline=False)
        embed.add_field(name='Advanced request', value='`$+ {symbol}` e.g. `$+ BTC`', inline=False)
        embed.add_field(name='Help', value='`$- help`', inline=False)
        await message.channel.send(embed=embed)

    elif message.content.startswith('$-'):
        symbol = message.content.split('$- ', 1)[-1].upper()
        data = get_data(symbol)
        percent_change = f':chart_with_upwards_trend: +{round(data["percent_change_24h"], 2)}%' if data[
            'percent_change_24h'] > 0 else f':chart_with_downwards_trend: {round(data["percent_change_24h"], 2)}%'
        # await message.channel.send('>>> [**{0}**] Current Price: ${1} USD ({2} {3}%)'.format(symbol, round(data["price"], 5), chart_emoji, round(data["percent_change_24h"], 2)))
        embed = discord.Embed(title=f'**${round(data["price"], 5):,}** USD ***{percent_change}***', description=f'', color=0x201f55)
        embed.set_author(name=symbol)
        embed.set_footer(text='Data provided by CoinMarketCap')
        await message.channel.send(embed=embed)

    elif message.content.startswith('$+'):
        symbol = message.content.split('$+ ', 1)[-1].upper()
        data = get_data(symbol)
        percent_change = f':chart_with_upwards_trend: +{round(data["percent_change_24h"], 2)}%' if data[
            'percent_change_24h'] > 0 else f':chart_with_downwards_trend: {round(data["percent_change_24h"], 2)}%'
        # await message.channel.send('>>> [**{0}**] Current Price: ${1} USD ({2} {3}%)\nFully Diluted Market Cap: ${4:,}\nCirculating Supply: {5:,}\nTotal Supply: {6:,}'.format(symbol, round(data['price'], 5), chart_emoji, round(data['percent_change_24h'], 2), round(data['fully_diluted_market_cap'], 2), round(data['circulating_supply'], 2), round(data['total_supply'], 2)))
        embed = discord.Embed(title=f'**${round(data["price"], 5):,}** USD ***{percent_change}***', description=f'', color=0x201f55)
        embed.set_author(name=symbol)
        embed.add_field(name='Fully Diluted Market Cap', value=f'${round(data["fully_diluted_market_cap"], 2):,}', inline=False)
        embed.add_field(name='Circulating Supply', value=f'{round(data["circulating_supply"], 2):,}', inline=True)
        embed.add_field(name='Total Supply', value=f'{round(data["total_supply"], 2):,}', inline=True)
        embed.set_footer(text='Data provided by CoinMarketCap')
        await message.channel.send(embed=embed)




client.run(os.getenv("token"))
