import telebot 
from telebot import types
import os
from dotenv import load_dotenv

# Carregar a chave da API
load_dotenv()
CHAVE_API = os.getenv("CHAVE_API")

bot = telebot.TeleBot(CHAVE_API)

# Dicionários para armazenar o progresso e os dados dos pedidos
usuarios_pedindo = {}
etapas_pedido = {}

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
    chat_id = call.message.chat.id
    
    if call.data == "cardapio":
        texto_cardapio = (
            "🍰 *Nosso cardápio:*\n\n"
            "- Bolo de chocolate\n"
            "- Cupcake de morango\n"
            "- Brownie recheado\n\n"
            "Você pode ver mais detalhes em nosso Instagram: @dvdoces\n\n"
            "... ou já pode fazer o seu pedido e garantir uma de nossas delícias!"
        )

        markup_cardapio = types.InlineKeyboardMarkup()
        markup_cardapio.add(
            types.InlineKeyboardButton("📦 Fazer Pedido", callback_data="pedido")
        )

        bot.send_message(
            call.message.chat.id,
            texto_cardapio,
            reply_markup=markup_cardapio,
            parse_mode="Markdown"
        )

    elif call.data == "pedido":
        etapas_pedido[chat_id] = "produto"
        usuarios_pedindo[chat_id] = {}
        bot.send_message(chat_id, "📦 Qual doce você gostaria de pedir?")

    elif call.data == "horario":
        bot.send_message(call.message.chat.id, "⏰ Funcionamos de segunda a sábado, das 10h às 18h.")

    elif call.data == "contato":
        bot.send_message(call.message.chat.id, "📍 Rua das Delícias, 123 – Centro\n📞 (81) 99999-9999\nInstagram: @dvdoces")

    elif call.data == "atendente":
        bot.send_message(call.message.chat.id, "💬 Você será redirecionado para o nosso atendimento humano:\nhttps://wa.me/5581999999999")

# Fluxo do pedido
@bot.message_handler(func=lambda msg: msg.chat.id in etapas_pedido)
def processar_pedido(mensagem):
    chat_id = mensagem.chat.id
    etapa = etapas_pedido[chat_id]

    if etapa == "produto":
        usuarios_pedindo[chat_id]["produto"] = mensagem.text
        etapas_pedido[chat_id] = "quantidade"
        bot.send_message(chat_id, "Quantas unidades você deseja?")

    elif etapa == "quantidade":
        usuarios_pedindo[chat_id]["quantidade"] = mensagem.text
        etapas_pedido[chat_id] = "nome"
        bot.send_message(chat_id, "Por favor, informe seu nome.")

    elif etapa == "nome":
        usuarios_pedindo[chat_id]["nome"] = mensagem.text
        etapas_pedido[chat_id] = "entrega"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("📍 Entrega", "🏠 Retirada")
        bot.send_message(chat_id, "Você prefere entrega ou retirada?", reply_markup=markup)

    elif etapa == "entrega":
        usuarios_pedindo[chat_id]["forma"] = mensagem.text
        if mensagem.text == "📍 Entrega":
            etapas_pedido[chat_id] = "endereco"
            bot.send_message(chat_id, "Informe o endereço de entrega:")
        else:
            etapas_pedido[chat_id] = "confirmar"
            confirmar_pedido(chat_id)

    elif etapa == "endereco":
        usuarios_pedindo[chat_id]["endereco"] = mensagem.text
        etapas_pedido[chat_id] = "confirmar"
        confirmar_pedido(chat_id)

# Função para mostrar o resumo do pedido
def confirmar_pedido(chat_id):
    dados = usuarios_pedindo[chat_id]
    texto = "✅ *Resumo do Pedido:*\n"
    texto += f"- Produto: {dados.get('produto')}\n"
    texto += f"- Quantidade: {dados.get('quantidade')}\n"
    texto += f"- Cliente: {dados.get('nome')}\n"
    texto += f"- Forma: {dados.get('forma')}\n"
    if dados.get("forma") == "📍 Entrega":
        texto += f"- Endereço: {dados.get('endereco')}\n"

    texto += "\nSeu pedido foi anotado com sucesso! 🍬 Em breve entraremos em contato."

    bot.send_message(chat_id, texto, parse_mode="Markdown")

    # Limpa os dados do pedido
    etapas_pedido.pop(chat_id)
    usuarios_pedindo.pop(chat_id)


print("Bot em execução...")
bot.infinity_polling()