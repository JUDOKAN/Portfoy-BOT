Proje Yöneticisi Discord Botu
Açıklama:
Bu proje, Mehmet’in yazılım şirketi tarafından geliştirilmiş olan ve Discord platformu üzerinden çalışan bir Proje Takip ve Yönetim Botudur. Bot, kullanıcıların projelerini kolayca kaydetmesine, güncellemesine, silmesine ve detaylarını görüntülemesine olanak sağlar. Özellikle bireysel geliştiriciler, küçük ekipler veya eğitim amaçlı projelerde kullanılmak üzere tasarlanmıştır.

Temel Özellikler
Yeni Proje Ekleme:
Kullanıcı, !new_project komutunu kullanarak bir proje adı, bağlantısı ve durumu girerek yeni bir proje oluşturabilir. Projeler, botun bağlı olduğu SQLite veri tabanına kaydedilir.

Proje Listeleme:
!projects komutu ile kullanıcı sadece kendi projelerini listeleyebilir. Her proje adı ve bağlantısı şeklinde gösterilir.

Proje Güncelleme:
!update_projects komutu ile bir projenin adı, açıklaması, bağlantısı veya durumu değiştirilebilir. Kullanıcı, değiştirmek istediği özelliği seçerek güncel veriyi sisteme girer.

Proje Silme:
!delete komutu, mevcut projelerden birinin silinmesini sağlar. Silinen projeye dair tüm veriler veri tabanından kaldırılır.

Proje Beceri Ekleme:
!skills komutu ile bir projeye Python, SQL, API veya Discord gibi önceden tanımlanmış yazılım becerileri eklenebilir. Bu sayede hangi projede hangi teknolojilerin kullanıldığı takip edilir.

Kullanıcı Listeleme:
!users komutu, veri tabanına kayıtlı kullanıcıları listeler. Her kullanıcı, sistemdeki ID’si ile görünür.

Kullanıcı-Proje İlişkileri:
!users_projects komutu, tüm kullanıcıların sahip olduğu projeleri listeler. Her kullanıcı için hangi projeleri yönettiği görüntülenebilir.

Teknik Altyapı
Backend: Python ile yazılmıştır.

Veri Tabanı: SQLite (mk.db) kullanılmıştır.

Discord API: discord.py ve discord.ext.commands kullanılarak bot yapısı oluşturulmuştur.

Komut Tabanlı Yapı: Kullanıcı etkileşimi tamamen komutlara dayalıdır.

Modüler Yapı: bot.py, logic.py, config.py, modal.py gibi ayrı dosyalarla yönetilir. Veri yönetimi ve komutlar ayrıştırılarak okunabilirlik ve sürdürülebilirlik artırılmıştır.

Ek Özellik: Modal ve Buton Sistemi
!test ve !modal komutları ile Discord üzerinde buton ve modal (pencere) etkileşimi sağlanmıştır. Bu sayede kullanıcılar yazılı girişleri doğrudan özel formlar aracılığıyla verebilir.

Hedef Kullanıcı Kitlesi
Bu bot, yazılım geliştiren genç girişimciler, öğrenci kulüpleri, bireysel geliştiriciler ve küçük yazılım ekipleri için geliştirilmiştir. Basit yapısı sayesinde herkesin kullanabileceği şekilde tasarlanmış, ancak altyapısı sayesinde daha gelişmiş versiyonlara da zemin hazırlamaktadır.

Mehmet’in Şirketi İçin Katkısı
Bu proje, Mehmet’in yazılım şirketi için önemli bir vitrindir. Hem Python hem de Discord API konularında bilgi sahibi olduğunu göstermekte, hem de ekip çalışmasına uygun mini bir proje yönetim aracı sunmaktadır. Geliştirilmeye açıktır ve kullanıcı arayüzü, rol bazlı yetkilendirme gibi yeni özelliklerle zenginleştirilebilir.
