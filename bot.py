import time
from datetime import date, timedelta, datetime
from random import randint

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from thought import Thought
from thoughtservice import ThoughtService


token = "5001962644:AAF-gpjO3CfE-pAHHCRMXH0hCWjkXPuW-Qg"
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
id_str = open("working_id", "r").read()
ali_id = int(id_str[:len(id_str)-1])
print(ali_id)
thought_service = ThoughtService()


def show(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == ali_id:
        thoughts = thought_service.get_thoughts_of_the_day(date.today())
        msg_body = ""
        for thought in thoughts:
            msg_body += "{}-{}\n".format(thought.id, thought.name)
        if msg_body == "":
            update.message.reply_text("No thought to show")
            return
        update.message.reply_text(msg_body)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user.id == ali_id:
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True))


def generate_id(name):
    print(hash(name), datetime.now().timestamp())
    return hash(name) + int(datetime.now().timestamp()) + randint(0, 100)


def add(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == ali_id:
        message_text = update.message["text"]
        name = message_text[5:]
        id = generate_id(name)
        t = Thought(name=name, id=id, date_to_alarm=date.today()+timedelta(days=2))
        thought_service.add_thought(t)
        update.message.reply_text("thought with id {} created".format(id))


def yes_handler(update: Update, context: CallbackContext) -> None:
    key = int(update.message.text.split()[1])
    thought_service.proceed_thought(key)
    update.message.reply_text("Great! I will ask again two days later")


def no_handler(update: Update, context: CallbackContext) -> None:
    key = int(update.message.text.split()[1])
    thought_service.delete_thought(key)
    update.message.reply_text("Aww! OK. Hope you the best!")


def msg_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("It may be a litte early to expect me to reply to this!")


dispatcher.add_handler(CommandHandler("n", no_handler))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("add", add))
dispatcher.add_handler(CommandHandler("y", yes_handler))
dispatcher.add_handler(CommandHandler("show", show))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, msg_handler))

updater.start_polling()
updater.idle()
