import discord
from discord import guild
from discord.ext import commands
import datetime

bot=commands.Bot(command_prefix='+',description="Bot De Magio")

@bot.command()

async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def sum(ctx,num1: int, num2: int):
    await ctx.send(num1+num2)

@bot.command()

async def info(ctx):
    embed=discord.Embed(title=f"{ctx.guild.name}",description="Descripcion del servidor",timestamp=datetime.datetime.utcnow(),color=discord.Color.dark_magenta())
    embed.add_field(name="Server creado en: ",value=f"{ctx.guild.created_at}")
    embed.add_field(name="Dueño del servidor: ",value=f"{ctx.guild.owner}")
    embed.add_field(name="Region del servidor: ",value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID",value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://i.pinimg.com/564x/12/f7/e3/12f7e3406e263bbdf04395a5d5ae6a1e.jpg")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Magio1995",url="https://www.twitch.tv/magio1995"))
    print("Bot Activado")


bot.run('OTEwMzQ2OTQ4NzAyMjY5NDkx.YZRgqQ.B_kgoCFkFzdWM2ViLocbNsaNDws')