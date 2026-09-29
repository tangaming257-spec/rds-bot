import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

JABATAN_MAP = {
    "Dragonhead": "[Dragonhead]",
    "Vanguard": "[Vanguard]",
    "Enforcer": "[Enforcer]",
    "Red Officer": "[Officer]",
    "Street Soldier": "[Soldier]",
    "Young Blood": "[Young Blood]"
}

@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai: {bot.user}")

@bot.event
async def on_member_update(before, after):
    # Cek role yang baru saja ditambahkan
    added_roles = [role for role in after.roles if role not in before.roles]
    
    for role in added_roles:
        if role.name in JABATAN_MAP:
            jabatan_tag = JABATAN_MAP[role.name]
            
            # Cari channel insider-form
            channel = discord.utils.get(after.guild.text_channels, name="insider-form")
            if not channel:
                channel = discord.utils.find(lambda c: "insider-form" in c.name, after.guild.text_channels)
                
            if channel:
                async for message in channel.history(limit=50):
                    if message.author == after:
                        for line in message.content.split("\n"):
                            if "Nama IC:" in line:
                                nama_ic = line.split("Nama IC:")[1].strip()
                                nickname_baru = f"{jabatan_tag} {nama_ic}"[:32]
                                
                                try:
                                    await after.edit(nick=nickname_baru)
                                    print(f"✨ Sukses ubah nama {after.name} jadi {nickname_baru}")
                                except Exception as e:
                                    print(f"❌ Error: {e}")
                                return

bot.run(os.environ['DISCORD_TOKEN'])
