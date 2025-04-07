import threading
import random
import string
import requests
import time

calisiyor = False
linkler_dict = {}

def rastgele_link_olustur():
    return f"https://justpaste.it/{''.join(random.choices(string.ascii_letters + string.digits, k=5))}"

def siteyi_kontrol_et():
    while calisiyor:
        link = rastgele_link_olustur()
        try:
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                title = response.text.split('<title>')[1].split('</title>')[0]
                if title and link not in linkler_dict:
                    yazdir_link(link, title)
                    linkler_dict[link] = title
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.1)  # sistemi yormasın diye biraz bekletiyoruz

def yazdir_link(link, baslik):
    print(f"[+] {link} - {baslik}")

def baslat():
    global calisiyor
    if not calisiyor:
        calisiyor = True
        thread = threading.Thread(target=siteyi_kontrol_et)
        thread.daemon = True  # Program kapandığında thread de kapansın
        thread.start()
        print("[!] Başlatıldı. Çıkmak için Ctrl+C")

def durdur():
    global calisiyor
    calisiyor = False
    print("[!] Durduruldu.")

if __name__ == "__main__":
    try:
        baslat()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        durdur()