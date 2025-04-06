import requests
import json
import os
from time import sleep
import subprocess
import sys
from colorama import Fore, init

init(autoreset=True)

def install_requirements():
    libraries = ["requests", "json", "os", "time", "colorama"]
    total_libraries = len(libraries)

    print(Fore.YELLOW + "Kütüphaneler kontrol ediliyor...")
    for index, library in enumerate(libraries, start=1):
        try:
            __import__(library)
            print(Fore.GREEN + f"{index}/{total_libraries} - {library} yüklü.")
        except ImportError:
            print(Fore.RED + f"{index}/{total_libraries} - {library} eksik, yükleniyor...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            print(Fore.GREEN + f"{library} başarıyla yüklendi.")
    print(Fore.GREEN + "\nTüm kütüphaneler kontrol edildi!\n")

def download_file(url, filename):
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

def load_menu():
    menu_url = "https://raw.githubusercontent.com/erenxw/tools/main/menu.json"
    download_file(menu_url, "menu.json")
    with open("menu.json", "r", encoding="utf-8") as file:
        menu = json.load(file)
    return menu

def show_menu(menu):
    print("\n==== Araç Menüsü ====\n")
    for idx, item in enumerate(menu['menu'], 1):
        print(f"[{idx}] {item['name']}")
    print(f"[{len(menu['menu']) + 1}] Çıkış\n")

def run_tool(tool_file):
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
    for char in text:
        print(Fore.MAGENTA + char, end='', flush=True)
    print(Fore.RESET)

def main():
    install_requirements()
    print_animated_text()
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
