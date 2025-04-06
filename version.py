import requests

# Yerel version.txt dosyasını oku
try:
    with open("version.txt", "r") as file:
        local_version = file.read().strip()
except FileNotFoundError:
    print("Yerel version.txt dosyası bulunamadı.")
    local_version = None

# GitHub'daki version.txt dosyasını al
url = "https://raw.githubusercontent.com/erenxw/tools/main/version.txt"
response = requests.get(url)

if response.status_code == 200:
    remote_version = response.text.strip()

    if local_version != remote_version:
        print("Yeni bir güncelleme mevcut. Lütfen en güncel kodu indirip çalıştırın:")
        print("https://github.com/erenxw/tools/blob/main/tools.py")
        
        # GitHub'daki yeni sürümü version.txt ile güncelle
        try:
            with open("version.txt", "w") as file:
                file.write(remote_version)
            print("Yerel version.txt dosyası güncellendi.")
        except Exception as e:
            print(f"version.txt dosyası güncellenemedi: {e}")
    else:
        print("Kodunuz güncel.")
else:
    print("Uzaktan sürüm bilgisi alınamadı.")
