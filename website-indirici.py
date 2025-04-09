import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
                    ".css", ".js", ".pdf", ".docx", ".xlsx", ".zip", ".rar",
                    ".mp3", ".mp4", ".avi", ".mov", ".ttf", ".woff", ".woff2", ".txt", ".html"]

def is_valid_file(url):
    return any(url.lower().endswith(ext) for ext in valid_extensions)

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def save_file(file_url, base_url, download_folder, session, downloaded_files):
    if file_url in downloaded_files:
        return
    downloaded_files.add(file_url)
    try:
        r = session.get(file_url, timeout=10)
        r.raise_for_status()
        relative_path = urlparse(file_url).path.lstrip('/')
        save_path = os.path.join(download_folder, relative_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(r.content)
    except:
        pass

def crawl_page(url, base_url, download_folder, session, visited, downloaded_files, executor):
    if url in visited:
        return
    visited.add(url)
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        if "text/html" not in r.headers.get("Content-Type", ""):
            executor.submit(save_file, url, base_url, download_folder, session, downloaded_files)
            return

        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        relative_path = urlparse(url).path.lstrip('/')
        file_path = os.path.join(download_folder, relative_path or "index.html")
        if file_path.endswith('/'):
            file_path += "index.html"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)

        for tag in soup.find_all(["img", "script", "link"]):
            src = tag.get("src") or tag.get("href")
            if src:
                full_url = urljoin(url, src)
                if is_same_domain(base_url, full_url) and is_valid_file(full_url):
                    executor.submit(save_file, full_url, base_url, download_folder, session, downloaded_files)

        for link in soup.find_all("a", href=True):
            href = link.get("href")
            full_url = urljoin(url, href)
            if is_same_domain(base_url, full_url):
                if is_valid_file(full_url):
                    executor.submit(save_file, full_url, base_url, download_folder, session, downloaded_files)
                else:
                    crawl_page(full_url, base_url, download_folder, session, visited, downloaded_files, executor)

    except Exception as e:
        print(f"[HATA] Siteye ulaşılamadı: {url}\nSebep: {e}")

def try_access_url(raw_url, session):
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        return raw_url
    for prefix in ["https://", "http://"]:
        test_url = prefix + raw_url
        try:
            response = session.get(test_url, timeout=5)
            response.raise_for_status()
            return test_url
        except:
            continue
    return None

def download_entire_site():
    while True:
        visited = set()
        downloaded_files = set()
        session = requests.Session()
        executor = ThreadPoolExecutor(max_workers=15)

        raw_url = input("\nİndirmek istediğin sitenin URL'sini gir (https://, http:// ya da sadece domain): ").strip()
        if raw_url.lower() == "q":
            print("Çıkılıyor...")
            break

        base_url = try_access_url(raw_url, session)

        if not base_url:
            print("[HATA] Siteye ulaşılamadı. Lütfen geçerli bir adres gir.")
            continue

        domain = urlparse(base_url).netloc.replace("www.", "")
        folder = domain

        print(f"\nİndirme başlatılıyor: {base_url}")
        crawl_page(base_url, base_url, folder, session, visited, downloaded_files, executor)
        executor.shutdown(wait=True)
        print(f"\nTamamlandı! Dosyalar burada: {folder}/")

        again = input("\nBaşka bir site indirmek ister misin? (q ile çık): ").strip().lower()
        if again == "q":
            print("Çıkılıyor...")
            break

download_entire_site()
