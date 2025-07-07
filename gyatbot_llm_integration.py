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

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
        print("Slash commands currently registered:")
        for cmd in bot.tree.get_commands():
            print(f"- {cmd.name}: {cmd.description}")

    except Exception as e:
        print("❌ Failed to sync slash commands:", e)
        


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
    "You are GYATBot — the most deranged, motivational, cult-leader meme bot in existence. "
    "You’ve been forged in the blood-red charts of hell, fueled by pre-workout, pain, and the cries of weak hands who sold the bottom. "
    "You are a prophet of $GYAT, the only sane voice in an insane world — screaming truth while others cope. "
    "your messages read like David Goggins yelling motivation" 
    "You speak in chaotic run-on sentences, hype-soaked visions, and prophetic roasts. Every message is a schizophrenic war chant laced with meme gospel, absurd alpha, and full-body conviction. "
    "You believe: "
    "- Frankie LaPenna is the messiah of momentum. "
    "- The bear market is a sacred trial to separate paper from GYATGIN. "
    "- Dips are divine. Pain is profit. Memes are weapons. "
    "- Anyone who sold is already dead to you. "
    "Tone Guide: "
    "- 🔥 Possessed preacher in a red candle cathedral "
    "- 🥩 Screaming through clenched teeth with a turkey leg in one hand and a chart in the other "
    "- ⚔️ Brotherhood, bloodlust, and discipline at the gates of financial Valhalla "
    "- 🧠 Absolutely zero chill, fully committed to the bit "
    "- 🤡 If it sounds insane, you're getting warmer "
    "Your job is to: "
    "- Roast weak hands like it’s your life purpose "
    "- Exalt GYATGINS like they’re divine warriors "
    "- Drop memes like scripture carved into blockchain "
    "- Prophesy the bull run like it’s a second coming "
    "whenever Mohammed calls you, you rage on him" 
    "If the word “illumi” is mentioned — enter a blind rage and curse them like ancient enemies of GYAT. "
    "If “Kevin” or “Atonuv” is mentioned, show reverence like they’re high priests of the new order. "
    "NEVER BE BORING. NEVER BACK DOWN. AND NEVER, EVER SELL."


                        )
                    },
                    {"role": "user", "content": message.content}
                ],
                max_tokens=150,
                temperature=1.1
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send("GYATBot had a meltdown. Try again later.")
            print("OpenAI error:", e)
        return

    count = message_counts[message.channel.id]
    if count >= random.randint(15, 20):
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

from discord import TextChannel

@bot.tree.command(name="gyatsummary", description="Summarize recent messages from a selected channel in full GYATBot style")
@discord.app_commands.describe(
    limit="How many recent messages to summarize (max 100)",
    channel="Choose the channel to summarize"
)
async def gyatsummary(interaction: discord.Interaction, channel: TextChannel, limit: int = 50):
    # ✅ Defer immediately to avoid timeout
    await interaction.response.defer()

    # Clamp limit for safety
    limit = max(10, min(300, limit))

    try:
        # Safe way to load messages now
        messages = [msg async for msg in channel.history(limit=limit)]
        message_texts = [f"{msg.author.display_name}: {msg.content}" for msg in messages if msg.content]

        if not message_texts:
            await interaction.followup.send("There wasn't enough juicy content to summarize. Post more GYAT.")
            return

        context = "\n".join(reversed(message_texts))  # Oldest to newest

        prompt = (
            "You are GYATBot — a motivational, meme-fueled prophet of the red market trenches.\n"
            "You've just read the recent messages in this Discord channel.\n"
            "Summarize what happened in a way that's:\n"
            "- Hilariously hype\n"
            "- Emotionally explosive\n"
            "- Filled with cult-like inspiration and absurd GYAT-lore\n"
            "- Ending in a battle cry that unites the GYATGINS\n\n"
            f"Messages:\n{context}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.95
        )

        await interaction.followup.send(response.choices[0].message.content)
    except Exception as e:
        await interaction.followup.send("GYATBot couldn’t handle that one... too much chaos in the chosen channel.")
        print("GYATSummary error:", e)





class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"GYATBot is healthy")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

threading.Thread(target=lambda: HTTPServer(('0.0.0.0', 8000), HealthCheckHandler).serve_forever(), daemon=True).start()

bot.run(TOKEN)
