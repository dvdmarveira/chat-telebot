import telebot 
from telebot import types
import os
from dotenv import load_dotenv

# Carregar a chave da API
load_dotenv()
CHAVE_API = os.getenv("CHAVE_API")

bot = telebot.TeleBot(CHAVE_API)

# /start 
@bot.message_handler(commands=["start"])
def start(mensagem):
  nome = mensagem.from_user.first_name
  texto = f"Olá, {nome}! 👋\nBem-vindo(a) ao *DvDoces*! Como posso te ajudar?"
  
  # Menu
  markup = types.InlineKeyboardMarkup()
  markup.add(
    types.InlineKeyboardButton("🍰 Cardápio", callback_data="cardapio"),
    types.InlineKeyboardButton("📦 Fazer Pedido", callback_data="pedido")
  )
  markup.add(
    types.InlineKeyboardButton("⏰ Horário de Funcionamento", callback_data="horario"),
    types.InlineKeyboardButton("📍 Endereço e Contato", callback_data="contato")
  )
  markup.add(
    types.InlineKeyboardButton("💬 Falar com Atendente", callback_data="atendente"),
  )
  
  bot.send_message(mensagem.chat.id, texto, reply_markup=markup, parse_mode="Markdown")

# Resposta aos botões do menu




print("Bot em execução...")
bot.infinity_polling()