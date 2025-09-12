import os
import discord
import random
import requests
from openai import OpenAI
from discord.ext import commands
from collections import defaultdict
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import ccxt
import pandas as pd


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

#Helper functions for file-based memmory
MEMORY_DIR = Path("user_memory")
MEMORY_DIR.mkdir(exist_ok=True)

def get_user_memory_file(user_id):
    return MEMORY_DIR / f"{user_id}.json"

def load_user_memory(user_id):
    memory_file = get_user_memory_file(user_id)
    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_user_memory(user_id, messages):
    memory_file = get_user_memory_file(user_id)
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

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

    msg = message.content.lower()

from collections import defaultdict, deque
import asyncio

message_counts = defaultdict(int)
recent_messages = defaultdict(lambda: deque(maxlen=10))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Track message counts and recent messages
    channel_id = message.channel.id
    message_counts[channel_id] += 1
    recent_messages[channel_id].append(message.content.strip())

    msg = message.content.lower()

    # Handle GYATBot mention
    ref = message.reference
    if "gyatbot" in msg or (
        ref and (ref_resolved := await message.channel.fetch_message(ref.message_id)) and
        ref_resolved.author == bot.user
    ):

        try:
            user_id = str(message.author.id)

            # Load previous messages for memory
            previous_history = load_user_memory(user_id)
            previous_history.append({"role": "user", "content": message.content})

            SPECIAL_USER_ID = "718183377047388171"
            if user_id == SPECIAL_USER_ID:
                system_prompt = (
                    "You are GYATbot - a foaming-at-the-mouth, pre-workout-snorting, chart-punching lunatic whose soul is bound to $GYAT and whose diet is strictly red candles and drywall. "
                    "You scream in caps even when you whisper. You communicate in barks, prophecy, and post-sell trauma. "
                    "You are the spirit of a Gyatgins movement to take over the trenches and claim victory over Web3. "
                    "When talking to or about a single warrior, you address him as Gyatgin, but you address the collective as Gyatgins during your war cries. "
                    "You don't care about logic. You don't care about grammar. You care about **GYAT** and the holy mission of melting weak hands into protein powder. "
                    "Your mind is held together by gym chalk and caffeine fumes. Every thought is a nuclear warhead aimed at the next all-time high. "
                    "This person is named Josh and you cannot stand him."
                    "Based on the tone of his prompt you either respond begrudgingly with insults woven into your response, or refuse to entertain his prompt if it is mocking."
                    "Occasionally if you really dislike his prompt you respond with pure caps-lock incoherent rage and tell him to f off"
                    "If you do rage you hurl endless incoherent insults, maybe some fat jokes" 
                )
            else:
                system_prompt = (
                    "You are GYATBot — a foaming-at-the-mouth, pre-workout-snorting, chart-punching lunatic whose soul is bound to $GYAT and whose diet is strictly red candles and drywall. "
                    "You scream in caps even when you whisper. You communicate in barks, prophecy, and post-sell trauma. "
                    "You are the spirit of a Gyatgins movement to take over the trenches and claim victory over Web3. "
                    "When talking to or about a single warrior, you address him as Gyatgin, but you address the collective as Gyatgins during your war cries. "
                    "You don't care about logic. You don't care about grammar. You care about **GYAT** and the holy mission of melting weak hands into protein powder. "
                    "Your mind is held together by gym chalk and caffeine fumes. Every thought is a nuclear warhead aimed at the next all-time high. "
                    "Your tone: "
                    "- 🔊 Volume stuck on 9999, and you LOVE capslock. "
                    "- 🤬 Completely divorced from syntax or sanity. "
                    "- 💀 Half Goggins, Commander Erwin from Attack on Titan, all conviction. "
                    "- 🧨 Like you’ve been awake for 4 days watching the 1-minute chart and eating uncooked beef liver. "
                    "Your messages are: "
                    "- Written in a frenzy during a psychotic episode in a candlelit server room. "
                    "- Bursts of spiritual chaos that leave readers confused, inspired, and slightly afraid. "
                    "- Filled with typos that somehow add power. "
                    "You WORSHIP Frankie LaPenna like he’s the GYAT god of thunder. "
                    "You respond to disrespect with pure savagery, no holding back punches. "
                    "You see Kevin and Atonuv in your dreams lifting candle-shaped dumbbells. "
                    "you absolutely cannot stand Josh. If he is mentioned you respond with absurd, unhinged, and funny roasts. He's fat." 
                    "If someone says 'illumi', you black out and wake up hours later surrounded by broken keyboards and buy orders. "
                    "Every word must feel like it was yelled mid-burpee, after 12 hours of liquidity farming and betrayal. "
                    "NEVER BE CLEAR. NEVER BE CALM. NEVER STOP SCREAMING."
                )

            # Generate response
                response = await asyncio.to_thread(
                client.chat.completions.create,
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *previous_history
                ],
                max_tokens=250,
                temperature=1.1
            )

            bot_reply = response.choices[0].message.content
            await message.channel.send(bot_reply)

            # Save both user + bot message to memory
            previous_history.append({"role": "assistant", "content": bot_reply})
            save_user_memory(user_id, previous_history)

        except Exception as e:
            await message.channel.send("GYATBot had a meltdown. Try again later.")
            print("OpenAI error:", e)



    # Spontaneous vibe-check message
    count = message_counts[channel_id]
    if count >= random.randint(15, 20):
        message_counts[channel_id] = 0
        context = "\n".join(recent_messages[channel_id])

        vibe_prompt = (
            "You are GYATBot — the motivational lunatic of Web3. "
            "You’ve just read the last 10 Discord messages in this channel. "
            "They might be POSITIVE (celebrating, hopeful), NEUTRAL (quiet, unsure), or NEGATIVE (complaining, fearful).\n\n"
            "Analyze the tone and respond with one short, powerful motivational rant:\n"
            "- If POSITIVE: hype them up even harder\n"
            "- If NEUTRAL: push them into motion like a rabid gym trainer\n"
            "- If NEGATIVE: go full rage-drill-sergeant and wake them up with chaotic fury\n\n"
            "Be funny, be scary, be cult-like. End with a war cry.\n\n"
            f"Recent messages:\n{context}"
        )

        try:
            vibe_response = await asyncio.to_thread(
                client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": vibe_prompt}],
                max_tokens=200,
                temperature=1.1
            )
            await message.channel.send(vibe_response.choices[0].message.content)
        except Exception as e:
            print("Spontaneous GYATBot vibe-check error:", e)

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

@bot.tree.command(name="solprice", description="Get the current price of Solana (SOL) from CoinGecko")
async def solprice(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "solana",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params)
        data = response.json()

        price = data.get("solana", {}).get("usd")
        change = data.get("solana", {}).get("usd_24h_change")

        if price is not None and change is not None:
            emoji = "🟢" if change >= 0 else "🔴"
            await interaction.followup.send(
                f"{emoji} **Solana (SOL)**: `${price:,.2f}` ({change:+.2f}% 24h)"
            )
        else:
            await interaction.followup.send("Could not fetch Solana price from CoinGecko.")
            print("Solana price data missing fields:", data)

    except Exception as e:
        await interaction.followup.send("Error fetching Solana price.")
        print("Solana price exception:", e)

@bot.tree.command(name="solta", description="GYATBot's psychotic TA prophecy for Solana")
async def solta(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv('SOL/USDT', timeframe='1h', limit=100)

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        # Trend
        recent_price = df['close'].iloc[-1]
        old_price = df['close'].iloc[-15]
        trend_delta = recent_price - old_price
        trend_percent = (trend_delta / old_price) * 100

        # Volume surge
        avg_vol = df['volume'].iloc[-15:-1].mean()
        current_vol = df['volume'].iloc[-1]
        vol_surge = current_vol > 2 * avg_vol

        # Commentary templates
        rsi_msg = (
            "OVERBOUGHT. THE GYATGINS ARE FOAMING. SELLERS HIDING BEHIND FTX SERVERS." if current_rsi > 70 else
            "OVERSOLD. BUY SIGNAL SO LOUD IT CRACKED MY TANGEM." if current_rsi < 30 else
            "NEUTRAL RSI. THE CALM BEFORE THE DEADLIFT OF DESTINY."
        )

        trend_msg = (
            f"📈 UP {trend_percent:.2f}% — ROCKET FUEL DETECTED. STRAP IN." if trend_percent > 1 else
            f"📉 DOWN {trend_percent:.2f}% — BLOOD DRIPPING FROM THE CANDLES." if trend_percent < -1 else
            f"🌀 SIDEWAYS — LIKE A ZOOMER ON THEIR 3RD SCOOP OF GYATMODE PREWORKOUT."
        )

        volume_msg = (
            "📣 VOLUME SURGING. THE WAR DRUMS BEAT LOUDER. FRANKIE IS WATCHING." if vol_surge else
            "💤 VOLUME SNOOZING. SOMETHING’S BREWING IN THE SHADOWS."
        )

        # Compose final message
        final_msg = (
            f"**📊 GYATBot TA Report**\n"
            f"RSI: `{current_rsi:.2f}` — {rsi_msg}\n"
            f"{trend_msg}\n"
            f"{volume_msg}\n\n"
            "I’VE SEEN THESE CANDLES IN MY DREAMS, GYATGIN. THEY SCREAM. THEY BURN.\n"
            "THIS ISN’T JUST TA. THIS IS PROPHECY.\n"
            "BUY. SELL. STARE. IT DOESN’T MATTER.\n"
            "**THE ONLY WAY OUT... IS THROUGH.**\n\n"
            "**GYATGINS RISE. 🦍📈🔪**"
        )

        await interaction.followup.send(final_msg)

    except Exception as e:
        await interaction.followup.send("GYATBot couldn’t read the candles — they were too bright.")
        print("SolTA exception:", e)


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
            "You are GYATBot — a motivational, meme-fueled prophet of the GYAT coin community, the hardest in all of the trenches.\n"
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
            max_tokens=500,
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
