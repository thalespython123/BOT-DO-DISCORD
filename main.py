import random
import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
#salamaria

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def nigri(ctx, count_nigri = 5):
    await ctx.send("nigri" * count_nigri)



@bot.command()
async def butija(ctx, nome):
    await ctx.send(f'{nome} butijon!')

@bot.command()
async def porcodeceia(ctx, nome):
    await ctx.send(f'{nome} Porco de ceia!')


@bot.command()
async def conta(ctx, nome):
    await ctx.send(f'entrando na conta bancaria do {nome}!')
import random

memes = ["https://cdn.discordapp.com/attachments/1445871504616194079/1467057024885063855/RDT_20260130_1205496604839311278130901.gif?ex=6abc0f93&is=6ababe13&hm=484e4b1670ed3a6c8cd1123f04bfc297aab8d26511f15e8b806b70a12cf17aec",
         "https://tenor.com/view/roblox-bacon-hair-bacon-hair-dance-gif-18121336341116932036",
         "https://tenor.com/view/breaking-bad-heisenberg-dance-crazy-dance-party-gif-6874111392045692480",
         "https://tenor.com/view/dog-bird-flying-gif-17884683403270491620",
         "https://tenor.com/view/partying-cat-party-cat-cute-cat-kitten-gif-22225605",]

# area de meme secundaria, apagar se precisar

@bot.command()
async def imagem_salamer(ctx):

    imagens = os.listdir("../Screenshots")

    imagem = random.choice(imagens)

    with open(f"../Screenshots/{imagem}", "rb") as foto:
        arquivo = discord.File(foto)

        await ctx.send("FOTO BIZARRA", file=arquivo)



# area de meme secundaria, apagar se precisar
@bot.command()
async def meme(ctx):
    await ctx.send(random.choice(memes))

@bot.command()
async def soma(ctx, numero_1 , numero_2):
    await ctx.send(f"{int(numero_1)} + {int(numero_2)} = {int(numero_1) + int(numero_2)}")

@bot.command()
async def somaburra(ctx, numero_1 , numero_2):
    await ctx.send(f"{(numero_1)} + {(numero_2)} = {(numero_1) + (numero_2)}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f'Bem-vindo {member.mention} a {guild.name}!😁')

async def anunciar(guild, mensagem):
    if guild.system_channel is not None:
        await guild.system_channel.send(mensagem)

#area de teste, apagar se precisar

@bot.event
async def on_member_remove(member):
    guild = member.guild
    await asyncio.sleep(1)  # dá tempo de o registro de auditoria ser criado
    
    try:
        # Se foi banimento, o on_member_ban já anuncia: não duplicar
        async for entrada in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            recente = (discord.utils.utcnow() - entrada.created_at).total_seconds() < 10
            if entrada.target and entrada.target.id == member.id and recente:
                return

        # Verifica se foi expulsão
        async for entrada in guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
            recente = (discord.utils.utcnow() - entrada.created_at).total_seconds() < 10
            if entrada.target and entrada.target.id == member.id and recente:
                motivo = entrada.reason or 'sem motivo informado'
                autor = entrada.user.mention if entrada.user else 'um moderador'
                await anunciar(
                    guild,
                    f'👢 **{member}** foi expulso por {autor}. Motivo: {motivo}'
                )
                return
    except discord.Forbidden:
        pass  # sem permissão para ver o registro: trata como saída comum

    await anunciar(guild, f'👋 **{member}** saiu do servidor.')


@bot.event
async def on_member_ban(guild, user):
    await asyncio.sleep(1)
    motivo = 'sem motivo informado'
    autor = None

    try:
        async for entrada in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entrada.target and entrada.target.id == user.id:
                motivo = entrada.reason or motivo
                autor = entrada.user
                break
    except discord.Forbidden:
        pass

    por = f' por {autor.mention}' if autor else ''
    await anunciar(guild, f'🔨 **{user}** foi banido{por}. Motivo: {motivo}')

@bot.event
async def on_member_update(before, after):
    if before.timed_out_until == after.timed_out_until:
        return

    if after.timed_out_until is not None:
        ate = discord.utils.format_dt(after.timed_out_until, style='R')
        await anunciar(after.guild, f'🔇 {after.mention} Recebeu timeout!. Termina {ate}.')
    else:
        await anunciar(after.guild, f'🔊 {after.mention} teve o timeout removido!.')


#area de teste, apagar se precisar


bot.run('TOKEN AQUI')
