from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

waiting_user = None
pairs = {}

def start(update, context):
    update.message.reply_text(
        "👋 Welcome to Random Chat Bot!\n\n"
        "Commands:\n"
        "/find – Find a random partner\n"
        "/stop – End chat"
    )

def find(update, context):
    global waiting_user
    user_id = update.message.from_user.id

    if user_id in pairs:
        update.message.reply_text("You are already chatting.")
        return

    if waiting_user is None:
        waiting_user = user_id
        update.message.reply_text("⏳ Waiting for a partner...")
    else:
        partner = waiting_user
        waiting_user = None

        pairs[user_id] = partner
        pairs[partner] = user_id

        context.bot.send_message(user_id, "✅ Connected! Say hi 👋")
        context.bot.send_message(partner, "✅ Connected! Say hi 👋")

def stop(update, context):
    user_id = update.message.from_user.id

    if user_id in pairs:
        partner = pairs.pop(user_id)
        pairs.pop(partner)

        context.bot.send_message(partner, "❌ Your partner left the chat.")
        update.message.reply_text("❌ Chat ended.")
    else:
        update.message.reply_text("You are not chatting.")

def message(update, context):
    user_id = update.message.from_user.id

    if user_id in pairs:
        partner = pairs[user_id]
        context.bot.send_message(partner, update.message.text)
    else:
        update.message.reply_text("Use /find to start chatting.")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("find", find))
dp.add_handler(CommandHandler("stop", stop))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message))

updater.start_polling()
updater.idle()
