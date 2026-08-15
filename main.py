import os
import telebot
import yt_dlp

TOKEN = 'ضع_توكن_البوت_هنا'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط الفيديو لأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    bot.reply_to(message, "جاري المعالجة وتحميل الفيديو، سأرسله لك حالاً...")
    
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        os.remove('video.mp4')
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء التحميل: {str(e)}")

bot.infinity_polling()
