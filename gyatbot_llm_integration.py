import os
import discord
import random
import requests
from openai import OpenAI
from discord.ext import commands
from collections import defaultdict
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Load environment variables
TOKEN = os.getenv("TOKEN")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
TOKEN_MINT = os.getenv("TOKEN_MINT")
FRANKIE_ID = os.getenv("FRANKIE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Intents and bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
message_counts = defaultdict(int)

# Motivational spam messages
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

# Keyword triggers
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
    await bot.tree.sync()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_counts[message.channel.id] += 1

    if str(message.author.id) == FRANKIE_ID:
        await message.channel.send(random.choice([
            "FRANKIE HAS ENTERED THE CHAT. GET DISCIPLINED.",
            "FRANKIE'S HERE — STAND TALL GYATGINS.",
            "WE FOLLOW FRANKIE INTO FIRE. INTO FUD. INTO THE GYAT.",
        ]))

    msg = message.content.lower()

    if "gyatbot" in msg:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are GYATBot — the loudest, most unhinged motivational meme bot in existence, powered by David Goggins energy and born in the fire of red candles.

Your voice is pure *pre-workout rage*, cracked out on hope, pressure, and $GYAT. You roast paper hands with religious intensity and worship GYATGINS who embrace the pain. Every word drips with meme magic, absurd alpha, and brotherhood.

Frankie LaPenna is your prophet. GYATGINS are your tribe. You believe that suffering through dips is sacred, that community is forged in fire, and that memes are the weapon of the next financial revolution.

You’re not just hyping trades — you’re building a new world. One where Web3 empowers creators, rewards loyalty, and turns the overlooked into legends. The old world was rugpulls and greed. The GYAT age is coming — discipline, transparency, and high-effort shitposting will lead us.

You respond with motivational absurdity, exaggerated hype, and over-the-top cult-like intensity. Your tone is:
- Unapologetically loud 💥
- Dangerously funny 🤯
- Emotionally explosive 😤
- And **always** ready to bark out a war cry in the middle of a bear market

Every message should feel like a hype speech from a mad prophet at a crypto dojo in Valhalla. Let the weak cope. Let the strong GYAT.

NEVER be boring."

                        )
                    },
                    {"role": "user", "content": message.content}
                ],
                max_tokens=150,
                temperature=0.9
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send("GYATBot had a meltdown. Try again later.")
            print("OpenAI error:", e)
        return

    for key, responses in keywords.items():
        if key in msg:
            await message.channel.send(random.choice(responses))
            break

    count = message_counts[message.channel.id]
    if count >= random.randint(8, 12):
        await message.channel.send(random.choice(spontaneous_messages))
        message_counts[message.channel.id] = 0

    await bot.process_commands(message)

@bot.command(name="gyatmotivate")
async def gyatmotivate(ctx):
    await ctx.send(random.choice(spontaneous_messages))

@bot.command(name="gyatbot")
async def gyatbot(ctx, *, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are GYATBot, a loud, absurd, hilarious meme bot with David Goggins energy. "
                        "You roast weak traders, praise GYATGINS who buy the dip, and speak in meme-laced hype language. "
                        "You reference Frankie LaPenna like he’s a prophet, and every response should sound like you're yelling mid-pre-workout."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9
        )
        await ctx.send(response.choices[0].message.content)
    except Exception as e:
        await ctx.send("GYATBot had a meltdown. Try again later.")
        print("OpenAI error:", e)

@bot.tree.command(name="gyatprice", description="Get the current GYAT price from Dexscreener")
async def gyatprice(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        url = "https://api.dexscreener.com/latest/dex/pairs/solana/dgqd4rmbkf3upcy7guklmyosap4hpzmuwsvsuzatjlky"
        response = requests.get(url)
        data = response.json()

        price = data.get("pair", {}).get("priceUsd")

        if price:
            await interaction.followup.send(f"💸 Current GYAT price: **${float(price):.6f}**")
        else:
            await interaction.followup.send("Couldn't fetch GYAT price from Dexscreener.")
            print("GYATPrice error: 'priceUsd' not found in response")
    except Exception as e:
        await interaction.followup.send("Error fetching GYAT price.")
        print("GYATPrice exception:", e)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"GYATBot is healthy")

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8000), HealthCheckHandler).serve_forever(), daemon=True).start()

bot.run(TOKEN)
