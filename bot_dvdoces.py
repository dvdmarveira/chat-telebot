import telebot 
from telebot import types
import os
from dotenv import load_dotenv

# Carregar a chave da API
load_dotenv()
CHAVE_API = os.getenv("CHAVE_API")

bot = telebot.TeleBot(CHAVE_API)

categorias_produtos = {
    "Bolos": {
        "Bolo de chocolate": 10.00,
        "Bolo de cenoura": 10.00,
        "Bolo de macaxeira": 12.00,
        "Bolo de milho": 12.00
    },
    "Cupcakes": {
        "Cupcake de morango": 5.00,
        "Cupcake de chocolate": 5.50,
        "Cupcake de pistache": 7.50
    },
    "Brownies": {
        "Brownie tradicional": 7.50,
        "Brownie de chocolate": 6.00,
        "Brownie de chocolate com amendoim": 8.00
    }
}

# Chat iniciado pelo usuário
usuarios_iniciados = set()

# Dicionários para armazenar o progresso e os dados dos pedidos
usuarios_pedindo = {}
etapas_pedido = {}

def mostrar_menu_inicial(mensagem):
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

# /start 
@bot.message_handler(commands=["start"])
def start(mensagem):
    mostrar_menu_inicial(mensagem)
  
# Resposta aos botões do menu
@bot.callback_query_handler(func=lambda call: True)
def responder_botoes(call):
    chat_id = call.message.chat.id
    
    # if call.data == "cardapio":
    #     texto_cardapio = (
    #         "🍰 *Nosso cardápio:*\n\n"
    #         "- Bolo de chocolate - R$ 10,00\n"
    #         "- Cupcake de morango - R$ 5,00\n"
    #         "- Brownie recheado - R$ 7,50\n\n"
    #         "Você pode ver mais detalhes em nosso Instagram: @dvdoces\n\n"
    #         "... ou já pode fazer o seu pedido e garantir uma de nossas delícias!"
    #     )

    if call.data == "cardapio":
        texto_cardapio = "🍰 *Nosso cardápio:*\n\n"
        for categoria, produtos in categorias_produtos.items():
            texto_cardapio += f"*{categoria}:*\n"
            for produto, preco in produtos.items():
                texto_cardapio += f"- {produto} - R$ {preco:.2f}\n"
            texto_cardapio += "\n"

        texto_cardapio += (
            "Você pode ver mais detalhes em nosso Instagram: @dvdoces\n\n"
            "... ou já pode fazer o seu pedido e garantir uma de nossas delícias!"
        )

        # bot.send_message(call.message.chat.id, texto_cardapio, parse_mode="Markdown")

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
        # Feedback visual do clique para o usuário
        bot.send_message(chat_id, "*Anotando o seu pedido... 📝*", parse_mode="Markdown")
        etapas_pedido[chat_id] = "categoria"
        usuarios_pedindo[chat_id] = {}
        # Botões para as categorias
        markup_pedido = types.InlineKeyboardMarkup()
        for categoria in categorias_produtos.keys():
            emoji = "🍰" if categoria == "Bolos" else "🧁" if categoria == "Cupcakes" else "🍫"
            markup_pedido.add(types.InlineKeyboardButton(f"{emoji} {categoria}", callback_data=f"categoria_{categoria}"))
        bot.send_message(chat_id, "Escolha uma categoria:", reply_markup=markup_pedido)
        # bot.send_message(chat_id, "📦 Qual doce você gostaria de pedir?")

    elif call.data.startswith("categoria_"):
        categoria = call.data.split("_", 1)[1]
        usuarios_pedindo[chat_id]["categoria"] = categoria
        etapas_pedido[chat_id] = "produto"
        # Cria botões para os produtos da categoria escolhida
        markup_produto = types.InlineKeyboardMarkup()
        for produto in categorias_produtos[categoria].keys():
            markup_produto.add(types.InlineKeyboardButton(produto, callback_data=f"produto_{produto}"))
        bot.send_message(chat_id, f"Escolha o produto que você deseja da categoria {categoria}:", reply_markup=markup_produto)

    elif call.data.startswith("produto_"):
        produto = call.data.split("_", 1)[1]
        usuarios_pedindo[chat_id]["produto"] = produto 
        etapas_pedido[chat_id] = "quantidade"
        bot.send_message(chat_id, f"Quantas unidades de {produto} você deseja?")

    elif call.data == "horario":
        bot.send_message(call.message.chat.id, "⏰ Funcionamos de segunda a sábado, das 10h às 18h.")

    elif call.data == "contato":
        bot.send_message(call.message.chat.id, "📍 Rua das Delícias, 123 – Centro\n📞 (81) 99999-9999\nInstagram: @dvdoces")

    elif call.data == "atendente":
        bot.send_message(call.message.chat.id, "💬 Você será redirecionado para o nosso atendimento humano:\nhttps://wa.me/5581999999999")
        
    elif call.data == "confirmar_pedido":
        bot.send_message(chat_id, "✅ Pedido confirmado com sucesso! Em breve entraremos em contato. 🍬")
        etapas_pedido.pop(chat_id, None)
        usuarios_pedindo.pop(chat_id, None)
        
    elif call.data == "editar_pedido":
        # Reiniciar o fluxo a partir da escola da categoria
        etapas_pedido[chat_id] = "categoria"
        usuarios_pedindo[chat_id] = {}
        markup = types.InlineKeyboardMarkup()
        for categoria in categorias_produtos.keys():
            emoji = "🍰" if categoria == "Bolos" else "🧁" if categoria == "Cupcakes" else "🍫"
            markup.add(types.InlineKeyboardButton(f"{emoji} {categoria}", callback_data=f"categoria_{categoria}"))
        bot.send_message(chat_id, "Vamos editar seu pedido! Escolha uma categoria:", reply_markup=markup)

# Fluxo do pedido
@bot.message_handler(func=lambda msg: msg.chat.id in etapas_pedido)
def processar_pedido(mensagem):
    chat_id = mensagem.chat.id
    etapa = etapas_pedido[chat_id]

    # if etapa == "produto":
    #     usuarios_pedindo[chat_id]["produto"] = mensagem.text
    #     etapas_pedido[chat_id] = "quantidade"
    #     bot.send_message(chat_id, "Quantas unidades você deseja?")

    if etapa == "quantidade":
        try:
            quantidade = int(mensagem.text)
            if quantidade <= 0:
                raise ValueError
            usuarios_pedindo[chat_id]["quantidade"] = quantidade
            etapas_pedido[chat_id] = "nome"
            bot.send_message(chat_id, "Por favor, informe seu nome.")
        except ValueError:
            bot.send_message(chat_id, "Desculpe, não entendi. Pode informar a quantidade que você deseja?")

    elif etapa == "nome":
        usuarios_pedindo[chat_id]["nome"] = mensagem.text
        etapas_pedido[chat_id] = "entrega"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("📍 Entrega", "🏠 Retirada")
        bot.send_message(chat_id, "Você prefere entrega ou retirada?", reply_markup=markup)

    elif etapa == "entrega":
        resposta = mensagem.text.strip().lower()
        if resposta in ["entrega"]:
            usuarios_pedindo[chat_id]["forma"] = "entrega"
            etapas_pedido[chat_id] = "endereco"
            bot.send_message(chat_id, "Informe o endereço de entrega:")
        elif resposta in ["retirada"]:
            usuarios_pedindo[chat_id]["forma"] = "retirada"
            etapas_pedido[chat_id] = "confirmar"
            resumo_pedido(chat_id)
        else:
            bot.send_message(chat_id, "Desculpa, não entendi. A forma de entrega será no seu endereço ou retirada?")

    elif etapa == "endereco":
        usuarios_pedindo[chat_id]["endereco"] = mensagem.text
        etapas_pedido[chat_id] = "confirmar"
        resumo_pedido(chat_id)
        
# iniciar genérico
@bot.message_handler(func=lambda msg: True)
def iniciar_apos_mensagem(mensagem):
    chat_id = mensagem.chat.id
    # Se o usuário já estiver em um fluxo, não mostra o menu
    if chat_id in etapas_pedido:
        return
    # Só mostra o menu se o usuário ainda não tenha recebido
    if chat_id not in usuarios_iniciados:
        mostrar_menu_inicial(mensagem)
        usuarios_iniciados.add(chat_id)

# Função para mostrar o resumo do pedido
def resumo_pedido(chat_id):
    dados = usuarios_pedindo[chat_id]
    produto = dados.get('produto')
    categoria = dados.get('categoria')
    quantidade = int(dados.get('quantidade'))
    preco_unitario = categorias_produtos.get(categoria, {}).get(produto,0)
    valor_total = preco_unitario * quantidade 
    cliente = dados.get('nome')
    forma = dados.get('forma')
    endereco = dados.get('endereco')
    
    texto = "📋 *Resumo do Pedido:*\n"
    texto += f"- Produto: {produto}\n"
    texto += f"- Quantidade: {quantidade}\n"
    texto += f"- Preço unitário: R$ {preco_unitario:.2f}\n"
    texto += f"- Valor total: R$ {valor_total:.2f}\n"
    texto += f"- Cliente: {cliente}\n"
    texto += f"- Forma: {forma}\n"
    if forma.lower() == "entrega":
        texto += f"- Endereço: {endereco}\n"
        
    markup_confirmar_pedido = types.InlineKeyboardMarkup()
    markup_confirmar_pedido.add(
        types.InlineKeyboardButton("📝 Editar pedido", callback_data="editar_pedido"),
        types.InlineKeyboardButton("✅ Confirmar pedido", callback_data="confirmar_pedido")
    )
    bot.send_message(chat_id, texto, parse_mode="Markdown")
    bot.send_message(chat_id, "Confirme o seu pedido para que possamos seguir.", reply_markup=markup_confirmar_pedido)
    
    
    # texto += "\nSeu pedido foi anotado com sucesso! 🍬 Em breve entraremos em contato."

    # bot.send_message(chat_id, texto, parse_mode="Markdown")

    # Limpa os dados do pedido
    etapas_pedido.pop(chat_id)
    usuarios_pedindo.pop(chat_id)


print("Bot em execução...")
bot.infinity_polling()