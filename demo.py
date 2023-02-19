import os
from dotenv import load_dotenv
import discord

TOKEN       = os.getenv( 'DISCORD_BOT_TOKEN' )
CHANNELID   = 875293401552125952 # チャンネルIDを貼り付け

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 起動時処理
@client.event
async def on_ready():
    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名：" + str(channel.name) )
        print("チャンネルID：" + str(channel.id) )
        print("----------")

# チャンネル入退室時の通知処理
@client.event
async def on_voice_state_update(member, before, after):
    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        # 通知メッセージを書き込むテキストチャンネル（チャンネルIDを指定）
        botRoom = client.get_channel(CHANNELID)

        # 入退室を監視する対象のボイスチャンネル（チャンネルIDを指定）
        announceChannelIds = [874162422125068325]

        # 退室通知
        if before.channel is not None and before.channel.id in announceChannelIds:
            await botRoom.send("**" + before.channel.name + "** から、__" + member.name + "__  が抜けました！")
        # 入室通知
        if after.channel is not None and after.channel.id in announceChannelIds:
            await botRoom.send("**" + after.channel.name + "** に、__" + member.name + "__  が参加しました！")

# Botのトークンを指定（デベロッパーサイトで確認可能）
client.run(TOKEN)

