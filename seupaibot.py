"""
Bot do servidor "a sua mãe" no discord

criado por rona1f

github.com/Rona1f
"""

from googletrans import Translator
from google_trans_new import google_translator
import discord
from discord.utils import get
from discord.ext import commands
from datetime import datetime, date
import asyncio
import sqlite3

token_archive = open('token_seupai.txt', 'r')
TOKEN = token_archive.read()
token_archive.close()

PREFIX = '--'

conn = sqlite3.connect('bday.db')
c = conn.cursor()

c.execute("""
            CREATE TABLE IF NOT EXISTS bday (
            user text,
            dia integer,
            mes integer
            )
""")

c.execute("""
            CREATE TABLE IF NOT EXISTS tga (
            usertga text,
            pontos integer
            )
""")

c.execute(f"SELECT * FROM bday")
bday_results = c.fetchall()
# bday_user_id = bday_results[0][0]
print(bday_results)

bot = commands.Bot(command_prefix="--")
msg_id = None
resultado = str()
#client = discord.Client()
player1 = int()
player2 = int()
field = []
geral_suamae = 543230515097108493
geral_rn = 750402160658743389
sua_mae_id = 543230515097108490
aniv_txt = ''
pontos_txt = ''
votaram = []
headtga = 'rona'

velhavez = 1

@bot.event
async def on_ready():
    print('Bot conectado')
    await bot.change_presence(activity=discord.Game(name='--help'))

    while True:
        await asyncio.sleep(3600)
        hora = datetime.now().hour
        if hora == 6:
            c.execute(f"SELECT * FROM bday WHERE dia={date.today().day} AND mes={date.today().month}")
            bday_results = c.fetchall()
            try:
                bday_user_id = bday_results[0][0]
            except:
                bday_user_id = ''
            if bday_user_id != '':
                bday_user = await bot.fetch_user(bday_user_id)
                await bot.get_channel(geral_suamae).send(embed=discord.Embed(title=f'Feliz aniversário {bday_user.name} :partying_face: :partying_face:', color=0x00FF00))


@bot.event
async def on_message(message):
    if message.author.name == 'FredBoat♪♪':
        text = message.content
        translator = google_translator()
        trad = translator.translate(text, lang_tgt='pt')
        #print(trad)
        await message.channel.send(trad)

    if message.content == f'-{PREFIX}help':
        helpembed = discord.Embed(title='Comandos', color=0xFF00FF)
        helpembed.add_field(name='Regras', value='--regras', inline=False)
        helpembed.add_field(name='Pedra papel e tesoura', value='--jokenpo [jogada]', inline=False)
        helpembed.add_field(name='Jogo da velha', value='**iniciar jogo:** --velha -i\n**fazer jogada:** --velha -j [linha][coluna]', inline=False)
        helpembed.add_field(name='Aniversarios', value='--aniversario [dia] [mes]', inline=False)
        helpembed.add_field(name='Lista de aniversariantes', value='--aniversariantes', inline=False)
        helpembed.add_field(name='Criar convite', value='--convite', inline=False)
        await message.channel.send(embed=helpembed)

    if message.content == f'{PREFIX}regras':
        regrasembed = discord.Embed(title='Constituição da sua mãe', color=0xFFF000)
        regrasembed.add_field(name='Lei 1:', value='Não importunar no voice(earrape, mamada no mic, etc...).', inline=False)
        regrasembed.add_field(name='Lei 2:', value='Não spammar no Chat.', inline=False)
        regrasembed.add_field(name='Lei 3: Usar os canais de voz devidamente:', value='''• "papo 10" para conversar; 
        • "aquele lol pica" para League of Legends; 
         • "valoranti" para Valorant;
         • "joguinhos aleatórios" para jogos sem canal;
         • “chat do uol” para World of Warcraft;
         • "shhhhhhh" para ficar em silêncio e o único som permitido é a música do bot;
         • "mini cellbit" para discutir enigmas.''')
        regrasembed.add_field(name='Lei 04: Usar os canais de texto devidamente: ', value='''
            • #geral para conversar;
            • #bot-falando para comandos dos bots; 
            • #cellbitizinho para assuntos relacionados a enigmas; 
            • #chernobyll-cuidado-18 para postar mídia em geral;
            • #mr-robot para postar assuntos relacionados a programação.
            • #valoroso para postar assuntos relacionados a Valorant
        ''', inline=False)
        await message.channel.send(embed=regrasembed)

    if message.content.startswith(f"{PREFIX}jokenpo"):

        if message.author.name != 'seu pai':
            await discord.Message.delete(message)
        global jogada
        jogada = message.content[10:]
        embed = discord.Embed(title="Pedra papel e tesoura", color=0x00ffff, description=f"@{message.author.name} quer jogar, reaja com sua jogada")
        if jogada == 'pedra' or jogada == 'papel' or jogada == 'tesoura':
            global jkpmsg
            jkpmsg = await message.channel.send(embed=embed)
            global results1
            if jogada ==  'pedra':
                results1 = ':punch:'
            if jogada == 'papel':
                results1 = ':hand_splayed:'
            if jogada == 'tesoura':
                results1 = ':v:'
        else:
            await message.channel.send(embed=discord.Embed(title=':x: Jogada inválida!', color=0xFF0000, description='Digite --jokenpo {pedra, papel ou tesoura}'))
        pedra = '👊🏼'
        papel = '🖐🏼'
        tesoura = '✌🏼'
        # or '\U0001f44d' or '👍'
        global msg_id
        global chn_id
        global msg_au
        msg_au = message.author
        chn_id = message.channel.id
        msg_id = jkpmsg.id
        await jkpmsg.add_reaction(pedra)
        await jkpmsg.add_reaction(papel)
        await jkpmsg.add_reaction(tesoura)

    if message.content.startswith(f'{PREFIX}velha -i'):
        global field
        global velhavez
        field = [':white_square_button:', ':white_square_button:', ':white_square_button:', ':white_square_button:',
                 ':white_square_button:', ':white_square_button:', ':white_square_button:', ':white_square_button:',
                 ':white_square_button:']
        msg_au = message.author
        print(field)

    if message.content.startswith(f'{PREFIX}velha') and '-j' not in message.content:
        velhaembed = discord.Embed(title='Jogo da velha', color=0xFFFF00, description=f"{message.author.name} quer jogar \n\n{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]} \n\nReaja # para aceitar ")
        velhaembed.add_field(name='Instruções:', value='--velha -j [linha][coluna] (ex. --velha -j 12)', inline=False)
        velhamsg = await message.channel.send(embed=velhaembed)
        hashtag = '#️⃣'
        global player1
        player1 = message.author.name
        msg_id = velhamsg.id
        await velhamsg.add_reaction(hashtag)

    if message.content.startswith(f'{PREFIX}velha -j'):
        if message.author.name == player1 and velhavez == 1:
            if message.content[11:] == '11' and field[0] == ':white_square_button:':
                field[0] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00, description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '12' and field[1] == ':white_square_button:':
                field[1] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '13' and field[2] == ':white_square_button:':
                field[2] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '21' and field[3] == ':white_square_button:':
                field[3] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '22' and field[4] == ':white_square_button:':
                field[4] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '23' and field[5] == ':white_square_button:':
                field[5] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '31' and field[6] == ':white_square_button:':
                field[6] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '32' and field[7] == ':white_square_button:':
                field[7] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '33' and field[8] == ':white_square_button:':
                field[8] = ':blue_circle:'
                velhavez = 2
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            print(velhavez)
        elif message.author.name == player2 and velhavez == 1:
            await message.channel.send(embed=discord.Embed(title=f'Vez de {player1}', color=0xFF0000))

        if message.author.name == player2 and velhavez == 2:
            if message.content[11:] == '11' and field[0] == ':white_square_button:':
                field[0] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00, description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '12' and field[1] == ':white_square_button:':
                field[1] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '13' and field[2] == ':white_square_button:':
                field[2] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '21' and field[3] == ':white_square_button:':
                field[3] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '22' and field[4] == ':white_square_button:':
                field[4] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '23' and field[5] == ':white_square_button:':
                field[5] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '31' and field[6] == ':white_square_button:':
                field[6] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '32' and field[7] == ':white_square_button:':
                field[7] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            if message.content[11:] == '33' and field[8] == ':white_square_button:':
                field[8] = ':x:'
                velhavez = 1
                velhamsg = await message.channel.send(embed=discord.Embed(title='Jogo da velha', color=0xFFFF00,
                                                                          description=f"{field[0]} {field[1]} {field[2]} \n{field[3]} {field[4]} {field[5]} \n{field[6]} {field[7]} {field[8]}"))
            print(velhavez)
            await message.channel.send(embed=discord.Embed(title=f'Vez de {player1}', color=0xFF0000))
        elif message.author.name == player1 and velhavez == 2:
            await message.channel.send(embed=discord.Embed(title=f'Vez de {player2}', color=0xFF0000))


    if message.content.startswith(f'{PREFIX}aniversario'):
        anidata = message.content[14:]
        dia = anidata[:2]
        mes = anidata[3:5]
        print(dia, mes)
        c.execute(f"SELECT * FROM bday WHERE user={message.author.id}")
        result_check = c.fetchall()

        if len(result_check) == 0:
            c.execute(f"INSERT INTO bday VALUES ('{message.author.id}', '{dia}', '{mes}')")
        else:
            c.execute(f"UPDATE bday SET dia={dia}, mes={mes} WHERE user={message.author.id}")



        await message.channel.send('Aniversario cadastrado!')
        conn.commit()


    if message.content.startswith(f'{PREFIX}aniversariantes'):
        c.execute("SELECT * FROM bday")
        aniversariantes = c.fetchall()
        aniv_txt = ''
        for a in range(0, len(aniversariantes)):
            aniv_user = await bot.fetch_user(aniversariantes[a][0])
            anivv = f'{aniv_user.name} - {aniversariantes[a][1]}/{aniversariantes[a][2]}\n'

            aniv_txt = aniv_txt + anivv
        await message.channel.send(aniv_txt)

        print(c.fetchall())

    if message.content.startswith(f'{PREFIX}convite'):
        link = await message.channel.create_invite(max_uses = 1, max_age = 300, reason=f'Solicitado por {message.author.name}')
        await message.author.send(f'Este convite para o servidor {message.guild.name} só pode ser usado uma vez e irá expirar em 5 minutos\n {link}')

        # arq = open('datas.txt', 'r')
        # for linha in arq[:2]:
        #     print(linha.rstrip())


    if message.content.startswith(f'{PREFIX}tga') and message.author.name in 'ronaalppyabbyzinhaherts a la hood':

        await discord.Message.delete(message)
        global tgamsgid
        global jg_list
        global votos
        votos = []
        global votaram
        votaram = []

        jogos = ''
        jg_list = message.content[6:].split(',')
        for i, j in enumerate(message.content[6:].split(',')):
            jogos += f'{i+1} - {j}\n'

        global tga_msg
        tga_msg = await message.channel.send(embed=discord.Embed(title='Opções', color=0x101DF, description=jogos))
        tgamsgid = tga_msg.id

        global emoji_list
        emoji_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']

        for j in range(0, len(jg_list)):
            await tga_msg.add_reaction(emoji_list[j])


    if message.content.startswith(f'{PREFIX}pontostga'):
        c.execute("SELECT * FROM tga")
        pontoslist = c.fetchall()
        pontos_txt = ''
        for p in pontoslist:
            if p[0] != 'rona':
                patu = f'{p[0]} - {p[1]} pontos\n'
                pontos_txt = pontos_txt + patu
        await message.channel.send(embed=discord.Embed(title='Pontuação', description=pontos_txt, color=0xf0ff00))
        print(pontoslist)

    if message.content.startswith(f'{PREFIX}headtga') and message.author.name in 'ronaalppyabbyzinhaherts a la hood':
        global headtga
        headtga = message.content[10:]

    if message.content.startswith(f'{PREFIX}vencedor') and message.author.name in 'ronaalppyabbyzinhaherts a la hood':
        await discord.Message.delete(message)
        await message.channel.send(embed=discord.Embed(title='Vencedor', description=f'{message.content[10:-2]} ganhou com {message.content[-2:]} pontos', color=0xf0ff00))

@bot.event
async def on_reaction_add(reaction, user):

    try:
        if user.name != 'seu pai' and user.name != msg_au.name:
            #print(user.name)

            if reaction.emoji == '👊🏼' and reaction.message.id == msg_id:
                if jogada.lower() == 'pedra':
                    resultado = 'empate'
                if jogada.lower() == 'papel':
                    resultado = 'j1ganhou'
                if jogada.lower() == 'tesoura':
                    resultado = 'j1perdeu'
                results2 = ':punch:'
            if reaction.emoji == '🖐🏼' and reaction.message.id == msg_id:
                if jogada.lower() == 'pedra':
                    resultado = 'j1perdeu'
                if jogada.lower() == 'papel':
                    resultado = 'empate'
                if jogada.lower() == 'tesoura':
                    resultado = 'j1ganhou'
                results2 = ':hand_splayed:'
            if reaction.emoji == '✌🏼' and reaction.message.id == msg_id:
                if jogada.lower() == 'pedra':
                    resultado = 'j1ganhou'
                if jogada.lower() == 'papel':
                    resultado = 'j1perdeu'
                if jogada.lower() == 'tesoura':
                    resultado = 'empate'
                results2 = ':v:'
            if reaction.emoji != '#️⃣':
                if resultado == 'empate':
                    await discord.Message.delete(jkpmsg)
                    await bot.get_channel(chn_id).send(embed=discord.Embed(title=f'{msg_au.name} e {user.name} empataram', color=0x5F9EA0, description=f'{msg_au.name} {results1} :regional_indicator_x: {results2} {user.name}'))
                if resultado == 'j1ganhou':
                    await discord.Message.delete(jkpmsg)
                    await bot.get_channel(chn_id).send(embed=discord.Embed(title=f'{msg_au.name} ganhou de {user.name}', color=0x00FA9A, description=f'{msg_au.name} {results1} :regional_indicator_x: {results2} {user.name}'))
                if resultado == 'j1perdeu':
                    await discord.Message.delete(jkpmsg)
                    await bot.get_channel(chn_id).send(embed=discord.Embed(title=f'{user.name} ganhou de {msg_au.name}', color=0x00FA9A, description=f'{msg_au.name} {results1} :regional_indicator_x: {results2} {user.name}'))


            if reaction.emoji == '#️⃣' and reaction.message.id == msg_id:
                global player2
                player2 = user.name
                print(player2)
    except: pass

    if user.name != 'seu pai' and reaction.message.id == tgamsgid:


        print(votaram)
        if user.id not in votaram:
            votos.append(f'{user.name},{emoji_list.index(reaction.emoji)+1}')
            print(votos)
            votaram.append(user.id)

        if user.name.lower() in f'{headtga}':
            print(headtga)
            resultado = emoji_list.index(reaction.emoji)+1

            for v in votos:
                if v.split(',')[1] == str(resultado):
                    c.execute(f"SELECT * FROM tga WHERE usertga='{v.split(',')[0]}'")
                    tga_check = c.fetchall()

                    if len(tga_check) == 0:
                        c.execute(f"INSERT INTO tga VALUES ('{v.split(',')[0]}', '1')")
                    else:
                        c.execute(f"UPDATE tga SET pontos={int(tga_check[0][1])+1} WHERE usertga='{v.split(',')[0]}'")
                    conn.commit()

@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name="Mortais")
    await member.add_roles(role)



bot.run(TOKEN)
