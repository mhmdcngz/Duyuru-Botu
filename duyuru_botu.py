import requests
from bs4 import BeautifulSoup
import os

# --- KENDİ BİLGİLERİNİ BURAYA GİR ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# ------------------------------------

URL = "https://yazilimtf.firat.edu.tr/announcements-all"
DOSYA_ADI = "son_duyuru.txt"

def telegram_mesaj_gonder(mesaj):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    parametreler = {"chat_id": CHAT_ID, "text": mesaj}
    requests.post(api_url, data=parametreler)

def duyurulari_kontrol_et():
    print("Site kontrol ediliyor...")
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        duyuru_kutusu = soup.find("div", class_="news-section-cards")

        if duyuru_kutusu:
            en_yeni_duyuru = duyuru_kutusu.find("a")
            if not en_yeni_duyuru:
                return

            # 1. METİN DÜZELTME: Tüm metni satır satır ayırıp gereksiz boşlukları siliyoruz
            # Bu sayede sadece dolu olan satırları bir liste haline getiriyoruz
            satirlar = [satir.strip() for satir in en_yeni_duyuru.text.splitlines() if satir.strip()]

            # Listenin ilk elemanı Başlık, varsa ikinci elemanı Özet metni olur
            baslik = satirlar[0]
            ozet = satirlar[1] if len(satirlar) > 1 else ""

            # 2. LİNK DÜZELTME: Link zaten http ile başlıyorsa olduğu gibi al, başlamıyorsa site adresiyle birleştir
            href = en_yeni_duyuru.get("href")
            if href.startswith("http"):
                link = href
            else:
                link = "https://yazilimtf.firat.edu.tr" + href

            eski_duyuru = ""
            if os.path.exists(DOSYA_ADI):
                with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
                    eski_duyuru = dosya.read()

            if baslik != eski_duyuru:
                print("Yeni duyuru bulundu! Telegram'a mesaj gönderiliyor...")

                # Mesajı Başlık ve Özet olacak şekilde çok daha temiz bir formata soktuk
                mesaj = f"🚨 YENİ DUYURU 🚨\n\n📌 Başlık: {baslik}\n\n📝 Özet: {ozet}\n\n🔗 Link: {link}"
                telegram_mesaj_gonder(mesaj)

                with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
                    dosya.write(baslik)

                print("İşlem tamamlandı.")
            else:
                print("Yeni duyuru yok. Sistem beklemede.")
        else:
            print("Duyuru kutusu bulunamadı.")
    else:
        print(f"Siteye ulaşılamadı. Hata: {response.status_code}")

duyurulari_kontrol_et()