import csv
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
tkn = "<YourBotToken>"
csvfile = "bot.csv"


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext):
    print(update.effective_user.username, update.effective_user.id, "Message:", update.message.text)
    msg = update.message.text
    with open(csvfile, encoding='utf8') as cfile:
        chatbot = csv.reader(cfile)
        for line in chatbot:
            for word in line[0].split(", "):
                if word.lower() == msg.lower():
                    print(update.effective_user.username, update.effective_user.id, "Reply:  ", line[1].split())
                    update.message.reply_text(line[1])
                    return
    print(update.effective_user.username, update.effective_user.id, "Reply:  ", "Please enter again! Unexpected input.")
    update.message.reply_text("Please enter again! Unexpected input.")


def main():
    updater = Updater(tkn)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
