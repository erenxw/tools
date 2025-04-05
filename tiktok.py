import requests
import time

def hesapla_yayin_geliri(total_coin):
    """TikTok yayın gelirini hesaplar"""
    coin_degeri = 0.29  # 1 coin'in TL karşılığı
    yayinci_pay = 0.5  # Yayıncıların kazandığı pay (yüzde 50)
    
    # Toplam coin'in TL karşılığını hesapla
    toplam_gelir = total_coin * coin_degeri
    yayinci_geliri = toplam_gelir * yayinci_pay
    
    # Sonuçları döndür
    return toplam_gelir, yayinci_geliri

def get_room_id(username):
    """TikTok kullanıcı adından yayın odası ID'sini alır"""
    url = f"https://api.tiktok.com/getRoomId?username={username}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'success':
        return data['room_id']
    else:
        return None

def get_coin_from_room_id(room_id):
    """Yayın odası ID'sinden toplam coin miktarını alır"""
    url = f"https://api.tiktok.com/getRoomStats?room_id={room_id}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'success':
        return data['data']['room_total_coin']
    else:
        return 0

def main():
    print("TikTok Canlı Yayın Geliri Hesaplayıcısı")
    
    # Kullanıcı adını al
    username = input("TikTok Kullanıcı Adını Girin (@kullaniciadi): ")
    
    # Yayın odası ID'sini al
    room_id = get_room_id(username)
    if not room_id:
        print("Kullanıcı şu anda yayında değil veya kullanıcı adı hatalı.")
        return
    
    print("Yayın odası bulundu. Coin bilgileri alınıyor...")
    
    # Coin miktarını al
    total_coin = get_coin_from_room_id(room_id)
    if total_coin == 0:
        print("Coin bilgisi alınamadı.")
        return
    
    # Gelir hesapla
    toplam_gelir, yayinci_geliri = hesapla_yayin_geliri(total_coin)
    
    # Sonuçları yazdır
    print(f"Toplam Gelir: {toplam_gelir:.2f} ₺")
    print(f"Yayıncının Kazancı (Kesintisiz): {yayinci_geliri:.2f} ₺")

if __name__ == "__main__":
    main()
