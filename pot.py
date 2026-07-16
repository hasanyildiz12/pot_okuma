import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def main():
    print("ADS1115 Başlatılıyor...")
    
    # I2C bağlantısını kur (SDA ve SCL pinleri)
    i2c = busio.I2C(board.SCL, board.SDA)

    # ADS1115 modülünü tanımla
    ads = ADS.ADS1115(i2c)
    
    # Gain (Kazanç) Ayarı:
    # Gain=1 ayarı, maksimum 4.096V'a kadar olan gerilimleri okumamızı sağlar.
    # Bizim A0 pinindeki voltajımız 3.3V'u geçmeyeceği için bu ayar en hassas ve doğru olanıdır.
    ads.gain = 1

    # A0 pinini analog giriş olarak ayarla
    chan = AnalogIn(ads, ADS.P0)

    # Gerilim Bölücü Çarpanı (100k ve 33k dirençler için)
    # Formül: (100 + 33) / 33 = 4.0303
    CARPAN = 4.0303

    print("\n" + "="*50)
    print("EV Şarj İstasyonu CP Sinyal Simülatörü")
    print("Potansiyometreyi çevirerek durumları test edin.")
    print("Çıkış için CTRL+C")
    print("="*50 + "\n")

    try:
        while True:
            # ADS1115'in A0 pininden korumalı voltajı oku (Örn: 2.68V)
            adc_voltaj = chan.voltage
            
            # Okunan bu değeri gerçek CP hat voltajına geri çevir (Örn: 10.8V)
            gercek_cp_voltaj = adc_voltaj * CARPAN
            
            # Durum Makinesi (State Machine) Mantığı
            durum = "BİLİNMİYOR"
            if gercek_cp_voltaj >= 11.0:
                durum = "DURUM A (Kablo Boşta - 12V)"
            elif 8.0 <= gercek_cp_voltaj <= 10.0:
                durum = "DURUM B (Araç Bağlandı - 9V)"
            elif 5.0 <= gercek_cp_voltaj <= 7.0:
                durum = "DURUM C (Şarj İstiyor - 6V)"
                
            # Sonuçları ekrana formatlı şekilde yazdır
            print(f"ADC Pini: {adc_voltaj:.2f} V  |  Gerçek Hat: {gercek_cp_voltaj:.2f} V  |  Durum: {durum}")
            
            # Okumalar arası bekleme süresi
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nTest sonlandırıldı.")

if __name__ == "__main__":
    main()