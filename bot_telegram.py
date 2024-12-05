import telebot

# Chave da API do Telegram
CHAVE_API = "7695344075:AAFlBN3P51XeJK57U6RnzL8cDWVpPtXpYig"

bot = telebot.TeleBot(CHAVE_API)

# Dicionário para armazenar dados dos usuários
user_data = {}

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
        user_data[chat_id] = {"name": nome}  # Salva o nome
        bot.send_message(chat_id, "Agora, por favor, cadastre o seu número de telefone:")
        bot.register_next_step_handler(mensagem, obter_telefone)  # Registra o próximo passo
    except Exception as e:
        bot.send_message(chat_id, f"Ocorreu um erro ao registrar o nome: {e}")

# Função para obter o telefone
def obter_telefone(mensagem):
    try:
        chat_id = mensagem.chat.id
        telefone = mensagem.text.strip()
        if not telefone.isdigit() or len(telefone) < 8:  # Valida se é numérico e tem tamanho mínimo
            bot.send_message(chat_id, "Número de telefone inválido! Digite apenas números com pelo menos 8 dígitos.")
            return bot.register_next_step_handler(mensagem, obter_telefone)
        user_data[chat_id]["phone"] = telefone  # Salva o telefone
        nome = user_data[chat_id]["name"]
        bot.send_message(chat_id, f"Cadastro concluído!\nNome: {nome}\nTelefone: {telefone}")
    except Exception as e:
        bot.send_message(chat_id, f"Ocorreu um erro ao registrar o telefone: {e}")

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
    AVISO: QUALQUER OUTRA OPÇÃO NÃO IRÁ FUNCIONAR
    """
    bot.reply_to(mensagem, texto)

# Mantém o bot em execução
bot.polling()
