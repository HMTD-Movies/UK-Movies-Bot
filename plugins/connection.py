from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are anonymous admin. Use /connect {message.chat.id} in PM</b>")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Enter in Correct Format!</b>\n\n"
                "<b>/connect Group ID</b>\n\n"
                "<b>Get your Group ID by Adding This Bot to Your Group and Use</b> <code>/id</code>",
                quote=True
            )
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and userid not in ADMINS
        ):
            await message.reply_text("<b>You should be an Admin in Given Group!</b>", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "<b>Invalid Group ID!\n\nIf Correct, Make sure I'm Present in Your Group!</b>",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"<b>Successfully Connect to {title}\nNow You Can Manage Your Group From Here...</b>",
                    quote=True,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await client.send_message(
                        userid,
                        f"<b>Connected to {title}!</b>",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
            else:
                await message.reply_text(
                    "<b>You're already Connected to This Chat!</b>",
                    quote=True
                )
        else:
            await message.reply_text("<b>Add me as an Admin in Group</b>", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('<b>Some Error Occurred! Try again later.</b>', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are Anonymous Admin. Use /connect {message.chat.id} in PM</b>")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("<b>Run /connections to View or Disconnect from Groups!</b>", quote=True)

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("<b>Successfully Disconnected from This Chat</b>", quote=True)
        else:
            await message.reply_text("<b>This chat isn't Connected to me!\nDo /connect to Connect.</b>", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "<b>There are no Active Connections! Connect to some Groups First.</b>",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "<b>Connected Groups :-\n\n</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "<b>There are no Active Connections!! Connect to some Groups First.</b>",
            quote=True
        )
