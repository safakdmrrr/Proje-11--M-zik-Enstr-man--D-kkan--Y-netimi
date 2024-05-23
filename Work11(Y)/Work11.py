import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QMessageBox, QSpinBox, QDoubleSpinBox, QDialog, QFormLayout, QComboBox, QTextEdit, QDialogButtonBox, QListWidgetItem
from PyQt5.QtGui import QFont

class Enstruman:
    def __init__(self, ad, stok, fiyat):
        self.ad = ad
        self.stok = stok
        self.fiyat = fiyat

class Satis:
    def __init__(self, siparis_numarasi, enstrumanlar, ad, soyad, adres):
        self.siparis_numarasi = siparis_numarasi
        self.enstrumanlar = enstrumanlar
        self.ad = ad
        self.soyad = soyad
        self.adres = adres

class Destek:
    def __init__(self, talep_numarasi, ad, soyad, detaylar):
        self.talep_numarasi = talep_numarasi
        self.ad = ad
        self.soyad = soyad
        self.detaylar = detaylar

class DestekTalebiDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Destek Talebi Oluştur")
        self.layout = QVBoxLayout()

        self.ad_input = QLineEdit()
        self.soyad_input = QLineEdit()
        self.detaylar_input = QTextEdit()

        self.talep_button = QPushButton("Talep Oluştur")
        self.talep_button.clicked.connect(self.accept)

        self.layout.addWidget(QLabel("Ad:"))
        self.layout.addWidget(self.ad_input)
        self.layout.addWidget(QLabel("Soyad:"))
        self.layout.addWidget(self.soyad_input)
        self.layout.addWidget(QLabel("Detaylar:"))
        self.layout.addWidget(self.detaylar_input)
        self.layout.addWidget(self.talep_button)

        self.setLayout(self.layout)

    def get_talep(self):
        return (
            self.ad_input.text(),
            self.soyad_input.text(),
            self.detaylar_input.toPlainText()
        )

class SiparisDialog(QDialog):
    def __init__(self, enstrumanlar):
        super().__init__()

        self.setWindowTitle("Sipariş Ver")
        self.layout = QVBoxLayout()

        self.enstrumanlar_combo = QComboBox()
        for enstruman in enstrumanlar:
            self.enstrumanlar_combo.addItem(enstruman.ad)

        self.ad_input = QLineEdit()
        self.soyad_input = QLineEdit()
        self.adres_input = QTextEdit()

        self.adet_spinbox = QSpinBox()
        self.adet_spinbox.setMinimum(1)
        self.adet_spinbox.setMaximum(999)

        self.siparis_button = QPushButton("Sipariş Ver")
        self.siparis_button.clicked.connect(self.accept)

        self.layout.addWidget(QLabel("Enstrüman Seçiniz:"))
        self.layout.addWidget(self.enstrumanlar_combo)

        form_layout = QFormLayout()
        form_layout.addRow("Ad:", self.ad_input)
        form_layout.addRow("Soyad:", self.soyad_input)
        form_layout.addRow("Adres:", self.adres_input)
        self.layout.addLayout(form_layout)

        self.layout.addWidget(QLabel("Adet:"))
        self.layout.addWidget(self.adet_spinbox)
        self.layout.addWidget(self.siparis_button)

        self.setLayout(self.layout)

    def get_siparis(self):
        return (
            self.enstrumanlar_combo.currentText(),
            self.adet_spinbox.value(),
            self.ad_input.text(),
            self.soyad_input.text(),
            self.adres_input.toPlainText()
        )

class MusteriBilgileri(QWidget):
    def __init__(self, satislar):
        super().__init__()

        self.setWindowTitle("Müşteri Bilgileri")
        self.layout = QVBoxLayout()

        self.satislar = satislar

        self.musteri_listesi = QListWidget()
        self.musteri_listesi.itemDoubleClicked.connect(self.musteri_detaylarini_goster)

        self.detaylar_button = QPushButton("Sipariş Detaylarını Göster")
        self.detaylar_button.clicked.connect(self.musteri_detaylarini_goster)

        self.layout.addWidget(QLabel("Müşteri Listesi:"))
        self.layout.addWidget(self.musteri_listesi)
        self.layout.addWidget(self.detaylar_button)

        self.setLayout(self.layout)

        self.musteri_listesini_guncelle()

    def musteri_listesini_guncelle(self):
        self.musteri_listesi.clear()
        for satis in self.satislar:
            item = f"{satis.ad} {satis.soyad} - Sipariş No: {satis.siparis_numarasi}"
            font = QFont()
            font.setPointSize(12)  # Yazı boyutunu ayarlıyoruz
            self.musteri_listesi.addItem(QListWidgetItem(item))
            self.musteri_listesi.item(self.musteri_listesi.count() - 1).setFont(font)  # Yeni eklenen öğenin yazı boyutunu ayarlıyoruz

    def musteri_detaylarini_goster(self):
        secili_item = self.musteri_listesi.currentItem()
        if secili_item:
            musteri_ad_soyad = secili_item.text().split()
            musteri_ad = musteri_ad_soyad[0]
            musteri_soyad = musteri_ad_soyad[1]
            dialog = QDialog(self)
            dialog.setWindowTitle("Müşteri Sipariş Detayları")
            layout = QVBoxLayout(dialog)
            for satis in self.satislar:
                if satis.ad == musteri_ad and satis.soyad == musteri_soyad:
                    layout.addWidget(QLabel(f"Sipariş Numarası: {satis.siparis_numarasi}"))
                    layout.addWidget(QLabel("Sipariş Detayları:"))
                    for enstruman, adet in satis.enstrumanlar:
                        layout.addWidget(QLabel(f"{enstruman}: {adet} adet"))
                    layout.addWidget(QLabel(f"Adres: {satis.adres}"))
            button_box = QDialogButtonBox(QDialogButtonBox.Ok)
            button_box.accepted.connect(dialog.accept)
            layout.addWidget(button_box)
            dialog.setLayout(layout)
            dialog.exec_()

class MuzikDukkani(QWidget):
    def __init__(self):
        super().__init__()

        self.enstrumanlar = [Enstruman("Gitar", 10, 500), Enstruman("Piyano", 5, 3000), Enstruman("Davul", 8, 1000)]
        self.satislar = []  # Satis nesnelerini tutacak liste
        self.destek_talepleri = []

        self.arayuzu_olustur()
        self.musteri_bilgileri_penceresi = None

    def arayuzu_olustur(self):
        self.setWindowTitle("Müzik Enstrümanı Dükkanı Yönetimi")
        self.setFixedSize(600, 400)  # Pencere boyutunu genişletiyoruz
        self.layout = QVBoxLayout()

        # Enstrümanlar Bölümü
        self.enstrumanlar_etiketi = QLabel("Enstrümanlar:")
        self.enstrumanlar_listesi = QListWidget()
        self.enstruman_listesini_guncelle()

        self.layout.addWidget(self.enstrumanlar_etiketi)
        self.layout.addWidget(self.enstrumanlar_listesi)

        # Enstrüman Ekleme Bölümü
        self.enstruman_ekle_label = QLabel("Enstrüman Adı:")
        self.enstruman_ekle_input = QLineEdit()
        self.enstruman_ekle_button = QPushButton("Enstrüman Ekle")
        self.enstruman_ekle_button.clicked.connect(self.enstruman_ekle)

        self.enstruman_stok_label = QLabel("Stok:")
        self.enstruman_stok_input = QSpinBox()
        self.enstruman_stok_input.setMinimum(0)
        self.enstruman_stok_input.setMaximum(9999)
        self.enstruman_stok_input.setValue(0)

        self.enstruman_fiyat_label = QLabel("Fiyat:")
        self.enstruman_fiyat_input = QDoubleSpinBox()
        self.enstruman_fiyat_input.setMinimum(0.0)
        self.enstruman_fiyat_input.setMaximum(99999.99)
        self.enstruman_fiyat_input.setDecimals(2)
        self.enstruman_fiyat_input.setValue(0.0)

        self.enstruman_ekle_layout = QHBoxLayout()
        self.enstruman_ekle_layout.addWidget(self.enstruman_ekle_label)
        self.enstruman_ekle_layout.addWidget(self.enstruman_ekle_input)
        self.enstruman_ekle_layout.addWidget(self.enstruman_stok_label)
        self.enstruman_ekle_layout.addWidget(self.enstruman_stok_input)
        self.enstruman_ekle_layout.addWidget(self.enstruman_fiyat_label)
        self.enstruman_ekle_layout.addWidget(self.enstruman_fiyat_input)
        self.enstruman_ekle_layout.addWidget(self.enstruman_ekle_button)

        self.layout.addLayout(self.enstruman_ekle_layout)

        # Sipariş Bölümü
        self.siparis_etiketi = QLabel("Sipariş:")
        self.siparis_butonu = QPushButton("Sipariş Ver")
        self.siparis_butonu.clicked.connect(self.siparis_ver)

        self.siparis_layout = QHBoxLayout()
        self.siparis_layout.addWidget(self.siparis_etiketi)
        self.siparis_layout.addWidget(self.siparis_butonu)

        self.layout.addLayout(self.siparis_layout)

        # Destek Bölümü
        self.destek_etiketi = QLabel("Destek:")
        self.destek_talebi_butonu = QPushButton("Destek Talebi Oluştur")
        self.destek_talebi_butonu.clicked.connect(self.destek_talebi_olustur)

        self.destek_layout = QHBoxLayout()
        self.destek_layout.addWidget(self.destek_etiketi)
        self.destek_layout.addWidget(self.destek_talebi_butonu)

        self.layout.addLayout(self.destek_layout)

        # Müşteri Bilgileri Bölümü
        self.musteri_bilgileri_butonu = QPushButton("Müşteri Bilgileri")
        self.musteri_bilgileri_butonu.clicked.connect(self.musteri_bilgileri_ac)

        # Satılan Enstrümanları Göster Butonu
        self.satilan_enstrumanlar_butonu = QPushButton("Satılan Enstrümanları Göster")
        self.satilan_enstrumanlar_butonu.clicked.connect(self.satilan_enstrumanlari_goster)

        self.layout.addWidget(self.musteri_bilgileri_butonu)
        self.layout.addWidget(self.satilan_enstrumanlar_butonu)  # Butonu arayüze ekliyoruz

        self.setLayout(self.layout)

    def enstruman_listesini_guncelle(self):
        self.enstrumanlar_listesi.clear()
        for enstruman in self.enstrumanlar:
            self.enstrumanlar_listesi.addItem(enstruman.ad + " - Stok: " + str(enstruman.stok) + " - Fiyat: " + str(enstruman.fiyat) + " TL")

    def enstruman_ekle(self):
        yeni_enstruman_adı = self.enstruman_ekle_input.text()
        yeni_enstruman_stok = self.enstruman_stok_input.value()
        yeni_enstruman_fiyat = self.enstruman_fiyat_input.value()
        if yeni_enstruman_adı:
            self.enstrumanlar.append(Enstruman(yeni_enstruman_adı, yeni_enstruman_stok, yeni_enstruman_fiyat))
            self.enstruman_listesini_guncelle()
            QMessageBox.information(self, "Bilgi", "Yeni enstrüman başarıyla eklendi.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir enstrüman adı girin.")

    def siparis_ver(self):
        dialog = SiparisDialog(self.enstrumanlar)
        if dialog.exec_() == QDialog.Accepted:
            secilen_enstruman, adet, ad, soyad, adres = dialog.get_siparis()
            for enstruman in self.enstrumanlar:
                if enstruman.ad == secilen_enstruman:
                    if enstruman.stok >= adet:
                        enstruman.stok -= adet
                        self.enstruman_listesini_guncelle()
                        satis_numarasi = len(self.satislar) + 1  # Yeni sipariş numarası
                        self.satislar.append(Satis(satis_numarasi, [(secilen_enstruman, adet)], ad, soyad, adres))  # Satis nesnesini oluşturup listeye ekle
                        QMessageBox.information(self, "Bilgi", f"{secilen_enstruman} adlı enstrümanın {adet} adet siparişi başarıyla verildi.")
                    else:
                        QMessageBox.warning(self, "Uyarı", f"Stokta yeterli {secilen_enstruman} bulunmamaktadır.")
                    return

    def destek_talebi_olustur(self):
        dialog = DestekTalebiDialog()
        if dialog.exec_() == QDialog.Accepted:
            ad, soyad, detaylar = dialog.get_talep()
            talep_numarasi = len(self.destek_talepleri) + 1
            self.destek_talepleri.append(Destek(talep_numarasi, ad, soyad, detaylar))
            print("Destek talebi başarıyla gönderildi!")

    def musteri_bilgileri_ac(self):
        if not self.musteri_bilgileri_penceresi:
            self.musteri_bilgileri_penceresi = MusteriBilgileri(self.satislar)
        self.musteri_bilgileri_penceresi.show()

    def satilan_enstrumanlari_goster(self):
        # Satılan enstrümanları gösterecek bir iletişim kutusu oluştur
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Satılan Enstrümanlar")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Şu anda satılan enstrümanlar:")
        # Satılan enstrümanları listelemek için satislar listesini dolaş
        satilan_enstrumanlar = []
        for satis in self.satislar:
            # Her bir satis nesnesinin enstrumanlar listesini dolaş
            for enstruman, adet in satis.enstrumanlar:
                # Enstruman adını ve satış miktarını iletişim kutusuna ekleyerek listele
                satilan_enstrumanlar.append(f"- {enstruman}: {adet} adet")
        if satilan_enstrumanlar:
            msg_box.setDetailedText("\n".join(satilan_enstrumanlar))
            msg_box.exec_()
        else:
            msg_box.setInformativeText("Henüz satılan enstrüman bulunmamaktadır.")
            msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    muzik_dukkani = MuzikDukkani()
    muzik_dukkani.show()
    sys.exit(app.exec_())
