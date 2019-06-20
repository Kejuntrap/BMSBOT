
# インストールした discord.py を読み込む
import discord
import json
import random
import re


TOKEN ='your token'
datafile= open('songs.json', 'r', encoding='utf-8')
jdata=json.load(datafile)

songs=0
difficulty=27		#1-25とそれ以上（0は使っていない）

lists= [[] for i in range(difficulty)]
for x in jdata:
    if int(jdata[x]["difficulty"])<99:
        lists[int(jdata[x]["difficulty"])].append(x)
    else:
        lists[difficulty-1].append(x)
    songs+=1 	#曲数

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content=='/help':
        await message.channel.send("// すべての難易度からランダム　\n 数字A ある難易度A内からランダムで1曲 \n 数字A 数字B 数字A以上数字B以下の難易度の曲からランダムで1曲")
    elif message.content == '//':
        tmp=message.content
        num=int(random.random()*songs)
        sends="難易度:★ %s \n曲名:%s \n アーティスト:%s"%(jdata[str(num)]["difficulty"],jdata[str(num)]["song"],jdata[str(num)]["artist"])
        await message.channel.send(sends)
    else:
        tmp=message.content
        match2="\d"
        if len(tmp)>=3:
            #2つの難易度のレンジ
            low,hig= list(map(int, tmp.split()))
            low=max(low,1)
            hig=max(hig,1)
            if(low>hig):
                low,hig=hig,low
            sentaku=min(low+int((hig-low+1)*random.random()),difficulty-1)     #難易度
            num=lists[sentaku][int(random.random()*len(lists[sentaku]))]    #番号
            sends="難易度:★ %s \n曲名:%s \n アーティスト:%s"%(jdata[str(num)]["difficulty"],jdata[str(num)]["song"],jdata[str(num)]["artist"])
            await message.channel.send(sends)

        elif re.match(match2,tmp):
            #1つの難易度
            slc=len(lists[min(max(1,int(tmp)),difficulty-1)])
            num=lists[min(max(1,int(tmp)),difficulty-1)][int(random.random()*slc)]
            sends="難易度:★ %s \n曲名:%s \n アーティスト:%s"%(jdata[str(num)]["difficulty"],jdata[str(num)]["song"],jdata[str(num)]["artist"])
            await message.channel.send(sends)

        else:
            await message.channel.send("?")


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
