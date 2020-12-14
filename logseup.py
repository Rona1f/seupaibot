"""script para enviar mensagens usando o bot

bot Seu pai criado por rona1f


"""

import discord
from discord.ext.commands import Bot

token_archive = open('token_seupai.txt', 'r')
TOKEN = token_archive.read()
token_archive.close()


player = {}
bot = Bot("!")

bot_falando = 652365155941875712
geral_suamae = 543230515097108493
geral_rn = 750402160658743389


client = discord.Client()
logmsg = str()
@client.event
async def on_ready():
    print('aaaaaaaaa')

    await client.change_presence(activity=discord.Game(name='para de falar chingling fred'))
    while True:
        logmsg = input('logmsg: ')
        if logmsg == 'quitlm':
            break
        if logmsg == 'attmsg':
            embed = discord.Embed(
                title=input('title-->'),
                color=0x101DF,
                description=input('msg-->')
            )
            await client.get_channel(geral_suamae).send(embed=embed)




client.run(TOKEN)

