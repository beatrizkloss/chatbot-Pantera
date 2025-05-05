from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils import menu_button

import os

# Simulando uma base manual dos jogadores
players_active = [
    {
        "photo_url": "./img/YUURIH.webp",
        "nickname": "yuurih",
        "real_name": "Yuri Gomes dos Santos Boian",
        "country": "🇧🇷 Brasil",
        "role": "Rifler",
        "birthdate": "22/12/1999",
        "joined": "2017",
        "socials": {
            "X": "https://x.com/yuurih",
            "Instagram": "https://www.instagram.com/yuurihfps/",
            "Twitch": "https://www.twitch.tv/yuurih"
        }
    },
    {
        "photo_url": "./img/KSCERATO.webp",
        "nickname": "KSCERATO",
        "real_name": "Kaike Silva Cerato",
        "country": "🇧🇷 Brasil",
        "role": "Rifler (lurker)",
        "birthdate": "12/09/1999",
        "joined": "2018",
        "socials": {
            "X": "https://x.com/kscerato",
            "Instagram": "https://instagram.com/kscerato",
            "Twitch": "https://www.twitch.tv/kscerato"
        }
    },
    {
        "photo_url": "./img/FALLEN.webp",
        "nickname": "FalleN",
        "real_name": "Gabriel Toledo de Alcântara Sguario",
        "country": "🇧🇷 Brasil",
        "role": "AWPer / Capitão",
        "birthdate": "30/05/1991",
        "joined": "2023",
        "socials": {
            "X": "https://x.com/FalleNCS",
            "Instagram": "https://www.instagram.com/fallen/",
            "Twitch": "https://www.twitch.tv/gafallen"
        }
    },
    {
        "photo_url": "./img/MOLODOY.jpg",
        "nickname": "molodoy",
        "real_name": "Danil Golubenko",
        "country": "🇰🇿 Cazaquistão",
        "role": "AWPer",
        "birthdate": "10/01/2005",
        "joined": "2025",
        "socials": {
            "X": "https://x.com/tvoy_molodoy",
            "Instagram": "https://www.instagram.com/danil.molodoy_/",
            "Twitch": ""
        }
    },
    {
        "photo_url": "./img/YEKINDAR.jpg",
        "nickname": "YEKINDAR",
        "real_name": "Mareks Gaļinskis",
        "country": "🇱🇻 Letônia",
        "role": "Rifler (entry fragger)",
        "birthdate": "04/10/1999",
        "joined": "2025",
        "socials": {
            "X": "https://x.com/yek1ndar",
            "Instagram": "https://instagram.com/yek1ndar",
            "Twitch": "https://www.twitch.tv/yekindar"
        }
    },
]

players_inactive = [
    {
        "photo_url": "./img/skullz.webp",
        "nickname": "skullz",
        "real_name": "Felipe Frank Medeiros",
        "country": "🇧🇷 Brasil",
        "role": "Rifler",
        "birthdate": "20/04/2002",
        "joined": "2024",
        "socials": {
            "X": "https://x.com/skullzcs",
            "Instagram": "https://www.instagram.com/skullzcs/",
            "Twitch": ""
        }
    },
    {
        "photo_url": "./img/CHELO.webp",
        "nickname": "chelo",
        "real_name": "Marcelo Cespedes",
        "country": "🇧🇷 Brasil",
        "role": "Rifler (entry fragger)",
        "birthdate": "08/06/1998",
        "joined": "2023",
        "socials": {
            "X": "https://x.com/chelok1ng",
            "Instagram": "https://www.instagram.com/chelok1ng/",
            "Twitch": "https://www.twitch.tv/chelok1ng?lang=pt-br"
        }
    },
]

async def show_players_list(query, players_list):
    img_dir = os.path.join(os.getcwd(), 'app', 'img')  

    for p in players_list:
        caption = (
            f"👤 {p['real_name']} ({p['nickname']})\n"
            f"🌎 País: {p['country']}\n"
            f"🎯 Função: {p['role']}\n"
            f"🎂 Nascimento: {p['birthdate']}\n"
            f"🗓 Entrou na FURIA: {p['joined']}\n"
            f"🔗 Redes sociais:\n"
            f" <a href='{p['socials']['X']}'>X</a>\n"
            f"<a href='{p['socials']['Instagram']}'>Instagram</a>\n"
            f"<a href='{p['socials']['Twitch']}'>{'Twitch' if p['socials']['Twitch'] else ''}</a>"
        )

        # Configurando o botão para curtir o jogador
        keyboard = InlineKeyboardMarkup([ 
            [InlineKeyboardButton(f"❤️ Curtir {p['nickname']}", callback_data=f"curtir_{p['nickname']}")]
        ])

        
        photo_path = os.path.join(img_dir, os.path.basename(p['photo_url']))

        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                
                await query.message.reply_photo(photo=photo, caption=caption, reply_markup=keyboard, parse_mode="HTML")
        else:
            
            await query.message.reply_text(caption, reply_markup=keyboard, parse_mode="HTML")

async def players(query):
    # Introdução dos jogadores
    await query.message.reply_text("🎮 Jogadores Ativos da FURIA CS:")

    # Jogadores ativos
    await show_players_list(query, players_active)

    # Jogadores inativos
    await query.message.reply_text("\n💤 Jogadores Inativos (Reservas):")
    await show_players_list(query, players_inactive)

    # Botão de menu no final
    await query.message.reply_text(
        "🔙 Voltar ao Menu:",
        reply_markup=menu_button()
    )