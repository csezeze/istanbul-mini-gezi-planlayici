
# İstanbul Mini-Gezi Planlayıcı

## Proje Amacı
Bu proje, İstanbul'daki gezilecek yerlerin planlanmasını kolaylaştıran bir araç sunmaktadır. Kullanıcılar, gezi kategorilerini (müze, yürüyüş, yemek vb.) seçebilir ve sabah, öğle, akşam gibi zaman dilimlerine göre kişiselleştirilmiş bir gezi planı alabilirler.

## Veri Seti Hakkında
Proje, **Kaggle** üzerinde bulunan `ouzcanmaden/places-to-visit-in-istanbul` veri setini kullanmaktadır. Bu veri seti, İstanbul’daki gezilecek yerlerin isimleri, kategorileri ve açıklamalarını içermektedir. Veri seti, CSV formatından Markdown formatına dönüştürülerek projemizde kullanılmaktadır.

## Kullanılan Yöntemler
- **Veri Temizleme ve İşleme:** Markdown dosyasındaki başlıklardan yer adları çıkarılarak kullanıcıya önerilen yerler sunulmuştur.
- **Gradio:** Web arayüzü oluşturmak için kullanılmıştır. Kullanıcılar, gezi kategorileri ve ipuçları ile planlama yapabilir.
- **Regex:** Yer adlarını doğru şekilde eşleştirmek için kullanılmıştır.
  
## Elde Edilen Sonuçlar
- Kullanıcılar, müze, yürüyüş ve yemek gibi kategorilerle filtreleme yaparak, İstanbul’daki gezilecek yerleri sabah/öğle/akşam dilimlerine yerleştirerek iki günlük bir plan oluşturabilmektedir.
- Uygulama, kullanıcıya kişiselleştirilmiş öneriler sunmaktadır.

## Kullanım
1. **Kategoriler Seçin:** Müze, yürüyüş veya yemek kategorilerinden birini seçin.
2. **Mini İpucu (Opsiyonel):** Gezi planınızı özelleştirmek için mini ipuçları ekleyin. (Örneğin: "Ayasofya sabah olsun")
3. **Plan Oluştur:** "Plan Oluştur" butonuna tıklayarak gezi planınızı oluşturun.

## Web Linki
Proje uygulamanıza [Gradio Web Uygulaması](https://9de61b3c7cdbbed131.gradio.live) üzerinden erişebilirsiniz (72 saat süreyle açık kalıyor).

