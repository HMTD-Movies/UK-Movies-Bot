from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired

"""-------------------------------------------------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>CHAT NOT ALLOWED 🐞\n\nMy Admins Has Restricted me from Working Here! If you Want to Know more About it Contact Owner...</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
            InlineKeyboardButton('How to Use Me ', url=f"https://t.me/{temp.U_NAME}?start=help"),
            InlineKeyboardButton('📢 Join Update Channel', url='https://t.me/UK_Studios_Official')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>›› Thanks to Add me to Your Group. {message.chat.title} ❣️\n›› Don't Forget to Make me Admin.\n›› Is Any Doubts About Using me Click Below Button...⚡⚡</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                video="https://telegra.ph/file/11d612c9f9a61c19427b0.mp4",                                               
                                                 caption=f'<b>Hello 👋🏻, {u.mention} Welcome to Our Group\nUK Movies Group\nWe are Providing Tamil and Tamil Dubbed Movies. More Languages Coming Soon. I Can Support Upto 4GB File. You Can Get added Files GDrive Links and 4GB above Links also. You Can Get GDrive Links in <a href=https://www.HMTDMovies.tk/><b></b>www.HMTDMovies.tk</a>. Keep me Join to Our Official Channel to Receive Bot & Movies Updates in <a href=https://t.me/UK_Movies_Zone_Updates><b></b>UK Movies Zone (Updates)</a>.</b>',
                                                 reply_markup=InlineKeyboardMarkup( [ [ InlineKeyboardButton('🚫 Group Rules 🚫', url='http://t.me/MissRose_bot?start=rules_-1001650088903') ] ] )
                )

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a chat 🆔</b>')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('👥 Support', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"<b>left the chat</b> `{chat}`")
    except Exception as e:
        await message.reply(f'<b>Error - {e}</b>')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a chat 🆔</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "<b>No reason Provided</b>"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('<b>Give Me A Valid Chat 🆔</b>')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("<b>Chat Not Found In DB!</b>")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('C<b>hat Successfully Disabled</b>')
    try:
        buttons = [[
            InlineKeyboardButton('👥 Support', url=f'https://t.me/{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>Hello Friends, \nMy Admin has told me to Leave From Group. So I go! If you Wanna Add me Again Contact my Support Group. \nReason :</b> <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"<b>Error - {e}</b>")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give Me a Chat 🆔</b>')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('<b>Give Me A Valid Chat 🆔</b>')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("<b>Chat Not Found In DB!</b>")
    if not sts.get('is_disabled'):
        return await message.reply('<b>This chat is Not Yet Disabled.</b>')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("<b>Chat Successfully re-enabled</b>")


@Client.on_message(filters.command('stats') & filters.incoming)
async def get_ststs(bot, message):
    rju = await message.reply('<b>Accessing Status 📊 Details...</b>')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await rju.edit(script.STATUS_TXT.format(files, total_users, totl_chats, size, free))


# a function for trespassing into others groups, Inspired by a Vazha
# Not to be used , But Just to showcase his vazhatharam.
# @Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give Me a Chat 🆔</b>')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('<b>Give Me A Valid Chat 🆔</b>')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("<b>Invite Link Generation Failed, Iam Not Having Sufficient Rights</b>")
    except Exception as e:
        return await message.reply(f'<b>Error {e}</b>')
    await message.reply(f'<b>Here is your Invite Link {link.invite_link}</b>')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('<b>Give me a user 🆔 / Username</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an invalid user, make sure ia have met him before.</b>")
    except IndexError:
        return await message.reply("<b>This might be a Channel, make sure its a user.</b>")
    except Exception as e:
        return await message.reply(f'<b>Error - {e}</b>')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is already banned\nReason: {jar['ban_reason']}</b>")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"<b>Successfully banned {k.mention}</b>")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('<b>Give me a user 🆔 / Username</b>')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("<b>This is an invalid user, make sure ia have met him before.</b>")
    except IndexError:
        return await message.reply("<b>This might be a Channel, make sure its a user.</b>")
    except Exception as e:
        return await message.reply(f'<b>Error - {e}</b>')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"<b>{k.mention} is not yet banned.</b>")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"<b>Successfully unbanned {k.mention}</b>")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('<b>Getting List Of Users</b>')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="<b>List Of Users</b>")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "<b>Chats Saved In DB Are:\n\n</b>"
    async for chat in chats:
        out += f"<b>Title : `{chat['title']}`\n- ID : `{chat['id']}`</b>"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="<b>List Of Chats</b>")
