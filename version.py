import requests

# Yerel version.txt dosyasını oku
with open("version.txt", "r") as file:
    local_version = file.read().strip()

# GitHub'daki version.txt dosyasını al
url = "https://raw.githubusercontent.com/erenxw/tools/main/version.txt"
response = requests.get(url)

if response.status_code == 200:
    remote_version = response.text.strip()

    if local_version != remote_version:
        print("Yeni bir güncelleme mevcut. Lütfen en güncel kodu indirip çalıştırın:")
        print("https://github.com/erenxw/tools/blob/main/version.txt")
    else:
        print("Kodunuz güncel.")
else:
    print("Uzaktan sürüm bilgisi alınamadı.")
