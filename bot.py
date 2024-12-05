from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Função para o comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("It's alive!")

# Configuração principal
def main():
    updater = Updater("7695344075:AAFlBN3P51XeJK57U6RnzL8cDWVpPtXpYig")
    dispatcher = updater.dispatcher

    # Adiciona o comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
