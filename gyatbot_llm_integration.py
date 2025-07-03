
import os
import discord
import random
import openai
import requests
from discord.ext import commands, tasks
from collections import defaultdict

# Load environment variables
TOKEN = os.getenv("TOKEN")
DEXPAIR = os.getenv("DEXPAIR")
FRANKIE_ID = os.getenv("FRANKIE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Intents and bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Track message counts per channel
message_counts = defaultdict(int)

# Motivational spam messages for every ~10 user messages
spontaneous_messages = [
    "WE LIVE FOR RED DAYS. PAIN IS JUST A PRE-WORKOUT.",
    "SEND IT LOWER. I’M NOT EVEN HARD YET.",
    "GET THE GYAT OUTTA BED AND GRIND.",
    "DIAMONDS FORM UNDER GYAT PRESSURE 💎",
    "GOGGINS WOULD BUY THIS DIP WITH A BROKEN CARDIOVASCULAR SYSTEM.",
    "THE WEAK SELL. THE GYATGINS GET STRONGER.",
    "STOP TRADING AND GYAT UP.",
    "FRANKIE IS WATCHING. DON’T FUMBLE THE BAG.",
    "BUY NOW OR REGRET WHEN WE'RE ON JOE ROGAN.",
]

# Keywords for GYAT reactions
keywords = {
    "gyat": [
        "HOLD ME BACK I’M TOO GYATTED RIGHT NOW.",
        "WE’RE GOING FULL GYAT MODE 🔥",
        "SOMEBODY SAID GYAT? BRICKED.",
        "GYATGINS NEVER SELL. EVER.",
    ],
    "frankie": [
        "Frankie just flexed. That’s alpha behavior.",
        "Protect Frankie at all costs.",
        "Our beacon. Our inspiration. Frankie LaPenna has spoken.",
    ],
    "moon": [
        "WE'RE NOT STOPPING AT THE MOON. WE’RE SHOOTING FOR ANDROMEDA.",
        "This thing's about to GYAT past Pluto.",
    ],
    "pump": [
        "EVERY PUMP MAKES US HARDER.",
        "THIS ISN'T A PUMP. THIS IS ASCENSION.",
    ],
    "pressure": [
        "BRING ON THE PRESSURE 💎",
        "PRESSURE MAKES DIAMOND HANDS.",
    ],
    "diamond": [
        "💎 HANDS ARE EARNED THROUGH SUFFERING.",
        "IF YOU AIN’T BLEEDING, YOU AIN’T DIAMOND.",
    ],
    "motivate": [
        "GET HARD. GET DISCIPLINED. GET GYATTED.",
        "REAL ONES GRIND WHILE OTHERS FUD.",
    ],
    "community": [
        "COMMUNITY ISN’T A WORD. IT’S A BLOOD OATH.",
        "GYATGINS STICK TOGETHER THROUGH THE DIP.",
    ],
    "support": [
        "TRUE SUPPORT IS BUYING WHEN EVERYONE ELSE CRIES.",
        "WE LIFT EACH OTHER UP — INTO ORBIT.",
    ],
}

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    check_dexscreener.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Track messages per channel
    message_counts[message.channel.id] += 1

    # Check if Frankie posted
    if str(message.author.id) == FRANKIE_ID:
        await message.channel.send(random.choice([
            "FRANKIE HAS ENTERED THE CHAT. GET DISCIPLINED.",
            "FRANKIE'S HERE — STAND TALL GYATGINS.",
            "WE FOLLOW FRANKIE INTO FIRE. INTO FUD. INTO THE GYAT.",
        ]))

    # Check for keyword triggers
    msg = message.content.lower()
    for key, responses in keywords.items():
        if key in msg:
            await message.channel.send(random.choice(responses))
            break

    # Trigger spontaneous message randomly every 8–12 user messages
    count = message_counts[message.channel.id]
    if count >= random.randint(8, 12):
        await message.channel.send(random.choice(spontaneous_messages))
        message_counts[message.channel.id] = 0  # Reset

    await bot.process_commands(message)

@bot.command(name="gyatmotivate")
async def gyatmotivate(ctx):
    await ctx.send(random.choice(spontaneous_messages))

@tasks.loop(seconds=60)
async def check_dexscreener():
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{DEXPAIR}"
        response = requests.get(url)
        data = response.json()

        txns = data.get("pair", {}).get("txns", {})
        buys = txns.get("m5", {}).get("buys", 0)
        sells = txns.get("m5", {}).get("sells", 0)

        if buys > 0:
            if buys >= 1:
                print("Big buy detected!")
                channel = discord.utils.get(bot.get_all_channels(), name="general")
                if channel:
                    await channel.send(random.choice([
                        f"CHAD BUY INCOMING. SOMEBODY’S GOT DIAMOND FOREARMS 💎",
                        f"{buys} BUYERS JUST GOT GYATTED UP. WE’RE BACK.",
                        "WHOEVER BOUGHT JUST BOUGHT IMMORTALITY.",
                    ]))

        if sells > 0:
            if sells >= 1:
                print("Sell detected.")
                channel = discord.utils.get(bot.get_all_channels(), name="general")
                if channel:
                    await channel.send(random.choice([
                        f"{sells} people just sold… and lost their manhood.",
                        "SELLERS DETECTED. WEAKNESS IN THE AIR.",
                        "YOU SOLD THE DIP? STAY DOWN.",
                    ]))

    except Exception as e:
        print("Dexscreener error:", e)

bot.run(TOKEN)
