from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="menu")]
    ])