import discord
from discord.ext import commands
import random, time
import os
import subprocess
import asyncio
from prettytable import PrettyTable
import public_ip as ip_lib
import csv

import data as xdata

client = commands.Bot(intents=discord.Intents.all(), command_prefix="Firefly.")

bot_channel = 716889120814923817
general = 716889730716925972
rules = 716886040849154129

KEY = input("KEY >>> ")


@client.event
async def on_ready():
    print("ready")
    # channel = client.get_channel(general)
    # await channel.send(f"Ready!")


@client.event
async def on_member_join(member):
    channel = general
    #ctx.channel.send(f"{member.mention} Has Joined!\nPlease Visit #rules For Server Rules")

    user = member
    embed = discord.Embed(title="Welcome!",
                          description="This is Firefly, a management bot made by Alex to help moderate the server.",
                          color=0x109319)
    embed.add_field(name="Thanks for joining!",
                    value="Thank you for joining the CSE Coding Club's official discord server!\nWe just need to confirm you are part of the club.",
                    inline=False)
    embed.add_field(name="Phone Number",
                    value="Kindly submit your phone number for verification.",
                    inline=True)
    embed.add_field(name="Command",
                    value="Firefly.verify <phone-num> where a sample phone num is 58907363 - no spaces or (+230)\n**Firefly.verify 58907363**",
                    inline=True)
    embed.set_footer(text="Message Alex (president) in case of issues")

    await member.send(embed=embed)


@client.event
async def on_member_leave(member, ctx):
    channel = general
    ctx.channel.send(f"{member.mention} Has Left! Farewell")


@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.channel.send(f'{(ctx.message.author).mention} Firefly Pinged! {latency} ms')


@client.command()
async def clear(ctx, amount=5):
    if str(ctx.message.author) == xdata.admin:
        await ctx.channel.purge(limit=(amount + 1))


@client.command()
async def doge(ctx):
    # await ctx.channel.send(file = discord.File(xdata.parent_folder + "/Doge-Meme-PNG-File.png"))
    await ctx.channel.send(file=discord.File("./Doge-Meme-PNG-File.png"))


@client.command()
async def swear(ctx):
    # channel = client.get_channel(bot_channel)
    if random.randint(1, 50) == 50:
        await ctx.channel.send(xdata.ultra_swear)
    else:
        await ctx.channel.send(random.choice(xdata.swear_list))


@client.command()
async def whereserver(ctx):
    if str(ctx.message.author) not in xdata.users:
        await ctx.channel.send("You do not have the permission to view my public IP.")
        return 0

    ip_addr = ip_lib.get()

    await ctx.channel.send(file="./whereserver.gif")
    await ctx.channel.send(f"Here's my IPv4 Address: {ip_addr}")


@client.command()
async def verify(ctx, phone_num):
    user = ctx.message.author
    rows = getRows()
    # check that the phone number format is correct
    if False in [num in "0123456789" for num in phone_num] or already_reg(user, phone_num, rows):
        embed = discord.Embed(title="Invalid Phone Number!",
                              description="The phone number input does not appear to be in the right format or it has already been registered.",
                              color=0x109319)
        embed.add_field(name="Try This:",
                        value="The phone number must not have spaces or country code.",
                        inline=False)
        await user.send(embed=embed)
        return 0

    # get the data from the CSV
    # check that the person has paid
    if checkPaid(rows, phone_num) == False:
        embed = discord.Embed(title="Not a Member!",
                              description="It would appear you have not paid the membership fee.",
                              color=0x109319)
        embed.add_field(name="But I did pay!",
                        value="Human error is possible and your phone number may be incorrect. If you still have trouble, contact Alex for help.",
                        inline=False)
        await user.send(embed=embed)
        return 0

    name, grade = modifyCSV(user, phone_num, rows)

    async def chnick(ctx,member: discord.Member,nick):
        await member.edit(nick=nick)

    async def roles(ctx,user: discord.Member, server, grade):
        #set_role(ctx, user, grade)
        role_txt = "Grade " + str(grade)
        role = discord.utils.get(server.roles, name=role_txt)
        await user.add_roles(role)
        if int(grade) <= 10:
            role_txt = "Junior"
        else:
            role_txt = "Senior"
        role = discord.utils.get(server.roles, name=role_txt)
        await user.add_roles(role)
        # change name of the dude


    user_id = user.id

    server = client.get_guild(1079303552322768896)
    member = server.get_member(user_id)

    await chnick(ctx,member,name)
    await roles(ctx,member,server, grade)

    embed = discord.Embed(title="Success!",
        description="Congratulations on verifying!",
        color=0x109319)

    await user.send(embed=embed)


def getRows():
    file_addr = "./members.csv"
    with open(file_addr, "r") as csvfile:
        csvhandle = csv.reader(csvfile, delimiter=",")
        rows = [row for row in csvhandle]
    return rows


def checkPaid(csvmatrix, phone_num):
    return phone_num in [row[4] for row in csvmatrix if row[7] == "Paid"]


def modifyCSV(discord_username, phone_no, rows):
    new_matrix = []
    for row in rows:
        if phone_no == row[4]:
            name = row[1]
            grade = row[2]
            row.append(discord_username)
        new_matrix.append(row)

    file_addr = "./members.csv"
    with open(file_addr, "w") as csvfile:
        csvhandle = csv.writer(csvfile, delimiter=",")
        csvhandle.writerows(new_matrix)

    return name, grade


def already_reg(discord_username, phone_no, rows):
    for row in rows:
        if discord_username in row:
            return True

        if row [-1] != "Paid":
            #there's already a username there
            return True

    return False
'''
def set_role(ctx, user, grade):
    # usr: discord.Member
    member = ctx.message.author

    role_txt = str(grade)
    role = get(member.server.roles, name=role_txt)
    await user.add_roles(role)

    if int(grade) <= 10:
        role_txt = "Junior"
    else:
        role_txt = "Senior"

    role = get(member.server.roles, name=role_txt)
    await user.add_roles(role)
'''

'''
@client.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')
'''

'''
@client.command()
async def who_online(ctx):
    files = []
    for file in os.listdir(xdata.logs):
        if os.path.isfile(os.path.join(xdata.logs, file)):
            files.append(file)

    #create dictionary
    latest_log = "/" + max(files)
    user_state = {}
    for user in xdata.user_xbox:
        user_state[user] = False

    #open file and change user states
    with open(xdata.logs+latest_log,"r") as file:
        lines = file.readlines()
        for line in lines:
            for user in xdata.user_xbox:
                if user in line:
                    user_state[user] = not user_state[user]

    string = ""
    for key,key_data in user_state.items():
        if key_data:
            key_data = "Online"
        else:
            key_data = "Offline"

        string +=  key + " : " + str(key_data) + "\n"

    await ctx.channel.send(string)
'''

'''
@client.command()
async def start_server(ctx):
    text_return = subprocess.check_output("/home/alex/minecraftbe/MC/start.sh")
    await ctx.channel.send(text_return)
'''


@client.command()
async def halp(ctx):
    await ctx.channel.send(cmds)


cmds = "ping,clear,doge,swear,whereserver"
client.run(KEY)
