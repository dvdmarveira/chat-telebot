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
@bot.callback_query_handler(func=lambda call: True)
def responder_botoes(call):
    if call.data == "cardapio":
        bot.send_message(call.message.chat.id, "🍰 Nosso cardápio:\n\n- Bolo de chocolate\n- Cupcake de morango\n- Brownie recheado\n\nAcesse mais detalhes no nosso Instagram: @dvdoces")

    elif call.data == "pedido":
        bot.send_message(call.message.chat.id, "📦 Para fazer um pedido, envie uma mensagem no nosso WhatsApp: https://wa.me/5581999999999\nOu informe seu pedido aqui e iremos anotar! 😊")

    elif call.data == "horario":
        bot.send_message(call.message.chat.id, "⏰ Funcionamos de segunda a sábado, das 10h às 18h.")

    elif call.data == "contato":
        bot.send_message(call.message.chat.id, "📍 Rua das Delícias, 123 – Centro\n📞 (81) 99999-9999\nInstagram: @dvdoces")

    elif call.data == "atendente":
        bot.send_message(call.message.chat.id, "💬 Você será redirecionado para o nosso atendimento humano:\nhttps://wa.me/5581999999999")

print("Bot em execução...")
bot.infinity_polling()