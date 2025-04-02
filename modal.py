import discord
from discord.ext import commands
from discord import ui, ButtonStyle, TextStyle
from config import TOKEN

# Modal pencere tanımlama
class TestModal(ui.Modal, title='Test Başlık'):
    field_1 = ui.TextInput(label='Kısa metin')
    field_2 = ui.TextInput(label='Uzun metin', style=TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        text = f"Kısa metin: {self.field_1.value}\nUzun metin: {self.field_2.value}"
        if interaction.message:
            await interaction.message.edit(content=text)
        if not interaction.response.is_done():
            await interaction.response.defer()

# Buton tanımı
class TestButton(ui.Button):
    def __init__(self, label="Test etiketi", style=ButtonStyle.blurple, row=0):
        super().__init__(label=label, style=style, row=row)

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.user.send("Bir butona bastınız ✉️")
        except discord.Forbidden:
            await interaction.channel.send("Kullanıcıya özel mesaj gönderilemiyor.")

        await interaction.channel.send("Butona tıklama algılandı! 🎯")
        await interaction.response.send_modal(TestModal())
        self.style = ButtonStyle.gray
        if not interaction.response.is_done():
            await interaction.response.defer()

# Görünüm (View) tanımı
class TestView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TestButton(label="Test Butonu", style=ButtonStyle.green))

# Bot yapılandırması
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot hazır olduğunda
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı.')

# Komut: test
@bot.command(name='test')
async def test(ctx):
    await ctx.send("🔘 Aşağıdaki butona tıklayın:", view=TestView())

# Komut: modal
@bot.command(name='modal')
async def modal(ctx):
    await ctx.send_modal(TestModal())

# Komut: mesaj
@bot.command(name='message')
async def message(ctx):
    try:
        await ctx.author.send("📩 Bu bir test DM mesajıdır.")
    except discord.Forbidden:
        await ctx.send("❌ Mesaj gönderilemedi. DM kapalı olabilir.")

# Botu başlatma
bot.run(TOKEN)