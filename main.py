import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# --- الإعدادات الأساسية ---
TOKEN = "8650625251:AAFcv5MnB3ssM5DMCFSvrzPEgYGWtRc1U88"  
CHANNEL_ID = "-1003631235602"  # رقم معرف قناة إيران تلكس نيوز
CHANNEL_LINK = "https://t.me/irantelexnews"  # رابط القناة

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

# --- أمر /start للترحيب والتحقق ---
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

    bot.send_message(message.chat.id, "أهلاً بك! أرسل رابط الفيديو من إنستغرام أو فيسبوك وسأقوم بتحميله لك فوراً.")

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

# --- معالج روابط التحميل (فيسبوك، إنستغرام، وغيرها) ---
@bot.message_handler(func=lambda message: True)
def handle_media_download(message):
    user_id = message.from_user.id
    
    # التأكد من الاشتراك قبل التحميل
    if not check_subscription(user_id):
        bot.send_message(message.chat.id, "عذراً، يجب عليك الاشتراك في القناة أولاً لتتمكن من استخدام البوت.")
        return
        
    url = message.text.strip()
    
    # التحقق من أن النص عبارة عن رابط صحيح
    if not url.startswith("http"):
        bot.send_message(message.chat.id, "الرجاء إرسال رابط صحيح (إنستغرام أو فيسبوك).")
        return

    msg = bot.send_message(message.chat.id, "⏳ جاري تحميل الفيديو، يرجى الانتظار قليلاً...")
    
    output_template = "video.mp4"
    
    # إعدادات أداة التحميل
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best',
        'socket_timeout': 30,
    }

    try:
        # مسح أي ملف قديم متراكم
        if os.path.exists(output_template):
            os.remove(output_template)

        # تحميل الفيديو باستخدام yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إذا تم التحميل بنجاح، أرسل الفيديو للمستخدم
        if os.path.exists(output_template):
            with open(output_template, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption="✅ تم التحميل بنجاح عبر بوت إيران تلكس")
            # حذف الملف من السيرفر لتفريغ المساحة
            os.remove(output_template)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ لم يتم العثور على الفيديو أو أن الرابط غير مدعوم.", message.chat.id, msg.message_id)

    except Exception as e:
        print(f"Download Error: {e}")
        try:
            bot.edit_message_text("❌ حدث خطأ أثناء التحميل: تأكد أن الرابط عام.", message.chat.id, msg.message_id)
        except:
            bot.send_message(message.chat.id, "❌ حدث خطأ أثناء التحميل.")

# --- تشغيل البوت باستمرار ---
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
