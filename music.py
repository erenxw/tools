import os
import asyncio
import logging

# MP3, MP4 ve WebM dosyaları için klasörler
MP3_DIR = os.path.join(os.getcwd(), 'mp3')
MP4_DIR = os.path.join(os.getcwd(), 'mp4')
WEBM_DIR = os.path.join(os.getcwd(), 'webm')

# Klasörlerin olup olmadığını kontrol et ve oluştur
if not os.path.exists(MP3_DIR):
    os.makedirs(MP3_DIR)

if not os.path.exists(MP4_DIR):
    os.makedirs(MP4_DIR)

if not os.path.exists(WEBM_DIR):
    os.makedirs(WEBM_DIR)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def check_device():
    """ Kullanıcıdan cihaz türünü alır """
    device = input("Mobil cihaz mı kullanıyorsunuz? (evet/hayır): ").lower()
    return device == 'evet'

async def download_song(query: str, format_choice: str) -> None:
    if not query:
        print("Lütfen geçerli bir sorgu girin!")
        return

    print(f"**'{query}'** için arama yapılıyor, lütfen bekleyin...")

    # Dosya formatlarına göre komutları ayarla
    if format_choice == "mp3":
        output_template = os.path.join(MP3_DIR, "%(title)s.%(ext)s")
        command = (
            f"yt-dlp --no-playlist --extract-audio --audio-format mp3 "
            f"--ffmpeg-location '/path/to/ffmpeg' "
            f"--output \"{output_template}\" \"ytsearch:{query}\""
        )
    elif format_choice == "mp4":
        output_template = os.path.join(MP4_DIR, "%(title)s.%(ext)s")
        command = (
            f"yt-dlp --no-playlist --format mp4 "
            f"--ffmpeg-location '/path/to/ffmpeg' "
            f"--output \"{output_template}\" \"ytsearch:{query}\""
        )
    elif format_choice == "webm":
        output_template = os.path.join(WEBM_DIR, "%(title)s.%(ext)s")
        command = (
            f"yt-dlp --no-playlist --format bestaudio/best "
            f"--ffmpeg-location '/path/to/ffmpeg' "
            f"--output \"{output_template}\" \"ytsearch:{query}\""
        )
    else:
        print("Geçersiz format seçimi! Lütfen 'mp3', 'mp4' veya 'webm' seçin.")
        return

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_message = stderr.decode().strip() or "Bilinmeyen hata."
            logging.error(f"yt-dlp hata: {error_message}")
            print(f"İndirme sırasında hata oluştu: {error_message}")
            return

        files = [
            os.path.join(MP3_DIR, f)
            for f in os.listdir(MP3_DIR)
            if f.endswith('.mp3')
        ] if format_choice == "mp3" else (
            [os.path.join(MP4_DIR, f)
             for f in os.listdir(MP4_DIR)
             if f.endswith('.mp4')] if format_choice == "mp4" else (
            [os.path.join(WEBM_DIR, f)
             for f in os.listdir(WEBM_DIR)
             if f.endswith('.webm')]
            ))

        if not files:
            print("Dosya bulunamadı, lütfen tekrar deneyin.")
            return

        filename = max(files, key=os.path.getmtime)
        print(f"İndirme tamamlandı: {filename}")

        with open(filename, 'rb') as media:
            print(f"{filename} dosyasını başarıyla okudum.")

        # Burada dosya silme işlemi yapılmıyor
        # os.remove(filename)
        logging.info(f"{filename} dosyası gönderildi.")

    except Exception as ex:
        logging.exception("İndirme işlemi sırasında bir hata oluştu.")
        print(f"Bir hata oluştu: {ex}")

async def download_all_songs(artist: str, format_choice: str, num_songs: int = 10) -> None:
    """
    Sanatçının ilk 'num_songs' şarkısını indir.
    """
    print(f"{artist} sanatçısının şarkıları indiriliyor...")

    for i in range(1, num_songs + 1):
        query = f"{artist} şarkı {i}"
        print(f"\n**'{query}'** için arama yapılıyor...")
        await download_song(query, format_choice)

def main():
    # Mobil uyarısı ekle
    if check_device():
        print("Mobil cihaz kullanıyorsunuz. MP3 dosyası yerine WebM kullanmanızı öneririz.")

    while True:
        query = input("Sanatçı adı girin (çıkmak için 'q' yazın): ")
        if query.lower() == 'q':
            print("Çıkılıyor...")
            break

        # Kullanıcıdan format seçimi alıyoruz
        format_choice = input("Hangi formatta indirmek istersiniz? (mp3/mp4/webm): ")
        
        # Tek şarkı indirmek için
        asyncio.run(download_song(query, format_choice))
        
        # Tüm şarkıları indirmek için
        # asyncio.run(download_all_songs(query, format_choice))
        
        # Başka şarkı indirmek ister misiniz diye soralım
        another = input("Başka bir şarkı indirmek ister misiniz? (evet/hayır): ")
        if another.lower() != 'evet':
            break

if __name__ == '__main__':
    main()