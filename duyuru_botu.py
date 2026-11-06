import requests
from bs4 import BeautifulSoup
import os

# --- KENDİ BİLGİLERİNİ BURAYA GİR ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# ------------------------------------

SITELER = [
    {
        "isim": "Yazılım Mühendisliği",
        "url": "https://yazilimtf.firat.edu.tr/announcements-all",
        "ana_link": "https://yazilimtf.firat.edu.tr",
        "kutu_class": "news-section-cards",
        "dosya_adi": "hafiza_yazilim.txt"
    },
    {
        "isim": "Teknoloji Fakültesi",
        "url": "https://teknolojif.firat.edu.tr/announcements-all",
        "ana_link": "https://teknolojif.firat.edu.tr",
        "kutu_class": "news-section-cards",
        "dosya_adi": "hafiza_teknoloji.txt"
    },
    {
        "isim": "Fırat Üniversitesi Ana Sayfa",
        "url": "https://www.firat.edu.tr/tr/page/announcement",
        "ana_link": "https://www.firat.edu.tr",
        "kutu_class": "blog-listing",
        "dosya_adi": "hafiza_firat.txt",
        "baslik_tag": "h3",
        "baslik_class": "title",
        "ozet_class": "item-excerpt"
    },
]

def telegram_mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    parametreler = {"chat_id": CHAT_ID, "text": mesaj}
    requests.post(api_url, data=parametreler, timeout=20)

def duyurulari_kontrol_et():
    for site in SITELER:
        isim = site["isim"]
        url = site["url"]
        ana_link = site["ana_link"]
        kutu_class = site["kutu_class"]
        dosya_adi = site["dosya_adi"]

        print(f"[{isim}] Site kontrol ediliyor...")
        try:
            response = requests.get(url, timeout=20)
        except requests.exceptions.RequestException as hata:
            print(f"[{isim}] Siteye bağlanılamadı, atlanıyor: {hata.__class__.__name__}")
            continue

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            duyuru_kutusu = soup.find("div", class_=kutu_class)

            if duyuru_kutusu:
                # Site özel selector'leri varsa (baslik_tag/ozet_class) onları kullan
                if "baslik_tag" in site:
                    baslik_el = duyuru_kutusu.find(site["baslik_tag"], class_=site.get("baslik_class"))
                    if not baslik_el:
                        print(f"[{isim}] Başlık etiketi bulunamadı, atlanıyor...")
                        continue

                    baslik_a = baslik_el.find("a")
                    baslik = baslik_a.get_text(strip=True) if baslik_a else baslik_el.get_text(strip=True)

                    href = baslik_a.get("href") if baslik_a else None

                    ozet_div = duyuru_kutusu.find("div", class_=site.get("ozet_class"))
                    ozet = ozet_div.get_text(strip=True) if ozet_div else ""
                else:
                    # Varsayılan mantık: ilk <a> etiketinden çek
                    en_yeni_duyuru = duyuru_kutusu.find("a")
                    if not en_yeni_duyuru:
                        continue

                    satirlar = [satir.strip() for satir in en_yeni_duyuru.text.splitlines() if satir.strip()]

                    if not satirlar:
                        print(f"[{isim}] Duyuru metni boş, atlanıyor...")
                        continue

                    baslik = satirlar[0]
                    ozet = satirlar[1] if len(satirlar) > 1 else ""
                    href = en_yeni_duyuru.get("href")

                # LİNK DÜZELTME: Link zaten http ile başlıyorsa olduğu gibi al, başlamıyorsa site adresiyle birleştir
                if not href:
                    link = ""
                elif href.startswith("http"):
                    link = href
                else:
                    link = ana_link + href

                eski_duyuru = ""
                if os.path.exists(dosya_adi):
                    with open(dosya_adi, "r", encoding="utf-8") as dosya:
                        eski_duyuru = dosya.read()

                if baslik != eski_duyuru:
                    print(f"[{isim}] Yeni duyuru bulundu! Telegram'a mesaj gönderiliyor...")

                    # Mesajı Başlık ve Özet olacak şekilde çok daha temiz bir formata soktuk
                    mesaj = f"🚨 YENİ DUYURU - {isim} 🚨\n\n📌 Başlık: {baslik}\n\n📝 Özet: {ozet}\n\n🔗 Link: {link}"
                    telegram_mesaj_gonder(mesaj)

                    with open(dosya_adi, "w", encoding="utf-8") as dosya:
                        dosya.write(baslik)

                    print(f"[{isim}] İşlem tamamlandı.")
                else:
                    print(f"[{isim}] Yeni duyuru yok. Sistem beklemede.")
            else:
                print(f"[{isim}] Duyuru kutusu bulunamadı.")
        else:
            print(f"[{isim}] Siteye ulaşılamadı. Hata: {response.status_code}")

duyurulari_kontrol_et()