from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from buttons import handle_button_click 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Criando os botões 
    keyboard = [
        [
            InlineKeyboardButton("💥 História ", callback_data='history'),
            InlineKeyboardButton("🎮 Ver jogadores", callback_data='players'),
        ],
        [
            InlineKeyboardButton("🌐 Redes sociais", callback_data='socials'),
            InlineKeyboardButton("🗓 Próximas partidas", callback_data='matches'),
        ],
        [
            InlineKeyboardButton("🛒 Loja", callback_data='shop'),
            InlineKeyboardButton("🔔 Notificações", callback_data='notifications'),
        ],
        
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = (
        "🐾 Olá, eu sou a PanteraBot!\n\n"
        "A Pantera chegou para te manter por dentro de tudo da FURIA CS! Estou aqui para trazer notícias, curiosidades, estatísticas e avisar quando a FURIA entrar em ação! 🎯\n\n"
        "🏆 Comigo você pode:\n"
        "- Conhecer a história da FURIA CS\n"
        "- Conhecer os jogadores e escolher seu favorito!\n"
        "- Acompanhar as redes sociais oficiais\n"
        "- Ver próximas partidas e lives\n"
        "- Receber alertas especiais!\n\n"
        "Clique nos botões para explorar! 🎮"
    )

    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await handle_button_click(query, context)  
