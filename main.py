import os
import unicodedata
from dotenv import load_dotenv
import discord


PREFIX                  = "/"
HELP                    = PREFIX + "help"
CHANGE_NOTIFY_CHANNEL   = PREFIX + "notify"
ADD_MONITOR_CHANNEL     = PREFIX + "addmonitor"

"""
    TODO
        コンストラクタで、selfのパラメータを設定したい。
        discord.Clientを継承しているからか、pythonのコンストラクタを使用すると、継承出来ない。
        取り合えずは、on_ready( コンストラクタ )で無理やり設定する
"""
class KEG_NotifyOfVC( discord.Client ):
    #BOT起動時
    async def on_ready( self ):
        print( f'Logged in as {self.user} (ID: {self.user.id})' )
        #通知と設定テキストチャンネル
        self.notifyChannel = client.get_channel( int( os.getenv( 'INIT_CHAT_ID' ) ) )
        # 入退室を監視する対象のボイスチャンネル
        self.monitorChannelIds = []


    # チャンネル入退室時の通知処理
    async def on_voice_state_update( self, member, before, after ):
        # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
        if before.channel == after.channel:
            return
        # 退室通知
        if before.channel is not None and before.channel.id in self.monitorChannelIds:
            print( "vc out" )
            await self.notifyChannel.send( "**" + before.channel.name + "** から __" + member.name + "__  が抜けました！" )
        # 入室通知
        if after.channel is not None and after.channel.id in self.monitorChannelIds:
            print( "vc in" )
            await self.notifyChannel.send( "**" + after.channel.name + "** に __" + member.name + "__  が参加しました！" )

    #BOTの設定変更
    async def on_message( self, message ):
        #BOTの発言なら
        if message.author.bot:
            return
        if message.content[:1] != PREFIX:
            return

        #全角を半角に変換
        content = unicodedata.normalize( 'NFKC', message.content )
        print( f"content: {content}" )

        #コマンド一覧
        if content == HELP:
            await self.notifyChannel.send( f"**通知場所の変更**\n{CHANGE_NOTIFY_CHANNEL} TextChannelID\n\n**監視するボイスチャンネルの追加**\n{ADD_MONITOR_CHANNEL} VCChannelID" )
            return

        #設定変更データの取得
        try:
            settings = content.split( " " )[0]
            data     = content.split( " " )[1]
            print( f"settings data:[{data}]" )
        except:
            print( f"[ERROR]{content}" )
            return

        #通知チャンネルの変更
        if settings == CHANGE_NOTIFY_CHANNEL:
            print( "change notify channel" )
            self.notifyChannel = client.get_channel( int( data ) )
            await self.notifyChannel.send( f"通知場所を**{self.notifyChannel}**に変更しました。" )

        #監視VCの追加
        elif settings == ADD_MONITOR_CHANNEL:
            print( "add monitor channel" )
            self.monitorChannelIds.append( int( data ) )
            await self.notifyChannel.send( f"{client.get_channel( int( data ) )}の入退出監視を追加しました。" )


#.envファイルをロードして環境変数へ反映
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = KEG_NotifyOfVC( intents=intents )
client.run( os.getenv( 'DISCORD_BOT_TOKEN' ) )
