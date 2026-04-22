   # -*- coding: utf-8 -*-
import requests, telebot, time
from datetime import datetime, timedelta
import pytz
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot vivo 💪🏽😊🪄🔥"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
TOKEN = "8601022037:AAGSAklgevPh0_y44ETbgfQTcqP7B-aGwXo"
CHAT_ID = "6358542941" 
TAG_Ferchu = "G9RGC9QG"      
TAG_FELLU = "RYLLQRUVU"  

bot = telebot.TeleBot(TOKEN)
zona_españa = pytz.timezone('Europe/Madrid')

def sacar_copas(tag):
    url = f"https://api.brawlapi.com/v1/players/%23{tag}"
    r = requests.get(url)
    if r.status_code != 200:
        return None, None
    data = r.json()
    return data['trophies'], data['name']

def mandar_reporte():
    copas_Ferchu, nombre_Ferchu = sacar_copas(TAG_Ferchu)
    copas_fellu, nombre_fellu = sacar_copas(TAG_FELLU)
    
    if not copas_Ferchu or not copas_fellu:
        bot.send_message(CHAT_ID, "Error ❌: No he podido sacar las copas. Revisa si los tags están bien.")
        return

    dif = copas_Ferchu - copas_fellu
    dias_para_pillar = abs(dif) // 150 if dif < 0 else 0
    fecha_pillas = datetime.now(zona_españa) + timedelta(days=dias_para_pillar)
    
    msg = f"**{datetime.now(zona_españa).strftime('%d %b')}**\n"
    msg += f"{nombre_Ferchu}: {copas_Ferchu} | {nombre_fellu}: {copas_fellu}\nDiferencia: {dif}\n"
    if dif < 0:
        msg += f" Ánimo Fer! Le pillas el {fecha_pillas.strftime('%d %b')} a +150/día"
    else:
        msg += "Ya le has ganado, campeón 💪🏽😊🪄"    
    bot.send_message(CHAT_ID, msg, parse_mode='Markdown')

#bot.send_message(CHAT_ID, "Bot encendido, Fer 🔥. Te aviso cada día a las 20:00 hora España")

ultimo_envio = None
while True:
    ahora_españa = datetime.now(zona_españa)
    if ahora_españa.hour == 20 and ahora_españa.minute == 0:
        fecha_hoy = ahora_españa.date()
        if ultimo_envio != fecha_hoy:
            mandar_reporte()
            ultimo_envio = fecha_hoy
    
    time.sleep(30)
