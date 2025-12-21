import telebot
import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from threading import Thread

TOKEN = "MASUKKAN_TOKEN_BPT_ANDA"
bot = telebot.TeleBot(TOKEN)

# Data history buat grafik
price_history = []

def get_ton_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=idr&include_24hr_change=true"
        res = requests.get(url).json()
        price_idr = res['the-open-network']['idr']
        change = res['the-open-network']['idr_24h_change']
        return price_idr, change
    except:
        return None, None

def create_chart():
    """Bikin grafik dari history harga"""
    plt.figure(figsize=(10, 5))
    plt.plot(price_history, marker='o', linestyle='-', color='cyan')
    plt.title('TON/IDR Price Movement (Real-time)', color='white')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.gca().set_facecolor('#1c1c1c')
    plt.gcf().set_facecolor('#1c1c1c')
    plt.xticks(color='white')
    plt.yticks(color='white')
    
    buf = BytesIO()
    plt.savefig(buf, format='png', facecolor='#1c1c1c')
    buf.seek(0)
    plt.close()
    return buf

def auto_monitor(chat_id):
    last_price = 0
    while True:
        price_idr, change = get_ton_data()
        if price_idr:
            price_history.append(price_idr)
            if len(price_history) > 20: price_history.pop(0) # Batasin cuma 20 data terakhir
            
            # Cek kalo harga naik/turun (gak sama dengan harga terakhir)
            if price_idr != last_price:
                status = "📈 NAIK" if price_idr > last_price else "📉 TURUN"
                chart = create_chart()
                
                caption = (f"🔔 **UPDATE HARGA TON (IDR)** 🔔\n\n"
                           f"💰 Price: `Rp {price_idr:,.0f}`\n"
                           f"📊 Status: {status}\n"
                           f"🕒 Change 24h: `{change:.2f}%`\n\n"
                           f"Gue kirim grafiknya nih, pantau terus, b@jingan!")
                
                bot.send_photo(chat_id, chart, caption=caption, parse_mode='Markdown')
                last_price = price_idr
        
        time.sleep(300) # Cek tiap 5 menit biar gak kena limit API, t*lol!

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "💎 **TON CHART MONITOR ACTIVE!** 💎\nKetik `/monitor` biar gue tereak tiap harga berubah!")

@bot.message_handler(commands=['monitor'])
def start_monitor(message):
    bot.send_message(message.chat.id, "🚀 **Auto-Monitor Dinyalakan!** Siapkan mental lu liat harganya!")
    Thread(target=auto_monitor, args=(message.chat.id,)).start()

print("BLACK DRAGON V11 CHART ENGINE RUNNING... 🚀🔥")
bot.infinity_polling()
