import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- الإعدادات ---
TOKEN = "8650625251:AAFcv5MnB3ssM5DMCFSvrzPEgYGWtRc1U88"  
CHANNEL_ID ="-1003631235602"  # رقم معرف القناة الصحيح
CHANNEL_LINK = "https://t.me/irantelexnews"  # رابط قناة إيران تلكس نيوز

bot = telebot.TeleBot(TOKEN)

# --- دالة التحقق من الاشتراك ---
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False

# --- أمر /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        markup = InlineKeyboardMarkup()
        channel_button = InlineKeyboardButton("اشترك في قناة إيران تلكس نيوز", url=CHANNEL_LINK)
        check_button = InlineKeyboardButton("تحقق من الاشتراك 🔄", callback_data="check_sub")
        markup.add(channel_button)
        markup.add(check_button)
        
        bot.send_message(
            message.chat.id, 
            "عذراً، يجب عليك الاشتراك في قناة إيران تلكس نيوز أولاً لتتمكن من استخدام البوت.\n\nبعد الاشتراك، اضغط على زر (تحقق من الاشتراك).",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    bot.send_message(message.chat.id, "أهلاً بك! يمكنك الآن استخدام البوت بكل سلاسة.")

# --- زر التحقق من الاشتراك ---
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "شكراً لاشتراكك! تم تفعيل البوت.")
        bot.send_message(call.message.chat.id, "ممتاز! أهلاً بك مجدداً، أرسل ما تريد.")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    else:
        bot.answer_callback_query(call.id, "لم تقم بالاشتراك بعد!", show_alert=True)

# --- تشغيل البوت ---
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
