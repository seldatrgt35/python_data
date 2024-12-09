from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ChromeDriver'ı Service ile başlatıyoruz
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

# Kullanıcıdan girdi al
arama_turu = input("Aramak istediğiniz türü girin (ör: hırdavatçı): ")
konum = input("Konumunuzu girin (ör: 'İstanbul' veya '41.015137,28.979530'): ")

# Google Maps'te arama yapmak için URL oluştur
url = f"https://www.google.com/maps/search/{arama_turu}+{konum}/"
browser.get(url)
time.sleep(5)  # Sayfanın yüklenmesi için bekleyin

# Sayfa kaynağını al ve BeautifulSoup ile ayrıştır
kaynak = browser.page_source
soup = BeautifulSoup(kaynak, "html.parser")

# İşletme bilgilerini toplamak için bir liste
liste = []

# İşletmeleri çek
isletmeler = soup.find_all("div", attrs={"class": "Nv2PK"})

for isletme in isletmeler:
    try:
        isim = isletme.find("div", attrs={"class": "qBF1Pd"}).text.strip()
    except AttributeError:
        isim = "İsim Bulunamadı"

    
    try:
        telefon = isletme.find("span", attrs={"class": "UsdlK"}).text.strip()
    except AttributeError:
        telefon = "Telefon Bulunamadı"

    liste.append([isim, telefon])

# Sonraki sayfa düğmesini takip et
for _ in range(5):  # Kaç sayfa ilerlemek istediğinize bağlı
    try:
        # Sonraki sayfa düğmesini bulun ve tıklayın
        sonraki_sayfa = browser.find_element("xpath", "//button[@aria-label='Sonraki sayfa']")
        sonraki_sayfa.click()
        time.sleep(5)  # Sayfanın yüklenmesi için bekleyin

        kaynak = browser.page_source
        soup = BeautifulSoup(kaynak, "html.parser")

        isletmeler = soup.find_all("div", attrs={"class": "Nv2PK"})

        for isletme in isletmeler:
            try:
                isim = isletme.find("div", attrs={"class": "qBF1Pd"}).text.strip()
            except AttributeError:
                isim = "İsim Bulunamadı"

            try:
                telefon = isletme.find("span", attrs={"class": "UsdlK"}).text.strip()
            except AttributeError:
                telefon = "Telefon Bulunamadı"

            liste.append([isim, telefon])
    except Exception as e:
        print("Sonraki sayfa düğmesi bulunamadı.")
        break

# Sonuçları kaydet
browser.quit()  # Tarayıcıyı kapat

# Sonuçları TXT dosyasına yaz
with open("isletmeler.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"Arama Türü: {arama_turu}\nKonum: {konum}\n\n")
    for isletme in liste:
        dosya.write(f"İsim: {isletme[0]}\nTelefon: {isletme[1]}\n\n")

print("Sonuçlar 'isletmeler.txt' dosyasına kaydedildi.")
