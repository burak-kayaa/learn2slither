Süper. O zaman bunu sana direkt **EPIC → TASK → alt görev** şeklinde, gerçekten uygulanabilir bir geliştirme planı olarak çıkarayım.

Bu roadmap’i subject’e göre hazırladım: 10x10 board, 2 yeşil + 1 kırmızı elma, 4 yön vision, sadece 4 action, reward sistemi, Q-learning, save/load, visual mode, step-by-step ve en az 1/10/100 session modeli zorunlu.    

# Proje Yol Haritası

## EPIC 0 — Proje iskeleti ve teknik kararlar

Amaç: Baştan subject’e uygun mimari kurmak. Subject modüler yapı bekliyor; environment, interpreter/state ve agent ayrımı önemli. 

### TASK 0.1 — Teknoloji seçimi

* Python seç
* UI için pygame seç
* Model için ilk sürümde Q-table seç
* Save/load için json ya da pickle seç

### TASK 0.2 — Klasör yapısını oluştur

Öneri:

```text
learn2slither/
├── main.py
├── cli.py
├── config.py
├── environment/
│   ├── board.py
│   ├── snake.py
│   ├── apples.py
│   └── game.py
├── state/
│   ├── vision.py
│   └── encoder.py
├── agent/
│   ├── q_agent.py
│   ├── q_table.py
│   └── policy.py
├── ui/
│   ├── renderer.py
│   └── step_mode.py
├── models/
├── tests/
└── README.md
```

### TASK 0.3 — Temel sabitleri belirle

* BOARD_WIDTH = 10
* BOARD_HEIGHT = 10
* INITIAL_SNAKE_LENGTH = 3
* GREEN_APPLE_COUNT = 2
* RED_APPLE_COUNT = 1
* ACTIONS = [UP, LEFT, DOWN, RIGHT]

---

## EPIC 1 — Environment / Board

Amaç: RL’den bağımsız olarak snake oyununun tüm kurallarını doğru çalıştırmak. Board kuralları subject’te açıkça tanımlı. 

### TASK 1.1 — Board modeli

* 10x10 grid yapısını kur
* Hücre koordinat sistemini belirle
* Boş hücre bulma fonksiyonu yaz

### TASK 1.2 — Snake veri modeli

* Snake body’yi ordered list/deque olarak tut
* Head ayrı kolay erişilebilir olsun
* Başlangıçta 3 hücrelik contiguous spawn yap

### TASK 1.3 — Apple spawn sistemi

* 2 green apple üret
* 1 red apple üret
* Apple’lar snake’in üstüne gelmesin
* Apple’lar birbirinin üstüne gelmesin

### TASK 1.4 — Hareket motoru

* Action’a göre yeni head hesapla
* Body update et
* Tail silme / uzatma mantığını net kur

### TASK 1.5 — Oyun sonu koşulları

* Duvara çarpma
* Kendi gövdesine çarpma
* Uzunluğun 0’a düşmesi

### TASK 1.6 — Elma etkileşimleri

* Green apple yenince +1 length
* Yeni green apple spawn
* Red apple yenince -1 length
* Yeni red apple spawn

### TASK 1.7 — Environment testleri

* Snake başlangıçta 3 mü
* Spawn’lar çakışmıyor mu
* Wall collision çalışıyor mu
* Self-collision çalışıyor mu
* Green/red apple kuralları doğru mu

**Bu epic bitince hedef:**
Agent olmadan bile oyun kuralları eksiksiz çalışmalı.

---

## EPIC 2 — State / Vision Interpreter

Amaç: Agent’a sadece snake’in görebildiği bilgi verilmesi. Fazla bilgi vermek subject’e göre direkt ceza sebebi. 

### TASK 2.1 — Vision mantığını tanımla

Head’den:

* yukarı
* aşağı
* sol
* sağ

yönlerinde görülen hücreleri üret.

### TASK 2.2 — Sembol standardı oluştur

Subject’e uygun olarak:

* W = wall
* H = head
* S = snake body
* G = green apple
* R = red apple
* 0 = empty 

### TASK 2.3 — Human-readable terminal çıktısı

Örnek gibi state yazdır:

```text
UP:    W 0 0 G R 0
LEFT:  W 0 0 0
DOWN:  0 S S W
RIGHT: 0 0 G
```

### TASK 2.4 — Agent için state encoding

* Vision çıktısını hashlenebilir key’e çevir
* tuple/string state key üret
* Q-table’ın bunu kullanmasını sağla

### TASK 2.5 — State doğrulama testleri

* Head kenardayken wall doğru mu
* Apple vision’da doğru çıkıyor mu
* Snake body doğru görünüyor mu
* Board’daki görünmeyen bilgi encode edilmiyor mu

**Bu epic bitince hedef:**
Agent sadece vision çıktısını görmeli; full board asla görmemeli. 

---

## EPIC 3 — Action sistemi

Amaç: Agent’ın subject’te istenen 4 action ile karar verebilmesi. 

### TASK 3.1 — Action enum oluştur

* UP
* LEFT
* DOWN
* RIGHT

### TASK 3.2 — Action → hareket dönüşümü

* Her action için delta tanımla
* `UP -> (0, -1)` gibi

### TASK 3.3 — Action logging

* Terminalde her step için:

  * current vision
  * seçilen action
    yazdır

### TASK 3.4 — Invalid action davranışı

* Şimdiden net kural koy
* Action her zaman bu 4’ten biri olmalı
* Ters yöne dönme desteğini ilk sürümde serbest bırakabilir ya da yasaklayabilirsin; ama nasıl yaptığını README’de belirt

---

## EPIC 4 — Reward sistemi

Amaç: Öğrenmeyi yönlendirecek ödül sistemini kurmak. Subject reward değerlerini sana bırakıyor ama yönünü açıkça tarif ediyor. 

### TASK 4.1 — Başlangıç reward seti

Öneri:

```python
GREEN_APPLE_REWARD = +10
RED_APPLE_REWARD = -8
STEP_REWARD = -0.1
GAME_OVER_REWARD = -20
```

### TASK 4.2 — Reward hesaplama fonksiyonu

`compute_reward(event)` gibi tek merkezli fonksiyon yaz:

* green apple
* red apple
* nothing
* game over

### TASK 4.3 — Reward tuning desteği

* Reward’ları config’ten okunur yap
* Sonradan hızlı deney yapabil

### TASK 4.4 — İsteğe bağlı iyileştirmeler

İlk sürümden sonra:

* uzun yaşama bonusu
* length 10’a yaklaşma bonusu
* gereksiz dolaşmayı azaltan ceza

**Bu epic bitince hedef:**
Agent’ın neye teşvik edildiği net olmalı: green apple, hayatta kalma, red apple’dan kaçınma.

---

## EPIC 5 — Q-learning Agent

Amaç: Subject’in zorunlu istediği şekilde Q-table ya da neural network ile Q-learning agent geliştirmek. En risksiz yol Q-table. 

### TASK 5.1 — Q-table veri yapısı

* `dict[state_key][action] = q_value`
* Bilinmeyen state/action için default 0.0

### TASK 5.2 — Action seçme politikası

* epsilon-greedy uygula
* exploration vs exploitation dengesi kur. Subject bunu açıkça bekliyor. 

### TASK 5.3 — Q update formülü

* `Q(s,a) <- Q(s,a) + alpha * (reward + gamma * max(Q(s')) - Q(s,a))`

### TASK 5.4 — Agent parametreleri

Başlangıç önerisi:

* alpha = 0.1
* gamma = 0.9
* epsilon = 1.0
* epsilon_decay = 0.995
* epsilon_min = 0.05

### TASK 5.5 — Dontlearn modu

Subject’e göre non-learning mod olmalı; model test edilirken Q update durmalı. 

Bunun için:

* `learning_enabled` flag’i ekle
* `--dontlearn` gelirse update yapma

### TASK 5.6 — Agent testleri

* Yeni state için q initialize oluyor mu
* epsilon=1 ise random davranıyor mu
* epsilon=0 ise greedy davranıyor mu
* update formülü doğru mu

---

## EPIC 6 — Training loop

Amaç: Yüzlerce/binlerce session çalıştırabilecek ana eğitim akışını kurmak. Subject çoklu training session istiyor.  

### TASK 6.1 — Tek session akışı

Her step:

1. state al
2. action seç
3. environment step yap
4. reward al
5. next_state al
6. Q update et
7. done ise çık

### TASK 6.2 — Çoklu session akışı

* `for episode in range(sessions):`
* session bitince environment reset

### TASK 6.3 — Session metrikleri

Her session sonunda tut:

* max length
* duration / step count
* green apple sayısı
* red apple sayısı
* ölüm sebebi

### TASK 6.4 — Training sırasında çıktı kontrolü

Subject eğitimde visual ve terminal output’un kapatılabileceğini söylüyor. 

Bu yüzden:

* `visual on/off`
* `verbose on/off`

### TASK 6.5 — Evaluation modu

* load edilmiş modelle
* `dontlearn = true`
* belirli sayıda session çalıştır
* performansı bozma

---

## EPIC 7 — Save / Load model

Amaç: Eğitim durumunu dosyaya yazmak ve geri yüklemek. Subject bunu zorunlu istiyor. 

### TASK 7.1 — Model dosya formatı

İlk sürüm için json yeterli:

```json
{
  "alpha": 0.1,
  "gamma": 0.9,
  "epsilon": 0.12,
  "q_table": {}
}
```

### TASK 7.2 — Save işlemi

* `--save models/10sess.json`
* eğitim bitince dosyaya yaz

### TASK 7.3 — Load işlemi

* `--load models/100sess.json`
* q_table ve parametreleri geri al

### TASK 7.4 — Model klasörü

Subject teslimde `models` klasörü istiyor. 

Bu dosyaları üret:

* `models/1sess.json`
* `models/10sess.json`
* `models/100sess.json`

### TASK 7.5 — İleri seviye model üretimi

Bonus değil ama savunmada işine yarar:

* `models/1000sess.json`

Çünkü subject örneğinde 1000 session model ile daha iyi sonuç beklentisi gösteriliyor. 

---

## EPIC 8 — CLI ve kullanım parametreleri

Amaç: Subject’te örneklenen komut satırı akışını sağlamak. 

### TASK 8.1 — Argparse yapısı

Parametreler:

* `--sessions`
* `--save`
* `--load`
* `--visual`
* `--dontlearn`
* `--step-by-step`
* `--speed`

### TASK 8.2 — Parametre kombinasyonları

Desteklenmesi gereken senaryolar:

* yeni eğitim başlat
* eğitim sonrası save et
* modeli yükle
* öğrenmeden test et
* step-by-step izle

### TASK 8.3 — Hata yönetimi

* load path yoksa anlaşılır hata
* save path oluşturulamıyorsa hata
* bozuk model dosyasına karşı koruma

### TASK 8.4 — Örnek komutlar

```bash
python main.py --sessions 10 --save models/10sess.json --visual off
python main.py --sessions 100 --save models/100sess.json --visual off
python main.py --load models/100sess.json --sessions 10 --dontlearn --visual on --step-by-step
```

---

## EPIC 9 — Görsel arayüz

Amaç: Board’u grafik pencere ile göstermek, hız ve adım adım mod sağlamak. Subject bunu zorunlu istiyor. 

### TASK 9.1 — Grid renderer

* 10x10 grid çiz
* her cell eşit boyutta olsun

### TASK 9.2 — Renkler

* Green apple = yeşil
* Red apple = kırmızı
* Snake = mavi 

### TASK 9.3 — Frame update

* her action sonrası board güncellensin
* training ve eval sırasında çalışsın

### TASK 9.4 — Hız kontrolü

* slow / medium / fast
* ya da ms delay

### TASK 9.5 — Step-by-step modu

* tuşa basınca 1 step ilerlesin
* savunmada gösterim için çok iyi olur

### TASK 9.6 — UI kapatma / training hızlandırma

* `visual off` iken pencere açma
* training hızlansın

---

## EPIC 10 — Test, debug ve stabilizasyon

Amaç: Savunmada patlamayacak, crash etmeyecek sürüm çıkarmak. Subject beklenmedik kapanmayı ağır cezalandırıyor. 

### TASK 10.1 — Kritik bug listesi

Kontrol et:

* apple spawn çakışmaları
* red apple sonrası length hesabı
* self-collision sırası
* move sonrası tail update sırası
* state encoding tutarlılığı
* load edilen modelde action set uyumu

### TASK 10.2 — Smoke test senaryoları

* 1 session train
* 10 session train + save
* 100 session train + save
* 100 model load + dontlearn eval
* visual on + step-by-step

### TASK 10.3 — Crash koruması

* try/except ile ana loop koru
* model dosya okuma/yazma hatalarını yakala
* pencere kapatma event’ini düzgün işle

---

## EPIC 11 — Teslim ve savunma hazırlığı

Amaç: Sadece kodu yazmak değil, subject’in teslim beklentisini eksiksiz karşılamak. 

### TASK 11.1 — Zorunlu teslim öğeleri

* board
* agent
* models klasörü
* en az 3 model: 1 / 10 / 100 session

### TASK 11.2 — README

README’de şunlar olsun:

* proje amacı
* kurulum
* bağımlılıklar
* komut satırı kullanımı
* reward mantığı
* Q-learning yaklaşımı
* state representation açıklaması
* visual ve dontlearn modları

### TASK 11.3 — Savunma demosu

Hazır komutlar:

1. `1sess` modeli göster
2. `10sess` modeli göster
3. `100sess` modeli göster
4. `dontlearn` ile kıyas yap
5. step-by-step açıp vision + action akışını anlat

### TASK 11.4 — Hedef metrik

Subject’in hedefi:

* snake uzunluğu en az 10
* mümkün olduğunca uzun yaşam süresi  

Bu yüzden savunmada şunu göstermen güzel olur:

* 1 session zayıf
* 10 biraz daha iyi
* 100 daha iyi
* 1000 çok daha iyi

---

# Sana önerdiğim gerçek çalışma sırası

## Faz 1

* EPIC 0
* EPIC 1

## Faz 2

* EPIC 2
* EPIC 3
* EPIC 4

## Faz 3

* EPIC 5
* EPIC 6
* EPIC 7

## Faz 4

* EPIC 8
* EPIC 9

## Faz 5

* EPIC 10
* EPIC 11

---

# 7 günlük kısa sprint planı

## Gün 1

* proje iskeleti
* board
* snake
* apple spawn

## Gün 2

* movement
* collision
* game over
* reward hook

## Gün 3

* state/vision
* encoding
* terminal output

## Gün 4

* q-table
* epsilon-greedy
* q-update

## Gün 5

* training loop
* save/load
* dontlearn


* pygame arayüz
* speed
* step-by-step

## Gün 7

* model üretimi
* README
* test
* savunma hazırlığı

---

# En kritik not

Bu projede önce “çok iyi öğrenen agent” yapmaya çalışma.
Önce:

* subject’e tam uyan environment
* doğru vision/state
* doğru action/reward/q-learning akışı

kur. Çünkü zorunlu puanı bunlar getiriyor. Bonuslar ancak mandatory kısım doğruysa sayılıyor. 

Bir sonraki mesajda istersen bunu daha da indirgerim ve sana direkt:
**“bugün başlayacağın ilk 20 task”**
şeklinde checkbox’lı yapılacaklar listesi çıkarırım.
