import discord
import asyncio
import os
import random
import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions
from easy_pil import Editor, load_image_async, Font
from discord import File

#Importowanie danych
from service import *


#konfiguracja
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help")
intents.members = True

#Komendy startowe
@bot.event
async def on_ready():
    print(" ")
    print(">>> Pomyślnie zalogowano na konto Victory Bot™!")
    print(" ")
    await bot.change_presence(activity=discord.Game(name = "$help | Official Bot"))

#Komenda setup
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, komenda):
    if komenda == "weryfikacja":
        embed=discord.Embed(title="**ZWERYFIKUJ SIĘ**", description="Po weryfikacji zobaczysz wszystkie kanały!", color=0x87CEFA)
        embed.set_author(name="Victory World™", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name="Aby się zweryfikować kliknij reakcję poniżej!", value="✅", inline=False)
        embed.set_footer(text="Victory World™")
        await ctx.send(embed=embed)

    elif komenda == "powitania":
        ctx.send("Ta komenda ma oddzielny setup! Aby zobić setup wpisz: $setup_powitania")

    elif komenda == " ":
        ctx.send("Podaj jaki setup chcesz wybrać!")

#Dodawanie roli
@bot.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

    if payload.emoji.name == "✅" and payload.message_id == 1025871139429425172:
        role = discord.utils.get(guild.roles, name="👥 | Użytkownik")
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

#Zabieranie roli
@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

    if payload.emoji.name == "✅" and payload.message_id == 1025871139429425172:
        role = discord.utils.get(guild.roles, name="👥 | Użytkownik")
        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

#Powitania
@bot.event
async def on_member_join(member):

    channel = bot.get_channel(lobby_id_channel)

    pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)

    background = Editor(filename_1)

    #Pprofilowe
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    poppins = Font.poppins(size=50, variant="bold")

    poppins_small = Font.poppins(size=40, variant="light")

    #Wysyłanie
    background.text((350, 140), f"Witaj na {member.guild.name}!", color="white", font=poppins, align="center")
    background.text((350, 260), f"{member.name}#{member.discriminator}", color="white", font=poppins_small, align="center")
    background.text((350, 310), f"Jesteś naszym {pos} użytkownikiem!", color="yellow", font=poppins_small, align="center")

    file = File(fp=background.image_bytes, filename=filename_1)

    await channel.send(file=file)

    #Licznik użytkowników
    #await asyncio.sleep(4)
    #for channel in member.guild.channels:
        #if channel.name.startswith('👥・Jest nas:'):
            #await channel.edit(name=f'👥・Jest nas: {member.guild.member_count}')
            #break

#Pożegnania
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(lobby_id_channel)

    await channel.send(f"{member.name} wyszedł z naszego serwera, żegnamy :(")

#Komenda add
@bot.command()
async def add(ctx, bot):
    if bot == "music":
        await ctx.reply(f"Link do naszego bota: {link_add_music}")
        await ctx.reply(f"Pamiętaj! Funkcja ekspeymentalna!")
    elif bot == "bot":
        await ctx.reply(f"Link do naszego bota: {link_add}")
        await ctx.reply(f"Pamiętaj! Funkcja ekspeymentalna!")

#Komenda help
@bot.command()
async def help(ctx):
    embed=discord.Embed(title="**POMOC**", description="Komendy:", color=0x87CEFA)
    embed.set_author(name="Victory World™", icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name="$add [music, bot]", value="Dodaj bota!", inline=False)
    embed.add_field(name="$setup [weryfikacja]", value="Skonfiguruj weryfikacje!", inline=True)
    embed.add_field(name="$help", value="Ta komenda!", inline=True)
    embed.add_field(name="$giveaway [sekundy] [wygrana] [osoby]", value="Swtóz giveway! Czas musi być podany w sekundach!", inline=True)
    embed.set_footer(text="Victory World™")
    await ctx.send(embed=embed)

#Errory
@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands. MissingRequiredArgument):
       await ctx.reply("Nie podałeś jaki setup chcesz wybrać!")

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands. MissingRequiredArgument):
       await ctx.reply("Nie podałeś jakiego bota chcesz dodać!")

@bot.command()
async def giveaway(ctx, seconds: int, prize: str, osoby: int): 
    if osoby < 5:
        if osoby > 0:
            embed = discord.Embed(title="**GIVEAWAY**", description=f"Nagroda: {prize}", color=0x87CEFA)
            embed.set_author(name="Victory World™", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)

            embed.add_field(name="Ilość wygranych", value=f"{osoby}", inline=False)
            embed.add_field(name="Aby wziąć udział kliknij reakcję", value="✨", inline=False)
            embed.set_footer(text=f"Kończy się za {seconds} sekund od startu!")

            my_msg = await ctx.send(embed=embed)

            await my_msg.add_reaction("✨")

            await asyncio.sleep(seconds)

            new_msg = await ctx.channel.fetch_message(my_msg.id)

            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(bot.user))

            winner = random.choice(users)
            winner2 = random.choice(users)
            winner3 = random.choice(users)
            winner4 = random.choice(users)
            
            if osoby == 1:
                await ctx.send(f"**KONIEC**")
                await ctx.send(f"Gratulacje {winner.mention}")
                await ctx.send(f"Wygrałeś {prize}!")
            elif osoby == 2:
                await ctx.send(f"Gratulacje {winner.mention}, {winner2.mention}")
                await ctx.send(f"Wygraliście {prize}!")
            elif osoby == 3:
                await ctx.send(f"Gratulacje {winner.mention}, {winner2.mention}, {winner3.mention}")
                await ctx.send(f"Wygraliście {prize}!")
            else:
                await ctx.send(f"Gratulacje {winner.mention}, {winner2.mention}, {winner3.mention}, {winner4.mention}")
                await ctx.send(f"Wygraliście {prize}")
        else:
            await ctx.reply(f"Minimalnie wygranych może być 1!")
    else:
        await ctx.reply(f"Maksymalnie wygranych może być 4!")


bot.run(f"{token}")