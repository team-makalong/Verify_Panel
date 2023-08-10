import discord
from discord import app_commands
from datetime import datetime
from discord.ui import Button, View
from discord import ui
import random
import json

code = 000000

# 역할넣기 부분엔 넣을 역할 적어주시면 됩니다

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'{self.user}이 시작되었습니다') 
        game = discord.Game('테스트')          
        await self.change_presence(status=discord.Status.idle, activity=game)

client = aclient()
tree = app_commands.CommandTree(client)

class password(ui.Modal, title = "패스워드 인증"):
    answer = ui.TextInput(label = "비밀번호를 입력해주세요", style = discord.TextStyle.short, required = True, min_length = 3, max_length = 30)

    async def on_submit(self, interaction: discord.Interaction):
        file_path = r"pwdata.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
            try:
                if data[str(interaction.user.id)] == str(self.answer):
                    embed1 = discord.Embed(title = "인증이 완료되었습니다.", description=f"역할이 지급되었습니다.", timestamp = datetime.now(), color=0x4000FF)
                    await interaction.user.add_roles(역할넣기)
                    await interaction.response.send_message(embed=embed1)
                else:
                    embed1 = discord.Embed(title = "오류가 발생했습니다", description=f"비밀번호가 틀렸습니다", timestamp = datetime.now(), color=0x4000FF)
                    await interaction.response.send_message(embed=embed1)
                    return
            except KeyError:
                embed1 = discord.Embed(title = "오류가 발생했습니다", description=f"invaild interaction | ERROR CODE : 335036**`", timestamp = datetime.now(), color=0x4000FF)
                await interaction.response.send_message(embed=embed1)
                return

class twofa(ui.Modal, title = "2FA 인증"):
    answer = ui.TextInput(label = "비밀번호를 입력해주세요", style = discord.TextStyle.short, required = True, min_length = 3, max_length = 30)

    async def on_submit(self, interaction: discord.Interaction):
        if str(self.answer) == str(code):
            embed1 = discord.Embed(title = "인증이 완료되었습니다.", description=f"역할이 지급되었습니다.", timestamp = datetime.now(), color=0x4000FF)
            await interaction.user.add_roles(역할넣기)
            await interaction.response.send_message(embed=embed1)
        else:
            embed1 = discord.Embed(title = "오류가 발생했습니다.", description=f"코드가 일치하지 않습니다.", timestamp = datetime.now(), color=0x4000FF)
            await interaction.response.send_message(embed=embed1)


@tree.command(name = '인증패널', description = '인증을 시도합니다') 
@app_commands.choices(인증방식=[
    app_commands.Choice(name="일반인증", value="인증 버튼을 사용해 인증을 시도합니다"),
    app_commands.Choice(name="2fa인증", value="2단계 인증을 사용해 인증을 시도합니다"),
    app_commands.Choice(name="패스워드인증", value="비밀번호를 사용해 인증을 시도합니다"),
    app_commands.Choice(name="프라이빗인증", value="인증이 가능한 유저를 지정합니다"),
])
async def slash2(interaction: discord.Interaction, 인증방식: app_commands.Choice[str]):
    if 인증방식.name == "일반인증":
        button1 = Button(label="인증하기", style = discord.ButtonStyle.green)
        embed = discord.Embed(title="인증하기", description="아래 버튼으로 인증을 시도하세요.", color=0x4000FF)
        async def button_callback1(interaction: discord.Interaction):
            embed1 = discord.Embed(title = "인증이 완료되었습니다.", description=f"역할이 지급되었습니다.", timestamp = datetime.now(), color=0x4000FF)
            await interaction.user.add_roles(역할넣기)
            await interaction.response.send_message(embed=embed1)
        button1.callback = button_callback1
        view = View()
        view.add_item(button1)
        await interaction.response.send_message(embed=embed,view=view)
    elif 인증방식.name == "2fa인증":
        global code
        code = random.randint(100000, 999999)
        embed1 = discord.Embed(title = "인증 요청이 도착했습니다.", description=f"인증번호는 **`" + str(code) + "`** 입니다. ", timestamp = datetime.now(), color=0x4000FF)
        await interaction.user.send(embed=embed1)
        button1 = Button(label="인증하기", style = discord.ButtonStyle.green)
        embed = discord.Embed(title="인증하기", description="아래 버튼으로 2fa 인증을 시도하세요.", color=0x4000FF)
        async def button_callback1(interaction: discord.Interaction):
            famodal = twofa()
            await interaction.response.send_modal(twofa())
        button1.callback = button_callback1
        view = View()
        view.add_item(button1)
        await interaction.response.send_message(embed=embed,view=view)
    elif 인증방식.name == "패스워드인증":
        file_path = r"pwdata.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
            try:
                data["{}".format(interaction.user.id)]
            except KeyError:
                embed1 = discord.Embed(title = "문제가 발생했습니다", description=f"회원가입이 되어있지 않은 유저입니다.", timestamp = datetime.now(), color=0x4000FF)
                await interaction.response.send_message(embed=embed1)
                return
            await interaction.response.send_modal(password())
    elif 인증방식.name == "프라이빗인증":
        file_path = r"pvdata.json"

        with open(file_path, 'r') as file:
            data = json.load(file)

        interaction_user_id = interaction.user.id

        if interaction_user_id in data["verifyuserid"]:
            embed1 = discord.Embed(title = "인증이 완료되었습니다.", description=f"역할이 지급되었습니다.", timestamp = datetime.now(), color=0x4000FF)
            await interaction.user.add_roles(역할넣기)
            await interaction.response.send_message(embed=embed1)
        else:
            embed1 = discord.Embed(title = "문제가 발생했습니다", description=f"등록되지 않은 유저입니다.", timestamp = datetime.now(), color=0x4000FF)
            await interaction.response.send_message(embed=embed1)
            return

client.run('Token')
