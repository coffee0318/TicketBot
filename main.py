from xmlrpc import server
import discord
from discord_components import DiscordComponents, ComponentsBot, Button, ButtonStyle, ActionRow
from discord_buttons_plugin import ButtonType
import asyncio
import sqlite3
import os

client = discord.Client()

common = '기본문의-'

charge = '충전문의-'

purchase = '구매문의-'

qs = '질문-'

@client.event
async def on_ready():
    DiscordComponents(client)
    print(f"Login: {client.user}\nInvite Link: https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
    while True:
        await client.change_presence(activity=discord.Game(f"TicketService | {len(client.guilds)}서버 사용중"),status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(f"TicketService | {len(client.guilds)}서버 사용중"),status=discord.Status.online)
        await asyncio.sleep(5)


@client.event
async def on_message(message):
    if message.author.bot: #봇이면 반응x
        return

    if message.content.startswith("!등록"):
        if message.author.guild_permissions.administrator:
            if not (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                con = sqlite3.connect("./DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("CREATE TABLE serverinfo (id TEXT, normal TEXT, charge TEXT, buy TEXT, qa TEXT, admin1 TEXT, admin2 TEXT, admin3 TEXT, admin4 TEXT, admin5 TEXT, title TEXT, desc TEXT, cus1 TEXT, cus2 TEXT, cus3 TEXT, cus4 TEXT);")
                con.commit()
                cur.execute("INSERT INTO serverinfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (message.guild.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, "V Ticket Service", "원하시는 버튼을 클릭해주세요.", "문의하실 내용을 남겨주세요!", "문의하실 내용을 남겨주세요!", "문의하실 내용을 남겨주세요!", "문의하실 내용을 남겨주세요!"))
                con.commit()
                cur.execute("SELECT * FROM serverinfo")
                server_info = cur.fetchone()
                con.close()
                await message.channel.send(embed=discord.Embed(title="서버 등록 성공", description="서버가 성공적으로 등록되었습니다.\n!명령어를 입력하여 명령어들을 확인해주세요.", color=0x010101))

    if message.content == "!명령어":
        await message.channel.send(embed=discord.Embed(title="V Ticket Service", description="!등록 : 서버를 등록합니다.\n!티켓 : 티켓버튼을 설정합니다.\n!수정 일반 : 일반문의가 생성되는 카테고리를 수정합니다.\n!수정 충전 : 일반문의가 생성되는 카테고리를 수정합니다.\n!수정 구매 : 구매문의가 생성되는 카테고리를 수정합니다.\n!수정 질문 : 질문티켓이 생성되는 카테고리를 수정합니다.\n!수정 관리자1, 2, 3, 4, 5 : 관리자를 지정합니다.\n!수정 제목 : 티켓버튼세팅을 할때 나오는 임베드의 타이틀을 수정합니다.\n!수정 내용 : 티켓버튼세팅을 할때 나오는 임베드의 내용을 수정합니다.\n!일반문의 : 티켓생성 시, 생성된 티켓채널에 전송되는 메시지를 수정합니다.\n!충전문의 : 티켓생성 시, 생성된 티켓채널에 전송되는 메시지를 수정합니다.\n!구매문의 : 티켓생성 시, 생성된 티켓채널에 전송되는 메시지를 수정합니다.\n!질문 : 티켓생성 시, 생성된 티켓채널에 전송되는 메시지를 수정합니다.\n!설정값 : 현재까지 설정한 값들을 정리해서 보여줍니다.", color=0x010101))

    if message.content == "!설정값":
        if message.author.guild_permissions.administrator:
            con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            con.close
            await message.channel.send(embed=discord.Embed(title="V Ticket Service", description=f"일반문의 카테고리 : {server_info[1]}\n충전문의 카테고리 : {server_info[2]}\n구매문의 카테고리 : {server_info[3]}\n질문 카테고리 : {server_info[4]}\n관리자 1 : <@{server_info[5]}>\n관리자 2 : <@{server_info[6]}>\n관리자 3 : <@{server_info[7]}>\n관리자 4 : <@{server_info[8]}>\n관리자 5 : <@{server_info[9]}>\n임베드 제목 : {server_info[10]}\n임베드 내용 : {server_info[11]}\n일반문의 메시지 : {server_info[12]}\n충전문의 메시지 : {server_info[13]}\n구매문의 메시지 : {server_info[14]}\n질문 메시지 : {server_info[15]}", color=0x010101))


    if message.content == "!수정 일반":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="일반문의 카테고리 수정", description="일반문의 카테고리 아이디를 입력해주세요.", color=0x010101))
                def check(normal):
                    return (normal.author.id == message.author.id)
                normal = await client.wait_for("message", timeout=60, check=check)
                normal = normal.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET normal = ?",(normal,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 일반문의 카테고리 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 제목":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="임베드 제목 수정", description="제목을 입력해주세요.", color=0x010101))
                def check(title):
                    return (title.author.id == message.author.id)
                title = await client.wait_for("message", timeout=60, check=check)
                title = title.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET title = ?",(title,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 임베드의 제목이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 내용":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="임베드 내용 수정", description="내용을 입력해주세요.", color=0x010101))
                def check(desc):
                    return (desc.author.id == message.author.id)
                desc = await client.wait_for("message", timeout=60, check=check)
                desc = desc.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET desc = ?",(desc,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 임베드의 내용이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!일반문의":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="내용 설정", description="티켓 생성 시, 생성된 티켓채널에 전송되는 메시지 설정입니다.\n내용을 입력해주세요.", color=0x010101))
                def check(cus1):
                    return (cus1.author.id == message.author.id)
                cus1 = await client.wait_for("message", timeout=60, check=check)
                cus1 = cus1.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cus1 = ?",(cus1,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 일반문의 티켓의 메시지내용이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!충전문의":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="내용 설정", description="티켓 생성 시, 생성된 티켓채널에 전송되는 메시지 설정입니다.\n내용을 입력해주세요.", color=0x010101))
                def check(cus2):
                    return (cus2.author.id == message.author.id)
                cus2 = await client.wait_for("message", timeout=60, check=check)
                cus2 = cus2.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cus2 = ?",(cus2,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 충전문의 티켓의 메시지내용이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!구매문의":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="내용 설정", description="티켓 생성 시, 생성된 티켓채널에 전송되는 메시지 설정입니다.\n내용을 입력해주세요.", color=0x010101))
                def check(cus3):
                    return (cus3.author.id == message.author.id)
                cus3 = await client.wait_for("message", timeout=60, check=check)
                cus3 = cus3.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cus3 = ?",(cus3,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 구매문의 티켓의 메시지내용이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!질문":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="내용 설정", description="티켓 생성 시, 생성된 티켓채널에 전송되는 메시지 설정입니다.\n내용을 입력해주세요.", color=0x010101))
                def check(cus4):
                    return (cus4.author.id == message.author.id)
                cus4 = await client.wait_for("message", timeout=60, check=check)
                cus4 = cus4.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET cus4 = ?",(cus4,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 질문 티켓의 메시지내용이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 충전":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="충전문의 카테고리 수정", description="충전문의 카테고리 아이디를 입력해주세요.", color=0x010101))
                def check(charge):
                    return (charge.author.id == message.author.id)
                charge = await client.wait_for("message", timeout=60, check=check)
                charge = charge.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET charge = ?",(charge,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 충전문의 카테고리 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 구매":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="구매문의 카테고리 수정", description="구매문의 카테고리 아이디를 입력해주세요.", color=0x010101))
                def check(buy):
                    return (buy.author.id == message.author.id)
                buy = await client.wait_for("message", timeout=60, check=check)
                buy = buy.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET buy = ?",(buy,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 구매문의 카테고리 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 질문":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="질문 카테고리 수정", description="질문 카테고리 아이디를 입력해주세요.", color=0x010101))
                def check(qa):
                    return (qa.author.id == message.author.id)
                qa = await client.wait_for("message", timeout=60, check=check)
                qa = qa.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET qa = ?",(qa,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 질문 카테고리 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 관리자1":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 아이디 수정", description="관리자1의 아이디를 입력해주세요.", color=0x010101))
                def check(admin1):
                    return (admin1.author.id == message.author.id)
                admin1 = await client.wait_for("message", timeout=60, check=check)
                admin1 = admin1.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET admin1 = ?",(admin1,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 관리자1의 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 관리자2":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 아이디 수정", description="관리자2의 아이디를 입력해주세요.", color=0x010101))
                def check(admin2):
                    return (admin2.author.id == message.author.id)
                admin2 = await client.wait_for("message", timeout=60, check=check)
                admin2 = admin2.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET admin2 = ?",(admin2,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 관리자2의 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 관리자3":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 아이디 수정", description="관리자3의 아이디를 입력해주세요.", color=0x010101))
                def check(admin3):
                    return (admin3.author.id == message.author.id)
                admin3 = await client.wait_for("message", timeout=60, check=check)
                admin3 = admin3.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET admin3 = ?",(admin3,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 관리자3의 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 관리자4":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 아이디 수정", description="관리자4의 아이디를 입력해주세요.", color=0x010101))
                def check(admin4):
                    return (admin4.author.id == message.author.id)
                admin4 = await client.wait_for("message", timeout=60, check=check)
                admin4 = admin4.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET admin4 = ?",(admin4,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 관리자4의 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 관리자5":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="관리자 아이디 수정", description="관리자5의 아이디를 입력해주세요.", color=0x010101))
                def check(admin5):
                    return (admin5.author.id == message.author.id)
                admin5 = await client.wait_for("message", timeout=60, check=check)
                admin5 = admin5.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET admin5 = ?",(admin5,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="수정 성공", description="성공적으로 관리자5의 아이디가 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="수정 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!수정 색깔":
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.channel.send(embed=discord.Embed(title="색깔 수정", description="원하시는 색깔을 입력해주세요. (예시: 0x010101)", color=0x010101))
                def check(color):
                    return (color.author.id == message.author.id)
                color = await client.wait_for("message", timeout=60, check=check)
                color = color.content
                con = sqlite3.connect("./DB/" + str(message.guild.id) +".db")
                cur = con.cursor()
                cur.execute("UPDATE serverinfo SET color = ?",(color,))
                con.commit()
                con.close()
                await message.channel.send(embed=discord.Embed(title="변경 성공", description="성공적으로 임베드 색깔이 변경되었습니다.", color=0x010101))
            else:
                await message.channel.send(embed=discord.Embed(title="변경 실패", description="오류가 발생했습니다. 처음부터 다시 시도해주세요.", color=0x010101))

    if message.content == "!티켓": #!티켓 명령어
        if message.author.guild_permissions.administrator:
            if (os.path.isfile("./DB/" + str(message.guild.id) + ".db")):
                await message.delete() #메시지 자동으로 삭제 #관리자라면 작동하기
                con = sqlite3.connect("./DB/" + str(message.guild.id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM serverinfo")
                server_info = cur.fetchone()
                con.close
                embed = discord.Embed(title=server_info[10], description=server_info[11], color=0x010101)
                await message.channel.send(
                        embed=embed,
                        components = [
                            ActionRow(
                                Button(style=ButtonStyle.blue,label="💌 문의하기",custom_id="문의하기")
                            )
                        ]
                    )


    if message.content.startswith("!닫기"): #!닫기 명령어
        if message.author.guild_permissions.administrator:
            await message.channel.send(embed=discord.Embed(title="티켓문의 종료", description="정말로 티켓문의를 닫으시겠습니까?"),
            components = [
                        ActionRow(
                            Button(style=ButtonStyle.red,label="💥티켓닫기",custom_id="close")
                        )
                    ])

    if message.channel.id == 935539240731807775: #구매후기칸에 자동으로 이모지달기 (채널 아이디 수정)
        await message.add_reaction('<:814800730275053598:933217521790771210>') #달 이모지

@client.event
async def on_button_click(interaction):

    if interaction.custom_id == "문의하기":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) + ".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close
        embed = discord.Embed(title=server_info[10], description=server_info[11], color=0x010101)
        await interaction.respond(
                embed=embed,
                components = [
                    ActionRow(
                        Button(style=ButtonStyle.blue,label="💌 일반문의",custom_id="ticket"),
                        Button(style=ButtonStyle.green,label="🧾 충전문의",custom_id="charge"),
                        Button(style=ButtonStyle.red,label="🛒 구매&예약문의",custom_id="p"),
                        Button(style=ButtonStyle.gray,label="💬 질문",custom_id="q"),
                    )
                ]
            )

    if interaction.custom_id == "ticket": #기본문의 버튼이 눌렸다면
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{common}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{common}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(int(server_info[1])))
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title=server_info[10], description=f"<@{str(interaction.user.id)}>\n\n{server_info[12]}", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            admin = [server_info[5], server_info[6], server_info[7], server_info[8], server_info[9]]
            con.close
            for i in range(0,int(len(admin))):
                user = await client.fetch_user(admin[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 일반문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
        else:
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f"❌ <#{str(channel.id)}>이미 티켓채널이 존재합니다.", color=0x010101))

    if interaction.custom_id == "charge":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{charge}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{charge}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(int(server_info[2])))
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title=server_info[10], description=f"<@{str(interaction.user.id)}>\n\n{server_info[13]}", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            admin = [server_info[5], server_info[6], server_info[7], server_info[8], server_info[9]]
            con.close
            owner = [admin]
            for i in range(0,int(len(admin))):
                user = await client.fetch_user(admin[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 충전문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f"❌ <#{str(channel.id)}>이미 티켓채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "q":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{qs}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{qs}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(int(server_info[3])))
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title=server_info[10], description=f"<@{str(interaction.user.id)}>\n\n{server_info[14]}", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            admin = [server_info[5], server_info[6], server_info[7], server_info[8], server_info[9]]
            con.close
            owner = [admin]
            for i in range(0,int(len(admin))):
                user = await client.fetch_user(admin[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 질문티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f"❌ <#{str(channel.id)}>이미 티켓채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "p":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{purchase}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{purchase}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(int(server_info[4])))
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title=server_info[10], description=f"<@{str(interaction.user.id)}>\n\n{server_info[15]}", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM serverinfo")
            server_info = cur.fetchone()
            admin = [server_info[5], server_info[6], server_info[7], server_info[8], server_info[9]]
            con.close
            owner = [admin]
            for i in range(0,int(len(admin))):
                user = await client.fetch_user(admin[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 구매&예약문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title=server_info[10], description=f"❌ <#{str(channel.id)}>이미 티켓채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "close":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close
        embed = discord.Embed(title=server_info[10], description=f"```티켓닫기를 취소하려면 닫기취소버튼을. \n진행하려면 티켓닫기버튼을눌러주세요```  <@{interaction.user.id}>님이 티켓닫기를 요청하셨습니다", color=0x2f3136)
        await interaction.respond(
                embed=embed,
                components = [
                    ActionRow(
                        Button(style=ButtonStyle.gray,label="💥닫기취소",custom_id="cancle"),
                        Button(style=ButtonStyle.red,label="💥티켓닫기",custom_id="close1"),
                    )
                ]
            )

    if interaction.component.custom_id == "cancle":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close
        await interaction.message.delete()
        await interaction.respond(content="> 티켓닫기가 취소되었습니다.")
        a3 = discord.Embed(title=server_info[10],
                           description=f"```diff\n- 티켓닫기가 취소되었습니다```  <@{interaction.user.id}>님이 티켓닫기를 취소하셨습니다. ",
                           color=0x2f3136)
        cancle_message = await interaction.channel.send(embed=a3)
        await asyncio.sleep(3)
        await cancle_message.delete()
    if interaction.component.custom_id == "close1":
        con = sqlite3.connect("./DB/" + str(interaction.guild.id) +".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM serverinfo")
        server_info = cur.fetchone()
        con.close
        await interaction.respond(content="> 티켓이 10초후 삭제됩니다.")
        a2 = discord.Embed(title=server_info[10],
                           description=f"```💥 10초후에 티켓이 삭제됩니다.```  <@{interaction.user.id}>님이 티켓을 닫았습니다. ",
                           color=0x2f3136)
        await interaction.channel.send(embed=a2)
        await asyncio.sleep(10)
        await interaction.channel.delete()
        return
    
    
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
