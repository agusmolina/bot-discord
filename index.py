
import datetime
import os
import re
import shutil
from tokenize import endpats
from urllib import parse, request

import discord
import youtube_dl
from discord import channel, guild, message, voice_client
from discord.errors import NoMoreItems
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='+', description="Bot De Magio")
###############################################################################################


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def sum(ctx, num1: float, num2: float):
    await ctx.send(num1+num2)


@bot.command()
async def rest(ctx, num1: float, num2: float):
    await ctx.send(num1-num2)


@bot.command()
async def div(ctx, num1: float, num2: float):
    if num2 != 0:
        await ctx.send(num1/num2)
    else:
        await ctx.send("No se puede dividir por 0")


@bot.command()
async def mult(ctx, num1: float, num2: float):
    await ctx.send(num1*num2)


@bot.command()
async def calcular(ctx, num1: float, operador, num2: float):
    if operador == "+":
        await sum(ctx, num1, num2)
    elif operador == "-":
        await rest(ctx, num1, num2)
    elif operador == "*":
        await mult(ctx, num1, num2)
    elif operador == "/":
        await div(ctx, num1, num2)
    else:
        await ctx.send("Operador no conocido por el bot")


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Descripcion del servidor",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_magenta())
    embed.add_field(name="Server creado en: ", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Dueño del servidor: ", value="Magio")
    embed.add_field(name="Region del servidor: ", value="Brazil")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(
        url="https://i.pinimg.com/236x/2c/a6/ee/2ca6eec84825d3a4affaba4904aa43d7.jpg")
    await ctx.send(embed=embed)


@bot.command()
async def redes(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Redes de Magio:",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_magenta())
    embed.add_field(name="Instagram: ",
                    value="https://www.instagram.com/magio.95/")
    embed.add_field(name="Twitch: ", value="https://www.twitch.tv/magio1995")
    embed.add_field(name="IP Server Minecraft: ",
                    value="play.latinoscraft.com.ar")
    embed.set_thumbnail(
        url="https://i.pinimg.com/236x/2c/a6/ee/2ca6eec84825d3a4affaba4904aa43d7.jpg")
    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen(
        'http://www.youtube.com/results?' + query_string)
    search_results = re.findall(
        'watch\?v=(.{11})', html_content.read().decode('utf-8'))
    print(search_results)
    await ctx.send('https://www.youtube.com/watch?v='+search_results[0])


@bot.command()
async def pregunta(ctx, *args):
    if args == "hitsu esta?" or "hitsu esta" or "Hitsu esta?" or "Hitsu esta":
        await ctx.send("chikito =3")
    else:
        await ctx.send("Pregunta no encontrada contacta con el staff")


@bot.command()
async def invitacion(ctx):
    await ctx.send("https://discord.com/invite/PJTpKMxZMG")
# comando help


@bot.command()
async def h(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Los comandos del bot son: (Prefijo +)", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_magenta())
    embed.add_field(name="invitacion ", value="Link para unirse al grupo")
    embed.add_field(name="info ", value="Info del servidor")
    embed.add_field(name="redes ", value="Redes del owner")
    embed.add_field(name="calcular 'numero1' 'operador' 'numero 2'", value="Suma,resta,multiplica o divide 2 numeros ")
    embed.add_field(name="pregunta 'pregunta'",value="Responde a las pregunta mas comunes")
    embed.add_field(name="conectar ", value="Conecta el bot al canal de voz")
    embed.add_field(name="desconectar ",value="Desconecta el bot del canal de voz")
    embed.add_field(name="youtube ", value="Realiza busqueda en youtube y trae el video mas popular")
    embed.add_field(name="play o p 'url' ",value="Reproduce el video o cancion")
    embed.add_field(name="pausa ", value="pausa el video o cancion")
    embed.add_field(name="continuar ",value="Reproduce el video o cancion pausada")
    embed.add_field(name="stop ", value="stopea el video o cancion")
    embed.set_thumbnail(url="https://i.pinimg.com/236x/2c/a6/ee/2ca6eec84825d3a4affaba4904aa43d7.jpg")
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def conectar(ctx):
    canal = ctx.message.author.voice.channel
    if not canal:
        await ctx.send("No estas conectado a un canal de voz")
        return

    voz = get(bot.voice_clients, guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz = await canal.connect()


@bot.command(pass_context=True)
async def desconectar(ctx):
    canal = ctx.message.author.voice.channel
    voz = get(bot.voice_clients, guild=ctx.guild)
    await voz.disconnect()


@bot.command(pass_context=True)
async def p(ctx, url: str):
    def revisar_lista():
        LR_en_Archivo = os.path.isdir("./Lista")
        if LR_en_Archivo is True:
            DIR = os.path.abspath(os.path.realpath("Lista"))
            tamaño = len(os.listdir(DIR))
            C_Activa = tamaño - 1
            try:
                C_primera = os.listdir(DIR)[0]
            except:
                print("No mas canciones\n")
                listar.clear()
                return
            localizacion_principal = os.path.dirname(
                os.path.realpath(__file__))
            C_localizacion = os.path.abspath(
                os.path.realpath("Lista") + "\\" + C_primera)
            if tamaño != 0:
                print("Cancion Lista, se reproducirá en momentos\n")
                print(f"Canciones en la lista: {C_Activa}")
                C_encontrada = os.path.isfile("cancion.mp3")
                if C_encontrada:
                    os.remove("cancion.mp3")
                    shutil.move(C_localizacion, localizacion_principal)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'cancion.mp3')

                    voice.play(discord.FFmpegPCMAudio("cancion.mp3"),
                               after=lambda e: revisar_lista())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07

                else:
                    listar.clear()
                    return

            else:
                listar.clear()
                print("No se agregó la cancion\n")

    C_encontrada = os.path.isfile("cancion.mp3")
    try:
        if C_encontrada:
            os.remove("cancion.mp3")
            listar.clear()
            print("Removido archivo antiguo")
    except PermissionError:
        print("Se ah intentado elminar un arhcivo en reproduccion")
        await ctx.send("Se ah intentado elminar un arhcivo en reproduccion")
        return
    LR_en_Archivo = os.path.isdir("./Lista")

    try:
        LR_Carpeta = "./Lista"
        if LR_en_Archivo is True:
             print("Removida la antigua carperta")
             shutil.rmtree(LR_Carpeta)
    except:
        print("No hay carpeta antigua")

    await ctx.send("Todo listo!")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Descargando Cancion ahora\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renombrando ahora: {file}\n")
            os.rename(file, "cancion.mp3")

    voice.play(discord.FFmpegPCMAudio("cancion.mp3"),after=lambda e: revisar_lista())
           
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nombre = name.rsplit("-", 2)
    await ctx.send(f"Reproduciendo: {nombre[0]}")
    print("Reproduciendo\n")

@bot.command(pass_context=True)
async def play(ctx, url: str):
    def revisar_lista():
        LR_en_Archivo = os.path.isdir("./Lista")
        if LR_en_Archivo is True:
            DIR = os.path.abspath(os.path.realpath("Lista"))
            tamaño = len(os.listdir(DIR))
            C_Activa = tamaño - 1
            try:
                C_primera = os.listdir(DIR)[0]
            except:
                print("No mas canciones\n")
                listar.clear()
                return
            localizacion_principal = os.path.dirname(
                os.path.realpath(__file__))
            C_localizacion = os.path.abspath(
                os.path.realpath("Lista") + "\\" + C_primera)
            if tamaño != 0:
                print("Cancion Lista, se reproducirá en momentos\n")
                print(f"Canciones en la lista: {C_Activa}")
                C_encontrada = os.path.isfile("cancion.mp3")
                if C_encontrada:
                    os.remove("cancion.mp3")
                    shutil.move(C_localizacion, localizacion_principal)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'cancion.mp3')

                    voice.play(discord.FFmpegPCMAudio("cancion.mp3"),
                               after=lambda e: revisar_lista())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07

                else:
                    listar.clear()
                    return

            else:
                listar.clear()
                print("No se agregó la cancion\n")

    C_encontrada = os.path.isfile("cancion.mp3")
    try:
        if C_encontrada:
            os.remove("cancion.mp3")
            listar.clear()
            print("Removido archivo antiguo")
    except PermissionError:
        print("Se ah intentado elminar un arhcivo en reproduccion")
        await ctx.send("Se ah intentado elminar un arhcivo en reproduccion")
        return
    LR_en_Archivo = os.path.isdir("./Lista")

    try:
        LR_Carpeta = "./Lista"
        if LR_en_Archivo is True:
             print("Removida la antigua carperta")
             shutil.rmtree(LR_Carpeta)
    except:
        print("No hay carpeta antigua")

    await ctx.send("Todo listo!")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Descargando Cancion ahora\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renombrando ahora: {file}\n")
            os.rename(file, "cancion.mp3")

    voice.play(discord.FFmpegPCMAudio("cancion.mp3"),after=lambda e: revisar_lista())
           
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nombre = name.rsplit("-", 2)
    await ctx.send(f"Reproduciendo: {nombre[0]}")
    print("Reproduciendo\n")





@bot.command(pass_context=True)
async def pausa(ctx):
    voz = get(bot.voice_clients,guild=ctx.guild) 
    if voz and voz.is_playing():
        print("Musica pausada")
        voz.pause()
        await ctx.send("Video pausado")
    else:
        print("No se esta reproduciendo nada")
        await ctx.send("No se esta reproduciendo nada!")


@bot.command(pass_context=True)
async def continuar(ctx):
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_paused():
        print("Reproduciendo nuevamente")
        voz.resume()
        await ctx.send("Reproduciendo nuevamente")
    else:
        print("No se encuentra pausada")
        await ctx.send("No se encuentra pausada")


@bot.command(pass_context=True)
async def stop(ctx):
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_playing():
        print("Musica detenida")
        voz.stop()
        await ctx.send("Musica detenida")
    else:
        print("No se esta reproduciendo nada")
        await ctx.send("No se esta reproduciendo nada")


listar = {}


@bot.command(pass_context = True)
async def lista(ctx, url: str):
    Cancion_lista = os.path.isdir("./Lista")
    if Cancion_lista is False:
        os.mkdir("Lista")
    DIR = os.path.abspath(os.path.realpath("Lista"))
    Lista_num = len(os.listdir(DIR))
    Lista_num += 1
    AgregarLista = True
    while AgregarLista:
        if Lista_num in listar:
            Lista_num = +1
        else:
            AgregarLista = False
            listar[Lista_num] = Lista_num

    Lista_path = os.path.abspath(os.path.realpath("Lista") + f"\cancion{Lista_num}.%(ext)s")

    ydl_op = {
        'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': Lista_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
    }
    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        print("Descargar Cancion")
        ydl.download([url])

    await ctx.send("Añadida la cancion "+str(Lista_num) + "a la lista de Reproduccion")

    print("Cancion añadida")


##################################################################################################################


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Magio1995", url="https://www.twitch.tv/magio1995"))
    print("Bot Activado")


bot.run('OTEwMzQ2OTQ4NzAyMjY5NDkx.YZRgqQ.d5foygcJRrbOOwNLV8xfZd-WvxY')  # token del bot
