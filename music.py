import os
import asyncio
import logging

# Mevcut dizini kullanıyoruz
DOWNLOAD_DIR = os.getcwd()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def download_song(query: str) -> None:
    if not query:
        print("Lütfen geçerli bir sorgu girin!")
        return

    print(f"**'{query}'** için arama yapılıyor, lütfen bekleyin...")

    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    command = (
        f"yt-dlp --no-playlist --extract-audio --audio-format mp3 "
        f"--ffmpeg-location '/path/to/ffmpeg' "
        f"--output \"{output_template}\" \"ytsearch1:{query}\""
    )

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

        mp3_files = [
            os.path.join(DOWNLOAD_DIR, f)
            for f in os.listdir(DOWNLOAD_DIR)
            if f.endswith('.mp3')
        ]
        if not mp3_files:
            print("Dosya bulunamadı, lütfen tekrar deneyin.")
            return

        filename = max(mp3_files, key=os.path.getmtime)
        print(f"İndirme tamamlandı: {filename}")

        with open(filename, 'rb') as audio:
            print(f"{filename} dosyasını başarıyla okudum.")

        os.remove(filename)
        logging.info(f"{filename} dosyası gönderildi ve silindi.")
    except Exception as ex:
        logging.exception("İndirme işlemi sırasında bir hata oluştu.")
        print(f"Bir hata oluştu: {ex}")

def main():
    while True:
        query = input("Şarkı adı veya sanatçı girin (çıkmak için 'q' yazın): ")
        if query.lower() == 'q':
            print("Çıkılıyor...")
            break
        asyncio.run(download_song(query))
        print("\nBaşka bir şarkı indirmek ister misiniz?")
    
if __name__ == '__main__':
    main()