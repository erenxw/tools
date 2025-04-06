import requests
import datetime
import threading
import os

# Proxy çekme API listesi
api_list = [
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://www.proxyscan.io/download?type=http",
    "https://api.openproxylist.xyz/http.txt"
]

daily_proxy_count = 0  # Bu, toplanan proxy sayısını takip eder

def proxy_scraper():
    global daily_proxy_count
    try:
        proxies = []

        # Tüm API'lerden proxy toplama
        for api_url in api_list:
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                proxies.extend(response.text.splitlines())
            except requests.exceptions.RequestException as e:
                print(f"Veri alınamadı: {api_url} API'si: {e}")

        # Proxy'leri filtrele (boş satırları kaldır)
        proxies = [proxy for proxy in proxies if proxy.strip()]
        daily_proxy_count = len(proxies)

        # Proxy'leri kaydet
        today = datetime.date.today()
        log_filename = f"{today}_log.txt"
        with open(log_filename, "w") as file:
            for proxy in proxies:
                file.write(f"{proxy}\n")

        print(f"Proxiler kaydedildi: {log_filename}")
        return proxies

    except Exception as e:
        print(f"Proxy toplama sırasında bir hata oluştu: {e}")
        return []

def proxy_checker(proxies):
    valid_proxies = []
    invalid_proxies = []

    def check_proxy(proxy):
        url = "http://www.google.com"
        proxies_dict = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        try:
            response = requests.get(url, proxies=proxies_dict, timeout=5)
            if response.status_code == 200:
                valid_proxies.append(proxy)
                print(f"Geçerli proxy: {proxy}")
            else:
                invalid_proxies.append(proxy)
                print(f"Geçersiz proxy: {proxy}")
        except requests.RequestException:
            invalid_proxies.append(proxy)
            print(f"Geçersiz proxy: {proxy}")

    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=(proxy,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    today = datetime.date.today()
    with open(f"{today}_valid_proxies.txt", "w") as file:
        for proxy in valid_proxies:
            file.write(f"{proxy}\n")

    with open(f"{today}_invalid_proxies.txt", "w") as file:
        for proxy in invalid_proxies:
            file.write(f"{proxy}\n")

    print(f"Geçerli proxiler {today}_valid_proxies.txt dosyasına kaydedildi.")
    print(f"Geçersiz proxiler {today}_invalid_proxies.txt dosyasına kaydedildi.")
    print(f"Toplam {len(proxies)} proxy işlendi.")

def menu():
    while True:
        print("\nLütfen bir seçenek girin:")
        print("1 - Proxy toplama işlemi başlat")
        print("2 - Proxy doğrulama işlemi başlat")
        print("3 - Günlük Toplanan Proxy Sayısını Göster")
        print("4 - Çıkış")
        
        choice = input("Seçiminiz (1/2/3/4): ")

        if choice == '1':
            print("Proxy toplama işlemi başlatılıyor...")
            proxies = proxy_scraper()
            input("Devam etmek için bir tuşa basın...")

        elif choice == '2':
            print("Proxy doğrulama işlemi başlatılıyor...")
            proxies = proxy_scraper()
            if proxies:
                proxy_checker(proxies)
            else:
                print("Proxy bulunamadı. Lütfen proxy toplama işlemini önce yapın.")
            input("Devam etmek için bir tuşa basın...")

        elif choice == '3':
            print(f"Günlük Toplanan Proxy Sayısı: {daily_proxy_count}")
            input("Devam etmek için bir tuşa basın...")

        elif choice == '4':
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçenek. Lütfen tekrar deneyin.")
            input("Devam etmek için bir tuşa basın...")

if __name__ == "__main__":
    menu()
