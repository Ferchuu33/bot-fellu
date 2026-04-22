import requests, telebot, time
from datetime import datetime, timedelta
import pytz

TOKEN = "PON_AQUI_TU_TOKEN_DEL_BOTFATHER"
CHAT_ID = "PON_AQUI_TU_NUMERO_DEL_USERINFOBOT" 
TAG_TUYO = "G9RGC9QG"      
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
    copas_yo, nombre_yo = sacar_copas(TAG_TUYO)
    copas_fellu, nombre_fellu = sacar_copas(TAG_FELLU)
    
    if not copas_yo or not copas_fellu:
        bot.send_message(CHAT_ID, "Error: No pude sacar las copas. Revisa si los tags están bien.")
        return

    dif = copas_yo - copas_fellu
    dias_para_pillar = abs(dif) // 150 if dif < 0 else 0
    fecha_pillas = datetime.now(zona_españa) + timedelta(days=dias_para_pillar)
    
    msg = f"**{datetime.now(zona_españa).strftime('%d %b')}**\n"
    msg += f"{nombre_yo}: {copas_yo} | {nombre_fellu}: {copas_fellu}\nDiferencia: {dif}\n"
    if dif < 0:
        msg += f"Le pillas el {fecha_pillas.strftime('%d %b')} a +150/día"
    else:
        msg += "Ya le ganaste 🥳"
    
    bot.send_message(CHAT_ID, msg, parse_mode='Markdown')

bot.send_message(CHAT_ID, "Bot encendido. Te aviso cada día a las 20:00 hora España")

ultimo_envio = None
while True:
    ahora_españa = datetime.now(zona_españa)
    if ahora_españa.hour == 20 and ahora_españa.minute == 0:
        fecha_hoy = ahora_españa.date()
        if ultimo_envio != fecha_hoy:
            mandar_reporte()
            ultimo_envio = fecha_hoy
    
    time.sleep(30)
