from handlers.players import players as show_players
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from services.notifications_manager import is_subscribed, subscribe_user, unsubscribe_user
from utils import menu_button


async def handle_button_click(query, context):
    data = query.data
    print(f"Botão clicado: {data}")  

    if data == 'history':
        await history(query)
    elif data == 'players':
        await show_players(query)
    elif data == 'socials':
        await socials(query)
    elif data == 'matches':
        await matches(query)
    elif data == 'shop':
        await shop(query)
    elif data == 'notifications':
        await notifications(query)
    elif data == "subscribe":
        subscribe_user(query.from_user.id)
        await query.answer("✅ Notificações ativadas com sucesso!")
        await notifications(query)
    elif data == "unsubscribe":
        unsubscribe_user(query.from_user.id)
        await query.answer("❌ Notificações desativadas com sucesso!")
        await notifications(query)

#-Lógica de cada botão

#---------------história------------------#
async def history(query):
    await query.edit_message_text(
        "📖 A FURIA é uma organização brasileira de esports fundada em 2017 com o objetivo de fortalecer o cenário brasileiro.\n\n"
        "Começou no Counter-Strike, que rapidamente virou sua principal vitrine internacional, com um estilo agressivo e identidade forte, a equipe conquistou respeito global,\n"
        "vencendo a ESL Pro League NA em 2020 e chegando à semifinal do IEM Rio Major 2022, com o apoio da torcida brasileira.\n\nAo longo dos anos, a FURIA expandiu sua atuação "
        "para outros jogos e modalidades, consolidando-se como uma das maiores organizações de esports do país. 🔥🔥",
        reply_markup=menu_button()
    )

#---------------Redes-Sociais------------------#
async def socials(query):
    await query.edit_message_text(
        "🌐 <b>Redes Sociais Oficiais da FURIA:</b>\n\n"
        "🐦 <a href='https://x.com/FURIA'>X</a>\n"
        "📸 <a href='https://instagram.com/furiagg'>Instagram</a>\n"
        "🎥 <a href='https://www.youtube.com/@FURIAggCS'>YouTube</a>\n"
        "🎮 <a href='https://www.twitch.tv/furiatv'>Twitch</a>\n"
        "📱 <a href='https://www.tiktok.com/@furiagg'>TikTok</a>\n"
        "💬 <a href='https://discord.gg/furia'>Discord</a>\n"
        "🔵 <a href='https://www.facebook.com/furiagg'>Facebook</a>",
        parse_mode="HTML",
        reply_markup=menu_button()
    )

#---------------loja------------------#
async def shop(query):
    await query.edit_message_text(
        "🛒 Confira a loja oficial da FURIA com produtos exclusivos para os fãs:\n\n"
        "🌍 <a href='https://www.furia.gg'>Clique Aqui!</a>",
        parse_mode="HTML",
        reply_markup=menu_button()
    )


#---------------partidas------------------#
async def matches(query):
    current_text = query.message.text

    new_text = (
        "❌ <b>Não há partidas futuras no momento.</b>\n"
        "📅 Confira as <b>4 últimas partidas</b> da FURIA:\n\n"

        "📅 <b>Quarta-feira, 9 de abril de 2025</b>\n"
        "🏆 <b>PGL Bucharest 2025</b>\n"
        "🆚 FURIA 0 x 2 The MongolZ\n"
        "🕓 09:50 \n\n"

        "📅 <b>Terça-feira, 8 de abril de 2025</b>\n"
        "🏆 <b>PGL Bucharest 2025</b>\n"
        "🆚 FURIA 0 x 2 Virtus.pro\n"
        "🕓 06:05 \n\n"

        "📅 <b>Segunda-feira, 7 de abril de 2025</b>\n"
        "🏆 <b>PGL Bucharest 2025</b>\n"
        "🆚 FURIA 1 x 2 Complexity\n"
        "🕓 11:05 \n\n"

        "📅 <b>Domingo, 6 de abril de 2025</b>\n"
        "🏆 <b>PGL Bucharest 2025</b>\n"
        "🆚 FURIA 2 x 0 Apogee\n"
        "🕓 12:35 \n"
    )

    if current_text != new_text:
        await query.edit_message_text(new_text, parse_mode="HTML", reply_markup=menu_button())

#---------------notficações------------------#
async def notifications(query):
    user_id = query.from_user.id
    subscribed = is_subscribed(user_id)

    if subscribed:
        text = "🔕 Você está <b>recebendo</b> notificações quando a FURIAtv estiver ao vivo na Twitch.\nDeseja <b>desativar</b>?"
        button = InlineKeyboardButton("Desativar Notificações", callback_data="unsubscribe")
    else:
        text = "🔔 Você <b>não está recebendo</b> notificações da FURIAtv.\nDeseja <b>ativar</b>?" 
        button = InlineKeyboardButton("Ativar Notificações", callback_data="subscribe")

    markup = InlineKeyboardMarkup([[button], [InlineKeyboardButton("🔙 Voltar", callback_data="menu")]])

    await query.edit_message_text(text, reply_markup=markup, parse_mode="HTML")