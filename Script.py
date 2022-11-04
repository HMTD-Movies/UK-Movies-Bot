import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class script(object):
    HOME_BUTTONURL_UPDATES = environ.get("HOME_BUTTONURL_UPDATES", 'https://mdiskpro.xyz/ref/Karthik')
    START_TXT = environ.get("START_TXT", '''<b>Hello {} 👋🏻 I'm an UK Studios Official Auto Filter Bot (Movie Search Bot) Maintained by @UK_Studios_Official. We are Providing Tamil and Tamil Dubbed Movies. More Languages Coming Soon. I Can Support Upto 4GB File. You Can Get added Files GDrive Links and 4GB above Links also. You Can Get GDrive Links in www.HMTDMovies.tk Keep me Join to Our Official Channel to Receive Bot & Movies Updates in @UK_Studios_Official. Check "😁 About" Button.''')
    HELP_TXT = """**Hi {}
𝙷𝙴𝚁𝙴 𝙸𝚂 𝙼𝚈 𝙷𝙴𝙻𝙿 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂.**"""
    ABOUT_TXT = """<b>🤖 My Name : <a href='https://t.me/UK_Auto_Filter_Bot'>UK Auto Filter Bot</a>\n\n🧑🏻‍💻 Developer : <a href='https://HMTDMovies.tk/'>Karthik</a>\n\n📝 Language : <a href='https://www.python.org/'>Python3</a>\n\n📚 Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {version}</a>\n\n📡 Hosted on : <a href='https://www.hostinger.in'>VPS</a>\n\n🌐 Website : <a href='https://HMTDMovies.tk/'>HMTD Movies</a>\n\n🧑🏻‍ Feedback : <a href='https://t.me/HMTD_Feedback_Bot'>Feedback Bot</a>\n\n📢 Updates Channel : <a href='https://t.me/UK_Studios_Official'>UK Studios Official</a>\n\n👥 Discussion Group : <a href='https://t.me/HMTD_Discussion_Group'>Discussion Group</a></b>"""
    SOURCE_TXT = """<b>Create One Like This:</b>
» I will Create One Bot For You. But Paid<b>
» Contact Me @HMTD_Karthik<b>"""
    MANUELFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and Search Bot will respond whenever a keyword is found the message

<b>NOTE:</b>
<b>1. Search Bot should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.</b>

<b>Commands and Usage:</b>
<b>• /filter - add a filter in chat
• /filters - list all the filters of a chat
• /del - delete a specific filter in chat
• /delall - delete the whole filters in a chat (chat owner only)</b>"""
    BUTTON_TXT = """Help: <b>Buttons</b>

- Search Bot Supports both url and alert inline buttons.

<b>NOTE:</b>
<b>1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. Search Bot supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format</b>

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/HMTD_Karthik)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""
    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>

<b>NOTE:</b>
<b>1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db.</b>"""
    CONNECTION_TXT = """Help: <b>Connections</b>

<b>- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.</b>

<b>NOTE:</b>
<b>1. Only admins can add a connection.
2. Send</b> <code>/connect</code> <b>for connecting me to ur PM</b>

<b>Commands and Usage:</b>
<b>• /connect  - connect a particular chat to your PM
• /disconnect  - disconnect from a chat
• /connections - list all your connections</b>"""
    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
<b>these are the extra features of Auto Filter Bot (Movie Search Bot)</b>

<b>Commands and Usage:</b>
• /id - <code>get id of a specified user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""
    ADMIN_TXT = """Help: <b>Admin mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    STATUS_TXT = """★ 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code>
★ 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code>
★ 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱
★ 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝚒𝙱"""
    LOG_TEXT_G = """#𝐍𝐞𝐰𝐆𝐫𝐨𝐮𝐩
    
<b>᚛› 𝐆𝐫𝐨𝐮𝐩 ⪼ {}(<code>{}</code>)</b>
<b>᚛› 𝐓𝐨𝐭𝐚𝐥 𝐌𝐞𝐦𝐛𝐞𝐫𝐬 ⪼ <code>{}</code></b>
<b>᚛› 𝐀𝐝𝐝𝐞𝐝 𝐁𝐲 ⪼ {}</b>
"""
    LOG_TEXT_P = """#𝐍𝐞𝐰𝐔𝐬𝐞𝐫  
    
<b>᚛› 𝐈𝐃 - <code>{}</code></b>
<b>᚛› 𝐍𝐚𝐦𝐞 - {}</b>
"""
