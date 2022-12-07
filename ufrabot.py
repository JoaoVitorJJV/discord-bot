import io
import discord
import aiohttp
from discord.ext import commands
import requests
import random
import datetime

intents = discord.Intents.all()
botDC = commands.Bot(command_prefix='!', intents=intents)

def getMovies():
    randNumber = random.randint(0, 50)
    apiToken = 'e54a4e4b7ceb1332f2b62f680bdc6941'
    r = requests.get(f'http://api.themoviedb.org/3/movie/popular?api_key={apiToken}&language=pt-BR&page={randNumber}')
    return r.json()
    

@botDC.command()
async def bot(ctx, msg):
    if msg == 'meu_dono':
        await ctx.send(f'O dono de <@{ctx.message.author.id}> é <@476079290585448498> ❤️')
        
    if msg == 'filmes':
        movies = getMovies()
        parse_filmes = ''
        for i in movies['results']:
            parse_filmes+= ' 🍿 ' + i['title'] + '\n'
            
        await ctx.send(f" Encontrei essa variedade de filmes, escolha um! \n\n{parse_filmes}")
        
    if msg == 'filme':
         
        response = getMovies()
        randomNumber = random.randint(0, len(response['results']))
        movie = response['results'][randomNumber]
        date = datetime.datetime.strptime(movie['release_date'], "%Y-%m-%d")
        url = "https://image.tmdb.org/t/p/w500/"+movie['poster_path'] 
        message  = ' 🍿 '+movie['title']+' \n\n📌 '+movie['overview']+' \n\n📆 Data de Lançamento: '+str(date.day)+'/'+str(date.month)+'/'+str(date.year)
        async with aiohttp.ClientSession() as session: 
            async with session.get(url) as resp: 
                img = await resp.read() 
                with io.BytesIO(img) as file: 
                    await ctx.send(message, file=discord.File(file, "movieimage.png"))

@botDC.command()
async def filme(ctx, *args):
    print(args)
    await ctx.send('Hi')


@botDC.event
async def on_ready():
    print('We have logged in as {0.user}'.format(botDC))

@botDC.event
async def on_message(message):
    await botDC.process_commands(message)
    # if message.content.startswith('!'):
    #     return
                

botDC.run('MTA1MDA2MjQ5NDc0OTcwMDE1Ng.GVLYvN.QiRPmc37YRMs03e5GkKXZqDlZKZTSLNP-fQvKU')