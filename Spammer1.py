import asyncio
import os
from aiohttp import web
from telegram import Bot, LinkPreviewOptions

BOT_TOKEN = "8905442520:AAG1cKiYotsIqFLoTGwaapBOHITLGqlLyIo"
CHANNEL_ID = "@SliderModMenuCodm"

bot = Bot(token=BOT_TOKEN)

# 1. TEMPLATE PARA SA CODM (Inuna ito)
CODM_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/SliderModMenuCodm/631">Latest Update:
Call of Duty v1.6.56
Injector v2.7.8</a>

NEED KEY LOGIN ??? :
For inquiries and availment, send a direct message ~ <a href="https://t.me/phia_maganda">𝑷𝒉𝒊𝒂 𝑭𝒆𝒍𝒊𝒄𝒊𝒂</a>

<a href="https://slider-info-slidermod-register-deviceid.onrender.com/free">Try Free Key Here:</a></i></blockquote>"""

# 2. TEMPLATE PARA SA MLBB UPDATE
MLBB_MESSAGE = """<blockquote expandable="true"><i><a href="https://t.me/SliderModMenuMlbb/6270">Latest Update:
Mobile Legends: Bang Bang
v2.1.88.12027 || Mod v3.1.5</a>

NEED KEY LOGIN ??? :
For inquiries and availment, send a direct message ~ <a href="https://t.me/phia_maganda">Phia Felicia</a>

No Free 🫪 GETS!?</i></blockquote>"""

# Dalawang templates na lang at inuna ang CODM bago MLBB
ALL_MESSAGES = [CODM_MESSAGE, MLBB_MESSAGE]

async def loop_spam():
    print("Spammer bot started (Alternating CODM and MLBB)...")
    index = 0
    
    while True:
        try:
            current_message = ALL_MESSAGES[index % len(ALL_MESSAGES)]
            
            # 1. IPAPALAPAG ANG CURRENT MESSAGE
            sent_message = await bot.send_message(
                chat_id=CHANNEL_ID,
                text=current_message,
                parse_mode="HTML",
                disable_notification=False,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            print(f"Message sent! (Index: {index} | ID: {sent_message.message_id})")

            # 2. BIBILANG NG ORAS BAGO BURAHIN (3600 seconds = 1 hour)
            await asyncio.sleep(3600)          

            # 3. BURAHIN PAGKATAPOS
            await bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=sent_message.message_id
            )
            print(f"Deleted Message ID: {sent_message.message_id}")

            # 4. AGWAT BAGO MAG-SEND ULIT NG KASUNOD NA MESSAGE (3 seconds)
            await asyncio.sleep(3)
            
            index += 1

        except Exception as e:
            print("Error sa loop:", e)
            await asyncio.sleep(10)

# --- RENDER WEB SERVER CONFIGURATION ---
async def handle_index(request):
    return web.Response(text="Bot is running smoothly on Render!")

async def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    print(f"Starting dummy web server on port {port} for Render...")
    await site.start()
    
    await loop_spam()

if __name__ == "__main__":
    asyncio.run(main())
