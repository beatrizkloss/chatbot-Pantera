import os
import requests
import asyncio
import nest_asyncio
import traceback
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram.request import HTTPXRequest
from commands import start_command
from buttons import handle_button_click
from services.notifications_manager import get_all_users, init_db, is_subscribed, subscribe_user, unsubscribe_user

nest_asyncio.apply()

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
TWITCH_STREAM_URL = "https://api.twitch.tv/helix/streams"

# Configura o request com timeout maior
custom_request = HTTPXRequest(read_timeout=60.0)
app = Application.builder().token(TOKEN).request(custom_request).build()

# Verifica se a FURIA está ao vivo na Twitch
def is_furia_live():
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "user_login": "furiatv"
    }
    try:
        response = requests.get(TWITCH_STREAM_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return bool(data["data"])
        else:
            print(f"Erro na requisição à Twitch: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erro na conexão com a Twitch: {e}")
        return False

# Envia notificação para todos os usuários inscritos
async def notify_users_if_live(application):
    if is_furia_live():
        users = get_all_users()
        for user_id in users:
            try:
                await application.bot.send_message(
                    chat_id=user_id,
                    text="🚨 A FURIA está AO VIVO na Twitch! 🎥 https://twitch.tv/furiatv"
                )
            except Exception as e:
                print("Erro ao verificar live na Twitch:")
                print(traceback.format_exc())
# Manipula cliques dos botões 
async def callback_query_handler(update, context):
    query = update.callback_query
    data = query.data

    if data.startswith("curtir_"):
        nickname = data.split("_")[1]
        await query.answer(f"Você curtiu o {nickname}! 🎉", show_alert=True)

    elif data == "menu":
        await start_command(update, context)

    elif data == "ativar_notificacoes":
        user_id = update.effective_user.id
        if is_subscribed(user_id):
            unsubscribe_user(user_id)
            await query.answer("❌ Notificações desativadas.")
        else:
            subscribe_user(user_id)
            await query.answer("✅ Notificações ativadas.")

    else:
        await handle_button_click(query, context)

# Função principal
async def main():
    init_db()
    print("Banco de dados inicializado com sucesso.")

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(callback_query_handler))


    scheduler = AsyncIOScheduler()
    scheduler.add_job(notify_users_if_live, IntervalTrigger(minutes=5), args=[app])
    scheduler.start()
    print("Bot está rodando...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    