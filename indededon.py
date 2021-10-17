"""
やあ。
どうしてここにいるんだい？
間違えてメモ帳で開いちゃった？
それともコードを見に来た？
ぜひ見て行ってくれ。
でも、無断でコードを盗むのだけはやめてほしい。
昔俺はそっくりそのままコードを盗まれたんだ。
はあ？ってなったね
コードがほしいときは俺に言ってくれれば渡すから。
ほしいときは https://twitter.com/brightnoahb にDMを送ってくれ。
とりあえず、無断で使用するのはやめてくれ。
よろしく。
"""

import fortnitepy
import platform
from fortnitepy import ClientPartyMember as clientparty
import requests
import traceback
import asyncio
import threading
import random
import traceback
import crayons
from requests.exceptions import Timeout
import datetime
import time
from functools import partial
from fortnitepy.ext import commands
import ujson as json

requests.models.complexjson = json

class SuicideException(Exception):
    pass

def authorization():
    with open("device_auths.json","w",encoding="utf-8") as f:
        code = input("https://www.epicgames.com/id/api/redirect?clientId=3446cd72694c4a4485d81b77adbb2141&responseType=code にアクセスし、ページ内の文字列をすべてコピーし、貼り付けてください。 ")
        authorization = requests.post("https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",headers={"Content_Type":"application/x-www-form-urlencoded","Authorization":f"basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="},data={"grant_type":"authorization_code","code":json.loads(code)['authorizationCode']}).json()
        create_device_auth = requests.post(f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{authorization['account_id']}/deviceAuth",headers={"Authorization":f"Bearer {authorization['access_token']}"}).json()
        device_auth = {'device_id':f'{create_device_auth["deviceId"]}','account_id':f'{create_device_auth["accountId"]}','secret':f'{create_device_auth["secret"]}'}
        json.dump(device_auth,f,indent=4)

class Bot():
    def __init__(self):
        global clients
        clients = []
        ######################必要jsonを読み込み#########################
        self.lang = json.load(open("lang\\ja.json","r+",encoding="UTF-8"))
        self.command = json.load(open("commands.json","r",encoding="utf-8"))
        self.config = json.load(open("config.json","r",encoding="utf-8"))
        self.blacklist = self.config["normal"]["blacklist"]
        self.debug = self.config["DEV"]["debug"]
        try:
            self.device = json.load(open("device_auths.json","r+",encoding="UTF-8"))
            self.device["device_id"]
            self.device["account_id"]
            self.device["secret"]
        except Exception as e:
            print(crayons.red(f"エラーコード:{e}\n認証ファイルが破損または欠落しています。"))
            authorization()
        self.device = json.load(open("device_auths.json","r+",encoding="UTF-8"))
        ################################################################
        self.public = fortnitepy.PartyPrivacy.PUBLIC
        self.private = fortnitepy.PartyPrivacy.PRIVATE
        self.friends_allow_friends_of_friends = fortnitepy.PartyPrivacy.FRIENDS_ALLOW_FRIENDS_OF_FRIENDS
        self.private_allow_friends_of_friends = fortnitepy.PartyPrivacy.PRIVATE_ALLOW_FRIENDS_OF_FRIENDS
        self.friends =  fortnitepy.PartyPrivacy.FRIENDS
        self.privacy = {
            "public":self.public,
            "private":self.private,
            "friends_allow_friends_of_friends":self.friends_allow_friends_of_friends,
            "private_allow_friends_of_friends":self.private_allow_friends_of_friends,
            "friend":self.friends
        }

        plt = fortnitepy.Platform
        self.platform = {
            "WIN":plt.WINDOWS,
            "MAC":plt.MAC,
            "PS4":plt.PLAYSTATION_4,
            "PS5":plt.PLAYSTATION_5,
            "XBO":plt.XBOX_ONE,
            "XBX":plt.XBOX_X,
            "SWT":plt.SWITCH,
            "IOS":plt.IOS,  
            "AND":plt.ANDROID
        }
        p_config = fortnitepy.DefaultPartyConfig(
            privacy=self.privacy_converter(self.config["party_settings"]["privacy"]),
            max_size=self.config["party_settings"]["max_size"],
            chat_enabled=self.config["party_settings"]["chat_enabled"],
        )
        pm_config = fortnitepy.DefaultPartyMemberConfig(
                meta=[
                    partial(clientparty.set_battlepass_info, has_purchased=True,level=self.config["normal"]["level"]),
                    partial(clientparty.set_banner, icon=self.config["normal"]["banner"] ,color=self.config["normal"]["color"] ,season_level=self.config["normal"]["level"]),
                    partial(clientparty.set_outfit, asset=self.config["normal"]["outfit"]),
                    partial(clientparty.set_backpack, asset=self.config["normal"]["backpack"]),
                    partial(clientparty.set_pickaxe, asset=self.config["normal"]["pickaxe"])
                ]
        )
        self.bot = commands.Bot(
            command_prefix=self.config["normal"]['prefix'],
            auth=fortnitepy.DeviceAuth(f"{self.device['device_id']}",f"{self.device['account_id']}",f"{self.device['secret']}"),
            case_insensitive=True,
            default_party_config=p_config,
            default_party_member_config=pm_config
        )
        clients.append(self.bot)
        ################################################################
        self.emotemimic = None
        
        if not self.config["normal"]["platform"] in self.privacy:
            self.bot.platform = self.platform["WIN"]
        else:
            self.bot.platform = self.platform[self.config["normal"]["platform"]]

        def language(url,name):
            data = requests.get(url,timeout=(11.0)).json()
            with open(f"{name}.json","w",encoding="UTF-8") as f:
                json.dump(data,f,ensure_ascii=False,indent=4)
        try:
            ja = threading.Thread(target=language,args=("https://fortnite-api.com/v2/cosmetics/br?language=ja","ja"))
            en = threading.Thread(target=language,args=("https://fortnite-api.com/v2/cosmetics/br?language=en","en"))
            ja.start()
            en.start()
        except Exception:
            print(traceback.format_exc())
            print(self.lang["api_downed"])
        print(f"{crayons.green('Python ' + platform.python_version())}")
        print(f"{crayons.green('fortnitepy ' + fortnitepy.__version__)}")
        print(self.lang["booting"])
        self.emote = self.config["normal"]["emote"]

        self.recruits = [
            "CID_001_Athena_Commando_F_Default",
            "CID_002_Athena_Commando_F_Default",
            "CID_003_Athena_Commando_F_Default",
            "CID_004_Athena_Commando_F_Default",
            "CID_005_Athena_Commando_M_Default",
            "CID_006_Athena_Commando_M_Default",
            "CID_007_Athena_Commando_M_Default",
            "CID_008_Athena_Commando_M_Default",
            "CID_556_Athena_Commando_F_RebirthDefaultA",
            "CID_557_Athena_Commando_F_RebirthDefaultB",
            "CID_558_Athena_Commando_F_RebirthDefaultC",
            "CID_559_Athena_Commando_F_RebirthDefaultD",
            "CID_560_Athena_Commando_M_RebirthDefaultA",
            "CID_561_Athena_Commando_M_RebirthDefaultB",
            "CID_562_Athena_Commando_M_RebirthDefaultC",
            "CID_563_Athena_Commando_M_RebirthDefaultD",
            "CID_873_Athena_Commando_M_RebirthDefaultE",
            "CID_874_Athena_Commando_M_RebirthDefaultF",
            "CID_875_Athena_Commando_M_RebirthDefaultG",
            "CID_876_Athena_Commando_M_RebirthDefaultH",
            "CID_877_Athena_Commando_M_RebirthDefaultI",
            "CID_878_Athena_Commando_F_RebirthDefault_E",
            "CID_879_Athena_Commando_F_RebirthDefault_F",
            "CID_880_Athena_Commando_F_RebirthDefault_G",
            "CID_881_Athena_Commando_F_RebirthDefault_H",
            "CID_882_Athena_Commando_F_RebirthDefault_I"
        ]

    def privacy_converter(self,raw_privacy):
        if raw_privacy in self.privacy:
            return self.privacy[raw_privacy]
        else:
            return self.private
    
    def main(self):
        bot = self.bot
        #オーナー判定
        def is_owner():
            def predicate(ctx):
                return ctx.author.display_name in self.config["normal"]["owner"]
            return commands.check(predicate)

        def time():
            return datetime.datetime.now().strftime('[%H:%M:%S]')

        @bot.event
        async def event_ready():
            print(time() + self.lang["boot"].format(bot.user.display_name))
            if self.debug:
                print(f"EMail: {bot.user.email}")
            while not bot.incoming_pending_friends == []:
                await bot.incoming_pending_friends[0].accept()
            bot.status = self.config["normal"]["status"]
            await bot.party.me.set_outfit(self.config["normal"]["outfit"])
            await bot.party.me.set_backpack(self.config["normal"]["backpack"])
            await bot.party.me.set_pickaxe(self.config["normal"]["pickaxe"])

        #メッセージ系を司る
        @bot.event
        async def event_party_message(message):
            print(f"{time()} {crayons.blue('Partymessage:')} [{message.author}] {message.content}")
        @bot.event
        async def event_friend_message(message):
            print(f"{time()} {crayons.green('Whisper:')} [{message.author}] {message.content}")
        #メンバー系
        @bot.event
        async def event_party_member_update(member):
            try:
                if member.display_name == self.emotemimic:
                    print(crayons.cyan(f"EID: {member.emote}"))
                    await bot.party.me.set_emote(member.emote)
            except TypeError:
                await bot.party.me.clear_emote()

        @bot.event  
        async def event_party_member_join(member):
            print(crayons.cyan(time()+self.lang["join_member"].format(member.display_name,member.party.member_count)))
            await bot.party.send(self.config["normal"]["join_message"])
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(self.emote)
        @bot.event
        async def event_party_member_leave(member):
            print(crayons.blue(time()+self.lang["leave_member"].format(member.display_name,member.party.member_count)))
        #フレンド系
        @bot.event
        async def event_friend_add(friend):
            print(time()+self.lang["add_friend"].format(friend.display_name))
        @bot.event
        async def event_friend_remove(friend):
            print(time()+self.lang["remove_friend"].format(friend.display_name))
        @bot.event
        async def event_friend_request(request):
            print(time()+self.lang["incoming_friend_request"].format(request.display_name,request.id))
            await request.accept()
        @bot.event
        async def event_friend_request_decline(friend):
            print(time()+self.lang["decline_outgoing_friend_request"].format(friend.display_name))
        #招待系を司る
        @bot.event
        async def event_party_invite(invitation):
            sender = invitation.sender.display_name
            print(time()+self.lang["incoming_invite"].format(sender))
            if invitation.sender in self.blacklist:
                await invitation.decline()
                print(time()+self.lang["decline_incoming_invite"].format(sender))
            else:
                await invitation.accept()
                print(time()+self.lang["accept_incoming_invite"].format(sender))
        #パーティー系
        @bot.event
        async def event_party_member_promote(old_leader,new_leader):
            print(time()+self.lang["promote"].format(old_leader.display_name,new_leader.display_name))
        @bot.event
        async def event_party_member_kick(member):
            print(time()+self.lang["kicked"].format(member.display_name))
        @bot.event
        async def event_party_member_zombie(member):
            print(time()+self.lang["kicked"].format(member.display_name))
        @bot.event
        async def event_party_member_reconnect(member):
            print(time()+self.lang["reconnect"].format(member.display_name))
        #パーティー参加許可
        @bot.event
        async def event_party_member_confirm(confirmation):
            if confirmation.user.display_name in self.blacklist:
                await confirmation.reject()
                print(time()+self.lang["join_rejected"].format(confirmation.user.display_name))
            else:
                await confirmation.confirm()
        #参加リクエストの処理
        @bot.event
        async def event_party_join_request(request):
            if self.config["normal"]["join_request"] and not request.friend.display_name in self.blacklist:
                await request.accept()
                print(time()+self.lang["join_request_accepted"].format(request.friend.display_name))
            else:
                await request.friend.send(self.lang["join_request_denied"])

        @bot.event
        async def event_command_error(ctx,error):
            if self.debug:
                print(str(type(error)))
            if str(type(error)) == "<class 'fortnitepy.ext.commands.errors.CheckFailure'>":
                await ctx.send(self.lang["not_owner"])
            elif str(type(error)) == "<class 'fortnitepy.ext.commands.errors.CommandNotFound'>":
                #what the fuck is this
                return None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None or None
            else:
                a = ""
                for i in traceback.format_exception(error.__class__, error, error.__traceback__,chain=False):
                    a = a+i
                print(crayons.red(a[:-1]))

        #commands
        @bot.command(aliases=self.command["cid"])
        async def cid_(ctx,arg):
            await bot.party.me.set_outfit(arg)
        
        @bot.command(aliases=self.command["eid"])
        async def eid_(ctx,arg):
            await bot.party.me.set_emote(arg)
        
        @bot.command(aliases=self.command["bid"])
        async def bid_(ctx,arg):
            await bot.party.me.set_backpack(arg)
        
        @bot.command(aliases=self.command["pickaxe_id"])
        async def pid_(ctx,arg):
            await bot.party.me.set_pickaxe(arg)
        
        @bot.command(aliases=self.command["partyinfo"])
        async def partyinfo_(ctx):
            empt = []
            for i in bot.party.members:
                print(i)
                empt.append(str(i))
            dt = ','.join(empt)
            await ctx.send(self.lang["party_info"].format(bot.party.id,bot.party.leader,bot.party.member_count,dt))

        @bot.command(aliases=self.command["exec"])
        @is_owner()
        async def aexec(ctx,*,code):
            exec(
            f'async def asyncexec(): ' +
            ''.join(f'\n {l}' for l in code.split('\n'))
            ,{"ctx":ctx,"bot":bot})
            return await locals()['asyncexec']()
        
        @bot.command(aliases=self.command["fetch"])
        async def fetch_(ctx,arg):
            fetch = await bot.fetch_user(arg)
            print(f"{time()} {fetch.id}")
            await ctx.send(f"{fetch.id}")
        
        @bot.command(aliases=self.command["hello"])
        async def hello_(ctx):
            await ctx.send(f"こんにちは {ctx.author.display_name} さん")
        
        @bot.command(aliases=self.command["clear"])
        async def clear_(ctx):
            await bot.party.me.clear_emote()
            await ctx.send(self.lang["stopped_emote"])

        @bot.command(aliases=self.command["outfit"])
        async def outfit_(ctx,*,arg: str):
            with open("ja.json","r",encoding="UTF-8") as f:
                for id in json.load(f)["data"]:
                    get_name = str(id.get("name")).lower()
                    get_id = id.get("id")
                    get_type = id["type"]["backendValue"]
                    if get_name in arg.lower() and get_type == "AthenaCharacter":
                        await bot.party.me.set_outfit(get_id)
                        await ctx.send(self.lang["changed_outfit"].format(get_name))
                        break
                else:
                    with open("en.json","r",encoding="UTF-8") as f:
                        for id in json.load(f)["data"]:
                            get_name = str(id.get("name")).lower()
                            get_id = id.get("id")
                            get_type = id["type"]["backendValue"]
                            if get_name == arg.lower() and get_type == "AthenaCharacter":
                                await bot.party.me.set_outfit(get_id)
                                await ctx.send(self.lang["changed_outfit"].format(get_name))
                                break
                            
        @bot.command(aliases=self.command["emote"])
        async def emotecommand(ctx,*,arg:str):
            global emote
            with open("ja.json","r",encoding="UTF-8") as f:
                for id in json.load(f)["data"]:
                    get_name = str(id.get("name")).lower()
                    get_id = id.get("id")
                    get_type = id["type"]["backendValue"]
                    if get_name == arg.lower() and get_type == "AthenaDance":
                        await bot.party.me.clear_emote()
                        await bot.party.me.set_emote(get_id)
                        await ctx.send(self.lang["changed_emote"].format(get_name))
                        self.emote = get_id
                        break
                else:
                    with open("en.json","r",encoding="UTF-8") as f:
                        for id in json.load(f)["data"]:
                            get_name = str(id.get("name")).lower()
                            get_id = id.get("id")
                            get_type = id["type"]["backendValue"]
                            if get_name == arg.lower() and get_type == "AthenaDance":
                                await bot.party.me.clear_emote()
                                await bot.party.me.set_emote(get_id)
                                await ctx.send(self.lang["changed_emote"].format(get_name))
                                self.emote = get_id
                                break
                            
        @bot.command(aliases=self.command["backpack"])
        async def backpackcommand(ctx,*,arg:str):
            with open("ja.json","r",encoding="UTF-8") as f:
                for id in json.load(f)["data"]:
                    get_name = str(id.get("name")).lower()
                    get_id = id.get("id")
                    get_type = id["type"]["backendValue"]
                    if get_name == arg.lower() and get_type == "AthenaBackpack":
                        await bot.party.me.set_backpack(get_id)
                        await ctx.send(self.lang["changed_backpack"].format(get_name))
                        break
                else:
                    with open("en.json","r",encoding="UTF-8") as f:
                        for id in json.load(f)["data"]:
                            get_name = str(id.get("name")).lower()
                            get_id = id.get("id")
                            get_type = id["type"]["backendValue"]
                            if get_name == arg.lower() and get_type == "AthenaBackpack":
                                await bot.party.me.set_backpack(get_id)
                                await ctx.send(self.lang["changed_backpack"].format(get_name))
                                break
                            
                            
        @bot.command(aliases=self.command["pickaxe"])
        async def pickaxecommand(ctx,*,arg:str):
            with open("ja.json","r",encoding="UTF-8") as f:
                for id in json.load(f)["data"]:
                    get_name = str(id.get("name")).lower()
                    get_id = id.get("id")
                    get_type = id["type"]["backendValue"]
                    if get_name == arg.lower() and get_type == "AthenaPickaxe":
                        await bot.party.me.clear_emote()
                        await bot.party.me.set_pickaxe(get_id)
                        await bot.party.me.set_emote("EID_Iceking")
                        await ctx.send(self.lang["changed_pickaxe"].format(get_name))
                        break
                else:
                    with open("en.json","r",encoding="UTF-8") as f:
                        for id in json.load(f)["data"]:
                            get_name = str(id.get("name")).lower()
                            get_id = id.get("id")
                            get_type = id["type"]["backendValue"]
                            if get_name == arg.lower() and get_type == "AthenaPickaxe":
                                await bot.party.me.clear_emote()
                                await bot.party.me.set_pickaxe(get_id)
                                await bot.party.me.set_emote("EID_Iceking")
                                await ctx.send(self.lang["changed_pickaxe"].format(get_name))
                                break
                            
        @bot.command(aliases=self.command["bp"])
        async def bp_(ctx,level):
            await bot.party.me.set_battlepass_info(has_purchased=True,level=int(level))
            await ctx.send(self.lang["changed_bp"])

        @bot.command(aliases=self.command["sitout"])
        async def sitout_(ctx):
            await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
            await ctx.send(self.lang["status_sitout"])

        @bot.command(aliases=self.command["ready"])
        async def ready_(ctx):
            await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
            await ctx.send(self.lang["status_ready"])

        @bot.command(aliases=self.command["unready"])
        async def unready_(ctx):
            await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
            await ctx.send(self.lang["status_unready"])

        @bot.command(name="raise")
        async def raise_(ctx):
            raise SuicideException("You committed suicide.")

        @bot.command(aliases=self.command["match"])
        async def match_(ctx,arg):
            await bot.party.me.set_in_match(players_left=int(arg),)
            await ctx.send(self.lang["match"].format(arg))

        @bot.command(aliases=self.command["unmatch"])
        async def unmatch_(ctx):
            await bot.party.me.clear_in_match()
            await ctx.send(self.lang["unmatch"])

        @bot.command(aliases=self.command["spamint"])
        @is_owner()
        async def spamint_(ctx):
            for i in range(15):
                await ctx.send("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
                
        @bot.command(aliases=self.command["block"])
        @is_owner()
        async def block_(ctx,*,arg):
            fetch = await bot.fetch_user(arg)
            await bot.block_user(fetch.id)
            await ctx.send(self.lang["block"].format(fetch.display_name))

        @bot.command(aliases=self.command["join"])
        @is_owner()
        async def join_(ctx,*,arg):
            fetch = await bot.fetch_user(arg)
            fetch = bot.get_friend(fetch.id)
            await fetch.join_party()

        @bot.command(aliases=self.command["invite"])
        async def invite_(ctx,*,arg):
            fetch = await bot.fetch_user(arg)
            fetch = bot.get_friend(fetch.id)
            await fetch.invite()
            await ctx.send(time()+self.lang["invite"].format(fetch.display_name))
            
        @bot.command(aliases=self.command["status"])
        @is_owner()
        async def status_(ctx,*,arg):
            await bot.set_presence(status=f"{arg}")
            await ctx.send(self.lang["changed_status"].format(arg))

        @bot.command(aliases=self.command["chatban"])
        @is_owner()
        async def chatban_(ctx,arg):
            fetch = await bot.fetch_user(arg)
            fetch = bot.party.get_member(fetch.id)
            await fetch.chatban()
            await ctx.send(self.lang["chatban"].format(fetch.display_name))

        @bot.command(aliases=self.command["togglepriv"])
        @is_owner()
        async def togglepriv_(ctx):
            if bot.party.privacy == self.public:
                await bot.party.set_privacy(self.private)
            elif bot.party.privacy == self.private:
                await bot.party.set_privacy(self.public)

        @bot.command(aliases=self.command["hide"])
        @is_owner()
        async def hide_(ctx,member):
            user_id = await bot.fetch_user(member)
            getmember = bot.party.get_member(user_id.id)
            await bot.party.set_squad_assignments({getmember:fortnitepy.SquadAssignment(hidden=True)})
            await ctx.send(self.lang["hide"].format(user_id.display_name))
            
        @bot.command(aliases=self.command["show"])
        @is_owner()
        async def show_(ctx,member):
            user = await bot.fetch_user(member)
            getmember = bot.party.get_member(user.id)
            await bot.party.set_squad_assignments({getmember:fortnitepy.SquadAssignment(hidden=False)})
            await ctx.send(self.lang["show"].format(user.display_name))


        @bot.command(aliases=self.command["kick"])
        @is_owner()
        async def kick_(ctx,user):
            fetch_user = await bot.fetch_user(user)
            fetch_member = bot.party.get_member(fetch_user.id)
            await fetch_member.kick()
            await ctx.send(self.lang["kick"].format(fetch_member.display_name))

        @bot.command(aliases=self.command["promote"])
        @is_owner()
        async def promote_(ctx,arg):
            fetch_user = await bot.fetch_user(arg)
            fetch_member = bot.party.get_member(fetch_user.id)
            await fetch_member.promote()
            await ctx.send(self.lang["promote"].format(fetch_member.display_name))

        @bot.command(aliases=self.command["leave"])
        @is_owner()
        async def leave_(ctx):
            await bot.party.me.leave()

        @bot.command(aliases=self.command["getkd"])
        async def getkd_(ctx,platform,*,username):
            user = await bot.fetch_user(username)
            stats = await bot.fetch_br_stats(user.id)
            try:
                if platform == "pad":
                    kill_death = stats.get_kd(stats.get_stats()['gamepad']['defaultsolo'])
                    await ctx.send(self.lang["kd_pad"].format(username,str(kill_death)))
                elif platform == "keyboard":
                    kill_death = stats.get_kd(stats.get_stats()['keyboardmouse']['defaultsolo'])
                    await ctx.send(self.lang["kd_keyboard"].format(username,str(kill_death)))
                elif platform == "touch":
                    kill_death = stats.get_kd(stats.get_stats()['touch']['defaultsolo'])
                    await ctx.send(self.lang["kd_touch"].format(username,str(kill_death)))
                else:
                    await ctx.send(self.lang["supported_platform"])
            except AttributeError:
                await ctx.send(self.lang["player_notfound"].format(username))     

        @bot.command(aliases=self.command["open"])
        @is_owner()
        async def forceopenparty_(ctx):
            await bot.party.set_privacy(self.public)
            await ctx.send(self.lang["change_to_public"])

        @bot.command(aliases=self.command["close"])
        @is_owner()
        async def forcecloseparty_(ctx):
            await bot.party.set_privacy(self.private)
            await ctx.send(self.lang["change_to_private"])

        @bot.command(aliases=self.command["friendlist"])
        async def friendlist_(ctx):
            empt = []
            for i in bot.friends:
                print(i)
                empt.append(str(i))
            await ctx.send("\n"+'\n'.join(empt))

        @bot.command(aliases=self.command["isowner"])
        async def isowner_(ctx):
            if ctx.author.display_name in self.config["normal"]["owner"]:
                await ctx.send("you are my owner")
            else:
                await ctx.send("you aren't my owner")

        @bot.command(aliases=self.command["randomrecruit"])
        async def randomrecruit_(ctx):
            for i in range(20):
                await bot.party.me.set_outfit(random.choice(self.recruits))
                await asyncio.sleep(0.01)
        
        try:
            bot.run()
        except fortnitepy.errors.AuthException as e:
            print(crayons.red(f"エラーコード:{e}\n認証に失敗しました。"))
            authorization()
            bot.run()

if __name__ == "__main__":
    Bot().main()