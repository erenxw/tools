import requests

def check_website_status(url):
    """Verilen URL'nin durumunu kontrol eder."""
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"{url} sitesi çalışıyor! (HTTP {response.status_code})")
        else:
            print(f"{url} sitesi çalışmıyor. (HTTP {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"{url} sitesine bağlanılamadı. Hata: {e}")

def main():
    """Ana fonksiyon: Kullanıcıdan URL alır ve durumu kontrol eder."""
    print("Web Site Durum Kontrol Aracı")
    url = input("Kontrol etmek istediğiniz web sitesinin URL'sini girin: ")
    
    # URL'yi http:// ile başlatıyoruz
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    check_website_status(url)

if __name__ == "__main__":
    main()
