class Sehir:
    def __init__(self, sehir_adi, sehir_id):
        self.sehir_adi = sehir_adi
        self.sehir_id = sehir_id
        self.alt_sehirler = []  # Çocuk düğümler

    def alt_sehir_ekle(self, alt_sehir):
        self.alt_sehirler.append(alt_sehir)


class KargoAgaci:
    def __init__(self, merkez_sehir):
        self.kok = merkez_sehir  # Ağaç yapısının kökü

    def agac_derinligi(self, sehir=None, derinlik=0):
        if sehir is None:
            sehir = self.kok
        if not sehir.alt_sehirler:
            return derinlik
        return max(self.agac_derinligi(alt, derinlik + 1) for alt in sehir.alt_sehirler)

    def agaci_yazdir(self, sehir=None, seviye=0):
        if sehir is None:
            sehir = self.kok
        print("  " * seviye + f"{sehir.sehir_adi} (ID: {sehir.sehir_id})")
        for alt_sehir in sehir.alt_sehirler:
            self.agaci_yazdir(alt_sehir, seviye + 1)


# Şehirler oluşturuluyor
merkez = Sehir("Merkez", 0)
sehir1 = Sehir("Şehir 1", 1)
sehir2 = Sehir("Şehir 2", 2)
sehir3 = Sehir("Şehir 3", 3)
sehir4 = Sehir("Şehir 4", 4)
sehir5 = Sehir("Şehir 5", 5)

# Şehirleri bağlama
merkez.alt_sehir_ekle(sehir1)
merkez.alt_sehir_ekle(sehir2)
sehir1.alt_sehir_ekle(sehir3)
sehir1.alt_sehir_ekle(sehir4)
sehir2.alt_sehir_ekle(sehir5)

# Ağaç yapısı
kargo_agaci = KargoAgaci(merkez)

# Derinlik hesaplama
print(f"Ağacın derinliği: {kargo_agaci.agac_derinligi()}")

# Ağaç görselleştirme (konsol)
print("Kargo Ağaç Yapısı:")
kargo_agaci.agaci_yazdir()
