import json
import random
import nextcord 
import requests
import colorama
import cooldowns
import asyncio
from case import case_all
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.utils import get
from nextcord.ext.commands import has_permissions, has_role

colorama.init(autoreset=True)

try:
    with open("config.json", "r") as file:
        config = json.load(file)
except:
    print(colorama.Fore.RED + "конфиг не найден")
    input()
else:
    print(colorama.Fore.GREEN + "конфиг найден, подключение")

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)
bot.remove_command("help")

admins = [
    977137333528821780,
    386186596182917122,
    926018668557643827
]

roles = {
        "фиолетовый": {
            "id": 1091661823322898475,
            "price": 5000,
            "ping": "<@&1091661823322898475>"
        },

        "желтый": {
            "id": 1091661754083315754,
            "price": 6000,
            "ping": "<@&1091661754083315754>"
        },

        "зеленый": {
            "id": 1091661517583294475,
            "price": 7000,
            "ping": "<@&1091661517583294475>"
        },

        "розовый": {
            "id": 1091661619374870651,
            "price": 7000,
            "ping": "<@&1091661619374870651>"
        },

        "оранжевый": {
            "id": 1091661324448174090,
            "price": 7000,
            "ping": "<@&1091661324448174090>"
        },

        "голубой": {
            "id": 1091943113347563600,
            "price": 10000,
            "ping": "<@&1091943113347563600>"
        },

        "сиреневый": {
            "id": 1091661096810729472,
            "price": 50000,
            "ping": "<@&1091661096810729472>"
        },

        "черный": {
            "id": 1091660997489606706,
            "price": 100000,
            "ping": "<@&1091660997489606706>"
        },

        "красный": {
            "id": 1091661428387237888,
            "price": 500000,
            "ping": "<@&1091661428387237888>"
        },

        "белый": {
            "id": 1092976540758851694,
            "price": 700000,
            "ping": "<@&1092976540758851694>"
        },

        "элита": {
            "id": 1092977116112507053,
            "price": 1000000,
            "ping": "<@&1092977116112507053>"
        }
    }

base_skins = {
    1:  0, 10: 0,
    2:  0, 11: 0,
    3:  0, 12: 0,
    4:  0, 13: 0,
    5:  0, 14: 0,
    6:  0, 15: 0,
    7:  0, 16: 0,
    8:  0, 17: 0,
    9:  0, 18: 0,
    19: 0, 20: 0,
    21: 0
}

with open("globalEconomic.json", "r") as file:
    economic = json.load(file)

WALLET_DEFAULT = {"balance": 100}

async def get_user_wallet(user_id):
    user_id = str(user_id)

    with open("database/wallets.json", "r") as file:
        users_wallets = json.load(file)

    if user_id not in users_wallets.keys():
        users_wallets[user_id] = WALLET_DEFAULT

    with open("database/wallets.json", "w") as file:
        json.dump(users_wallets, file)

    return users_wallets[user_id]

async def get_balance_top():

    users = []

    with open("database/wallets.json", "r") as file:
        users_wallets = json.load(file)

        for user_id in users_wallets:
            users.append(user_id)

        maximal = max(users)
        minimal = min(users)

        all_top = [minimal, maximal]

    return all_top

async def set_user_wallet(user_id, parameter=None, new_value=None):
    user_id = str(user_id)

    with open("database/wallets.json", "r") as file:
        users_wallets = json.load(file)

    if user_id not in users_wallets.keys():
        users_wallets[user_id] = WALLET_DEFAULT

    users_wallets[user_id][parameter] = new_value

    with open("database/wallets.json", "w") as file:
        json.dump(users_wallets, file)

async def get_check_info(check):

    with open("database/checks.json", "r") as file:
        checks_json = json.load(file)

    if (check not in checks_json.keys()):
        return "чек не был найден"
    
    else:
        return checks_json[check]
    
async def set_check_info(check, user_id, role, role_id):

    with open("database/checks.json", "r") as file:
        checks_json = json.load(file)

    if (check in checks_json.keys()):
        return "такой чек уже есть"
    
    if (check not in checks_json.keys()):
        checks_json[check] = {"id": user_id, "role": role, "roleID": role_id}

        with open("database/checks.json", "w") as file:
            json.dump(checks_json, file)

async def get_skin(user_id, id):
    user_id = str(user_id)
    
    with open("database/skins.json", "r") as file:
        skins_json = json.load(file)

    if (user_id not in skins_json.keys()):
        skins_json[user_id] = base_skins

    with open("database/skins.json", "w") as file:
        json.dump(skins_json, file)

    return skins_json[user_id][id]

async def set_skin(user_id, id, count):
    user_id = str(user_id)

    with open("database/skins.json", "r") as file:
        skins_json = json.load(file)  

    if (user_id not in skins_json.keys()):
        skins_json[user_id] = base_skins

    user_id[str(id)] = count

    with open("database/skins.json", "w") as file:
        json.dump(skins_json, file)

async def sell_skin(user_id, id):

    with open("database/skins.json", "r") as file:
        skins_json = json.load(file)

    if (user_id not in skins_json.keys()):
        skins_json[user_id] = base_skins
        return "у вас нет скинов!"
    
    else:
        user_bal = await get_user_wallet(user_id)
        skins_json[user_id][id] - 1    
        await set_user_wallet(user_id, "balance", user_bal+case_all[id]["price"])

        with open("database/skins.json", "w") as file:
            json.dump(skins_json, file)

@bot.event
async def on_ready():
    channel = bot.get_channel(int(config["log"]))
    print(colorama.Fore.GREEN + "к службе готов!")
    await channel.send("```| бот был запущен, айди: {0} |```".format("None"))
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name=f"/help"))

@bot.event
async def on_command_error(ctx, error):
    if (isinstance(error, commands.MissingPermissions)):
        await ctx.send("у вас нет прав на выполнение данной команды")

    if (isinstance(error, cooldowns.CallableOnCooldown)):

        embed = nextcord.Embed(
            title="таймаут!",
            description="подождите {0}".format(economic["cooldown"]),
            color=nextcord.Color.purple()
        )
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

        await ctx.send(embed=embed)

    if (isinstance(error, commands.CommandOnCooldown)):
        await ctx.send("подождите `{0}` секунд для использования команды".format(economic["cooldown"]))

@bot.event
async def on_application_command_error(inter: nextcord.Interaction, error):
    error = getattr(error, "original", error)

    if isinstance(error, cooldowns.CallableOnCooldown):
        embed = nextcord.Embed(
            title="таймаут!",
            description="подождите `{0}` секунд!".format(error.retry_after),
            color=nextcord.Color.purple()
        )
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await inter.send(embed=embed)

    else:
        raise error

@bot.slash_command(name="dance", description="танец")
async def dance(ctx):
    embed = nextcord.Embed(
        title="{0} танцует".format(ctx.user.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/GOYRQva4UeoAAAAd/anime-dance.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="whaaa", description="удивление")
async def whaaa(ctx):
    embed = nextcord.Embed(
        title="{0} удивился".format(ctx.user.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/o39q7qPq24gAAAAM/k-on-yui.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="smile", description="улыбнуться")
async def smile(ctx):
    embed = nextcord.Embed(
        title="{0} улыбнулся".format(ctx.user.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/3S9l9HzhGVcAAAAM/shake-kaninayuta.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="scare", description="испугался")
async def scare(ctx, username: nextcord.User=None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} испугался".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/x4TPrE9RvQgAAAAM/marin-marin-kitagawa.gif")
        await ctx.send(embed=embed)
    
    else:
        embed = nextcord.Embed(
            title="{0} испугался {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/x4TPrE9RvQgAAAAM/marin-marin-kitagawa.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="no", description="отрицать")
async def no(ctx, username: nextcord.User=None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} отрицает".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/up1YgR4VdkMAAAAM/vtuber-foxplushy.gif")
        await ctx.send(embed=embed)

    else:
        embed = nextcord.Embed(
            title="{0} отрицает {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/up1YgR4VdkMAAAAM/vtuber-foxplushy.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="love", description="любить")
async def love(ctx, username: nextcord.User=None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} влюбился".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/PGXshKPAUh4AAAAM/my-dress-up-darling-anime-love.gif")
        await ctx.send(embed=embed)

    else:

        embed = nextcord.Embed(
            title="{0} влюбился в {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/PGXshKPAUh4AAAAM/my-dress-up-darling-anime-love.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="sad", description="грустить")
async def sad(ctx, username: nextcord.User = None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} грустит".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/n-TmmTy2NdkAAAAM/%D0%BD%D0%B0%D0%B0%D0%B2%D1%83.gif")
        await ctx.send(embed=embed)

    else:
        embed = nextcord.Embed(
            title="{0} грустит по {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/n-TmmTy2NdkAAAAM/%D0%BD%D0%B0%D0%B0%D0%B2%D1%83.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="hug", description="обнять")
async def hug(ctx, username: nextcord.User):
    embed = nextcord.Embed(
        title="{0} обнимает {1}".format(ctx.user.name, username.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/yc_shX2Xl_QAAAAM/girl-anime.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="pat", description="гладить")
async def pat(ctx, username: nextcord.User):
    embed = nextcord.Embed(
        title="{0} гладит {1}".format(ctx.user.name, username.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/9R7fzXGeRe8AAAAC/fantasista-doll-anime.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="kiss", description="целовать")
async def kiss(ctx, username: nextcord.User):
    embed = nextcord.Embed(
        title="{0} целует {1}".format(ctx.user.name, username.name),
        color=nextcord.Color.purple()
    )
    embed.set_image(url="https://media.tenor.com/el8DHxNp9IsAAAAM/kiss-anime-love.gif")
    await ctx.send(embed=embed)

@bot.slash_command(name="cry", description="плакать")
async def cry(ctx, username: nextcord.User = None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} плачет".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/VcdTcSy-sJMAAAAM/sad-cry.gif")
        await ctx.send(embed=embed)

    else:
        embed = nextcord.Embed(
            title="{0} плачет по {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/VcdTcSy-sJMAAAAM/sad-cry.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="yes", description="согласиться")
async def yes(ctx, username: nextcord.User = None):

    if (username is None):

        embed = nextcord.Embed(
            title="{0} соглашается".format(ctx.user.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/_2dT6aW89tkAAAAM/keppeki-danshi-aoyama-kun-clean-freak-aoyama-kun.gif")
        await ctx.send(embed=embed)

    else:
        embed = nextcord.Embed(
            title="{0} соглашается с {1}".format(ctx.user.name, username.name),
            color=nextcord.Color.purple()
        )
        embed.set_image(url="https://media.tenor.com/_2dT6aW89tkAAAAM/keppeki-danshi-aoyama-kun-clean-freak-aoyama-kun.gif")
        await ctx.send(embed=embed)

@bot.slash_command(name="youtube", description="ссылка на ютуб канал стримера HeeDina")
async def youtube(ctx):
    await ctx.send("нажми: ||https://youtube.com/@HeeDina||")

@bot.slash_command(name="donate", description="ссылка на донат для стримера HeeDina")
async def donate(ctx):
    await ctx.send("нажми: ||https://www.donationalerts.com/r/dinokhee||")

@bot.slash_command(name="links", description="все ссылки стримера HeeDina")
async def links(ctx):
    embed = nextcord.Embed(
        title="ссылки",
        description="все ссылки стримера HeeDina",
        color=nextcord.Color.purple()
    )
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    embed.add_field(name="youtube", value="https://youtube.com/@HeeDina")
    embed.add_field(name="omlet arcade", value="https://omlet.gg/profile/hee.dina.")
    embed.add_field(name="telegram", value="https://t.me/p7qp2")
    embed.add_field(name="donate", value="https://www.donationalerts.com/r/dinokhee")
    
    await ctx.send(embed=embed)

@has_permissions(administrator=True)
@bot.slash_command(name="say", description="сказать от лица бота (ДОСТУПНО ТОЛЬКО АДМИНИСТРАЦИИ)")
async def say(ctx, message, channel_id):

    if (not ctx.user.guild_permissions.administrator):
        await ctx.send("у вас нет прав на использование данной команды")
        return

    try:
        channel = bot.get_channel(int(channel_id))
    except:
        await ctx.send("ошибка, не верное ID канала")
    else:
        try:
            await channel.send(message)
            await ctx.send("сообщение отправлено!")
        except:
            await ctx.send("ошибка! не удалось отправить сообщение")

@bot.slash_command(name="profile", description="просмотр профилей платформы Omlet Arcade")
async def profile(ctx, username):

    embed = nextcord.Embed(
        title="информация об аккаунте {0}".format(username),
        color=nextcord.Color.purple()
    )
    embed.set_author( name=username, icon_url=requests.get("https://omapi.ru/api/user/getAvatar?username={0}&token=default".format(username))
            .json()["result"])
    
    embed.add_field(name="кол-во подписок", 
                    
        value=requests.get(f"https://omapi.ru/api/user/getFollowsCount?username={username}&token=default")
            .json()["result"])
    embed.add_field(name="кол-во подписчиков", 
                    
        value=requests.get("https://omapi.ru/api/user/getFollowersCount?username={0}&token=default".format(username))
            .json()["result"])
    
    embed.add_field(name="уровень", 
                    
        value=requests.get("https://omapi.ru/api/user/getLevel?username={0}&token=default".format(username))
            .json()["result"])
    
    response = requests.get("https://omapi.ru/api/user/isVerified?username={0}&token=default".format(username)).json()["result"]

    if (response == True):
        embed.set_footer(icon_url="https://images-ext-1.nextcordapp.net/external/2Akz2zlcrMVeCtytlYNWGWFeQmmCzmEaW6PXGkq-h4k/https/relationsai.com/wp-content/uploads/2021/07/23.png", text="аккаунт верифицирован платформой omlet arcade!")
    
    await ctx.send(embed=embed)

@bot.slash_command(name="members", description="список участников на сервере")
async def members(ctx):

    for guild in bot.guilds: ...

    embed = nextcord.Embed(
        title="участники на сервере",
        description=f"на данный момент на сервере находится {len(guild.members)} участника",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="количество ботов на сервере", value=len(guild.bots))
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    await ctx.send(embed=embed)

@bot.slash_command(name="case", description="открытие кейсов из игры CS:GO")
@cooldowns.cooldown(1, 5, bucket=cooldowns.SlashBucket.author)
async def case(ctx):

    embed = nextcord.Embed(
        title="вам выпало...",
        color=nextcord.Color.purple()
    )
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    
    skin = random.choice(case_all)

    if (skin == 0):
        skin = 1

    moneys = await get_user_wallet(ctx.user.id)

    if (moneys["balance"] < 250):
        await ctx.send("у вас недостаточно денег!")
        return

    embed.set_image(url=skin["img"])
    embed.add_field(name="айди скина", value=skin["id"])
    embed.add_field(name="цена", value=skin["price"])

    await ctx.send(embed=embed)
    await ctx.send("с продажи скина вы получили {0} печенек!".format(skin["price"]))
    await set_user_wallet(ctx.user.id, "balance", moneys["balance"]+skin["price"]-250)

@has_permissions(administrator=True)
@bot.slash_command(name="news", description="новости (ТОЛЬКО ДЛЯ РАЗРАБОТЧИКА И АДМИНИСТРАТОРОВ СЕРВЕРА)")
async def news(ctx, message):

    if (not ctx.user.guild_permissions.administrator):
        await ctx.send("у вас нет прав на использование данной команды")
        return
    
    channel = bot.get_channel(938502139477651476)

    embed = nextcord.Embed(
        title="обновление бота",
        description=f"`{message}`",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="версия", value=config["version"])
    embed.set_author(name=ctx.user.name, icon_url=ctx.user.icon_url)

    await ctx.send(embed=embed)

@bot.slash_command(name="daily", description="ежедневный бонус")
@cooldowns.cooldown(1, 43200, bucket=cooldowns.SlashBucket.author)
async def daily(ctx):

    moneys = await get_user_wallet(ctx.user.id)
    await set_user_wallet(ctx.user.id, "balance", moneys["balance"]+economic["daily"])

    embed = nextcord.Embed(
        title="ежедневный бонус",
        description="вы получили {0}".format(economic["daily"]),
        color=nextcord.Color.purple()
    )
    embed.add_field(name="повторите команду через", value="12 часа")
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

    await ctx.send(embed=embed)

@bot.slash_command(name="pay", description="платеж")
@cooldowns.cooldown(1, 2, bucket=cooldowns.SlashBucket.author)
async def pay(ctx, user: nextcord.User, amount):
    
    moneys = await get_user_wallet(ctx.user.id)
    user_moneys = await get_user_wallet(user.id)
    
    if (int(amount) < 0):
        await ctx.send("вы не можете совершить перевод на сумму которая меньше нуля!")
        return
    
    await set_user_wallet(ctx.user.id, "balance", int(moneys["balance"])-int(amount))
    await set_user_wallet(user.id, "balance", int(user_moneys["balance"])+int(amount)-economic["commission"])
    
    embed = nextcord.Embed(
    	title="успешный перевод!",
        description=f"совершен платеж на сумму {amount}",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="получатель", value=user.name)
    embed.add_field(name="комиссия", value=economic["commission"])
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    
    await ctx.send(embed=embed)


@bot.slash_command(name="casino", description="казино, есть шанс выйграть много денег)")
@cooldowns.cooldown(1, 5, bucket=cooldowns.SlashBucket.author)
async def casino(ctx, amount:int):

    user_wallet = await get_user_wallet(ctx.user.id)


    if (amount is None):
        await ctx.send("вы должны поставить какую-то сумму!")
        return
    
    if (user_wallet["balance"] < amount):
        await ctx.send("у вас не хватает денег")

    if (amount < 0):
        await ctx.send("вы не можете поставить ставку которая будет меньше нуля!")

    else:
        casino_var = ["no", "yes"]

        result = random.choice(casino_var)

        if (result == casino_var[0]):
            await set_user_wallet(ctx.user.id, "balance", user_wallet["balance"]-amount)

            embed = nextcord.Embed(
                title="результат",
                description="результат: ||вы проиграли!:cookie:||",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="ваша ставка", value=amount)
            embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

            await ctx.send(embed=embed)

        if (result == casino_var[1]):
            await set_user_wallet(ctx.user.id, "balance", user_wallet["balance"]+amount)

            embed = nextcord.Embed(
                title="результат",
                description="результат: ||вы выиграли!:cookie:||",
                color=nextcord.Color.purple()
            )
            embed.add_field(name="ваша ставка", value=amount)
            embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

            await ctx.send(embed=embed)

@bot.slash_command(name="return", description="вернуть деньги потраченные за роль")
async def ret(ctx, check=None):

    if (check is None): 
        await ctx.send("нужен чек для возврата валюты!")
    
    else:
        try:
            ch = await get_check_info(check)
        except:
            await ctx.send("убедитесь правильности написания вашего чека или обратитесь к администрации")
            return 
        else:
            if (ctx.user.id == ch["id"]):
                await ctx.send("запрос принят!")

                guild = bot.get_guild(923235153000661003)
                getRole = guild.get_role(roles[ch["role"]]["id"])

                await ctx.user.remove_roles(getRole)
                
                moneys = await get_user_wallet(ctx.user.id)
                get_role_price = roles[ch["role"]]["price"] / 2

                await set_user_wallet(ctx.user.id, "balance", moneys["balance"]+get_role_price)

                embed = nextcord.Embed(
                    title="успешно!",
                    description="вам вернули 50% от суммы роли",
                    color=nextcord.Color.purple()
                )
                embed.add_field(name="роль которая была отобрана", value="<@&{0}>".format(ch["roleID"]))
                embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

                await ctx.send(embed=embed)
            else:
                await ctx.send("это не ваш чек!")

@bot.slash_command(name="check", description="информация о чеке")
async def getChechInfo(ctx, check):
    
    if (not ctx.user.guild_permissions.administrator):
        await ctx.send("у вас нет прав на использование данной команды")
        return    
    
    get_info = await get_check_info(check)
    
    embed = nextcord.Embed(
        title="информация по чеку",
        description=f"чек: {check}",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="владелец чека", value="<@{0}>".format(get_info["id"]))
    embed.add_field(name="айди", value=get_info["id"])
    embed.add_field(name="товар", value=get_info["role"])
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    
    await ctx.send(embed=embed)

@bot.slash_command(name="startevent", description="запускает ивент")
async def start_event(ctx, message:str, prize:str, everyone:bool, time:int, winners_count:int):

    channel = bot.get_channel(938502139477651476)

    embed = nextcord.Embed(
        title="стартует конкурс",
        description=f"{message}",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="результаты через", value=f"{time*60}" + " минут")
    embed.add_field(name="количество победителей", value=winners_count)
    embed.add_field(name="приз", value=f"{prize}")
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

    if (everyone == True):
        await channel.send("@everyone")
    
    await channel.send(embed=embed)
    await asyncio.sleep(time)

    await channel.send(f"время закончилось! время выбора победителей, `ожидание`")

@bot.slash_command(name="buy", description="покупка роли в магазине")
async def buy(ctx, role=None):

    user_wallet = await get_user_wallet(ctx.user.id)

    SYMBS = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890"

    check = "".join(random.choice(SYMBS) for i in range(6))

    if (role is None):
        await ctx.send("выберите роль из списка! `/shop`")
    
    if (role not in roles.keys()):
        await ctx.send("роль должна быть из списка магазина! `/shop`")

    if (user_wallet["balance"] < roles[role]["price"]):
        await ctx.send("у вас не достаточно денег!")

    else:
        guild = bot.get_guild(923235153000661003)
        getRole = guild.get_role(roles[role]["id"])

        await set_user_wallet(ctx.user.id, "balance", user_wallet["balance"] - roles[role]["price"])
        await ctx.user.add_roles(getRole)
        await set_check_info(check=f"#{check}", user_id=ctx.user.id, role=role, role_id=roles[role]["id"])

        embed = nextcord.Embed(
            title="успешная покупка!",
            description=f"вы купили роль!",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="ваш чек", value=f"#{check}")
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)
    
@bot.slash_command(name="balance", description="ваш личный счет")
async def balance(ctx, username:nextcord.User=None):

    if (username is None):
        user_wallet = await get_user_wallet(ctx.user.id)
        
        embed = nextcord.Embed(
            title="ваш баланс",
            description="на вашем счете `{0}` :cookie:".format(user_wallet["balance"]),
            color=nextcord.Colour.purple()
        )
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        embed.add_field(name="для работы пропишите", value="/work")
        await ctx.send(embed=embed)

    else:
        user_wallet = await get_user_wallet(username.id)
        
        embed = nextcord.Embed(
            title=f"баланс {username.name}",
            description="на счете {0} `{1}` :cookie:".format(username.mention, user_wallet["balance"]),
            color=nextcord.Colour.purple()
        )
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        embed.add_field(name="для работы пропишите", value="/work")
        await ctx.send(embed=embed)

@bot.slash_command(name="change", description="смена баланса (ТОЛЬКО ДЛЯ АДМИНИСТРАЦИИ)")
async def change_balance(ctx, user_mention=None, amount=None):

    if (not ctx.user.guild_permissions.administrator):
        await ctx.send("у вас нет прав на использование данной команды")
        return

    user = get(ctx.guild.members, id=int(user_mention[2:-1]))
    user_wallet = await get_user_wallet(user.id)
    user_wallet["balance"] += int(amount)
    await set_user_wallet(user.id, "balance", user_wallet['balance'])

    embed = nextcord.Embed(
        title="изменен баланс!",
        description="теперь у {0} стало {1} :cookie:".format(user.name, user_wallet["balance"]),
        color=nextcord.Color.purple()
    )
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    embed.add_field(name="баланс был изменен администратором", value=ctx.user.name)
    await ctx.send(embed=embed)

@bot.slash_command(name="work", description="заработок денег")
@cooldowns.cooldown(1, economic["cooldown"], bucket=cooldowns.SlashBucket.author)
async def work(ctx):

    min_num = economic["getWorkMoney"][0]
    max_num = economic["getWorkMoney"][1]

    value = random.randint(min_num, max_num)

    user_wallet = await get_user_wallet(ctx.user.id)
    user_wallet["balance"] += int(value)
    await set_user_wallet(ctx.user.id, "balance", user_wallet['balance'])

    embed = nextcord.Embed(
        title="рабочий день закончен!",
        description="повторите команду через `{0}`".format(economic["cooldown"]),
        color=nextcord.Color.purple()
    )
    embed.add_field(name="вы заработали", value=str(value))
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

    await ctx.send(embed=embed)

@bot.slash_command(name="stats", description="статистика по балансу")
async def stats(ctx):
    top = await get_balance_top()

    embed = nextcord.Embed(
        title="топ сервера",
        color=nextcord.Color.purple()
    )
    embed.add_field(name="самый богатый", value=f"<@{top[0]}>")
    embed.add_field(name="самый бедный", value=f"<@{top[1]}>")
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")

    await ctx.send(embed=embed)

@bot.slash_command(name="shop", description="магазин")
async def shop(ctx):

    embed = nextcord.Embed(
        title="магазин",
        description=f"""
        <@&1092977116112507053> - цена 1000000:cookie:
        <@&1092976540758851694> - цена 700000:cookie:
        <@&1091661428387237888> - цена 500000:cookie:
        <@&1091660997489606706> - цена 100000:cookie:
        <@&1091661096810729472> - цена 50000:cookie:
        <@&1091943113347563600> - цена 10000:cookie:
        <@&1091661324448174090> - цена 7000:cookie:
        <@&1091661619374870651> - цена 7000:cookie:
        <@&1091661517583294475> - цена 7000:cookie:
        <@&1091661754083315754> - цена 6000:cookie:
        <@&1091661823322898475> - цена 5000:cookie:
        """,
        color=nextcord.Color.purple()
    )
    embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
    embed.add_field(name="как купить?", value="пропишите /buy и цвет роли")
    embed.add_field(name="покупка кейса", value="пропишите /case")

    await ctx.send(embed=embed)

@bot.slash_command(name="help", description="помощь по командам")
async def help(ctx, category=None):

    if (category is None):
        embed = nextcord.Embed(
            title="помощь по категориям",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="категория", value="модерация")
        embed.add_field(name="категория", value="экономика")
        embed.add_field(name="категория", value="игровое")
        embed.add_field(name="категория", value="другое")
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)

    elif (category == "модерация"):
        embed = nextcord.Embed(
            title="помощь по командам модерации",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="members", value="все участники сервера")    
        embed.add_field(name="ban", value="бан участника")  
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)    

    elif (category == "экономика"):
        embed = nextcord.Embed(
            title="помощь по командам экономики",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="balance", value="ваш счет")    
        embed.add_field(name="work", value="работа") 
        embed.add_field(name="casino", value="казино, шанс выигрыша 25%")  
        embed.add_field(name="buy", value="покупка роли")  
        embed.add_field(name="stats", value="статистика")    
        embed.add_field(name="pay", value="платеж другому участнику")
        embed.add_field(name="daily", value="ежедневный бонус")  
        embed.add_field(name="shop", value="магазина")   
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)  

    elif (category == "игровые"):
        embed = nextcord.Embed(
            title="помощь по игровым командам",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="case", value="открыть кейс из игры CS:GO")    
        embed.add_field(name="profile", value="информация о профиле с платформы Omlet Arcade")   
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)   

    elif (category == "другие"):
        embed = nextcord.Embed(
            title="помощь по игровым командам",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="help", value="помощь по командам")    
        embed.add_field(name="links", value="все ссылки стримера HeeDina")   
        embed.add_field(name="donate", value="ссылка на донат стримеру")  
        embed.add_field(name="youtube", value="ссылка на ютуб стримера")
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)

    elif (category == "эмоции"):
        embed = nextcord.Embed(
            title="помощь по эмоциям",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="dance", value="танцы")    
        embed.add_field(name="whaaa", value="удивление")    
        embed.add_field(name="smile", value="улыбнуться")    
        embed.add_field(name="scare", value="испугаться")    
        embed.add_field(name="no", value="отрицать")   
        embed.add_field(name="yes", value="соглашаться")     
        embed.add_field(name="love", value="влюбиться")    
        embed.add_field(name="sad", value="грустить")    
        embed.add_field(name="hug", value="обнимать")    
        embed.add_field(name="pat", value="гладить")    
        embed.add_field(name="kiss", value="целовать")    
        embed.add_field(name="cry", value="плакать")    

        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)

    else:
        embed = nextcord.Embed(
            title="помощь по категориям",
            description="префикс бота: `слеш команды`",
            color=nextcord.Color.purple()
        )
        embed.add_field(name="категория", value="модерация")
        embed.add_field(name="категория", value="экономика")
        embed.add_field(name="категория", value="игровое")
        embed.add_field(name="категория", value="другое")
        embed.set_author(name="HeeDinaBot", icon_url="https://cdn.discordapp.com/avatars/926018668557643827/94258e2d4ef616d6e44c921944b40727.png?size=512")
        await ctx.send(embed=embed)     

bot.run(config["token"])
