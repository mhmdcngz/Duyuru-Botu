# 🎓 Fırat Üniversitesi Otomatik Duyuru Botu

Bu proje, Fırat Üniversitesi'nin çeşitli fakülte ve bölüm web sitelerindeki duyuruları 7/24 takip eden ve yeni bir duyuru yayınlandığında anında **Telegram** üzerinden bildirim gönderen Python tabanlı bir otomasyon botudur.

Sunucu maliyeti olmadan tamamen **GitHub Actions** üzerinde çalışacak şekilde tasarlanmıştır.

## ✨ Özellikler

* **Çoklu Site Desteği:** Tek bir betik üzerinden Yazılım Mühendisliği, Teknoloji Fakültesi ve Üniversite Ana Sayfası eşzamanlı olarak taranır.
* **Akıllı Hafıza:** Kazınan (scrape) son duyuru verisi depoya otomatik olarak kaydedilir (commitlenir). Böylece bot tekrar çalıştığında aynı mesajı defalarca göndermez (Spam koruması).
* **7/24 Bulut Otomasyonu:** GitHub Actions entegrasyonu sayesinde bilgisayarınız kapalı olsa dahi Cron Job mantığıyla her saat başı tetiklenir.
* **Hata Toleransı (Error Handling):** Farklı DOM yapılarına (HTML) sahip sitelere özel veri çekme mantığı içerir. Siteye ulaşılamadığında veya etiketler değiştiğinde çökmeden diğer siteleri taramaya devam eder.

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.10
* **Kütüphaneler:** `requests`, `beautifulsoup4`
* **Otomasyon & CI/CD:** GitHub Actions
* **Bildirim:** Telegram Bot API
* **Versiyon Kontrol:** Git & GitHub

## 🚀 Kurulum & Kendi Reponda Çalıştırma

Bu botu kendi hesabınızda çalıştırmak isterseniz (Fork) aşağıdaki adımları izleyebilirsiniz:

### 1. Repoyu Forklayın veya Klonlayın
Terminalinize şu komutu yazarak projeyi bilgisayarınıza indirin:
`git clone https://github.com/mhmdcngz/Duyuru-Botu.git`

### 2. Telegram Botu Oluşturun
* Telegram'da **@BotFather** ile konuşarak yeni bir bot oluşturun ve **Token** bilgisini alın.
* Kendi botunuza bir mesaj atın ve tarayıcıdan `https://api.telegram.org/bot<TOKEN>/getUpdates` adresine giderek kendi **Chat ID**'nizi öğrenin.

### 3. GitHub Secrets Ayarları
Projenizi GitHub'a yükledikten sonra deponuzun `Settings > Secrets and variables > Actions` menüsüne gidin ve şu iki gizli anahtarı ekleyin:
* `TELEGRAM_TOKEN`: Botunuzun API anahtarı
* `TELEGRAM_CHAT_ID`: Telegram Chat ID numaranız

### 4. Botu Uyandırın
* GitHub deposundaki **Actions** sekmesine gidin.
* Sol menüden **Firat Duyuru Kontrol** iş akışını seçip **Run workflow** butonuna basarak botu manuel tetikleyin.
* Bundan sonra bot her saat başı otomatik olarak uyanıp çalışmaya devam edecektir.

## 🗂️ Dosya Yapısı

* `duyuru_botu.py`: Veri çekme ve Telegram bildirimlerini yöneten ana Python dosyası.
* `.github/workflows/otomasyon.yml`: Botun GitHub sunucularında ne zaman ve nasıl çalışacağını belirleyen CI/CD yapılandırma dosyası.
* `hafiza_*.txt`: Botun son gördüğü duyuruları hatırlamasını sağlayan dinamik bellek dosyaları.

---
*Bu proje Muhammed Cengiz tarafından geliştirilmiştir. Geri bildirimleriniz ve katkılarınız (Pull Request) için teşekkürler!* 🚀
