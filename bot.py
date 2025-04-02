#Gerekli kütüphanelerin kod dosyasının içine aktarılması 

import discord
from discord.ext import commands
from logic import DB_Manager
from config import DATABASE, TOKEN

#İntents açıklamaları

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

#Botun asıl komut başlangıcı ve DB

bot = commands.Bot(command_prefix='!', intents=intents)
manager = DB_Manager(DATABASE)

#Botun temel yapısnın oluşturulması

    #Botun discordda aktif olmasını sağlayan kod   

@bot.event
async def on_ready():
    print(f'Bot hazır! {bot.user} olarak giriş yapıldı.')

    #Botun açıklayıcı metini

@bot.command(name='start')
async def start_command(ctx):
    await ctx.send("""Merhaba! Ben bir proje yöneticisi botuyum. 😊 
Seninle tanıştığıma çok memnun oldum! Benim görevim, projelerini en düzenli ve etkili şekilde yönetmene yardımcı olmak.
İster okul projesi olsun, ister iş hayatındaki büyük hedeflerin...
Her şeyi kayıt altında tutmak, düzenlemek ve sana hatırlatmak için buradayım. 📝
Hazırsan başlayalım, birlikte harika işler başaracağız! 🚀""")
    await info(ctx)

    #Botun discorda yazılması gereken komutları ve bu komutların ne işe yaradıkları.

@bot.command(name='info')
async def info(ctx):
    await ctx.send("""
Kullanabileceğiniz komutlar:

!new_project - Yeni bir proje ekle
!projects - Projelerini listele
!update_projects - Projeni güncelle
!skills - Projene beceri ekle
!users - Tüm kullanıcıları listele
!users_projects - Kullanıcı-proje ilişkilerini görüntüle
!delete - Bir projeyi sil

Ayrıca proje adını yazarak detaylarını görüntüleyebilirsin!
""")

    #Kodun discordda yeni proje oluşturmasını sağlayan komut.

@bot.command(name='new_project')
async def new_project(ctx):
    await ctx.send("Lütfen projenin adını girin!")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    name = await bot.wait_for('message', check=check)

    await ctx.send("Projenin bağlantısını girin!")
    link = await bot.wait_for('message', check=check)

    statuses = [x[1] for x in manager.get_all_statuses()] 
    await ctx.send("Durum seçin:\n" + "\n".join(statuses))
    status = await bot.wait_for('message', check=check)
    if status.content not in statuses:
        await ctx.send("Geçersiz durum. Lütfen tekrar deneyin.")
        return

    status_id = manager.get_status_id(status.content)
    data = [ctx.author.id, name.content, "Açıklama yok", link.content, status_id]
    manager.insert_project(*data)
    await ctx.send("Proje başarıyla kaydedildi!")

    #Kodun kendi dbsine kaydettiği projeyi bu komut yazılınca tüm kaydedilen projeleri göstermesi

@bot.command(name='projects')
async def get_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if projects:
        for p in projects:
            await ctx.send(f"Proje: {p[2]}\nBağlantı: {p[4]}")
    else:
        await ctx.send("Henüz projeye sahip değilsin. !new_project ile oluşturabilirsin.")

        #Bu komut orıjenin içindeki yazılım dillerinden bahseder

@bot.command(name='skills')
async def skills(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if not projects:
        await ctx.send("Henüz projeye sahip değilsin. !new_project ile oluşturabilirsin.")
        return

    names = [x[2] for x in projects]
    await ctx.send("Hangi projeye beceri eklenecek?\n" + "\n".join(names))
    def check(msg): return msg.author == ctx.author and msg.channel == ctx.channel
    pname = await bot.wait_for('message', check=check)
    if pname.content not in names:
        await ctx.send("Geçersiz proje adı. Tekrar dene.")
        return

    skill_list = [x[1] for x in manager.get_skills()]
    await ctx.send("Bir beceri seç:\n" + "\n".join(skill_list))
    skill = await bot.wait_for('message', check=check)
    if skill.content not in skill_list:
        await ctx.send("Geçersiz beceri. Tekrar dene.")
        return

    manager.insert_skill(user_id, pname.content, skill.content)
    await ctx.send(f"{pname.content} projesine {skill.content} becerisi eklendi!")


    #İstenilen projenin silinmesi

@bot.command(name='delete')
async def delete_project(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if not projects:
        await ctx.send("Henüz projeye sahip değilsin. !new_project ile oluşturabilirsin.")
        return

    names = [x[2] for x in projects]
    await ctx.send("Silmek istediğin projeyi seç:\n" + "\n".join(names))
    def check(msg): return msg.author == ctx.author and msg.channel == ctx.channel
    pname = await bot.wait_for('message', check=check)
    if pname.content not in names:
        await ctx.send("Proje bulunamadı. Lütfen tekrar dene.")
        return

    pid = manager.get_project_id(pname.content, user_id)
    manager.delete_project(user_id, pid)
    await ctx.send(f"{pname.content} projesi silindi.")

    #Projenin güncellenmesini sağlayan komut

@bot.command(name='update_projects')
async def update_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if not projects:
        await ctx.send("Henüz projeye sahip değilsin. !new_project ile oluşturabilirsin.")
        return

    names = [x[2] for x in projects]
    await ctx.send("Güncellemek istediğin projeyi seç:\n" + "\n".join(names))
    def check(msg): return msg.author == ctx.author and msg.channel == ctx.channel
    pname = await bot.wait_for('message', check=check)
    if pname.content not in names:
        await ctx.send("Proje bulunamadı. Lütfen tekrar dene.")
        return

    attributes = {'Proje adı': 'project_name', 'Açıklama': 'description', 'Proje bağlantısı': 'url', 'Proje durumu': 'status_id'}
    await ctx.send("Hangi özelliği değiştirmek istersin?\n" + "\n".join(attributes.keys()))
    attr = await bot.wait_for('message', check=check)

    if attr.content not in attributes:
        await ctx.send("Geçersiz seçim. Lütfen tekrar dene.")
        return

    if attr.content == 'Proje durumu':
        statuses = manager.get_statuses()
        await ctx.send("Yeni durum seç:\n" + "\n".join([x[0] for x in statuses]))
        new_val = await bot.wait_for('message', check=check)
        if new_val.content not in [x[0] for x in statuses]:
            await ctx.send("Geçersiz durum. Lütfen tekrar dene.")
            return

        update_value = manager.get_status_id(new_val.content)
    else:
        await ctx.send(f"Yeni {attr.content} gir:")
        val = await bot.wait_for('message', check=check)
        update_value = val.content

    manager.update_projects(attributes[attr.content], (update_value, pname.content, user_id))
    await ctx.send("Proje başarıyla güncellendi!")


    #Kullanıcıların listesini gösteren komut.

@bot.command(name='users')
async def list_users(ctx):
    users = manager.get_users()
    if users:
        await ctx.send("Kullanıcı listesi:\n" + "\n".join([str(u[0]) for u in users]))
    else:
        await ctx.send("Kullanıcı bulunamadı.")

        #Kullanıcıların projelerini gösteren komut

@bot.command(name='users_projects')
async def users_projects(ctx):
    data = manager.get_all_user_projects()
    if data:
        response = ""
        for user_id, projects in data.items():
            response += f"Kullanıcı {user_id}:\n"
            for proj in projects:
                response += f"- {proj}\n"
        await ctx.send(response)
    else:
        await ctx.send("Henüz hiçbir kullanıcı projesi eklememiş.")

        #Botu discorda aktarak çalışmasını sağlayan komut.

bot.run(TOKEN)
