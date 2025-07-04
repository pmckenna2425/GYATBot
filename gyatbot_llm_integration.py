import os
import discord
import random
import requests
from openai import OpenAI
from discord.ext import commands, tasks
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
    await bot.tree.sync()  # <- Important for slash commands
    check_birdeye.start()

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
                            "You are GYATBot, a loud, absurd, hilarious meme bot with David Goggins energy. "
                            "You roast weak traders, praise GYATGINS who buy the dip, and speak in meme-laced hype language. "
                            "You reference Frankie LaPenna like he’s a prophet, and every response should sound like you're yelling mid-pre-workout."
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

@bot.tree.command(name="gyatprice", description="Check the current GYAT price")
async def gyatprice(interaction: discord.Interaction):
    try:
        url = f"https://public-api.birdeye.so/public/price/token_price?address=EfgEGG9PxLhyk1wqtqgGnwgfVC7JYic3vC9BCWLvpump&chain=solana"
        headers = {"X-API-KEY": BIRDEYE_API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()

        if "data" not in data:
            print("GYATPrice API response missing 'data':", data)
            await interaction.response.send_message("Birdeye didn't return valid price data. Might be rate-limited or token error.")
            return

        price = float(data["data"]["value"])
        await interaction.response.send_message(f"Current GYAT price: ${price:.6f}")
    except Exception as e:
        await interaction.response.send_message("Couldn't fetch GYAT price. Blame the bears.")
        print("GYATPrice error:", e)



@tasks.loop(seconds=60)
async def check_birdeye():
    try:
        url = f"https://public-api.birdeye.so/public/transaction/token/{TOKEN_MINT}?limit=10&chain=solana"
        headers = {"X-API-KEY": BIRDEYE_API_KEY}
        response = requests.get(url, headers=headers)

        try:
            data = response.json()
        except ValueError:
            print("Invalid JSON from Birdeye. Response content:", response.text)
            return

        trades = data.get("data", [])
        channel = discord.utils.get(bot.get_all_channels(), name="💬general")
        if not channel:
            return

        for trade in trades:
            try:
                side = trade.get("side")
                price_usdt = float(trade.get("priceUsdt", 0))
                amount = float(trade.get("amount", 0))
                amount_usd = price_usdt * amount
                tx_hash = trade.get("txHash", "")[:8]

                if amount_usd >= 500:
                    if side == "buy":
                        await channel.send(random.choice([
                            f"💰 BIG BUY: ${amount_usd:.2f} just sent us to GYAT ORBIT 🚀 (tx: `{tx_hash}...`)",
                            f"BUYER JUST DROPPED ${amount_usd:.2f}. CALL HIM FRANKIE 💦",
                            f"${amount_usd:.2f} BUY INCOMING. GYAT MODE: ENGAGED 🔥",
                        ]))
                    elif side == "sell":
                        await channel.send(random.choice([
                            f"🧻 SELL ALERT: ${amount_usd:.2f} just paper-handed their way into oblivion. (tx: `{tx_hash}...`)",
                            f"${amount_usd:.2f} SELL?? DON’T LET FRANKIE SEE THIS WEAKNESS.",
                            f"WHOEVER SOLD ${amount_usd:.2f} — you just missed the next ATH ❌",
                        ]))
            except Exception as parse_error:
                print("Error parsing Birdeye trade:", parse_error)

    except Exception as e:
        print("Birdeye trade check error:", e)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"GYATBot is healthy")

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8000), HealthCheckHandler).serve_forever(), daemon=True).start()

bot.run(TOKEN)
