import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- الإعدادات ---
TOKEN = "8650625251:AAFcv5MnB3ssM5DMCFSvrzPEgYGWtRc1U88"  
CHANNEL_ID = "-1003631235602"  # رقم معرف القناة الصحيح
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

    bot.send_message(message.chat.id, "أهلاً بك! يمكنك الآن إرسال الرابط ليقوم البوت بمعالجته وتحميله.")

# --- زر التحقق من الاشتراك ---
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "شكراً لاشتراكك! تم تفعيل البوت.")
        bot.send_message(call.message.chat.id, "ممتاز! أهلاً بك مجدداً، أرسل الرابط الآن.")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    else:
        bot.answer_callback_query(call.id, "لم تقم باشتراكك بعد!", show_alert=True)

# --- معالج الروابط والرسائل النصية (هنا يتم استقبال ما ترسله) ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    # التأكد من أنه مشترك قبل معالجة أي رابط ترسله
    if not check_subscription(user_id):
        bot.send_message(message.chat.id, "عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت.")
        return
        
    text = message.text
    
    # هنا يتم التعامل مع الرابط الذي ترسله
    bot.send_message(message.chat.id, f"جاري العمل على الرابط الذي أرسلته...\n{text}", parse_mode="Markdown")
@bot.message_handler(func=lambda message: True)
def handle_media_download(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "عذراً، يجب عليك الاشتراك في القناة أولاً.")
        return
    url = message.text.strip()
    if not url.startswith("http"):
        bot.send_message(message.chat.id, "الرجاء إرسال رابط صحيح.")
        return
    msg = bot.send_message(message.chat.id, "⏳ جاري تحميل الفيديو...")
    output_template = "video.mp4"
    try:
        if os.path.exists(output_template): os.remove(output_template)
        with yt_dlp.YoutubeDL({'outtmpl': output_template, 'format': 'best', 'socket_timeout': 30}) as ydl:
            ydl.download([url])
        if os.path.exists(output_template):
            with open(output_template, 'rb') as f:
                bot.send_video(message.chat.id, f, caption="✅ تم التحميل بنجاح عبر إيران تلكس")
            os.remove(output_template)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ لم يتم العثور على الفيديو.", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("❌ حدث خطأ أثناء التحميل.", message.chat.id, msg.message_id)
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
