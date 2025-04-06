import requests
import json
import os
from time import sleep
import subprocess
import sys
from colorama import Fore, init

init(autoreset=True)

def install_requirements():
    """Gerekli kütüphaneleri kontrol edip, yükler."""
    libraries = ["requests", "json", "os", "time", "colorama"]
    total_libraries = len(libraries)

    print(Fore.YELLOW + "Kütüphaneler kontrol ediliyor...")  
    for index, library in enumerate(libraries, start=1):  
        try:  
            __import__(library)  # Kütüphaneyi kontrol et  
            print(Fore.GREEN + f"{index}/{total_libraries} - {library} yüklü.")  
        except ImportError:  
            print(Fore.RED + f"{index}/{total_libraries} - {library} eksik, yükleniyor...")  
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])  
            print(Fore.GREEN + f"{library} başarıyla yüklendi.")  

    print(Fore.GREEN + "\nTüm kütüphaneler kontrol edildi!\n")

def download_file(url, filename):
    """GitHub'dan dosya indirir ve kaydeder."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(response.text)
            print(f"{filename} başarıyla indirildi.\n")
        else:
            print("Dosya indirilemedi. HTTP", response.status_code)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Dosya indirilirken hata oluştu: {e}")

def check_for_update():
    """GitHub'dan en son sürüm bilgisini kontrol eder."""
    try:
        response = requests.get("https://raw.githubusercontent.com/erenxw/tools/main/version.txt")
        if response.status_code == 200:
            latest_version = response.text.strip()
            current_version = "1.0"  # Mevcut sürüm numarasını buraya girin

            if latest_version != current_version:
                return latest_version
            else:
                return None
        else:
            print(Fore.RED + "Sürüm kontrolü yapılamadı.")
            return None
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Sürüm kontrolü yapılırken hata oluştu: {e}")
        return None

def update_tools():
    """Yeni sürüm varsa, güncellemeyi yapar."""
    print(Fore.YELLOW + "Yeni bir güncelleme mevcut! Güncellemek istiyor musunuz? (E/H)")
    choice = input().strip().lower()

    if choice == "e":
        print("Güncelleniyor...")
        download_file("https://raw.githubusercontent.com/erenxw/tools/main/tools.py", "tools.py")
        print(Fore.GREEN + "Güncelleme başarılı! Yeniden başlatılıyor...")
        try:
            # Yeniden başlatma işlemi
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(Fore.RED + f"Yeniden başlatırken hata oluştu: {e}")
            sys.exit(1)  # Hata ile çıkış yap

    else:
        print("Güncelleme işlemi iptal edildi.")

def load_menu():
    """menu.json dosyasını GitHub'dan çeker ve menüyü döndürür."""
    menu_url = "https://raw.githubusercontent.com/erenxw/tools/main/menu.json"
    download_file(menu_url, "menu.json")

    with open("menu.json", "r", encoding="utf-8") as file:  
        menu = json.load(file)  
    return menu

def show_menu(menu):
    """Menüyü ekrana yazdırır."""
    print("\n==== Araç Menüsü ====\n")
    for idx, item in enumerate(menu['menu'], 1):
        print(f"[{idx}] {item['name']}")
    print(f"[{len(menu['menu']) + 1}] Çıkış\n")

def run_tool(tool_file):
    """Seçilen tool'u GitHub'dan indirip çalıştırır."""
    tool_url = f"https://raw.githubusercontent.com/erenxw/tools/main/{tool_file}"
    download_file(tool_url, tool_file)

    with open(tool_file, "r", encoding="utf-8") as file:  
        code = file.read()  
    exec(code, globals())

def print_animated_text():
    text = """
    ███████╗██████╗░███████╗███╗░░██╗
    ██╔════╝██╔══██╗██╔════╝████╗░██║
    █████╗░░██████╔╝█████╗░░██╔██╗██║
    ██╔══╝░░██╔══██╗██╔══╝░░██║╚████║
    ███████╗██║░░██║███████╗██║░╚███║
    ╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝
    """
    # Sadece mavi renk uygulanacak
    for char in text:
        print(Fore.MAGENTA + char, end='', flush=True)
    
    print(Fore.RESET)  # Rengi sıfırlamak

def main():
    install_requirements()  # Gerekli kütüphaneleri yükle

    print_animated_text()  # Animasyonlu yazıyı ekrana yazdır  

    menu = load_menu()  

    update_version = check_for_update()
    if update_version:
        update_tools()  # Eğer yeni sürüm varsa, güncelleme yap

    while True:  
        show_menu(menu)  
        choice = input("Seçiminizi yapın: ")  

        if choice.isdigit():  
            choice = int(choice)  

            if choice == len(menu['menu']) + 1:  
                print("Çıkılıyor...\n")  
                break  
            elif 1 <= choice <= len(menu['menu']):  
                tool_file = menu['menu'][choice - 1]['file']  
                print(f"\n{tool_file} yükleniyor...")  
                run_tool(tool_file)  
            else:  
                print("Geçersiz seçim!\n")  
        else:  
            print("Lütfen geçerli bir seçim yapın!\n")  

        sleep(1)

if __name__ == "__main__":
    main()
