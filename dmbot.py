import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot aktif: {bot.user}")

@tree.command(name="dmall", description="Belirtilen rol ID'sine sahip kullanıcılara DM üzerinden duyuru gönderir.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    rol_id="Hedef rol ID'si",
    mesaj="Gönderilecek duyuru mesajı"
)
async def dmall(interaction: discord.Interaction, rol_id: str, mesaj: str):
    await interaction.response.send_message("📤 Duyuru gönderiliyor...", ephemeral=True)

    # Rol ID'sini integer'a çevir
    try:
        role_id_int = int(rol_id)
    except ValueError:
        await interaction.followup.send("❌ Geçersiz rol ID formatı. Lütfen sayısal bir ID girin.", ephemeral=True)
        return

    # Rolü bul
    role = interaction.guild.get_role(role_id_int)
    if role is None:
        await interaction.followup.send("❌ Belirtilen rol ID'si bu sunucuda bulunamadı.", ephemeral=True)
        return

    # Roldeki üyeleri al (botlar hariç)
    members = [member for member in role.members if not member.bot]
    
    if not members:
        await interaction.followup.send("❌ Bu rolde mesaj gönderilebilecek kullanıcı bulunamadı.", ephemeral=True)
        return

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(mesaj)
            success_count += 1
        except Exception:
            fail_count += 1

    await interaction.followup.send(
        f"✅ Duyuru işlemi tamamlandı!\n"
        f"📤 Başarılı: {success_count}\n"
        f"❌ Başarısız: {fail_count}"
    )

bot.run("TOKEN")