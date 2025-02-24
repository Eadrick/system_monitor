# Sistem İzleme ve Optimizasyon Aracı

Modern bir sistem izleme ve kaynak optimizasyon aracı. Gerçek zamanlı olarak sistem performansını izler, sorunları tespit eder ve sistem kaynaklarını optimize etmek için öneriler sunar.

## Özellikler

- ✅ CPU kullanımı ve sıcaklık izleme
- ✅ RAM ve sanal bellek takibi
- ✅ Disk alanı kullanım analizi
- ✅ Ağ bandgenişliği izleme
- ✅ En çok kaynak tüketen süreçlerin tespiti
- ✅ Renkli ve interaktif terminal arayüzü
- 🚧 Sistem temizleme ve optimizasyon
- 🚧 Başlangıç programları yönetimi
- 🚧 Zamanlanmış görevler
- 🚧 Performans raporları ve öneriler

## Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Windows, Linux veya macOS işletim sistemi
- Yönetici hakları (bazı özellikler için)

## Kurulum

1. Depoyu klonlayın:
```bash
git clone https://github.com/Eadrick/system_monitor.git
cd system_monitor
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### Temel İzleme

Sistem izleme aracını başlatmak için:

```bash
python main.py
```

### Parametreler

- `--refresh`: Yenileme hızını ayarlar (saniye cinsinden, varsayılan: 2.0)

Örnek:
```bash
python main.py --refresh 1.5
```

## Klavye Kısayolları

- `Ctrl+C`: Uygulamayı sonlandır

## Çıktı Örneği

```
┌──────────────────────────┐
│       CPU Durumu         │
├──────────┬───────────────┤
│ CPU 0    │     25.3%     │
│ CPU 1    │     18.7%     │
└──────────┴───────────────┘

┌──────────────────────────┐
│      Bellek Durumu       │
├──────────┬───────────────┤
│ RAM      │  8.2GB/16GB   │
│ Swap     │  1.1GB/4GB    │
└──────────┴───────────────┘
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Güncellemeler ve Yol Haritası

- [ ] Web arayüzü desteği
- [ ] Uzak sistem izleme
- [ ] Makine öğrenimi tabanlı anormallik tespiti
- [ ] Performans raporu e-posta bildirimleri
- [ ] Çoklu sistem karşılaştırma

## Sorun Giderme

Yaygın sorunlar ve çözümleri:

1. "PermissionError" hatası:
   - Uygulamayı yönetici olarak çalıştırın

2. ModuleNotFoundError:
   - requirements.txt dosyasındaki tüm bağımlılıkların yüklendiğinden emin olun
   
3. Sıcaklık verisi görünmüyor:
   - Bu özellik tüm platformlarda desteklenmeyebilir

## İletişim

Sorularınız veya önerileriniz için:
- GitHub Eadrick
