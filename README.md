
    # İstanbul 2 Günlük Seyahat Planı

    Bu projede İstanbul'da 2 gün süresince gezilebilecek önemli yerleri kategorize ederek, önerilen bir günlük plan oluşturulmuştur. Kullanıcılar, müze, yürüyüş ve yemek gibi kategorileri filtreleyerek, kişiselleştirilmiş bir gezi planı oluşturabilirler.

    ## Proje Yapısı

    - **Gradio Web Arayüzü**: Kullanıcıların seyahat planlarını kişiselleştirmelerine olanak tanır. Kategoriler ve mini ipuçları girilerek, sabah, öğle ve akşam için gezilecek yerler sıralanır.
    - **Markdown Rehber**: Veri setindeki yerler, Markdown formatında kullanıcıya sunulur. Her yer için açıklamalar, semtler, kategoriler ve önerilen ziyaret saatleri bulunur.
    - **Veri Seti**: Kaggle üzerinde bulunan "places-to-visit-in-istanbul" veri seti kullanılarak, İstanbul’daki ziyaret edilebilecek noktalar hakkında bilgi toplanmıştır.

    ## Kurulum

    Proje, Google Colab ortamında çalışmak üzere tasarlanmıştır. Colab üzerinden çalışabilmek için aşağıdaki adımları takip edebilirsiniz.

    1. Colab'i açın ve gerekli kütüphaneleri yüklemek için aşağıdaki hücreyi çalıştırın:

    ```python
    !pip install gradio
    !pip install kaggle
    ```

    2. Verilerinizi Google Drive'a yükleyin ve `kaggle.json` dosyasını doğru konumda sağlayın.
    3. Projeyi kendi Google Drive'ınıza kopyalayın ve çalıştırın.

    ## Kullanım

    1. **Kategori Filtreleri**: Seyahat planınızı özelleştirmek için "müze", "yürüyüş" ve "yemek" gibi kategori filtrelerinden seçim yapabilirsiniz. Bu seçenekleri seçmek, planı daha kişiselleştirilmiş hale getirecektir.
    
    2. **Mini İpucu**: Seyahat planınızda yerlerin sabah, öğle veya akşam saatlerine yerleştirilmesini isterseniz, "Mini ipucu" kısmını kullanabilirsiniz. Örneğin: "Ayasofya sabah olsun".
    
    3. **Plan Oluştur**: Planınızı oluşturduktan sonra, sabah, öğle ve akşam saatlerine göre gezilecek yerlerin listesi görüntülenecektir.

    ## Proje Bağlantısı

    Bu projeyi aşağıdaki bağlantıdan çalıştırabilirsiniz:

    [Gezi Planı Uygulaması - Gradio Link](https://9de61b3c7cdbbed131.gradio.live/)

    **Not**: Bu bağlantı 72 saat boyunca aktif kalacaktır.

    ## Veri Kaynağı

    Bu projede kullanılan veri seti, [Kaggle - places-to-visit-in-istanbul](https://www.kaggle.com/datasets/ouzcanmaden/places-to-visit-in-istanbul) veri setine dayanmaktadır.

    ## Geliştirme Ortamı

    - Python 3
    - Google Colab
    - Gradio
    - Kaggle API

    ## Kolay Kurulum

    Bu projeyi Google Colab üzerinde kolayca çalıştırabilirsiniz. İlgili hücrelerin sırasıyla çalıştırılması ve gerekli kütüphanelerin yüklenmesi yeterlidir. Kodlar ve gradio arayüzü otomatik olarak başlatılacaktır.

    ## Adım Adım Talimatlar

    1. **Gradio ve Kaggle API kurulumu**: Gerekli kütüphaneleri yüklemek için yukarıdaki komutları kullanın.
    
    2. **Google Drive bağlantısı**: Proje dosyalarını ve verilerinizi Google Drive'da tutun. Drive'ınızı bağladıktan sonra, proje klasörünü uygun şekilde ayarlayın.
    
    3. **Veri İndirme**: Kaggle API kullanarak İstanbul'un gezilecek yerlerini içeren veri setini indirin ve verilerinizi işleyin.
    
    4. **Gradio Arayüzü**: Gradio arayüzü üzerinden seyahat planınızı oluşturun. Filtreler ve mini ipuçları ekleyerek, kişiselleştirilmiş bir plan oluşturun.

    ## Kolay Çalıştırma

    Aşağıdaki Colab hücresini çalıştırarak projeyi başlatabilirsiniz:

    ```python
    # Gerekli kütüphaneler
    import gradio as gr
    import pandas as pd

    # Verilerinizi yükleyin ve işleyin
    def load_data():
        # Verilerinizi yükleme ve işleme kodu
        pass

    # Seyahat planı oluşturma fonksiyonu
    def generate_plan():
        # Plan oluşturma mantığı
        return plan

    # Gradio arayüzü
    with gr.Blocks() as demo:
        gr.Markdown("İstanbul 2 Günlük Seyahat Planı")
        # Kullanıcıdan giriş alacak elementler
        plan_button = gr.Button("Plan Oluştur")
        plan_output = gr.Markdown()

        plan_button.click(generate_plan, outputs=plan_output)

    demo.launch(share=True)
    ```

    Bu adımları takip ederek, projenizi Colab üzerinde çalıştırabilirsiniz. Ayrıca, proje bağlantısı aracılığıyla Gradio arayüzünü de kullanabilirsiniz.

    