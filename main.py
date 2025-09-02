import asyncio  # Đảm bảo đã import
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
import random
import webserver
webserver.keep_alive()
load_dotenv()
token = os.getenv("DISCORD_TOKEN")  

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="Cmd:", intents=intents)

bay = ("cặc", "lồn", "địt", "đị","djt","dm","cc","cl","vcl","vl","đm","đmẹ","đm mày","đm con mẹ mày","đm con mày","đm con đĩ","đĩ","dmm","dmn","dcmn","dcm","dcmẹ","dcmẹ mày","dcm con mày","dcm con mẹ mày","con cặc")

@bot.event
async def on_ready():
    now = datetime.now()
    if now.month == 9 and now.day == 2:
        for guild in bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="quoc-khanh-2-9")
            if not channel:
                channel = await guild.create_text_channel("quoc-khanh-2-9")

            await channel.send("🇻🇳 **Chúc mừng Quốc Khánh 2/9!**\nHôm nay bot Minh chính chủ sẽ tổ chức sự kiện đặc biệt 🎉")
            await channel.send("📜 Gõ `Cmd:quiz_2_9`, `Cmd:freedom_quote`, hoặc `Cmd:flag` để tham gia nhé!")

    bot.loop.create_task(auto_chuc_quoc_khanh())
async def auto_chuc_quoc_khanh():
    while True:
        now = datetime.now()
        if now.month == 9 and now.day == 2:
            for guild in bot.guilds:
                channel = discord.utils.get(guild.text_channels, name="quoc-khanh-2-9")
                if channel:
                    await channel.send("🎉 Chúc mừng Quốc Khánh! Hãy cùng nhau lan tỏa tinh thần tự do 🇻🇳")
        await asyncio.sleep(21600)  # 6 tiếng


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Chào mừng {member.name} đã tham gia máy chủ này.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    content = message.content.lower()
@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return

    # Convert message content to lowercase and split into words
    content = message.content.lower()
    words = content.split()

    # Define your list of banned words (make sure 'bay' is defined somewhere) # Example set
    if any(word in bay for word in words):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} 🚫 Không dùng từ bậy trong server!"
            )
        except discord.Forbidden:
            await message.channel.send(
                f"{message.author.mention} ⚠️ Bot không có quyền xóa tin nhắn."
            )
        return

    # Allow commands to be processed
    await bot.process_commands(message)
@bot.command()
async def hello(ctx):
    await ctx.send(f"Xin chào!, {ctx.author.name}")

@bot.command()
async def list_player(ctx):
    members = ctx.guild.members
    member_names = [member.name for member in members if not member.bot]
    await ctx.send(f"Các thành viên trong server: {', '.join(member_names)}")

@bot.command()
async def poll_yes_no(ctx, *, question):
    await ctx.send(f"Bình chọn có/không: {question}")
    add_reaction = await ctx.send("Bình chọn 1 trong 2:✅,❌.")
    await add_reaction.add_reaction("✅")
    await add_reaction.add_reaction("❌")

@bot.command()
async def poll_luachon(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Vui lòng cung cấp ít nhất 2 lựa chọn.")
        return

    options_str = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
    await ctx.send(f"Bình chọn nhiều lựa chọn: {question}\n{options_str}")

@bot.command()
async def remind(ctx, time: int, *, message):
    await ctx.send(f"Đã đặt nhắc nhở sau {time} giây: {message}")
    await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=time))
    await ctx.send(f"{ctx.author.mention} Nhắc nhở: {message}")

@bot.command()
async def time(ctx):
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    await ctx.send(f"Giờ hiện tại: {now}")

@bot.command()
async def random_number(ctx, start: int, end: int):
    num = random.randint(start, end)
    await ctx.send(f"Số ngẫu nhiên từ {start} đến {end}: {num}")

@bot.command()
async def roll_dice(ctx, sides: int = 6):
    result = random.randint(1, sides)
    await ctx.send(f"{ctx.author.mention} đã tung xúc xắc {sides} mặt và được: {result}")

@bot.command()
async def countdown_you(ctx, seconds: int):
    if seconds < 1:
        await ctx.send("⚠️ Thời gian phải lớn hơn 0 giây.")
        return

    # Gửi tin nhắn ban đầu
    msg = await ctx.send(f"⏳ Đếm ngược: {seconds}")

    # Cập nhật nội dung mỗi giây
    for i in range(seconds - 1, 0, -1):
        await asyncio.sleep(1)
        await msg.edit(content=f"⏳ Đếm ngược: {i}")

    # Giây cuối cùng
    await asyncio.sleep(1)
    await msg.edit(content=f"🎉 Hết giờ! {ctx.author.mention}")

@bot.command()
async def countdown_all(ctx, seconds: int):
    if seconds < 1:
        await ctx.send("⚠️ Thời gian phải lớn hơn 0 giây.")
        return

    # Gửi tin nhắn ban đầu
    msg = await ctx.send(f"⏳ Đếm ngược: {seconds}")

    # Cập nhật nội dung mỗi giây
    for i in range(seconds - 1, 0, -1):
        await asyncio.sleep(1)
        await msg.edit(content=f"⏳ Đếm ngược: {i}")

    # Giây cuối cùng
    await asyncio.sleep(1)
    await msg.edit(content=f"🎉 Hết giờ! {ctx.author.mention} @everyone")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    owner = guild.owner
    created = guild.created_at.strftime("%d/%m/%Y %H:%M")
    roles = len(guild.roles)
    channels = len(guild.channels)
    emojis = len(guild.emojis)
    members = guild.member_count

    embed = discord.Embed(title=f"📊 Thông tin server: {guild.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    embed.add_field(name="👑 Chủ server", value=owner.mention, inline=True)
    embed.add_field(name="📅 Tạo ngày", value=created, inline=True)
    embed.add_field(name="👥 Thành viên", value=str(members), inline=True)
    embed.add_field(name="📁 Kênh", value=str(channels), inline=True)
    embed.add_field(name="🎭 Role", value=str(roles), inline=True)
    embed.add_field(name="😄 Emoji", value=str(emojis), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def playerinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    joined = member.joined_at.strftime("%d/%m/%Y %H:%M")
    created = member.created_at.strftime("%d/%m/%Y %H:%M")
    roles = [role.name for role in member.roles if role.name != "@everyone"]

    embed = discord.Embed(title=f"👤 Thông tin người dùng: {member.display_name}", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
    embed.add_field(name="🆔 ID", value=str(member.id), inline=True)
    embed.add_field(name="📅 Tham gia server", value=joined, inline=True)
    embed.add_field(name="📆 Tạo tài khoản", value=created, inline=True)
    embed.add_field(name="🎭 Role", value=", ".join(roles) if roles else "Không có", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def serverstats(ctx):
    guild = ctx.guild
    total_members = guild.member_count
    bots = len([m for m in guild.members if m.bot])
    humans = total_members - bots
    online = len([m for m in guild.members if m.status != discord.Status.offline])
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)

    embed = discord.Embed(title="📊 Thống kê server", color=discord.Color.orange())
    embed.add_field(name="👥 Tổng thành viên", value=total_members)
    embed.add_field(name="🤖 Bot", value=bots)
    embed.add_field(name="🧍 Người thật", value=humans)
    embed.add_field(name="🟢 Đang online", value=online)
    embed.add_field(name="💬 Kênh văn bản", value=text_channels)
    embed.add_field(name="🔊 Kênh thoại", value=voice_channels)
    await ctx.send(embed=embed)

@bot.command()
async def playerstats(ctx, member: discord.Member = None):
    member = member or ctx.author
    joined = member.joined_at.strftime("%d/%m/%Y")
    created = member.created_at.strftime("%d/%m/%Y")
    roles = [role.name for role in member.roles if role.name != "@everyone"]

    embed = discord.Embed(title=f"📈 Thống kê người dùng: {member.display_name}", color=discord.Color.purple())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
    embed.add_field(name="🆔 ID", value=member.id)
    embed.add_field(name="📅 Tham gia server", value=joined)
    embed.add_field(name="📆 Tạo tài khoản", value=created)
    embed.add_field(name="🎭 Role", value=", ".join(roles) if roles else "Không có")
    await ctx.send(embed=embed)

@bot.command()
async def user_info(ctx, member: discord.Member = None):
    member = member or ctx.author
    joined = member.joined_at.strftime("%d/%m/%Y %H:%M")
    created = member.created_at.strftime("%d/%m/%Y %H:%M")
    roles = [role.name for role in member.roles if role.name != "@everyone"]

    embed = discord.Embed(title=f"👤 Thông tin người dùng: {member.display_name}", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
    embed.add_field(name="🆔 ID", value=str(member.id), inline=True)
    embed.add_field(name="📅 Tham gia server", value=joined, inline=True)
    embed.add_field(name="📆 Tạo tài khoản", value=created, inline=True)
    embed.add_field(name="🎭 Role", value=", ".join(roles) if roles else "Không có", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🖼️ Avatar của {member.display_name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url if member.avatar else "")
    await ctx.send(embed=embed)

@bot.command()
async def rolesinfo(ctx):
    guild = ctx.guild
    roles = [role for role in guild.roles if role.name != "@everyone"]
    messages = []

    for role in roles:
        members = [member.display_name for member in role.members]
        if members:
            member_list = ", ".join(members[:10])
            if len(members) > 10:
                member_list += f" và {len(members) - 10} người nữa..."
        else:
            member_list = "❌ Không có ai"

        messages.append(f"🔹 **{role.name}**: {member_list}")

    # Gửi từng khối tin nhắn dưới 2000 ký tự
    chunk = ""
    for line in messages:
        if len(chunk) + len(line) + 1 > 2000:
            await ctx.send(chunk)
            chunk = ""
        chunk += line + "\n"

    if chunk:
        await ctx.send(chunk)

@bot.command()
async def flag(ctx):
    await ctx.send("🇻🇳 Cờ đỏ sao vàng tung bay! Tự hào là người Việt Nam!")

    role = discord.utils.get(ctx.guild.roles, name="Công dân danh dự")
    if not role:
        role = await ctx.guild.create_role(name="Công dân danh dự", color=discord.Color.red())

    await ctx.author.add_roles(role)
    await ctx.send(f"{ctx.author.mention} đã nhận role **Công dân danh dự** 🎖️")

@bot.command()
async def quiz_2_9(ctx):
    questions = [
        ("Ngày 2/9/1945, Bác Hồ đọc Tuyên ngôn Độc lập ở đâu?", "Quảng trường Ba Đình"),
        ("Bài hát quốc ca Việt Nam tên là gì?", "Tiến quân ca"),
        ("Ai là người soạn thảo Tuyên ngôn Độc lập?", "Hồ Chí Minh")
    ]
    q, a = random.choice(questions)
    await ctx.send(f"📜 Câu hỏi lịch sử: {q}")

    def check(m):
        return m.author == ctx.author

    try:
        msg = await bot.wait_for("message", check=check, timeout=15)
        if a.lower() in msg.content.lower():
            await ctx.send("✅ Chính xác! Tự hào quá!")
        else:
            await ctx.send(f"❌ Sai rồi! Đáp án đúng là: **{a}**")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Hết thời gian trả lời rồi!")
        
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

