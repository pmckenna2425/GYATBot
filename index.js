const {
  Client,
  GatewayIntentBits,
  REST,
  Routes,
  SlashCommandBuilder,
} = require("discord.js");
const axios = require("axios");
const express = require("express");
require("dotenv").config();

const app = express();
app.get("/", (req, res) => res.send("GYATBot is alive"));
app.listen(3000, () => console.log("Uptime ping server running on port 3000"));

const TOKEN = process.env.TOKEN;
const FRANKIE_ID = "457371310536785932";

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const PAIR_ID = "dgqd4rmbkf3upcy7guklmyosap4hpzmuwsvsuzatjlky";
const DEX_API = `https://api.dexscreener.com/latest/dex/pairs/solana/${PAIR_ID}`;

let messageCounter = 0;
let nextBlurtThreshold = getRandomInt(10, 14);
let lastBuyTx = "",
  lastSellTx = "";

const blurts = [
  "BRING ON THE PRESSURE. PRESSURE MAKES DIAMOND HANDS.",
  "WE HAVEN’T SUFFERED ENOUGH. RED MEANS WE'RE ALIVE.",
  "SELL? BRO I’D RATHER CHEW GLASS.",
  "IM BRICKED UP. THIS DUMP IS A GIFT.",
  "PAIN BUILDS THE GYATGINS. EMBRACE IT.",
  "STAY HARD. BUY GYAT.",
  "IF YOU’RE COMFORTABLE, YOU’RE LOSING.",
  "THE DIP IS YOUR COACH. SHUT UP AND LISTEN.",
  "GYAT ISN’T A COIN. IT’S A CHARACTER TEST.",
  "I’M GONNA GO CRASH INTO A TREE TO GET HARDER.",
];

const motivateLines = [
  "STAY HARD. BRICK UP.",
  "WE LIVE FOR THE SUFFERING. RED IS FUEL.",
  "EMBRACE THE DIP. FEEL THE WEIGHT.",
  "I BUY THE FEAR. I EAT THE PAIN.",
  "PRESSURE BUILDS LEGENDS. STAY GYATTED.",
  "IF YOU SOLD, DO 500 PUSHUPS.",
  "FRANKIE IS WATCHING. DON’T BE WEAK.",
  "EVERY CANDLE IS A TEST. PASS IT.",
  "REAL GYATGINS THRIVE ON VOLATILITY.",
  "WE DON’T SLEEP. WE DON’T SELL. WE JUST GET HARDER.",
];

const frankieHype = [
  "⚡ FRANKIE HAS SPOKEN. STAND BRICKED.",
  "🦾 MESSAGE FROM THE QUAD GOD HIMSELF.",
  "🔥 IF FRANKIE’S HERE, WE’RE GETTING HARDER.",
  "💪 FRANKIE’S WORD IS MARKET LAW. LISTEN UP.",
  "🧱 BRICK ENERGY JUST SPIKED. THANK YOU FRANKIE.",
  "📢 FRANKIE HAS ENTERED THE CHAT. EVERYONE TIGHTEN UP.",
];
const keywordResponses = {
  gyat: [
    "GYATGINS UNITE. STOP TRADING AND BELIEVE.",
    "BRICKED UP JUST SEEING THAT WORD.",
    "IF IT’S NOT GYAT, IT’S NOT REAL.",
    "THE ONLY DIRECTION IS FORWARD — THROUGH PAIN AND GYAT.",
    "GYAT ISN’T JUST A TOKEN. IT’S A TEST.",
  ],
  frankie: [
    "FRANKIE DIDN’T RISK HIS QUADS FOR YOU TO SELL.",
    "FRANKIE IS WATCHING. STAY HARD.",
    "IMAGINE DUMPING IN FRONT OF FRANKIE LAPEENYA.",
    "FRANKIE BLESSED THIS TOKEN. HONOR THE PAIN.",
    "FRANKIE’S WORD IS BRICK.",
  ],
  pump: [
    "THE PUMP IS JUST THE WARM-UP. THE PAIN IS THE GAIN.",
    "YOU DON’T CHASE GREEN. YOU CHASE GREATNESS.",
    "EVERY CANDLE IS A TEST OF YOUR BRICKNESS.",
    "PUMP IT TILL YOU BREAK. THEN KEEP GOING.",
  ],
  moon: [
    "WE DON’T ASK FOR MOON. WE SUFFER FOR IT.",
    "MOON? BRO, WE’RE SHOOTING THROUGH STARS IN PAIN.",
    "REAL GYATGINS GET THERE WITHOUT LOOKING UP.",
    "MOON IS JUST MILESTONE ONE.",
  ],
  send: [
    "SEND IT LOWER. I’M TRYNA GET HARDER.",
    "SEND IT TO ZERO. I’LL STILL BE HERE.",
    "SEND ME PAIN. SEND ME GLORY.",
    "SEND IT. GYATGINS DON’T FLINCH.",
  ],
  lambo: [
    "LAMBO? I’M DRIVING STRAIGHT INTO ADVERSITY.",
    "I’M NOT HERE FOR LUXURY. I’M HERE FOR LEGEND.",
    "LAMBO COMES AFTER 10,000 PUSHUPS.",
    "I’LL WALK TO THE LAMBO FACTORY IF I HAVE TO.",
  ],
  believe: [
    "STOP TRADING AND BELIEVE IN THE GYAT.",
    "BELIEF BUILDS BRICKS.",
    "BELIEF OVER BALANCE. ALWAYS.",
    "THE MARKET TESTS FAITH. HOLD FAST.",
  ],
  hard: [
    "GET HARDER. STAY HARD.",
    "THIS PAIN? IT’S THE WARM-UP.",
    "I’M BRICKED UP ON A RED DAY.",
    "STAY DISCIPLINED. STAY DANGEROUS.",
  ],
  goggins: [
    "WHAT WOULD GOGGINS DO? HE’D HOLD.",
    "STAY HARD. STAY DISCIPLINED.",
    "YOU DON’T ESCAPE PAIN. YOU EMBRACE IT.",
    "GOGGINS MENTALITY: NO STOPPING, ONLY SUFFERING.",
  ],
  salty: [
    "YOU’RE NOT SALTY. YOU’RE JUST WEAK.",
    "STAY BRICKED. STAY UNSHAKABLE.",
    "SALT IS JUST A BYPRODUCT OF LOSS. STAY GYATTED.",
    "SALTY? DO MORE PUSHUPS.",
  ],
  top: [
    "TOP? BRO THIS IS JUST THE FIRST MOUNTAIN.",
    "TOP SIGNALS ARE FOR TOURISTS.",
    "PAIN HAS NO CEILING.",
    "TOP IS AN ILLUSION. STAY HUNGRY.",
  ],
  bottom: [
    "BOTTOM IS WHERE LEGENDS TRAIN.",
    "WE BUY HELL. WE SELL NEVER.",
    "BOTTOM? GOOD. IT’S HARDER DOWN HERE.",
    "FIND ME AT THE BOTTOM. I’M TRAINING.",
  ],
  pressure: [
    "BRING THE PRESSURE. MAKE ME A DIAMOND.",
    "PRESSURE IS JUST BRICK TRAINING.",
    "STAY IN THE FIRE. PRESSURE SHARPENS.",
    "NO PRESSURE, NO LEGACY.",
  ],
  diamond: [
    "DIAMOND HANDS ARE FORGED IN RED.",
    "IF YOU'RE NOT BLEEDING, YOU'RE NOT SHINING.",
    "PRESSURE BUILDS DIAMOND MINDS.",
    "THIS AIN’T FINANCE. THIS IS FORTITUDE.",
  ],
  motivate: [
    "NEED MOTIVATION? LOOK AT YOUR BAG. THEN STAND UP.",
    "MOTIVATION IS FAKE. DISCIPLINE IS REAL.",
    "YOU DON’T NEED A REASON. JUST A TARGET.",
    "IF THIS AIN’T HARD, YOU’RE NOT TRYING.",
  ],
  community: [
    "THIS COMMUNITY IS BRICKED TOGETHER.",
    "WE BLEED RED. WE BUILD TOGETHER.",
    "COMMUNITY MEANS SUFFERING SIDE BY SIDE.",
    "NO LEADER. JUST LIONS.",
  ],
  support: [
    "SUPPORT COMES IN PAIN. THANK YOUR BROTHERS.",
    "BRICK ON BRICK, WE HOLD EACH OTHER UP.",
    "YOU SUPPORT? THEN STAY THROUGH RED.",
    "BACK YOUR GYATGINS. NO QUESTIONS.",
  ],
  "stop trading": [
    "STOP TRADING. START TRANSFORMING.",
    "STOP TRADING AND BELIEVE IN THE GYAT.",
    "TRADING IS FOR THE WEAK. GYAT IS FOR THE BRICKED.",
  ],
};

const bigBuyMessages = [
  "A GYATGIN JUST WENT FULL PSYCHOPATH WITH $${amount}. 🔥",
  "BRO JUST GOT HARDER WITH $${amount}. WELCOME TO THE SUFFERING.",
  "HE ATE THE FEAR. HE BOUGHT $${amount}. RESPECT.",
  "$GYAT JUST GOT MORE DANGEROUS. $${amount} WORTH.",
  "WELCOME TO THE DARK PLACE. $${amount} ENTRY ACCEPTED.",
];

const bigSellMessages = [
  "💀 SOLD $${amount}? HE'S PROBABLY SOFT.",
  "SOMEONE TOOK PROFITS. WE TOOK **SOULS.**",
  "IMAGINE SELLING. COULDN’T BE A GYATGIN.",
  "$${amount} RAN FROM THE GRIND. WE STAYED AND GOT **HARDER.**",
  "SOMEONE JUST QUIT MID-PAIN. $${amount} GONE. GYATGINS LAUGH.",
];

client.once("ready", () => {
  console.log(`GYATBot is online as ${client.user.tag}`);
  registerSlashCommands();
  pollDexscreener();
  setInterval(pollDexscreener, 60000);
});
client.on("messageCreate", (message) => {
  if (message.author.bot) return;

  // Frankie auto-hype trigger
  if (message.author.id === FRANKIE_ID) {
    message.channel.send(pick(frankieHype));
    return;
  }

  const msg = message.content.toLowerCase();

  // Keyword triggers
  for (const key in keywordResponses) {
    if (msg.includes(key)) {
      const res = pick(keywordResponses[key]);
      message.channel.send(res);
      return;
    }
  }

  // Random blurt
  messageCounter++;
  if (messageCounter >= nextBlurtThreshold) {
    message.channel.send(pick(blurts));
    messageCounter = 0;
    nextBlurtThreshold = getRandomInt(10, 14);
  }
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === "gyatprice") {
    try {
      const res = await axios.get(DEX_API);
      const pair = res.data.pair;
      if (!pair || !pair.priceUsd) {
        return interaction.reply(
          "Dexscreener isn't showing data right now. Frankie might be taking a nap.",
        );
      }
      await interaction.reply(
        `$GYAT is $${pair.priceUsd} | Market Cap: $${pair.fdv} | Volume (24h): $${pair.volume.h24}`,
      );
    } catch (e) {
      await interaction.reply(
        "Couldn't fetch price. Frankie must be sleeping.",
      );
    }
  }

  if (interaction.commandName === "gyatmotivate") {
    const line = pick(motivateLines);
    await interaction.reply(`**💪 MOTIVATION:** ${line}`);
  }
});

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function pollDexscreener() {
  try {
    const res = await axios.get(DEX_API);
    const pair = res.data.pair;
    if (!pair || !pair.txns || !pair.txns.h1) return;

    const txs = pair.txns.h1;
    for (const tx of txs) {
      if (tx.txid === lastBuyTx || tx.txid === lastSellTx) continue;

      const amount = Number(tx.usdValue);
      if (amount >= 800) {
        if (tx.type === "buy") {
          lastBuyTx = tx.txid;
          const msg = pick(bigBuyMessages).replace(
            "$${amount}",
            `$${amount.toFixed(0)}`,
          );
          postToMain(msg);
        } else if (tx.type === "sell") {
          lastSellTx = tx.txid;
          const msg = pick(bigSellMessages).replace(
            "$${amount}",
            `$${amount.toFixed(0)}`,
          );
          postToMain(msg);
        }
      }
    }
  } catch (e) {
    console.error("Dexscreener error:", e.message);
  }
}

function postToMain(message) {
  const channel = client.channels.cache.find((c) => c.isTextBased() && c.guild);
  if (channel) channel.send(message);
}

async function registerSlashCommands() {
  const commands = [
    new SlashCommandBuilder()
      .setName("gyatprice")
      .setDescription("Get current $GYAT price"),
    new SlashCommandBuilder()
      .setName("gyatmotivate")
      .setDescription("Get a motivational scream"),
  ].map((cmd) => cmd.toJSON());

  const rest = new REST({ version: "10" }).setToken(TOKEN);
  try {
    const appId = (await rest.get("/users/@me")).id;
    await rest.put(Routes.applicationCommands(appId), { body: commands });
    console.log("Slash commands registered.");
  } catch (err) {
    console.error("Slash command error:", err);
  }
}

client.login(TOKEN);
