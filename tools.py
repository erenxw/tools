import requests
import json
import os
from time import sleep
import subprocess
import sys
from colorama import Fore, Back, Style, init

# Renkli yazının animasyonlu olarak ekrana yazdırılması için başlatma
init(autoreset=True)

def install_requirements():
    """Gerekli kütüphaneleri kontrol edip, yükler."""
    try:
        import requests
        import json
        import os
        import time
        from colorama import Fore
    except ImportError:
        print(Fore.RED + "Gerekli kütüphaneler eksik, yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests', 'colorama'])
        print(Fore.GREEN + "Kütüphaneler başarıyla yüklendi!\n")
    
def download_file(url, filename):
    """GitHub'dan dosya indirir ve kaydeder."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(response.text)
        print(f"{filename} başarıyla indirildi.\n")
    else:
        print("Dosya indirilemedi. HTTP", response.status_code)

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
    
    # Renkli yazının her bir satırını animasyonlu olarak yazdırmak
    for i in range(len(text)):
        # Animasyonlu şekilde yazdırma
        print(Fore.GREEN + text[:i+1], end="\r")
        sleep(0.05)

    print("\n")  # Sonrasında yeni bir satır açma

def main():
    install_requirements()  # Gerekli kütüphaneleri yükle
    
    print_animated_text()  # Animasyonlu yazıyı ekrana yazdır
    
    menu = load_menu()

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
