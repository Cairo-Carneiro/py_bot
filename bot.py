import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from datetime import datetime

# Chave da API do Telegram
CHAVE_API = "8192131058:AAGgdcENW5KV2wMYps9krcAzWxXcpYut9QU"

bot = telebot.TeleBot(CHAVE_API)

# Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Conecta ao MongoDB local
db = client["telegram_bot"]  # Nome do banco de dados
users_collection = db["users"]  # Nome da coleção de usuários
relatos_collection = db["relatos"]  # Nome da coleção de relatos

# Função para o comando de cadastro
@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    chat_id = mensagem.chat.id
    bot.send_message(chat_id, "Qual o seu nome?")
    bot.register_next_step_handler(mensagem, obter_nome)  # Registra o próximo passo

# Função para obter o nome
def obter_nome(mensagem):
    try:
        chat_id = mensagem.chat.id
        nome = mensagem.text.strip()
        if not nome.isalpha():  # Valida se o nome contém apenas letras
            bot.send_message(chat_id, "Nome inválido! Digite apenas letras.")
            return bot.register_next_step_handler(mensagem, obter_nome)
        user_data = {"chat_id": chat_id, "name": nome}  # Salva o nome temporariamente
        bot.send_message(chat_id, "Agora, por favor, cadastre o seu número de telefone:")
        bot.register_next_step_handler(mensagem, obter_telefone, user_data)  # Passa os dados temporários
    except Exception as e:
        bot.send_message(mensagem.chat.id, f"Ocorreu um erro ao registrar o nome: {e}")

# Função para obter o telefone e salvar no MongoDB
def obter_telefone(mensagem, user_data):
    try:
        chat_id = mensagem.chat.id
        telefone = mensagem.text.strip()
        if not telefone.isdigit() or len(telefone) < 8:  # Valida se é numérico e tem tamanho mínimo
            bot.send_message(chat_id, "Número de telefone inválido! Digite apenas números com pelo menos 8 dígitos.")
            return bot.register_next_step_handler(mensagem, obter_telefone, user_data)
        
        # Atualiza os dados do usuário com o telefone
        user_data["phone"] = telefone

        # Salvar a data e a hora da mensagem
        user_data["timestamp"] = datetime.now()

        # Salva os dados no MongoDB
        users_collection.insert_one(user_data)

        # Formatar a hora e a data e mostrar ao usuário
        data_formatada = user_data["timestamp"].strftime("%d/%m/%Y %H:%M")

        # Confirmação para o usuário
        bot.send_message(
            chat_id, 
            f"Cadastro concluído!\nNome: {user_data['name']}\nTelefone: {telefone}\nCadastrado em: {data_formatada}\n\n"
            "Agora você pode relatar um ocorrido usando o comando /relato."
        )
    except Exception as e:
        bot.send_message(mensagem.chat.id, f"Ocorreu um erro ao registrar o telefone: {e}")

# Função para o comando de relato
@bot.message_handler(commands=["relato"])
def relato(mensagem):
    chat_id = mensagem.chat.id
    # Verificar se o usuário está cadastrado
    if not users_collection.find_one({"chat_id": chat_id}):
        bot.send_message(chat_id, "Você precisa se cadastrar antes de relatar um ocorrido. Use /opcao1 para se cadastrar.")
        return
    bot.send_message(chat_id, "Por favor, descreva o ocorrido:")
    bot.register_next_step_handler(mensagem, registrar_relato)

# Função para registrar o relato no MongoDB
def registrar_relato(mensagem):
    try:
        chat_id = mensagem.chat.id
        texto_relato = mensagem.text.strip()
        if len(texto_relato) < 10:  # Verificar se o relato é muito curto
            bot.send_message(chat_id, "Relato muito curto! Por favor, descreva com mais detalhes.")
            return bot.register_next_step_handler(mensagem, registrar_relato)
        
        # Salvar o relato no MongoDB
        relato_data = {
            "chat_id": chat_id,
            "relato": texto_relato,
            "timestamp": datetime.now()
        }
        relatos_collection.insert_one(relato_data)

        # Confirmar o registro ao usuário
        bot.send_message(chat_id, "Relato registrado com sucesso! Obrigado por sua colaboração.")
        
        # Exibir o relato de volta ao usuário
        bot.send_message(chat_id, f"Você relatou:\n\n\"{texto_relato}\"")

        # Adicionar botões para reiniciar o chat
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Recomeçar", callback_data="restart"))
        bot.send_message(chat_id, "Deseja recomeçar o chat?", reply_markup=markup)

    except Exception as e:
        bot.send_message(mensagem.chat.id, f"Ocorreu um erro ao registrar o relato: {e}")

# Função para tratar o callback dos botões
@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart_chat(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Recomeçando o chat...")
    responder(call.message)  # Chama a mensagem inicial

# Função genérica para verificar mensagens
def verificar(mensagem):
    return True

# Mensagem inicial
@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    O Bot ColabZoonoses é uma ferramenta colaborativa para monitoramento de zoonoses, utilizando georreferenciamento e integração com WhatsApp/Telegram.
    Antes de começarmos, cadastre-se por favor:
    /opcao1 Cadastro
    Depois de cadastrado, use /relato para registrar um ocorrido.
    """
    bot.reply_to(mensagem, texto)

# Mantém o bot em execução
bot.polling()
