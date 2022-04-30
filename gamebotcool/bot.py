import discord
import asyncio
import cog_1
import random as rd
from discord import message
from Data.db_handler import add_inscriptions, clear_db
from discord import reaction as rt
from discord import embeds
from discord.colour import Color
from discord.ext import commands, tasks
from discord.ext.commands.core import check

bot = commands.Bot(command_prefix="$", description="Bleachbot")
status = ["!help", "Naruto storm", "Regarder la version 4.4.0.1", "Rendre ce serveur meilleur", "bleach brave soul", "Dragon Ball fighterZ"]

#_________________________________________________________________Events_______________________________________________________________________________________________________________________

@bot.event
async def on_ready():
    print("Ready !")
    change_status.start()

@tasks.loop(seconds=4000)
async def change_status():
    game = discord.Game(rd.choice(status))
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="**Missing Riquired Permissions**", color=0xFF0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/5099-no.png")
        embed.add_field(name="Warning", value="*Oops tu n'as pas les permissions requises pour faire cette commande.*", inline=True)
        
        
        await ctx.send(embed=embed)
        
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="**Missing Command**", color=0xFF0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/5099-no.png")
        embed.add_field(name="Warning", value="*Oops j'ai l'impression que cette commande n'existe pas*", inline=True)
        
        
        await ctx.send(embed=embed)

#@bot.event
#async def on_message(message):
   # if message.author == bot.user:
        #return
    #await message.channel.send(f">{message.content}\n{message.author}")
   # await bot.process_commands(message)
#__________________________________________________________________ServerInfo_________________________________________________________________________________________________________________

@bot.command()
async def ServerInfo(ctx):
    server = ctx.guild
    number_Of_Text_Channels = len(server.text_channels)
    number_Of_Voice_channels = len(server.voice_channels)
    server_description = server.description
    number_of_member = server.member_count
    server_name = server.name
    embed = discord.Embed(title="**Server_Info**", description=server_description, color=0xf06292)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/4863-info.png")
    embed.add_field(name="Server_name", value=server_name, inline=True)
    embed.add_field(name="Member_count", value=f"{number_of_member} membres.", inline=False)
    embed.add_field(name="Text_channel", value=f"{number_Of_Text_Channels} salons textuels.", inline=False)
    embed.add_field(name="Voice_channel", value=f"{number_Of_Voice_channels} salons vocaux.", inline=False)

    await ctx.send(embed=embed)
#_____________________________________________________________________reaction_____________________________________________________________________________________________________________

# cette commande cuisiner est un model 
@bot.command()
async def cuisiner(ctx):
    await ctx.send("Envoyer le plat que voulez cuisiner")

    def check_message(message):
        # on verifie que le message envpoye est dans le meme salon que la qu'on fait la commande
        return message.author == ctx.message.author and ctx.channel == message.channel
    try:
        recette = await bot.wait_for("message", timeout = 20, check = check_message)
    except:
        return
    print(recette.content)
    message = await ctx.send(f"La préparation de {recette.content} va commencer. Veuiller valider en réagissant avec :white_check_mark: ou avec :x:")
    # ajouter des emojis
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    
    def check_emoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌")
        
    # attendre pour une reaction
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout = 20, check=check_emoji)
        if reaction.emoji == "✅":
            await ctx.send("La recette a démarré.")
        else:
            await ctx.send("La recette a bien été annulé.")
    except:
        await ctx.send("La recette a bien été annulé.")
        
        
@bot.command()
async def inscriptions(ctx, number : int):
    embed = discord.Embed(title="**Inscriptions**", color=0xCCFF66)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/3756-letter.png")
    embed.add_field(name="**Descriptions**", value="*Veuillez réagir avec l'emoji ✅ pour vous inscrire*", inline=True)
    
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    def chemj(reaction, user):
        return user.roles.has("Gamer🎮") and message.id == reaction.message.id and (str(reaction.emoji) == "✅")
    try:
        reacted_users = []
        count_r_u = len(reacted_users)
        while count_r_u < number +1:
            reaction, user = await bot.wait_for("reaction_add", check=chemj)
            if reaction.emoji == "✅":
                reacted_users.append(user.name)
                print(reacted_users)
                for usr in reacted_users:
                    if usr == reacted_users[-1]:
                        add_inscriptions(usr)
                        await ctx.send("Félicitations vous avez bien été inscrit.")
                    else:
                        pass
            else:
                await ctx.send("Veuillez réagir avec l'emoji ✅ s'il vous plait.")
    except Exception as e:
        print(e)
@inscriptions.error
async def inscriptions_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="**Missing Riquired Argument**", color=0xFF0000)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/5099-no.png")
        embed.add_field(name="**Warning**", value="Oops la commande  *$inscriptions*  prend obligatoirement un argument !\n*E.x: '$inscriptions 32'*", inline=True)
        
        
        await ctx.send(embed=embed)

@bot.command()
async def cdbase(ctx):
    try:
        clear_db(channel_id =961172283777495070)
        await ctx.send("*La database a bien été effacée*")
    except Exception as error:
        await ctx.send(f"cela n'a pas marché car {error}")

bot.add_cog(cog_1.CogOwner(bot))
try:
    with open('token.txt', 'r') as file:
        token = file.read()
    bot.run(token)
except:
    print("Le fichier n'a pas pu etre lu !")
 

