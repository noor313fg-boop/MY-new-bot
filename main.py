import telebot
from telebot import types

# --- الإعدادات ---
TOKEN = "8650625251:AAFcv5MnB3ssM5DMCFSvrzPEgYGWtRc1U88"  
CHANNEL_ID = "@iran_telex"  # معرف قناتك (تأكد أن البوت مشرف فيها)
bot = telebot.TeleBot(TOKEN)

# --- دالة التحقق من الاشتراك ---
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False

# --- الرسالة الترحيبية ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت إيران تليكس نيوز. أرسل لي رابط الفيديو من فيسبوك، إنستغرام أو يوتيوب للتحميل.")

# --- المعالج الرئيسي للرسائل ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # التحقق من الاشتراك أولاً
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في قناة إيران تليكس نيوز", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")
        markup.add(btn)
        bot.reply_to(message, "⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت.", reply_markup=markup)
        return

    # --- كود التحميل (مكان وضع كودك السابق) ---
    bot.reply_to(message, "✅ تم التحقق! جاري معالجة الفيديو الخاص بك...")
    
    # هنا يجب أن تضع المنطق البرمجي الخاص بك لتحميل الفيديو (مثلاً: استخدام yt-dlp)
    # bot.send_video(message.chat.id, ...)

# --- تشغيل البوت ---
print("Bot is running...")
bot.infinity_polling()
