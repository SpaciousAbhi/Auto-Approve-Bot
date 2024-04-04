from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://telegra.ph/file/2d326373f7aedada55fcc.mp4'
]

# Main process
@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        welcome_message = f"Hello {m.from_user.mention}!\n\nI'm an auto-approve [Admin Join Requests](https://telegram.me/VenomStoneNetwork) Bot. I specialize in efficiently approving users in Groups/Channels. Simply add me to your Channel or Group and promote me as an Admin with the 'Add Members' permission.\n\nLooking forward to assisting you!\n\nBy: @VenomStoneNetwork"
        await app.send_video(kk.id, img, welcome_message)
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("User isn't starting the bot (means group).")
    except Exception as err:
        print(str(err))    

# Start command
@app.on_message(filters.command("start"))
async def start_command(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://telegram.me/VenomStoneNetwork"),
                        InlineKeyboardButton("💬 Support", url="https://telegram.me/VenomStoneNetwork")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://telegram.me/VenomStoneAutoRequestAceeptBot?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            welcome_message = """**Hello {}!\n\nI am an auto-approve [Admin Join Requests](https://telegram.me/VenomStoneNetwork) Bot. I specialize in efficiently approving users in Groups/Channels. Simply add me to your Channel or Group and promote me as an Admin with the 'Add Members' permission.\n\nLooking forward to assisting you!\n\nBy: @VenomStoneNetwork**""".format(m.from_user.mention)
            await m.reply_photo("https://telegra.ph/file/63d723680cca52ba46319.jpg", caption=welcome_message, reply_markup=keyboard)
        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://telegram.me/VenomStoneAutoRequestAceeptBot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text(f"**{m.from_user.first_name}**, write me private for more details.", reply_markup=keyboard)
        print(f"{m.from_user.first_name} has started your bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👉 Update Channel 👈", url="https://telegram.me/VenomStoneNetwork")
                ],
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
                ]
            ]
        )
        await m.reply_text(f"**⚠️ Access Denied! ⚠️\n\nPlease Join my Updates Channel to use me. If you joined, click the check again button to confirm.**", reply_markup=key)

# Callback query
@app.on_callback_query(filters.regex("chk"))
async def check_callback(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://telegram.me/VenomStoneNetwork"),
                        InlineKeyboardButton("💬 Support", url="https://telegram.me/VenomStoneNetwork")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://telegram.me/VenomStoneAutoRequestAceeptBot?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            welcome_message = """**Hello {}!\n\nI am an auto-approve [Admin Join Requests](https://telegram.me/MovieVillaYT) Bot. I specialize in efficiently approving users in Groups/Channels. Simply add me to your Channel or Group and promote me as an Admin with the 'Add Members' permission.\n\nLooking forward to assisting you!\n\nBy: @VenomStoneNetwork**""".format(cb.from_user.mention)
            await cb.message.edit(welcome_message, reply_markup=keyboard, disable_web_page_preview=True)
        print(f"{cb.from_user.first_name} has started your bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to the channel. Join and try again. 🙅‍♂️")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
