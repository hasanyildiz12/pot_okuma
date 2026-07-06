import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def main():
    print("I2C başlatılıyor...")
    # Raspberry Pi'nin I2C pinlerini (SDA ve SCL) başlat
    i2c = busio.I2C(board.SCL, board.SDA)

    # ADS1115 modülünü I2C hattı üzerinden tanımla
    ads = ADS.ADS1115(i2c)
    
    # İsteğe bağlı: Ölçüm aralığını (Gain) ayarlayabilirsin. 
    # Gain=1 ayarı 0 ile 4.096V arasını çok hassas ölçer (3.3V okuyacağımız için idealdir)
    ads.gain = 1

    # Ölçüm yapılacak kanalı A0 olarak belirle
    chan = AnalogIn(ads, ADS.P0)

    print("\n" + "="*50)
    print("ADS1115 Voltaj Okuma Simülasyonu Başladı")
    print("Potansiyometreyi çevirerek değerleri gözlemleyin.")
    print("Çıkmak için CTRL+C tuşlarına basın.")
    print("="*50 + "\n")

    try:
        while True:
            # Modülden voltajı ve ham 16-bit değeri oku
            okunan_voltaj = chan.voltage
            ham_deger = chan.value
            
            # Değerleri terminale formatlı bir şekilde yazdır
            print(f"A0 Pini -> Ölçülen Voltaj: {okunan_voltaj:>5.3f} V  |  Ham ADC Değeri: {ham_deger:>6}")
            
            # Saniyede iki kez okuma yapmak için yarım saniye bekle
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nTest sonlandırıldı. İyi çalışmalar!")

if __name__ == "__main__":
    main()